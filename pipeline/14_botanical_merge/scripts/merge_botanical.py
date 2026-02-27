import pandas as pd
import os

# Step 1: Merge all 9 normalized botanical CSVs
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_dir = os.path.join(base_dir, 'input')
output_dir = os.path.join(base_dir, 'output')
os.makedirs(output_dir, exist_ok=True)

# Get all normalized CSVs (exclude SAMPLE files)
all_files = os.listdir(input_dir)
csv_files = sorted([f for f in all_files if f.startswith('botanical_') and f.endswith('_normalized.csv')])

print(f"Found {len(csv_files)} botanical CSVs to merge:")
for f in csv_files:
    print(f"  - {f}")

# Read and concatenate all CSVs
dfs = []
for csv_file in csv_files:
    file_path = os.path.join(input_dir, csv_file)
    df = pd.read_csv(file_path, encoding='latin-1')
    print(f"\n{csv_file}: {len(df)} rows, {len(df.columns)} columns")
    dfs.append(df)

# Concatenate all dataframes
botanical_master = pd.concat(dfs, ignore_index=True)

# Validate
print(f"\n=== VALIDATION ===")
print(f"Total rows: {len(botanical_master)}")
print(f"Total columns: {len(botanical_master.columns)}")
print(f"Unique strain_ids: {botanical_master['strain_id'].nunique()}")
print(f"Duplicate strain_ids: {botanical_master['strain_id'].duplicated().sum()}")

# Save
output_path = os.path.join(output_dir, 'botanical_master.csv')
botanical_master.to_csv(output_path, index=False, encoding='latin-1')
print(f"\nSaved: {output_path}")
print(f"   {len(botanical_master)} rows, {len(botanical_master.columns)} columns")
