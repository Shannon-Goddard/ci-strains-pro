import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('../input/pipeline_14_final.csv', encoding='latin-1')

# Column pairs: (old, new, final_name)
pairs = [
    ('thc_content_raw', 'thc_avg', 'thc_avg'),
    ('thc_min_raw', 'thc_min', 'thc_min'),
    ('thc_max_raw', 'thc_max', 'thc_max'),
    ('cbd_content_raw', 'cbd_avg', 'cbd_avg'),
    ('cbd_min_raw', 'cbd_min', 'cbd_min'),
    ('cbd_max_raw', 'cbd_max', 'cbd_max'),
    ('flowering_time_days_clean', 'flowering_days_avg', 'flowering_days_avg'),
    ('height_indoor_cm_clean', 'height_indoor_cm_min', 'height_indoor_cm_min'),
    ('height_outdoor_cm_clean', 'height_outdoor_cm_min', 'height_outdoor_cm_min'),
    ('yield_indoor_g_m2_clean', 'yield_indoor_g_m2_min', 'yield_indoor_g_m2_min'),
    ('yield_outdoor_g_plant_clean', 'yield_outdoor_g_plant_min', 'yield_outdoor_g_plant_min'),
]

conflicts = []

for old_col, new_col, final_col in pairs:
    # Skip if columns don't exist
    if old_col not in df.columns or new_col not in df.columns:
        continue
    
    # Convert to numeric
    df[old_col] = pd.to_numeric(df[old_col], errors='coerce')
    df[new_col] = pd.to_numeric(df[new_col], errors='coerce')
    
    # Create final column: prefer new, fill with old
    df[final_col + '_final'] = df[new_col].fillna(df[old_col])
    
    # Find conflicts (both have data, differ significantly)
    both_exist = df[old_col].notna() & df[new_col].notna()
    
    if both_exist.sum() > 0:
        diff = abs(df.loc[both_exist, old_col] - df.loc[both_exist, new_col])
        
        # Threshold based on column type
        if 'thc' in final_col or 'cbd' in final_col:
            threshold = 10
        elif 'flowering' in final_col:
            threshold = 7
        elif 'height' in final_col:
            threshold = 20
        elif 'yield' in final_col:
            threshold = 100
        else:
            threshold = 10
        
        conflict_mask = diff > threshold
        if conflict_mask.sum() > 0:
            conflict_rows = df.loc[both_exist][conflict_mask].copy()
            conflict_rows['column'] = final_col
            conflict_rows['old_value'] = df.loc[both_exist][conflict_mask][old_col]
            conflict_rows['new_value'] = df.loc[both_exist][conflict_mask][new_col]
            conflict_rows['difference'] = diff[conflict_mask]
            conflict_rows['current_value'] = conflict_rows['new_value']
            conflict_rows['final_value'] = ''
            conflicts.append(conflict_rows[['strain_id', 'strain_name_display', 'seed_bank_display', 'column', 'old_value', 'new_value', 'current_value', 'difference', 'final_value']])

# Save conflicts
if conflicts:
    pd.concat(conflicts).to_csv('../output/conflicts_flagged.csv', index=False, encoding='latin-1')

# Keep only final columns + identity columns
identity_cols = [col for col in df.columns if not any(x in col for x in ['thc_', 'cbd_', 'flowering_', 'height_', 'yield_'])]
final_cols = [col for col in df.columns if col.endswith('_final')]
keep_cols = identity_cols + final_cols

# Rename _final columns (remove suffix)
df_final = df[keep_cols].copy()
df_final.columns = [col.replace('_final', '') if col.endswith('_final') else col for col in df_final.columns]

# Save
df_final.to_csv('../output/pipeline_15_consolidated.csv', index=False, encoding='latin-1')

print(f"Consolidated {len(pairs)} column pairs")
print(f"Flagged {len(conflicts)} conflict groups")
print(f"Final dataset: {len(df_final)} strains, {len(df_final.columns)} columns")
