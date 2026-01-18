import pandas as pd
import json
from pathlib import Path
from schema import COLUMN_MAPPINGS, EXCLUDED_COLUMNS
import uuid

CSV_DIR = Path("../csv")
OUTPUT_DIR = Path("../output")

# Load mapping
with open(OUTPUT_DIR / "column_mapping.json") as f:
    mappings = json.load(f)

# Build lookup: (seed_bank, original_col) -> unified_col
mapping_lookup = {}
for m in mappings:
    key = (m['seed_bank'], m['original_column'])
    mapping_lookup[key] = m['maps_to']

# Process each CSV
all_data = []
csv_files = sorted(CSV_DIR.glob("*.csv"))

for csv_file in csv_files:
    seed_bank = csv_file.stem.replace('_extracted', '').replace('_maximum_extraction', '').replace('_js_extracted', '')
    
    print(f"Processing {seed_bank}...")
    df = pd.read_csv(csv_file, encoding='latin-1')
    
    # Create mapped dataframe
    mapped_data = {}
    
    for col in df.columns:
        col_lower = col.lower()
        
        # Skip excluded columns
        if any(excl in col_lower for excl in EXCLUDED_COLUMNS):
            continue
        
        # Check if mapped
        key = (seed_bank, col)
        if key in mapping_lookup:
            unified_col = mapping_lookup[key]
            mapped_data[unified_col] = df[col]
    
    # Create dataframe with mapped columns
    if mapped_data:
        mapped_df = pd.DataFrame(mapped_data)
        mapped_df['seed_bank'] = seed_bank
        mapped_df['strain_id'] = [str(uuid.uuid4()) for _ in range(len(mapped_df))]
        all_data.append(mapped_df)
        print(f"  Mapped {len(mapped_data)} columns, {len(mapped_df)} strains")

# Combine all
master_df = pd.concat(all_data, ignore_index=True)

# Reorder columns (core fields first)
core_cols = ['strain_id', 'seed_bank', 'strain_name_raw']
other_cols = [c for c in master_df.columns if c not in core_cols]
master_df = master_df[core_cols + sorted(other_cols)]

# Save
output_file = OUTPUT_DIR / "master_strains_raw.csv"
master_df.to_csv(output_file, index=False, encoding='utf-8')

print(f"\nMaster dataset created:")
print(f"  Total strains: {len(master_df)}")
print(f"  Total columns: {len(master_df.columns)}")
print(f"  Saved to: {output_file}")
