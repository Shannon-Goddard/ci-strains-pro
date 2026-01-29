import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"

print("Loading merged breeder data...")
df = pd.read_csv(OUTPUT_DIR / "all_breeders_extracted.csv", encoding='utf-8')

print("Generating breeder list...")
breeder_counts = df['breeder_extracted'].value_counts().sort_index()

# Create markdown
md = f"""# Breeder List - Phase 6 Extraction

**Total Strains**: {len(df):,}  
**Unique Breeders**: {len(breeder_counts)}  
**Date**: January 20, 2026

---

## Breeder Counts

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
- **Top Breeder**: {breeder_counts.index[0]} ({breeder_counts.iloc[0]} strains)

---

**Next Step**: Review for standardization (e.g., "00 Seeds" vs "00Seeds", capitalization, etc.)

**Logic designed by Amazon Q, verified by Shannon Goddard.**
"""

output_path = OUTPUT_DIR.parent / "BREEDER_LIST.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(md)

print(f"\nBreeder list created: {output_path}")
print(f"Unique breeders: {len(breeder_counts)}")
