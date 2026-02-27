import pandas as pd

# Load conflicts with your final_value decisions
conflicts = pd.read_csv('../output/conflicts_flagged.csv', encoding='latin-1')

# Filter only rows where you made a decision
overrides = conflicts[conflicts['final_value'].notna() & (conflicts['final_value'] != '')].copy()

if len(overrides) == 0:
    print("No overrides found. Fill in final_value column in conflicts_flagged.csv")
    exit()

# Map "old_value" and "new_value" strings to actual values
for idx, row in overrides.iterrows():
    if str(row['final_value']).strip().lower() == 'old_value':
        overrides.at[idx, 'final_value'] = row['old_value']
    elif str(row['final_value']).strip().lower() == 'new_value':
        overrides.at[idx, 'final_value'] = row['new_value']

# Load consolidated dataset
df = pd.read_csv('../output/pipeline_15_consolidated.csv', encoding='latin-1')

# Apply overrides
for _, row in overrides.iterrows():
    strain_id = row['strain_id']
    column = row['column']
    final_value = pd.to_numeric(row['final_value'], errors='coerce')
    
    df.loc[df['strain_id'] == strain_id, column] = final_value

# Save
df.to_csv('../output/pipeline_15_consolidated_reviewed.csv', index=False, encoding='latin-1')

# Count by decision type
old_count = conflicts[conflicts['final_value'].str.lower() == 'old_value'].shape[0]
new_count = conflicts[conflicts['final_value'].str.lower() == 'new_value'].shape[0]
custom_count = len(overrides) - old_count - new_count

print(f"Applied {len(overrides)} overrides:")
print(f"  - Kept OLD: {old_count}")
print(f"  - Kept NEW: {new_count}")
print(f"  - Custom: {custom_count}")
print(f"Saved to pipeline_15_consolidated_reviewed.csv")
