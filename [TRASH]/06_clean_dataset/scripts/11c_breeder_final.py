"""
Step 11C: Final Breeder Cleanup
Cleans Seedsman breeders and removes non-cannabis products.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd
import re

df = pd.read_csv('../../cleaning_csv/11b_breeder_merged.csv', encoding='latin-1', low_memory=False)
print(f"Input: {len(df)} rows")
print(f"Missing breeders: {df['breeder_name_clean'].isna().sum()}")

# Fix Seedsman: Extract breeder before "Parental lines"
seedsman_mask = (df['seed_bank'] == 'seedsman_js') & df['breeder_name_clean'].isna() & df['breeder_name_raw'].notna()
for idx in df[seedsman_mask].index:
    raw = df.at[idx, 'breeder_name_raw']
    if 'Parental lines' in raw:
        breeder = raw.split('Parental lines')[0].strip()
        df.at[idx, 'breeder_name_clean'] = breeder

seedsman_fixed = seedsman_mask.sum()
print(f"Seedsman fixed: {seedsman_fixed}")

# Remove non-cannabis products
non_cannabis_urls = [
    'https://seeds.compound-genetics.com/products/compound-genetics-x-method-seven',  # sunglasses
    'https://exoticgenetix.com/product/splitz-strain-t-shirt/',  # t-shirt
    'https://exoticgenetix.com/product/neon-nights-gen/',  # t-shirt
]
initial = len(df)
df = df[~df['source_url_raw'].isin(non_cannabis_urls)]
removed = initial - len(df)
print(f"Non-cannabis removed: {removed}")

# Fill remaining with seed bank name as fallback
remaining_mask = df['breeder_name_clean'].isna()
df.loc[remaining_mask, 'breeder_name_clean'] = df.loc[remaining_mask, 'seed_bank'].str.replace('_', ' ').str.title()
fallback_filled = remaining_mask.sum()
print(f"Fallback filled: {fallback_filled}")

print(f"\nFinal breeder coverage: {df['breeder_name_clean'].notna().sum()} ({df['breeder_name_clean'].notna().sum()/len(df)*100:.1f}%)")

df.to_csv('../../cleaning_csv/11c_breeder_final.csv', index=False, encoding='utf-8')
df.head(100).to_csv('output/11c_breeder_final_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: {len(df)} rows -> ../../cleaning_csv/11c_breeder_final.csv")
