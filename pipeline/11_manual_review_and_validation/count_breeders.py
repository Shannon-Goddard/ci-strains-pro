import pandas as pd

df = pd.read_csv('output/pipeline_11_manual_review.csv', encoding='latin-1')

# Count unique breeders
breeder_counts = df['breeder_display_manual'].value_counts()

print("=" * 80)
print("BREEDER VARIETY COUNT")
print("=" * 80)
print(f"\nTotal strains: {len(df):,}")
print(f"Strains with breeder_display_manual: {df['breeder_display_manual'].notna().sum():,}")
print(f"Unique breeders: {df['breeder_display_manual'].nunique()}")
print(f"\nTop 20 Breeders:")
print("-" * 80)
for breeder, count in breeder_counts.head(20).items():
    print(f"{breeder:40} {count:>6,} strains")
print("\n" + "=" * 80)
