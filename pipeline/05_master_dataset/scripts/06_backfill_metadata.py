import pandas as pd
from pathlib import Path

# Paths
MASTER_FILE = Path("../output/master_strains_raw.csv")
S3_INVENTORY = Path("../../03_s3_inventory/s3_html_inventory.csv")
S3_JS_INVENTORY = Path("../../03_s3_inventory/s3_js_html_inventory.csv")

# Load master dataset
print("Loading master dataset...")
df = pd.read_csv(MASTER_FILE, low_memory=False)
print(f"  {len(df):,} strains")

# Load S3 inventories
print("\nLoading S3 inventories...")
s3_df = pd.read_csv(S3_INVENTORY, encoding='latin-1')
s3_js_df = pd.read_csv(S3_JS_INVENTORY, encoding='latin-1')
s3_combined = pd.concat([s3_df, s3_js_df], ignore_index=True)

# Create lookups
s3_to_url = dict(zip(s3_combined['s3_html_key'], s3_combined['url']))
s3_to_date = dict(zip(s3_combined['s3_html_key'], s3_combined['collection_date']))

# Backfill source_url from s3_html_key (only if missing)
print("\nBackfilling source_url from S3 keys...")
missing_url = df['source_url_raw'].isna() & df['s3_html_key_raw'].notna()
df.loc[missing_url, 'source_url_raw'] = df.loc[missing_url, 's3_html_key_raw'].map(s3_to_url)
print(f"  Filled: {missing_url.sum()} records")

# Backfill scraped_at from s3_html_key (only if missing)
print("\nBackfilling scraped_at from S3 keys...")
missing_date = df['scraped_at_raw'].isna() & df['s3_html_key_raw'].notna()
df.loc[missing_date, 'scraped_at_raw'] = df.loc[missing_date, 's3_html_key_raw'].map(s3_to_date)
print(f"  Filled: {missing_date.sum()} records")

# Final coverage
print("\nFinal coverage:")
print(f"  source_url: {df['source_url_raw'].notna().sum()}/{len(df)} ({df['source_url_raw'].notna().sum()/len(df)*100:.1f}%)")
print(f"  scraped_at: {df['scraped_at_raw'].notna().sum()}/{len(df)} ({df['scraped_at_raw'].notna().sum()/len(df)*100:.1f}%)")
print(f"  s3_html_key: {df['s3_html_key_raw'].notna().sum()}/{len(df)} ({df['s3_html_key_raw'].notna().sum()/len(df)*100:.1f}%)")

# Save
df.to_csv(MASTER_FILE, index=False, encoding='utf-8')
print(f"\nSaved: {MASTER_FILE}")
