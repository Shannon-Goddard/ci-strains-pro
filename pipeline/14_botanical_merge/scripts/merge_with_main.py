import pandas as pd
import os

# Step 2: Merge botanical_master with Pipeline 11 main dataset
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_dir = os.path.join(base_dir, 'input')
output_dir = os.path.join(base_dir, 'output')

# Load Pipeline 11 main dataset
pipeline_11_path = os.path.join(input_dir, 'pipeline_11_final.csv')
main_df = pd.read_csv(pipeline_11_path, encoding='latin-1')
print(f"Pipeline 11 dataset: {len(main_df)} rows, {len(main_df.columns)} columns")

# Load botanical_master
botanical_path = os.path.join(output_dir, 'botanical_master.csv')
botanical_df = pd.read_csv(botanical_path, encoding='latin-1')
print(f"Botanical master: {len(botanical_df)} rows, {len(botanical_df.columns)} columns")

# Left join: Keep all Pipeline 11 strains, add botanical data where available
merged_df = main_df.merge(botanical_df, on='strain_id', how='left')

print(f"\n=== VALIDATION ===")
print(f"Total rows: {len(merged_df)} (expected: {len(main_df)})")
print(f"Total columns: {len(merged_df.columns)}")
print(f"Strains with botanical data: {merged_df[botanical_df.columns[1]].notna().sum()}")
print(f"Strains without botanical data: {merged_df[botanical_df.columns[1]].isna().sum()}")

# Save
output_path = os.path.join(output_dir, 'pipeline_14_final.csv')
merged_df.to_csv(output_path, index=False, encoding='latin-1')
print(f"\nSaved: {output_path}")
print(f"   {len(merged_df)} rows, {len(merged_df.columns)} columns")
