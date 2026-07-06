import os
import pandas as pd
from google import genai
from google.genai.types import Tool, GenerateContentConfig, UrlContext
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURATION ---
PROJECT_ID = os.environ["GCP_PROJECT_ID"]
LOCATION = "us-central1"
INPUT_FILE = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\input\pipeline_16_cleaned.csv"
OUTPUT_FILE = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\output\full_validation_results.json"
BATCH_SIZE = 10  # Process 10 strains per API call
CHECKPOINT_INTERVAL = 100

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# Load data
df = pd.read_csv(INPUT_FILE, encoding='latin-1', low_memory=False)
print(f"📊 Loaded {len(df):,} strains for validation")
print(f"📦 Batch size: {BATCH_SIZE} strains per API call")
print(f"⏱️  Estimated API calls: {len(df) // BATCH_SIZE:,}\n")

def validate_batch(batch_rows):
    """Validate multiple strains in a single API call"""
    
    # Build batch data
    batch_data = []
    for _, row in batch_rows.iterrows():
        batch_data.append({
            "strain_id": row['strain_id'],
            "strain_name": row['strain_name_display'],
            "url": row['source_url'],
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
                "flowering_avg": row.get('flowering_days_avg') if pd.notna(row.get('flowering_days_avg')) else None,
                "height_indoor_min": row.get('height_indoor_cm_min') if pd.notna(row.get('height_indoor_cm_min')) else None,
                "height_indoor_max": row.get('height_indoor_cm_max') if pd.notna(row.get('height_indoor_cm_max')) else None,
                "height_outdoor_min": row.get('height_outdoor_cm_min') if pd.notna(row.get('height_outdoor_cm_min')) else None,
                "height_outdoor_max": row.get('height_outdoor_cm_max') if pd.notna(row.get('height_outdoor_cm_max')) else None,
                "yield_indoor_min": row.get('yield_indoor_g_m2_min') if pd.notna(row.get('yield_indoor_g_m2_min')) else None,
                "yield_indoor_max": row.get('yield_indoor_g_m2_max') if pd.notna(row.get('yield_indoor_g_m2_max')) else None,
                "yield_outdoor_min": row.get('yield_outdoor_g_plant_min') if pd.notna(row.get('yield_outdoor_g_plant_min')) else None,
                "yield_outdoor_max": row.get('yield_outdoor_g_plant_max') if pd.notna(row.get('yield_outdoor_g_plant_max')) else None
            }
        })
    
    prompt = f"""Validate botanical data for {len(batch_data)} cannabis strains by accessing their source URLs.

**Strains to validate:**
{json.dumps(batch_data, indent=2)}

**For EACH strain:**
1. Access the URL using URL grounding
2. Extract ALL botanical data present
3. Compare with current values
4. Return validation status

**Return JSON array with this structure:**
[
  {{
    "strain_id": "uuid",
    "strain_name": "name",
    "fields": {{
      "thc_min": {{"current": X, "extracted": Y, "status": "correct|incorrect|missing|not_found", "confidence": "high|medium|low"}},
      "thc_max": {{...}},
      "thc_avg": {{...}},
      "cbd_min": {{...}},
      "cbd_max": {{...}},
      "cbd_avg": {{...}},
      "indica_pct": {{...}},
      "sativa_pct": {{...}},
      "genetics_type": {{...}},
      "flowering_min": {{...}},
      "flowering_max": {{...}},
      "flowering_avg": {{...}},
      "height_indoor_min": {{...}},
      "height_indoor_max": {{...}},
      "height_outdoor_min": {{...}},
      "height_outdoor_max": {{...}},
      "yield_indoor_min": {{...}},
      "yield_indoor_max": {{...}},
      "yield_outdoor_min": {{...}},
      "yield_outdoor_max": {{...}}
    }}
  }}
]

**Status values:**
- "correct": Current matches source
- "incorrect": Current differs from source  
- "missing": No current value but found on source
- "not_found": Not on source page

Return ONLY valid JSON array."""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                tools=[Tool(url_context=UrlContext())]
            )
        )
        
        # Parse JSON from response text
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:-3].strip()
        elif text.startswith('```'):
            text = text[3:-3].strip()
        
        return json.loads(text)
        
    except Exception as e:
        return [{"strain_id": row["strain_id"], "error": str(e)} for row in batch_data]

# Process in batches
results = []
total_batches = (len(df) + BATCH_SIZE - 1) // BATCH_SIZE

print("🚀 Starting batched validation...\n")

for batch_num in range(total_batches):
    start_idx = batch_num * BATCH_SIZE
    end_idx = min(start_idx + BATCH_SIZE, len(df))
    batch = df.iloc[start_idx:end_idx]
    
    print(f"⏳ Batch {batch_num + 1}/{total_batches} | Strains {start_idx + 1}-{end_idx} ({(end_idx/len(df)*100):.1f}%)")
    
    batch_results = validate_batch(batch)
    results.extend(batch_results)
    
    # Checkpoint save
    if (batch_num + 1) % (CHECKPOINT_INTERVAL // BATCH_SIZE) == 0:
        checkpoint_file = OUTPUT_FILE.replace('.json', f'_checkpoint_{end_idx}.json')
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Checkpoint: {end_idx:,} strains\n")
    
    time.sleep(0.5)  # Rate limiting

# Save final results
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Validation Complete!")
print(f"📊 Total Strains: {len(df):,}")
print(f"📦 Total Batches: {total_batches:,}")
print(f"💾 Results: {OUTPUT_FILE}")
