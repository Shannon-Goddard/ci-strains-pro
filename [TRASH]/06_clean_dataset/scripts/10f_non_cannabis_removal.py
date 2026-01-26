"""
Step 10F: Non-Cannabis Product Removal
Removes vape products, variety packs, and non-strain entries.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd

# Read input
df = pd.read_csv('../../cleaning_csv/10e_breeder_standardized.csv', encoding='latin-1', low_memory=False)
print(f"Input: {len(df)} rows")

# URLs to remove (from BREEDER_EXTRACTION_FAILURES.md)
URLS_TO_REMOVE = [
    # Variety packs
    'https://www.gorilla-cannabis-seeds.co.uk/bulkseeds/feminized/bulk-cannabis-seeds.html',
    'https://www.northatlanticseed.com/product/early-girls-multipack-f/',
    
    # Puffco vape products
    'https://neptuneseedbank.com/product/puffco-proxy-droplet/',
    'https://neptuneseedbank.com/product/puffco-proxy-travel-pack/',
    'https://www.northatlanticseed.com/product/proxy-kit/',
    'https://www.northatlanticseed.com/product/plus/',
    'https://www.northatlanticseed.com/product/hot-knife/',
    'https://www.northatlanticseed.com/product/peak-pro/',
]

# Remove by URL
initial_count = len(df)
df = df[~df['source_url_raw'].isin(URLS_TO_REMOVE)]
url_removed = initial_count - len(df)
print(f"Removed by URL: {url_removed} rows")

# Remove by breeder name (Puffco products)
initial_count = len(df)
df = df[df['breeder_name_clean'] != 'Puffco']
breeder_removed = initial_count - len(df)
print(f"Removed by breeder (Puffco): {breeder_removed} rows")

total_removed = url_removed + breeder_removed
print(f"Total removed: {total_removed} rows")

# Output
df.to_csv('../../cleaning_csv/10f_non_cannabis_removed.csv', index=False, encoding='utf-8')
df.head(100).to_csv('output/10f_non_cannabis_removed_sample.csv', index=False, encoding='utf-8')
print(f"Output: {len(df)} rows -> ../../cleaning_csv/10f_non_cannabis_removed.csv")
