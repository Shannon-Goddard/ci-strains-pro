import pandas as pd

# Read both CSVs
df_clean = pd.read_csv('output/pipeline_11_clean.csv', encoding='latin-1')
df_review = pd.read_csv('output/url_extraction_review.csv', encoding='latin-1', 
                        dtype={'is_fast_flowering': str, 'is_regular_flowering': str, 
                               'is_feminized_flowering': str, 'is_auto_flowering': str})

# Merge on strain_id
df_final = df_clean.merge(
    df_review[['strain_id', 'strain_name_from_source_url', 'is_fast_flowering', 
               'is_regular_flowering', 'is_feminized_flowering', 'is_auto_flowering', 
               'aka_strain_names', 'version']], 
    on='strain_id', 
    how='left'
)

# Save as pipeline_11_final.csv
df_final.to_csv('output/pipeline_11_final.csv', index=False, encoding='latin-1')

print(f"Created pipeline_11_final.csv with {len(df_final)} rows")
print(f"Total columns: {len(df_final.columns)}")
print(f"\nNew columns added:")
print("- strain_name_from_source_url")
print("- is_fast_flowering")
print("- is_regular_flowering")
print("- is_feminized_flowering")
print("- is_auto_flowering")
print("- aka_strain_names")
print("- version")
