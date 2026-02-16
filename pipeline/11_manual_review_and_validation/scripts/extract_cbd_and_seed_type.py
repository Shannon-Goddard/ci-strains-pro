import pandas as pd
import re

input_file = 'output/pipeline_11_clean.csv'
output_file = 'output/pipeline_11_clean.csv'

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df):,}\n")

# Initialize new columns
df['cbd_level'] = None
df['cbd_ratio'] = None
df['flowering_type'] = 'Unknown'
df['is_feminized'] = False

# 1. CBD Level extraction
high_cbd_pattern = r'\b(high cbd|cbd rich|cbd crew)\b'
df.loc[df['strain_name_raw'].fillna('').str.contains(high_cbd_pattern, case=False, regex=True), 'cbd_level'] = 'High'

# 2. CBD Ratio extraction (1:1, 2:1, 1:20, etc.)
ratio_pattern = r'(\d+:\d+)'
ratios = df['strain_name_raw'].fillna('').str.extract(ratio_pattern, expand=False)
df.loc[ratios.notna(), 'cbd_ratio'] = ratios[ratios.notna()]

# 3. Flowering Type (use existing is_autoflower)
df.loc[df['is_autoflower'] == True, 'flowering_type'] = 'Autoflower'
df.loc[df['is_autoflower'] == False, 'flowering_type'] = 'Photoperiod'

# 4. Feminized detection
fem_pattern = r'\b(fem|feminized|feminised)\b'
df['is_feminized'] = df['strain_name_raw'].fillna('').str.contains(fem_pattern, case=False, regex=True)

# Stats
print("=== CBD LEVEL ===")
print(df['cbd_level'].value_counts(dropna=False))
print()

print("=== CBD RATIO ===")
print(f"Found {df['cbd_ratio'].notna().sum()} strains with CBD ratios")
if df['cbd_ratio'].notna().sum() > 0:
    print(df['cbd_ratio'].value_counts().head(10))
print()

print("=== FLOWERING TYPE ===")
print(df['flowering_type'].value_counts(dropna=False))
print()

print("=== IS FEMINIZED ===")
print(df['is_feminized'].value_counts(dropna=False))
print()

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"Saved to: {output_file}\n")

# Samples
print("Sample High CBD strains:")
if (df['cbd_level'] == 'High').sum() > 0:
    print(df[df['cbd_level'] == 'High'][['strain_name_raw', 'cbd_level', 'cbd_ratio']].head(10).to_string(index=False))
print()

print("\nSample CBD Ratio strains:")
if df['cbd_ratio'].notna().sum() > 0:
    print(df[df['cbd_ratio'].notna()][['strain_name_raw', 'cbd_ratio', 'cbd_level']].head(10).to_string(index=False))
print()

print("\nSample Feminized Autoflowers:")
fem_auto = (df['is_feminized'] == True) & (df['flowering_type'] == 'Autoflower')
if fem_auto.sum() > 0:
    print(df[fem_auto][['strain_name_raw', 'flowering_type', 'is_feminized']].head(10).to_string(index=False))
