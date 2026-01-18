import pandas as pd
from pathlib import Path

# Paths
MASTER_FILE = Path("../output/master_strains_raw.csv")
S3_INVENTORY = Path("../../03_s3_inventory/s3_html_inventory.csv")
S3_JS_INVENTORY = Path("../../03_s3_inventory/s3_js_html_inventory.csv")

# Load master dataset
print("Loading master dataset...")
df = pd.read_csv(MASTER_FILE, low_memory=False)
print(f"  {len(df):,} strains loaded")

# Load S3 inventories
print("\nLoading S3 inventories...")
s3_df = pd.read_csv(S3_INVENTORY, encoding='latin-1')
s3_js_df = pd.read_csv(S3_JS_INVENTORY, encoding='latin-1')

# Rename html_key to s3_html_key in JS inventory if needed
if 'html_key' in s3_js_df.columns:
    s3_js_df = s3_js_df.rename(columns={'html_key': 's3_html_key'})

print(f"  Regular HTML: {len(s3_df):,} records")
print(f"  JS HTML: {len(s3_js_df):,} records")

# Combine inventories
s3_combined = pd.concat([s3_df, s3_js_df], ignore_index=True)
print(f"  Combined: {len(s3_combined):,} records")

# Create lookup: url -> s3_html_key
s3_lookup = dict(zip(s3_combined['url'], s3_combined['s3_html_key']))

# Map s3_html_key_raw from source_url_raw (only if missing)
print("\nMapping S3 keys...")
missing_s3 = df['s3_html_key_raw'].isna()
df.loc[missing_s3, 's3_html_key_raw'] = df.loc[missing_s3, 'source_url_raw'].map(s3_lookup)

matched = df['s3_html_key_raw'].notna().sum()
print(f"  Matched: {matched:,} / {len(df):,} ({matched/len(df)*100:.1f}%)")

# Save updated master
df.to_csv(MASTER_FILE, index=False, encoding='utf-8')
print(f"\nUpdated master dataset saved: {MASTER_FILE}")
