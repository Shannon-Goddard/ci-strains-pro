import pandas as pd

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)

attitude_mask = df['seed_bank_display'] == 'The Attitude Seedbank'
attitude_count = attitude_mask.sum()
print(f"\nAttitude strains: {attitude_count:,}")

# Use strain_name_display for Attitude (it's already clean)
print("Setting Attitude strain_name_raw_2 to strain_name_display...")
df.loc[attitude_mask, 'strain_name_raw_2'] = df.loc[attitude_mask, 'strain_name_display']

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")
print("Attitude strain names fixed!")
