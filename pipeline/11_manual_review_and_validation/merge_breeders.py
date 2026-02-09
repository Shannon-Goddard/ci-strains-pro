"""
Merge extracted breeders into manual review CSV

Copies breeder_extracted → breeder_display_manual where confidence >= 0.85
"""

import pandas as pd

# Load files
print("Loading files...")
df_extracted = pd.read_csv('output/pipeline_11_breeder_extracted.csv', encoding='utf-8')
df_manual = pd.read_csv('output/pipeline_11_manual_review.csv', encoding='latin-1')

print(f"Extracted: {len(df_extracted):,} rows")
print(f"Manual: {len(df_manual):,} rows")

# Merge on strain_id
df_merged = df_manual.merge(
    df_extracted[['strain_id', 'breeder_extracted', 'breeder_confidence', 'breeder_reasoning']], 
    on='strain_id', 
    how='left'
)

# Copy high-confidence extractions to breeder_display_manual
high_confidence = (df_merged['breeder_confidence'] >= 0.85) & (df_merged['breeder_extracted'] != 'Unknown')
df_merged.loc[high_confidence, 'breeder_display_manual'] = df_merged.loc[high_confidence, 'breeder_extracted']

# Stats
total_updated = high_confidence.sum()
print(f"\n✅ Updated {total_updated:,} breeders (confidence >= 0.85)")

# Save
df_merged.to_csv('output/pipeline_11_manual_review_updated.csv', index=False, encoding='utf-8')
print(f"✅ Saved to: output/pipeline_11_manual_review_updated.csv")

# Show new breeder counts
print("\n" + "=" * 80)
print("UPDATED BREEDER COUNTS")
print("=" * 80)
breeder_counts = df_merged['breeder_display_manual'].value_counts()
print(f"\nTotal strains: {len(df_merged):,}")
print(f"Unique breeders: {df_merged['breeder_display_manual'].nunique()}")
print(f"Still Unknown: {(df_merged['breeder_display_manual'] == 'Unknown').sum():,}")

print(f"\nTop 20 Breeders:")
print("-" * 80)
for breeder, count in breeder_counts.head(20).items():
    print(f"{breeder:40} {count:>6,} strains")
