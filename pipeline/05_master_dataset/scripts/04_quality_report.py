import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("../output")
df = pd.read_csv(OUTPUT_DIR / "master_strains_raw.csv", low_memory=False)

print("=" * 80)
print("MASTER DATASET QUALITY REPORT")
print("=" * 80)

print(f"\nTOTAL RECORDS: {len(df):,}")
print(f"TOTAL COLUMNS: {len(df.columns)}")

print("\n" + "=" * 80)
print("STRAINS BY SEED BANK")
print("=" * 80)
for bank in sorted(df['seed_bank'].unique()):
    count = len(df[df['seed_bank'] == bank])
    print(f"{bank:<30} {count:>6,} strains")

print("\n" + "=" * 80)
print("DATA COMPLETENESS BY FIELD")
print("=" * 80)
completeness = []
for col in df.columns:
    if col in ['strain_id', 'seed_bank']:
        continue
    non_null = df[col].notna().sum()
    pct = (non_null / len(df)) * 100
    completeness.append((col, non_null, pct))

completeness.sort(key=lambda x: x[2], reverse=True)

for col, count, pct in completeness:
    print(f"{col:<35} {count:>6,} ({pct:>5.1f}%)")

print("\n" + "=" * 80)
print("KEY METRICS")
print("=" * 80)

# THC coverage
thc_any = df[['thc_content_raw', 'thc_min_raw', 'thc_max_raw']].notna().any(axis=1).sum()
print(f"Strains with THC data:        {thc_any:>6,} ({(thc_any/len(df)*100):>5.1f}%)")

# CBD coverage
cbd_any = df[['cbd_content_raw', 'cbd_min_raw', 'cbd_max_raw']].notna().any(axis=1).sum()
print(f"Strains with CBD data:        {cbd_any:>6,} ({(cbd_any/len(df)*100):>5.1f}%)")

# Genetics coverage
genetics = df['genetics_lineage_raw'].notna().sum()
print(f"Strains with genetics:        {genetics:>6,} ({(genetics/len(df)*100):>5.1f}%)")

# Effects coverage
effects = df['effects_all_raw'].notna().sum()
print(f"Strains with effects:         {effects:>6,} ({(effects/len(df)*100):>5.1f}%)")

# Flowering time coverage
flowering = df['flowering_time_raw'].notna().sum()
print(f"Strains with flowering time:  {flowering:>6,} ({(flowering/len(df)*100):>5.1f}%)")

print("\n" + "=" * 80)
print("SAMPLE RECORDS")
print("=" * 80)
print(f"First 5 strains: {df['strain_name_raw'].head(5).tolist()}")

print("\n" + "=" * 80)
print("REPORT COMPLETE")
print("=" * 80)
