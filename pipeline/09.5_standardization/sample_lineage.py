import pandas as pd

df = pd.read_csv('output/all_strains_standardized_clean.csv', encoding='latin-1', low_memory=False)

# Find descriptions with parent crosses
desc_with_x = df[df['description_raw'].str.contains(' x ', case=False, na=False)].head(20)

print("Sample lineage patterns:\n")
for idx, row in desc_with_x.iterrows():
    strain = row['strain_name_display']
    desc = str(row['description_raw'])[:200]
    print(f"{strain}:")
    print(f"  {desc}\n")
