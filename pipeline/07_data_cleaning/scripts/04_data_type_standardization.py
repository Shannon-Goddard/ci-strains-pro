import pandas as pd
import numpy as np
from pathlib import Path

# Paths
input_file = Path('../output/03_placeholders_removed.csv')
output_file = Path('../output/04_data_types_standardized.csv')
report_file = Path('../output/04_data_type_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

conversions = {}

# Numeric columns (clean fields should be numeric)
numeric_cols = [col for col in df.columns if col.endswith('_clean') and 'percentage' in col or 'days' in col or 'cm' in col or 'g_' in col]

for col in numeric_cols:
    before_type = df[col].dtype
    df[col] = pd.to_numeric(df[col], errors='coerce')
    after_type = df[col].dtype
    if before_type != after_type:
        conversions[col] = f"{before_type} -> {after_type}"

# THC/CBD min/max/avg columns
for prefix in ['thc', 'cbd', 'cbn']:
    for suffix in ['min', 'max', 'average', 'avg']:
        col = f"{prefix}_{suffix}_raw"
        if col in df.columns:
            before_type = df[col].dtype
            df[col] = pd.to_numeric(df[col], errors='coerce')
            after_type = df[col].dtype
            if before_type != after_type:
                conversions[col] = f"{before_type} -> {after_type}"

# Percentage columns
percentage_cols = [col for col in df.columns if 'percentage' in col and col.endswith('_raw')]
for col in percentage_cols:
    before_type = df[col].dtype
    df[col] = pd.to_numeric(df[col], errors='coerce')
    after_type = df[col].dtype
    if before_type != after_type:
        conversions[col] = f"{before_type} -> {after_type}"

# Boolean columns
bool_cols = [col for col in df.columns if col.startswith('is_') and col.endswith('_raw')]
for col in bool_cols:
    before_type = df[col].dtype
    df[col] = df[col].map({'true': True, 'false': False, 'True': True, 'False': False, '1': True, '0': False, 1: True, 0: False})
    after_type = df[col].dtype
    if str(before_type) != str(after_type):
        conversions[col] = f"{before_type} -> {after_type}"

# Text columns (ensure string type)
text_cols = ['strain_name_raw', 'breeder_name_raw', 'seed_bank', 'dominant_type_raw', 
             'seed_type_raw', 'flowering_type_raw', 'difficulty_raw']
for col in text_cols:
    if col in df.columns:
        before_type = df[col].dtype
        df[col] = df[col].astype(str)
        df[col] = df[col].replace('nan', np.nan)
        after_type = df[col].dtype
        if before_type != after_type:
            conversions[col] = f"{before_type} -> {after_type}"

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 04: Data Type Standardization Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n")
    f.write(f"Columns converted: {len(conversions)}\n\n")
    f.write("Type conversions:\n")
    for col, conversion in sorted(conversions.items()):
        f.write(f"  {col}: {conversion}\n")

print(f"\n[SUCCESS] Step 04 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Columns converted: {len(conversions)}")
