import pandas as pd
import re

input_file = 'output/pipeline_11_clean.csv'
output_file = 'output/pipeline_11_clean.csv'

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df):,}\n")

# Count current autoflower status
print("Current is_autoflower status:")
print(df['is_autoflower'].value_counts(dropna=False))
print()

# Pattern to detect auto/automatic (case-insensitive, word boundary)
auto_pattern = r'\b(auto|automatic)\b'

# Find strains with auto keywords in strain_name_raw
has_auto_keyword = df['strain_name_raw'].fillna('').str.contains(auto_pattern, case=False, regex=True)

# Update is_autoflower to TRUE where auto keyword found
updates = has_auto_keyword & (df['is_autoflower'] != True)
df.loc[has_auto_keyword, 'is_autoflower'] = True

print(f"Updated {updates.sum():,} strains to is_autoflower=TRUE based on strain_name_raw\n")

print("New is_autoflower status:")
print(df['is_autoflower'].value_counts(dropna=False))
print()

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"Saved to: {output_file}\n")

# Show sample updates
if updates.sum() > 0:
    print("Sample strains updated:")
    sample = df[updates][['strain_name_raw', 'strain_name_display', 'is_autoflower']].head(20)
    print(sample.to_string(index=False))
