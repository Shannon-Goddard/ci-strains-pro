import pandas as pd

df = pd.read_csv('output/all_strains_standardized.csv', encoding='latin-1', low_memory=False)
print(f"Before: {len(df)} rows")

# Remove null URLs
df_clean = df[df['source_url_raw'].notna()].copy()
print(f"After: {len(df_clean)} rows")
print(f"Removed: {len(df) - len(df_clean)} null URLs")

df_clean.to_csv('output/all_strains_standardized_clean.csv', index=False, encoding='latin-1')
print("\nSaved: output/all_strains_standardized_clean.csv")
