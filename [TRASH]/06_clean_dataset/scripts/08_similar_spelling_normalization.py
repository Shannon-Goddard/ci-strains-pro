import pandas as pd
import re
from pathlib import Path

# Paths
input_file = Path('../output/07_aka_extracted.csv')
output_file = Path('../output/08_similar_spelling_normalized.csv')
report_file = Path('../output/08_similar_spelling_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

# Normalize for similar spelling matching
def normalize_similar_spelling(name):
    if pd.isna(name): return None
    
    name = str(name).lower().strip()
    
    # Remove all spaces (handles "grand daddy" vs "granddaddy")
    name_no_space = re.sub(r'\s+', '', name)
    
    # Remove hyphens and underscores
    name_no_space = name_no_space.replace('-', '').replace('_', '')
    
    # Remove special characters except numbers
    name_no_space = re.sub(r'[^\w]', '', name_no_space)
    
    return name_no_space if name_no_space else None

df['similar_spelling_clean'] = df['strain_name_normalized'].apply(normalize_similar_spelling)

# Calculate impact
unique_normalized = df['strain_name_normalized'].nunique()
unique_similar = df['similar_spelling_clean'].nunique()
additional_matches = unique_normalized - unique_similar

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 08: Similar Spelling Normalization Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n\n")
    f.write("Normalization impact:\n")
    f.write(f"  Unique normalized names: {unique_normalized}\n")
    f.write(f"  Unique similar spelling forms: {unique_similar}\n")
    f.write(f"  Additional matches identified: {additional_matches}\n")
    f.write(f"  Additional match rate: {(additional_matches / unique_normalized * 100):.2f}%\n\n")
    f.write("Examples:\n")
    f.write("  'grand daddy purple' -> 'granddaddypurple'\n")
    f.write("  'girl-scout-cookies' -> 'girlscoutcookies'\n")
    f.write("  'og #1' -> 'og1'\n")

print(f"\n[SUCCESS] Step 08 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Additional matches: {additional_matches}")
