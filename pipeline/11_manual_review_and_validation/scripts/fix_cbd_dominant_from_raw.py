import pandas as pd

input_file = 'output/pipeline_11_clean.csv'
output_file = 'output/pipeline_11_clean.csv'

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df):,}\n")

print("Current cbd_dominant status:")
print(df['cbd_dominant'].value_counts(dropna=False))
print()

# Detect CBD in strain_name_raw (case-insensitive, word boundary)
has_cbd = df['strain_name_raw'].fillna('').str.contains(r'\bCBD\b', case=False, regex=True)

# Set cbd_dominant: TRUE if CBD found, FALSE otherwise
df['cbd_dominant'] = has_cbd

print(f"Set cbd_dominant=TRUE for {has_cbd.sum():,} strains with 'CBD' in strain_name_raw")
print(f"Set cbd_dominant=FALSE for {(~has_cbd).sum():,} strains without 'CBD'\n")

print("New cbd_dominant status:")
print(df['cbd_dominant'].value_counts(dropna=False))
print()

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"Saved to: {output_file}\n")

# Show sample CBD strains
if has_cbd.sum() > 0:
    print("Sample CBD strains:")
    sample = df[has_cbd][['strain_name_raw', 'strain_name_display', 'cbd_dominant']].head(20)
    print(sample.to_string(index=False))
