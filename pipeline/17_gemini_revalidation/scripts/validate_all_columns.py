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
CHECKPOINT_INTERVAL = 100

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# Load data
df = pd.read_csv(INPUT_FILE, encoding='latin-1', low_memory=False)
print(f"📊 Loaded {len(df):,} strains for validation\n")

# Define column groups to validate
COLUMN_GROUPS = {
    "cannabinoids": ["thc_min", "thc_max", "thc_avg", "cbd_min", "cbd_max", "cbd_avg"],
    "genetics": ["indica_percentage", "sativa_percentage", "genetics_type"],
    "flowering": ["flowering_days_min", "flowering_days_max", "flowering_days_avg"],
    "height_indoor": ["height_indoor_cm_min", "height_indoor_cm_max"],
    "height_outdoor": ["height_outdoor_cm_min", "height_outdoor_cm_max"],
    "yield_indoor": ["yield_indoor_g_m2_min", "yield_indoor_g_m2_max"],
    "yield_outdoor": ["yield_outdoor_g_plant_min", "yield_outdoor_g_plant_max"]
}

def validate_strain(row):
    """Validate all columns for a single strain using URL grounding"""
    
    url = row['source_url']
    strain_name = row['strain_name_display']
    
    # Build current data summary
    current_data = {}
    for group_name, columns in COLUMN_GROUPS.items():
        current_data[group_name] = {}
        for col in columns:
            val = row.get(col)
            current_data[group_name][col] = val if pd.notna(val) else None
    
    prompt = f"""You are validating cannabis strain data against the source webpage.

**Strain:** {strain_name}
**URL:** {url}

**Current Data to Validate:**
{json.dumps(current_data, indent=2)}

**Your Task:**
1. Access the URL and extract ALL botanical data present
2. For each field group, validate current values OR extract if missing
3. Flag inconsistencies, impossible values, or missing data

**Validation Rules:**
- THC/CBD: Ranges must be logical (min ≤ max), avg should be between min/max
- Genetics: Indica + Sativa should = 100% (allow small rounding errors)
- Flowering: Typical range 40-120 days
- Heights: Indoor typically < Outdoor
- Yields: Must be positive numbers

**Return JSON Format:**
{{
  "cannabinoids": {{
    "thc_min": {{
      "current": <value or null>,
      "extracted": <value or null>,
      "status": "correct|incorrect|missing|not_found",
      "confidence": "high|medium|low",
      "note": "brief explanation"
    }},
    ... (all cannabinoid fields)
  }},
  "genetics": {{ ... }},
  "flowering": {{ ... }},
  "height_indoor": {{ ... }},
  "height_outdoor": {{ ... }},
  "yield_indoor": {{ ... }},
  "yield_outdoor": {{ ... }},
  "source_text_sample": "relevant excerpt from page showing data"
}}

**IMPORTANT:** Return ONLY valid JSON. If data not found on page, set extracted to null and status to "not_found".
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=GenerateContentConfig(
                tools=[Tool(url_context=UrlContext())],
                response_mime_type="application/json"
            )
        )
        
        result = json.loads(response.text)
        return {
            "strain_id": row['strain_id'],
            "strain_name": strain_name,
            "source_url": url,
            "validation": result,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "strain_id": row['strain_id'],
            "strain_name": strain_name,
            "source_url": url,
            "validation": None,
            "status": "error",
            "error": str(e)
        }

# Process strains
results = []
total = len(df)

print("🚀 Starting validation...\n")

for idx, row in df.iterrows():
    strain_num = idx + 1
    
    if strain_num % 10 == 0:
        print(f"⏳ Processing {strain_num:,}/{total:,} ({(strain_num/total*100):.1f}%)")
    
    result = validate_strain(row)
    results.append(result)
    
    # Checkpoint save
    if strain_num % CHECKPOINT_INTERVAL == 0:
        checkpoint_file = OUTPUT_FILE.replace('.json', f'_checkpoint_{strain_num}.json')
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Checkpoint saved: {strain_num:,} strains\n")
    
    # Rate limiting
    time.sleep(0.1)

# Save final results
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

# Generate summary
success_count = sum(1 for r in results if r['status'] == 'success')
error_count = sum(1 for r in results if r['status'] == 'error')

print(f"\n✅ Validation Complete!")
print(f"📊 Total Strains: {total:,}")
print(f"✅ Successful: {success_count:,}")
print(f"❌ Errors: {error_count:,}")
print(f"💾 Results saved: {OUTPUT_FILE}")
