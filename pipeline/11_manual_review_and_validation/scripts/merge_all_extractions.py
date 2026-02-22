import pandas as pd

# Read all CSVs
df_base = pd.read_csv('output/strain_name_from_source_url_v2.csv', encoding='latin-1')
df_fast = pd.read_csv('output/is_fast_flowering.csv', encoding='latin-1', dtype={'is_fast_flowering': str})
df_regular = pd.read_csv('output/is_regular_flowering.csv', encoding='latin-1', dtype={'is_regular_flowering': str})
df_feminized = pd.read_csv('output/is_feminized_flowering.csv', encoding='latin-1', dtype={'is_feminized_flowering': str})
df_auto = pd.read_csv('output/is_auto_flowering.csv', encoding='latin-1', dtype={'is_auto_flowering': str})
df_aka = pd.read_csv('output/aka_strain_names.csv', encoding='latin-1')
df_version = pd.read_csv('output/version.csv', encoding='latin-1')

# Merge all on strain_id
df = df_base.copy()
df = df.merge(df_fast[['strain_id', 'is_fast_flowering']], on='strain_id', how='left')
df = df.merge(df_regular[['strain_id', 'is_regular_flowering']], on='strain_id', how='left')
df = df.merge(df_feminized[['strain_id', 'is_feminized_flowering']], on='strain_id', how='left')
df = df.merge(df_auto[['strain_id', 'is_auto_flowering']], on='strain_id', how='left')
df = df.merge(df_aka[['strain_id', 'aka_strain_names']], on='strain_id', how='left')
df = df.merge(df_version[['strain_id', 'version']], on='strain_id', how='left')

# Save merged file
df.to_csv('output/url_extraction_review.csv', index=False, encoding='latin-1')

print(f"Created url_extraction_review.csv with {len(df)} rows")
print(f"\nColumns: {', '.join(df.columns)}")
