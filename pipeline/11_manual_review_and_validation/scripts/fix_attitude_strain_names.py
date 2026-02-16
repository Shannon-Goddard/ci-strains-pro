import pandas as pd

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)

# Check Attitude issue
attitude_mask = df['seed_bank_display'] == 'The Attitude Seedbank'
attitude_count = attitude_mask.sum()
print(f"\nAttitude strains: {attitude_count:,}")

# Check how many have the issue
issue_mask = attitude_mask & df['strain_name_raw_2'].str.contains('world largest cannabis', case=False, na=False)
issue_count = issue_mask.sum()
print(f"With 'world largest cannabis' issue: {issue_count:,}")

# Swap: Use strain_name_raw for Attitude strains
print("\nSwapping Attitude strain_name_raw_2 with strain_name_raw...")
df.loc[attitude_mask, 'strain_name_raw_2'] = df.loc[attitude_mask, 'strain_name_raw']

# Verify fix
issue_after = df[attitude_mask]['strain_name_raw_2'].str.contains('world largest cannabis', case=False, na=False).sum()
print(f"After swap: {issue_after} strains still have issue")

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")

# Show sample
print("\nSample Attitude strains:")
print(df[attitude_mask][['strain_name_raw', 'strain_name_raw_2', 'strain_name_display']].head(10).to_string(index=False))
