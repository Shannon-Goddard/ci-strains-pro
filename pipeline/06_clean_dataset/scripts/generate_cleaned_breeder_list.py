import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"

print("Loading cleaned breeder data...")
df = pd.read_csv(OUTPUT_DIR / "all_breeders_cleaned.csv", encoding='utf-8', low_memory=False)

print("Generating cleaned breeder list...")
breeder_counts = df['breeder_cleaned'].value_counts().sort_index()

# Create markdown
md = f"""# Breeder List - Cleaned & Standardized

**Total Strains**: {len(df):,}  
**Unique Breeders**: {len(breeder_counts)}  
**Date**: January 20, 2026

---

## Breeder Counts (A-Z)

| Breeder | Strain Count |
|---------|--------------|
"""

for breeder, count in breeder_counts.items():
    md += f"| {breeder} | {count} |\n"

md += f"""
---

## Summary Statistics

- **Total Strains**: {len(df):,}
- **Unique Breeders**: {len(breeder_counts)}
- **Average Strains per Breeder**: {len(df) / len(breeder_counts):.1f}
- **Top Breeder**: {breeder_counts.sort_values(ascending=False).index[0]} ({breeder_counts.sort_values(ascending=False).iloc[0]} strains)

---

## Standardization Applied

Based on manual review (MANUAL_BREEDER_REVIEW.md), 61 duplicate breeder names were merged:
- Variations in capitalization (e.g., "Fast Buds" vs "Fast buds")
- Variations with/without "Seeds" suffix (e.g., "DNA Genetics" vs "DNA Genetics Seeds")
- Spacing variations (e.g., "Cali Connection" vs "Caliconnection")
- Abbreviation variations (e.g., "Humboldt Seed Co" vs "Humboldt Seed Company")

**Result**: 580 raw breeders → 519 standardized breeders

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
"""

output_path = OUTPUT_DIR.parent / "BREEDER_LIST_CLEANED.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(md)

print(f"\nCleaned breeder list created: {output_path}")
print(f"Unique breeders: {len(breeder_counts)}")
