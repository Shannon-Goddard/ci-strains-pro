import pandas as pd

# Load datasets
print("Loading datasets...")
main_df = pd.read_csv('output/all_strains_validated.csv', encoding='latin-1', low_memory=False)
manual_df = pd.read_csv('output/all_strains_validated_flagged_manual_review.csv', encoding='latin-1')

print(f"Main dataset: {len(main_df)} rows")
print(f"Manual review: {len(manual_df)} rows")

# Extract manual columns
manual_cols = ['strain_id', 'strain_name_aka_manual', 'strain_name_manual', 'breeder_manual', 'manual_notes']
manual_updates = manual_df[manual_cols].copy()

# Merge manual updates into main dataset
main_df = main_df.merge(manual_updates, on='strain_id', how='left', suffixes=('', '_new'))

# Update columns where manual review exists
for col in ['strain_name_aka_manual', 'strain_name_manual', 'breeder_manual', 'manual_notes']:
    if f'{col}_new' in main_df.columns:
        main_df[col] = main_df[f'{col}_new'].combine_first(main_df.get(col, pd.Series()))
        main_df.drop(columns=[f'{col}_new'], inplace=True)
    elif col not in main_df.columns:
        main_df[col] = manual_updates.set_index('strain_id')[col]

# Save merged dataset
output_path = 'output/all_strains_validated_merged.csv'
main_df.to_csv(output_path, index=False, encoding='latin-1')
print(f"\nMerged dataset saved: {output_path}")
print(f"Total rows: {len(main_df)}")
print(f"Manual reviews merged: {main_df['strain_name_manual'].notna().sum()}")
