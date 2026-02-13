import pandas as pd

clean_file = "output/pipeline_11_clean.csv"
source_file = "input/pipeline_11_breeder_extracted.csv"

print("Reading files...")
df_clean = pd.read_csv(clean_file, encoding='latin-1', low_memory=False)
df_source = pd.read_csv(source_file, encoding='latin-1', low_memory=False)

print(f"Clean: {len(df_clean):,} strains")
print(f"Source: {len(df_source):,} strains")

# Check current state
empty_count = df_clean['strain_name_raw'].isna().sum()
print(f"\nEmpty strain_name_raw: {empty_count:,}")

# Update from source
print("\nUpdating strain_name_raw from source...")
df_clean = df_clean.drop(columns=['strain_name_raw'])
df_clean = df_clean.merge(
    df_source[['strain_id', 'strain_name_raw']], 
    on='strain_id', 
    how='left'
)

# Reorder
cols = df_clean.columns.tolist()
cols.remove('strain_name_raw')
cols.insert(1, 'strain_name_raw')
df_clean = df_clean[cols]

# Check coverage
missing = df_clean['strain_name_raw'].isna().sum()
print(f"Coverage: {len(df_clean) - missing:,} / {len(df_clean):,} ({((len(df_clean) - missing) / len(df_clean) * 100):.1f}%)")

df_clean.to_csv(clean_file, index=False, encoding='utf-8')
print(f"\nSaved to: {clean_file}")

print("\nSample:")
print(df_clean[['strain_name_raw', 'strain_name_display_manual', 'strain_name_slug']].head(5).to_string(index=False))
