import pandas as pd
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_dir = os.path.join(base_dir, 'output')

# Load final dataset
final_path = os.path.join(output_dir, 'pipeline_14_final.csv')
df = pd.read_csv(final_path, encoding='latin-1', low_memory=False)

print("=== PIPELINE 14 VALIDATION REPORT ===\n")

# Basic stats
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Unique strain_ids: {df['strain_id'].nunique()}")
print(f"Duplicate strain_ids: {df['strain_id'].duplicated().sum()}")

# Botanical coverage
botanical_cols = ['thc_avg', 'cbd_avg', 'flowering_days_avg', 'height_indoor_cm_min', 'yield_indoor_g_m2_min']
print(f"\n=== BOTANICAL DATA COVERAGE ===")
for col in botanical_cols:
    if col in df.columns:
        coverage = df[col].notna().sum()
        pct = (coverage / len(df)) * 100
        print(f"{col}: {coverage} strains ({pct:.1f}%)")

# Check for data loss
print(f"\n=== DATA INTEGRITY ===")
print(f"Expected rows: 21,220")
print(f"Actual rows: {len(df)}")
print(f"Difference: {21220 - len(df)}")

# Column list
print(f"\n=== ALL COLUMNS ({len(df.columns)}) ===")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")
