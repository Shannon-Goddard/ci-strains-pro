import pandas as pd

df = pd.read_csv('output/all_strains_genetics_standardized.csv', encoding='latin-1', low_memory=False)

print("Missing Lineage Analysis by Seed Bank\n")
print("="*70)

missing = df[df['parent_1_display'].isna()].groupby('seed_bank').size().sort_values(ascending=False)
total = df.groupby('seed_bank').size()

for bank in missing.index:
    m = missing[bank]
    t = total[bank]
    pct = (m/t)*100
    print(f"{bank:25} | Total: {t:5} | Missing: {m:5} ({pct:5.1f}%)")

print("="*70)
print(f"TOTAL: {len(df)} strains | Missing lineage: {df['parent_1_display'].isna().sum()} ({df['parent_1_display'].isna().sum()/len(df)*100:.1f}%)")
