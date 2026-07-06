import json
import pandas as pd

V2_RESULTS = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\output\s3_validation_v2_results.json"
INPUT_CSV = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\input\pipeline_16_no_avg.csv"
OUTPUT_DIR = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\18_full_validation\output"

with open(V2_RESULTS, 'r', encoding='utf-8') as f:
    results = json.load(f)

df = pd.read_csv(INPUT_CSV, encoding='latin-1', low_memory=False)

print(f"Total strains: {len(results):,}")

# Count successes/errors
success = [r for r in results if 'error' not in r]
errors = [r for r in results if 'error' in r]
print(f"Success: {len(success):,} ({len(success)/len(results)*100:.1f}%)")
print(f"Errors: {len(errors):,} ({len(errors)/len(results)*100:.1f}%)\n")

# Extract all corrections
corrections = []
for result in success:
    strain_id = result['strain_id']
    fields = result.get('fields', {})
    
    for field_name, field_data in fields.items():
        if field_data.get('status') == 'incorrect':
            corrections.append({
                'strain_id': strain_id,
                'field': field_name,
                'current_value': field_data.get('current'),
                'extracted_value': field_data.get('extracted'),
                'status': field_data.get('status'),
                'confidence': field_data.get('confidence')
            })

print(f"Total corrections: {len(corrections):,}\n")

# Breakdown by field
field_counts = pd.Series([c['field'] for c in corrections]).value_counts()
print("Corrections by field:")
for field, count in field_counts.items():
    print(f"  {field}: {count}")

# Breakdown by confidence
conf_counts = pd.Series([c['confidence'] for c in corrections]).value_counts()
print(f"\nBy confidence:")
for conf, count in conf_counts.items():
    print(f"  {conf}: {count}")

# Save corrections
corrections_df = pd.DataFrame(corrections)

# Add strain_name and source_url
strain_names = df.set_index('strain_id')['strain_name_display'].to_dict()
source_urls = df.set_index('strain_id')['source_url'].to_dict()
corrections_df['strain_name'] = corrections_df['strain_id'].map(strain_names)
corrections_df['source_url'] = corrections_df['strain_id'].map(source_urls)

corrections_df = corrections_df[['strain_id', 'strain_name', 'source_url', 'field', 'current_value', 'extracted_value', 'status', 'confidence']]

corrections_df.to_csv(f"{OUTPUT_DIR}\\v2_all_corrections.csv", index=False, encoding='latin-1')
print(f"\nSaved: v2_all_corrections.csv")

# High confidence only
high_conf = corrections_df[corrections_df['confidence'] == 'high']
high_conf.to_csv(f"{OUTPUT_DIR}\\v2_high_confidence.csv", index=False, encoding='latin-1')
print(f"Saved: v2_high_confidence.csv ({len(high_conf):,} corrections)")
