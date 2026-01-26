"""
Step 11D: Fix Breeder Extraction Failures
Fixes documented breeder extraction issues from Shannon's QA.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd
import re

df = pd.read_csv('../../cleaning_csv/11_breeder_extracted.csv', encoding='latin-1', low_memory=False)
print(f"Input: {len(df)} rows")

operations = 0

# Fix 1: Exotic Genetics - all exoticgenetix.com should be "Exotic Genetix"
mask = df['source_url_raw'].str.contains('exoticgenetix.com', na=False)
df.loc[mask, 'breeder_name_clean'] = 'Exotic Genetix'
ops1 = mask.sum()
print(f"Exotic Genetix fixed: {ops1}")
operations += ops1

# Fix 2: Barney's Farm - encoding issues
mask = df['breeder_name_clean'].str.contains('Barney', na=False)
df.loc[mask, 'breeder_name_clean'] = df.loc[mask, 'breeder_name_clean'].str.replace(
    r"Barney[â€™'s]+\s*Farm.*", "Barney's Farm", regex=True
)
ops2 = mask.sum()
print(f"Barney's Farm fixed: {ops2}")
operations += ops2

# Fix 3: Cali Connection - remove "Seeds" suffix
mask = df['breeder_name_clean'] == 'Cali Connection Seeds'
df.loc[mask, 'breeder_name_clean'] = 'Cali Connection'
ops3 = mask.sum()
print(f"Cali Connection fixed: {ops3}")
operations += ops3

# Fix 4: Crop King - all cropkingseeds.com should be "Crop King"
mask = df['source_url_raw'].str.contains('cropkingseeds.com', na=False)
df.loc[mask, 'breeder_name_clean'] = 'Crop King'
ops4 = mask.sum()
print(f"Crop King fixed: {ops4}")
operations += ops4

# Fix 5: Clean encoding artifacts (â€™, â€", etc.)
encoding_fixes = {
    'â€™': "'",
    'â€"': '-',
    'â€"': '--',
    'Â ': ' ',
}
for old, new in encoding_fixes.items():
    mask = df['breeder_name_clean'].str.contains(old, na=False, regex=False)
    if mask.any():
        df.loc[mask, 'breeder_name_clean'] = df.loc[mask, 'breeder_name_clean'].str.replace(old, new)
        ops = mask.sum()
        print(f"Encoding fix '{old}': {ops}")
        operations += ops

# Fix 6: Remove "Home/Seeds/" prefix patterns
mask = df['breeder_name_clean'].str.contains('Home/', na=False)
df.loc[mask, 'breeder_name_clean'] = df.loc[mask, 'breeder_name_clean'].str.replace(
    r'^Home/Seeds/\s*', '', regex=True
)
ops6 = mask.sum()
print(f"Home/Seeds prefix removed: {ops6}")
operations += ops6

# Fix 7: Clean trailing junk (pack sizes, codes)
df['breeder_name_clean'] = df['breeder_name_clean'].str.replace(
    r'\s*[–—-]\s*.*\(F\)\s*\(\d+\).*$', '', regex=True
)
df['breeder_name_clean'] = df['breeder_name_clean'].str.strip()

print(f"\nTotal operations: {operations}")

# Verify no nulls
nulls = df['breeder_name_clean'].isna().sum()
print(f"NULL breeders: {nulls}")

df.to_csv('../../cleaning_csv/11d_breeder_fixed.csv', index=False, encoding='utf-8')
df.head(100).to_csv('output/11d_breeder_fixed_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: {len(df)} rows -> ../../cleaning_csv/11d_breeder_fixed.csv")
