import pandas as pd
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURATION ---
VALIDATION_FILE = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\output\s3_validation_results.json"
INPUT_CSV = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\input\pipeline_16_cleaned.csv"
OUTPUT_DIR = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\18_full_validation\output"

# Load validation results
print("📂 Loading validation results...")
with open(VALIDATION_FILE, 'r', encoding='utf-8') as f:
    results = json.load(f)

print(f"✅ Loaded {len(results):,} validation results\n")

# Analyze results
corrections_needed = []
high_confidence_corrections = []
low_confidence_flags = []
errors = []

for result in results:
    if 'error' in result:
        errors.append(result)
        continue
    
    strain_id = result.get('strain_id')
    strain_name = result.get('strain_name')
    fields = result.get('fields', {})
    
    for field_name, field_data in fields.items():
        status = field_data.get('status')
        confidence = field_data.get('confidence')
        current = field_data.get('current')
        extracted = field_data.get('extracted')
        
        if status in ['incorrect', 'missing']:
            correction = {
                'strain_id': strain_id,
                'strain_name': strain_name,
                'field': field_name,
                'current_value': current,
                'extracted_value': extracted,
                'status': status,
                'confidence': confidence
            }
            
            corrections_needed.append(correction)
            
            if confidence == 'high':
                high_confidence_corrections.append(correction)
            elif confidence == 'low':
                low_confidence_flags.append(correction)

# Generate summary
print("=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)
print(f"Total Strains Validated: {len(results):,}")
print(f"Errors: {len(errors):,}")
print(f"Total Corrections Needed: {len(corrections_needed):,}")
print(f"  - High Confidence: {len(high_confidence_corrections):,}")
print(f"  - Medium/Low Confidence: {len(low_confidence_flags):,}")
print("=" * 60)

# Save correction files
print("\n💾 Saving correction files...")

# High confidence corrections (auto-apply)
high_conf_df = pd.DataFrame(high_confidence_corrections)
high_conf_file = f"{OUTPUT_DIR}\\high_confidence_corrections.csv"
high_conf_df.to_csv(high_conf_file, index=False, encoding='utf-8')
print(f"✅ High confidence: {high_conf_file}")

# Low confidence flags (manual review)
low_conf_df = pd.DataFrame(low_confidence_flags)
low_conf_file = f"{OUTPUT_DIR}\\manual_review_needed.csv"
low_conf_df.to_csv(low_conf_file, index=False, encoding='utf-8')
print(f"⚠️  Manual review: {low_conf_file}")

# All corrections
all_corr_df = pd.DataFrame(corrections_needed)
all_corr_file = f"{OUTPUT_DIR}\\all_corrections.csv"
all_corr_df.to_csv(all_corr_file, index=False, encoding='utf-8')
print(f"📊 All corrections: {all_corr_file}")

# Errors
if errors:
    errors_df = pd.DataFrame(errors)
    errors_file = f"{OUTPUT_DIR}\\validation_errors.csv"
    errors_df.to_csv(errors_file, index=False, encoding='utf-8')
    print(f"❌ Errors: {errors_file}")

# Field-level breakdown
print("\n" + "=" * 60)
print("CORRECTIONS BY FIELD")
print("=" * 60)
field_counts = all_corr_df['field'].value_counts()
for field, count in field_counts.items():
    print(f"{field:25} {count:,}")

print("\n✅ Analysis complete!")
