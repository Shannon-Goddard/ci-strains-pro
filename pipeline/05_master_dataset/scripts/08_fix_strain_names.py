import pandas as pd
import re
from pathlib import Path

MASTER_FILE = Path("../output/master_strains_raw.csv")

print("Loading master dataset...")
df = pd.read_csv(MASTER_FILE, low_memory=False)
print(f"  Total: {len(df)} strains")

# 1. Remove Gorilla non-strain pages
print("\n1. Removing Gorilla non-strain pages...")
gorilla_bad = df[
    (df['seed_bank'] == 'gorilla') & 
    (df['strain_name_raw'].isna()) &
    (df['source_url_raw'].str.contains('seed-banks|cannabis-seeds', na=False))
]
print(f"  Found {len(gorilla_bad)} non-strain pages")
df = df[~df.index.isin(gorilla_bad.index)]
print(f"  Removed. New total: {len(df)}")

# 2. Extract strain names from URLs for missing names
print("\n2. Extracting strain names from URLs...")
missing = df['strain_name_raw'].isna()

def extract_name_from_url(url):
    if pd.isna(url):
        return None
    # Get last part of URL path
    parts = url.rstrip('/').split('/')
    name = parts[-1] if parts else None
    if name:
        # Remove common suffixes
        name = re.sub(r'\.(html|php|aspx)$', '', name)
        # Remove product IDs
        name = re.sub(r'prod_\d+$', '', name)
        # Replace hyphens/underscores with spaces
        name = name.replace('-', ' ').replace('_', ' ')
        # Remove extra whitespace
        name = ' '.join(name.split())
        return name if name else None
    return None

df.loc[missing, 'strain_name_raw'] = df.loc[missing, 'source_url_raw'].apply(extract_name_from_url)

filled = df['strain_name_raw'].notna().sum()
print(f"  Filled: {filled}/{len(df)} ({filled/len(df)*100:.1f}%)")

# Save
df.to_csv(MASTER_FILE, index=False, encoding='utf-8')
print(f"\nSaved: {MASTER_FILE}")

# Final stats
print("\nFinal coverage:")
print(f"  Total strains: {len(df)}")
print(f"  strain_name: {df['strain_name_raw'].notna().sum()}/{len(df)} ({df['strain_name_raw'].notna().sum()/len(df)*100:.1f}%)")
print(f"  Still missing: {df['strain_name_raw'].isna().sum()}")
