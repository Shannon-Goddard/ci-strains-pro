import pandas as pd
import re
from pathlib import Path

# Paths
input_file = Path('../output/05_genetics_normalized.csv')
output_file = Path('../output/06_strain_names_normalized.csv')
report_file = Path('../output/06_strain_name_normalization_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

# Normalize strain name for matching
def normalize_strain_name(name):
    if pd.isna(name): return None
    
    name = str(name).lower().strip()
    
    # Remove common suffixes/prefixes
    patterns = [
        r'\s*\(.*?\)',  # Remove parentheses content
        r'\s*\[.*?\]',  # Remove brackets content
        r'\s*feminized.*$',
        r'\s*feminised.*$',
        r'\s*fem.*$',
        r'\s*auto.*$',
        r'\s*autoflower.*$',
        r'\s*regular.*$',
        r'\s*seeds.*$',
        r'\s*strain.*$',
        r'\s*cannabis.*$',
        r'\s*marijuana.*$',
        r'\s*\d+\s*pack.*$',  # Remove pack sizes
        r'\s*x\s*\d+.*$',     # Remove quantities
    ]
    
    for pattern in patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # Remove extra whitespace
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Remove special characters except #
    name = re.sub(r'[^\w\s#-]', '', name)
    
    return name if name else None

df['strain_name_normalized'] = df['strain_name_raw'].apply(normalize_strain_name)

# Count normalizations
normalized_count = df['strain_name_normalized'].notna().sum()
unique_raw = df['strain_name_raw'].nunique()
unique_normalized = df['strain_name_normalized'].nunique()
duplicates_created = unique_raw - unique_normalized

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 06: Strain Name Normalization Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n")
    f.write(f"Strain names normalized: {normalized_count}\n\n")
    f.write("Normalization impact:\n")
    f.write(f"  Unique raw names: {unique_raw}\n")
    f.write(f"  Unique normalized names: {unique_normalized}\n")
    f.write(f"  Potential duplicates identified: {duplicates_created}\n")
    f.write(f"  Deduplication rate: {(duplicates_created / unique_raw * 100):.2f}%\n")

print(f"\n[SUCCESS] Step 06 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Potential duplicates identified: {duplicates_created}")
