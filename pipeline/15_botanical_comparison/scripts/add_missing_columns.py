import pandas as pd

# Load reviewed dataset
df = pd.read_csv('../output/pipeline_15_consolidated_reviewed.csv', encoding='latin-1')

# Load botanical master with all min/max columns
botanical = pd.read_csv('../input/botanical_master.csv', encoding='latin-1')

# Columns to add
add_cols = [
    'flowering_days_min', 'flowering_days_max',
    'height_indoor_cm_max', 'height_outdoor_cm_max',
    'yield_indoor_g_m2_max', 'yield_outdoor_g_plant_max'
]

# Keep only strain_id and columns to add
botanical_subset = botanical[['strain_id'] + [c for c in add_cols if c in botanical.columns]]

# Merge
df = df.merge(botanical_subset, on='strain_id', how='left')

# Save
df.to_csv('../output/pipeline_15_final.csv', index=False, encoding='latin-1')

print(f"Added {len([c for c in add_cols if c in botanical.columns])} columns")
print(f"Final dataset: {len(df)} strains, {len(df.columns)} columns")
