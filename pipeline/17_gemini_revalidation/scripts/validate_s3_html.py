import os
import pandas as pd
import boto3
from google import genai
from google.genai.types import GenerateContentConfig
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURATION ---
PROJECT_ID = os.environ["GCP_PROJECT_ID"]
LOCATION = "us-central1"
INPUT_FILE = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\input\pipeline_16_cleaned.csv"
OUTPUT_FILE = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\output\s3_validation_results.json"
BATCH_SIZE = 5
CHECKPOINT_INTERVAL = 100

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
s3 = boto3.client('s3')

# Load data
df = pd.read_csv(INPUT_FILE, encoding='latin-1', low_memory=False)
print(f"📊 Loaded {len(df):,} strains")
print(f"📦 Batch size: {BATCH_SIZE} strains per API call\n")

def get_html_from_s3(s3_key):
    """Fetch HTML from S3"""
    try:
        response = s3.get_object(Bucket='ci-strains-html-archive', Key=s3_key)
        return response['Body'].read().decode('utf-8', errors='ignore')[:50000]  # First 50K chars
    except Exception as e:
        return None

def validate_batch(batch_rows):
    """Validate batch using S3 HTML"""
    
    batch_data = []
    for _, row in batch_rows.iterrows():
        html = get_html_from_s3(row['s3_html_key'])
        if not html:
            batch_data.append({
                "strain_id": row['strain_id'],
                "error": "Failed to fetch HTML from S3"
            })
            continue
        
        batch_data.append({
            "strain_id": row['strain_id'],
            "strain_name": row['strain_name_display'],
            "html_snippet": html,
            "current_data": {
                "thc_min": row.get('thc_min') if pd.notna(row.get('thc_min')) else None,
                "thc_max": row.get('thc_max') if pd.notna(row.get('thc_max')) else None,
                "thc_avg": row.get('thc_avg') if pd.notna(row.get('thc_avg')) else None,
                "cbd_min": row.get('cbd_min') if pd.notna(row.get('cbd_min')) else None,
                "cbd_max": row.get('cbd_max') if pd.notna(row.get('cbd_max')) else None,
                "cbd_avg": row.get('cbd_avg') if pd.notna(row.get('cbd_avg')) else None,
                "indica_pct": row.get('indica_percentage') if pd.notna(row.get('indica_percentage')) else None,
                "sativa_pct": row.get('sativa_percentage') if pd.notna(row.get('sativa_percentage')) else None,
                "genetics_type": row.get('genetics_type') if pd.notna(row.get('genetics_type')) else None,
                "flowering_min": row.get('flowering_days_min') if pd.notna(row.get('flowering_days_min')) else None,
                "flowering_max": row.get('flowering_days_max') if pd.notna(row.get('flowering_days_max')) else None,
                "flowering_avg": row.get('flowering_days_avg') if pd.notna(row.get('flowering_days_avg')) else None
            }
        })
    
    # Filter out errors
    valid_batch = [b for b in batch_data if 'error' not in b]
    if not valid_batch:
        return batch_data
    
    prompt = f"""Validate botanical data for {len(valid_batch)} cannabis strains using their HTML source.

For EACH strain, extract data from HTML and compare with current values.

**Strains:**
{json.dumps([{k: v for k, v in b.items() if k != 'html_snippet'} for b in valid_batch], indent=2)}

**HTML Content for each strain is provided above.**

Return JSON array:
[
  {{
    "strain_id": "uuid",
    "fields": {{
      "thc_min": {{"current": X, "extracted": Y, "status": "correct|incorrect|missing|not_found", "confidence": "high|medium|low"}},
      "thc_max": {{}},
      "thc_avg": {{}},
      "cbd_min": {{}},
      "cbd_max": {{}},
      "cbd_avg": {{}},
      "indica_pct": {{}},
      "sativa_pct": {{}},
      "genetics_type": {{}},
      "flowering_min": {{}},
      "flowering_max": {{}},
      "flowering_avg": {{}}
    }}
  }}
]

**HTML for validation:**
{chr(10).join([f"Strain {i+1} ({b['strain_id']}):{chr(10)}{b['html_snippet'][:10000]}{chr(10)}" for i, b in enumerate(valid_batch)])}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        return [{"strain_id": b["strain_id"], "error": str(e)} for b in valid_batch]

# Process in batches
results = []
total_batches = (len(df) + BATCH_SIZE - 1) // BATCH_SIZE

print("🚀 Starting S3-based validation...\n")

for batch_num in range(total_batches):
    start_idx = batch_num * BATCH_SIZE
    end_idx = min(start_idx + BATCH_SIZE, len(df))
    batch = df.iloc[start_idx:end_idx]
    
    print(f"⏳ Batch {batch_num + 1}/{total_batches} | Strains {start_idx + 1}-{end_idx} ({(end_idx/len(df)*100):.1f}%)")
    
    batch_results = validate_batch(batch)
    results.extend(batch_results)
    
    if (batch_num + 1) % (CHECKPOINT_INTERVAL // BATCH_SIZE) == 0:
        checkpoint_file = OUTPUT_FILE.replace('.json', f'_checkpoint_{end_idx}.json')
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Checkpoint: {end_idx:,} strains\n")
    
    time.sleep(0.2)

# Save final
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Validation Complete!")
print(f"📊 Total: {len(df):,}")
print(f"📦 Batches: {total_batches:,}")
print(f"💾 Results: {OUTPUT_FILE}")
