import pandas as pd

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print(f"Reading {input_file}...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)

print(f"Original: {len(df):,} strains")

# Check for DELETE rows
delete_mask = df['notes_manual'].fillna('').str.contains('DELETE', case=False, na=False)
delete_count = delete_mask.sum()

if delete_count > 0:
    print(f"\nFound {delete_count} rows marked for deletion:")
    print(df[delete_mask][['strain_id', 'strain_name_display_manual', 'notes_manual']].to_string(index=False))
    
    # Remove DELETE rows
    df_clean = df[~delete_mask].copy()
    
    print(f"\nAfter deletion: {len(df_clean):,} strains")
    print(f"Removed: {delete_count} strains")
    
    # Save
    df_clean.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nSaved to: {output_file}")
else:
    print("\nNo rows marked for deletion found.")
