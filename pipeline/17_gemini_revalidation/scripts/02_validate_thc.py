import pandas as pd
import boto3
import json
import time
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Vertex AI
aiplatform.init(project="gen-lang-client-0100184589", location="us-central1")
model = GenerativeModel('gemini-2.5-flash')

# Initialize S3
s3 = boto3.client('s3')
try:
    s3.head_bucket(Bucket='ci-strains-html-archive')
    print("✅ S3 connection successful\n")
except Exception as e:
    print(f"❌ S3 connection failed: {e}")
    sys.exit(1)

# Load data
df = pd.read_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\input\pipeline_16_cleaned.csv', encoding='latin-1', low_memory=False)

thc_strains = df.copy()
thc_existing = df['thc_avg'].notna().sum()
thc_missing = df['thc_avg'].isna().sum()
print(f"🎯 Group 1: THC Validation")
print(f"📊 Processing ALL {len(thc_strains):,} strains")
print(f"   - {thc_existing:,} with existing THC data (validate + correct)")
print(f"   - {thc_missing:,} with missing THC data (extract if found)\n")

results = []
checkpoint_interval = 500

def get_html_from_s3(s3_key):
    try:
        response = s3.get_object(Bucket='ci-strains-html-archive', Key=s3_key)
        return response['Body'].read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def validate_thc_with_gemini(strain_data, html_content):
    has_data = pd.notna(strain_data['thc_avg'])
    
    if has_data:
        current_info = f"""- THC Min: {strain_data['thc_min']}
- THC Max: {strain_data['thc_max']}
- THC Avg: {strain_data['thc_avg']}"""
    else:
        current_info = "- THC data is MISSING - extract if found in HTML"
    
    prompt = f"""You are validating cannabis strain THC data against the source HTML.

**Current Data:**
- Strain: {strain_data['strain_name_display']}
{current_info}

**Your Task:**
1. Find THC information in the HTML
2. {"Validate if current values are correct" if has_data else "Extract THC values if present"}
3. If incorrect, provide corrected values
4. If missing, extract values (set to null if not found)
5. Flag impossible values (>40% is suspicious)

**Return JSON only:**
{{
  "thc_min": {{
    "current_value": {strain_data['thc_min'] if has_data else 'null'},
    "gemini_value": null,
    "confidence": "high",
    "action": "not_found",
    "reasoning": "brief explanation",
    "source_text": "exact text from HTML or not found"
  }},
  "thc_max": {{}},
  "thc_avg": {{}}
}}

**HTML Content:**
{html_content[:15000]}
"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith('```'):
            response_text = response_text[3:-3].strip()
        return json.loads(response_text)
    except Exception as e:
        return {"error": str(e)}

# Process strains
for idx, row in thc_strains.iterrows():
    strain_num = idx + 1
    
    if strain_num % 100 == 0:
        print(f"⏳ Processing strain {strain_num:,}/{len(thc_strains):,} ({(strain_num/len(thc_strains)*100):.1f}%)")
    
    html = get_html_from_s3(row['s3_html_key'])
    if not html:
        results.append({
            'strain_id': row['strain_id'],
            'strain_name': row['strain_name_display'],
            'error': 'Failed to retrieve HTML from S3'
        })
        continue
    
    validation = validate_thc_with_gemini(row, html)
    
    results.append({
        'strain_id': row['strain_id'],
        'strain_name': row['strain_name_display'],
        'validation': validation
    })
    
    if strain_num % checkpoint_interval == 0:
        checkpoint_df = pd.DataFrame(results)
        checkpoint_df.to_json(
            f'c:\\Users\\uthin\\OneDrive\\Desktop\\ci-strains-pro\\pipeline\\17_gemini_revalidation\\output\\thc_validation_checkpoint_{strain_num}.json',
            orient='records',
            indent=2
        )
        print(f"💾 Checkpoint saved at {strain_num:,} strains\n")
    
    time.sleep(0.1)

final_df = pd.DataFrame(results)
final_df.to_json(
    r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\output\thc_validation_results.json',
    orient='records',
    indent=2
)

print(f"\n✅ THC Validation Complete!")
print(f"📊 Processed: {len(results):,} strains")
print(f"💾 Saved: thc_validation_results.json")
