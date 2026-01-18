import pandas as pd
from pathlib import Path

MASTER_FILE = Path("../output/master_strains_raw.csv")

print("Loading master dataset...")
df = pd.read_csv(MASTER_FILE, low_memory=False)

# Get Seedsman versions
seedsman_reg = df[df['seed_bank'] == 'seedsman'].copy()
seedsman_js = df[df['seed_bank'] == 'seedsman_js'].copy()

print(f"\nSeedsman regular: {len(seedsman_reg)} strains")
print(f"Seedsman JS: {len(seedsman_js)} strains")

# Seedsman regular has s3_html_key_raw like "html/0001e4b9a9c43140.html"
# Seedsman JS has s3_html_key_raw like "html_js/0001e4b9a9c43140_js.html"
# Extract hash and match

# Create lookup: hash -> (source_url, s3_html_key) from JS version
js_lookup = {}
for idx, row in seedsman_js.iterrows():
    s3_key = row['s3_html_key_raw']
    if pd.notna(s3_key):
        # Extract hash from "html_js/0001e4b9a9c43140_js.html"
        hash_val = s3_key.split('/')[-1].replace('_js.html', '')
        js_lookup[hash_val] = (row['source_url_raw'], s3_key)

print(f"\nBuilt lookup with {len(js_lookup)} JS entries")

# Match regular version by extracting hash from their s3_key
matched = 0
for idx, row in seedsman_reg.iterrows():
    s3_key = row['s3_html_key_raw']
    if pd.notna(s3_key):
        # Extract hash from "html/0001e4b9a9c43140.html"
        hash_val = s3_key.split('/')[-1].replace('.html', '')
        if hash_val in js_lookup:
            url, js_s3_key = js_lookup[hash_val]
            df.at[idx, 'source_url_raw'] = url
            # Keep the JS version s3_key (better data)
            df.at[idx, 's3_html_key_raw'] = js_s3_key
            matched += 1

print(f"\nMatched by strain name: {matched}/{len(seedsman_reg)}")

# Save
df.to_csv(MASTER_FILE, index=False, encoding='utf-8')

# Final coverage
print(f"\nFinal coverage:")
print(f"  source_url: {df['source_url_raw'].notna().sum()}/{len(df)} ({df['source_url_raw'].notna().sum()/len(df)*100:.1f}%)")
print(f"  s3_html_key: {df['s3_html_key_raw'].notna().sum()}/{len(df)} ({df['s3_html_key_raw'].notna().sum()/len(df)*100:.1f}%)")

print(f"\nSaved: {MASTER_FILE}")
