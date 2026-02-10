import pandas as pd
import os

input_file = "output/pipeline_11_breeder_extracted.csv"
output_file = "output/column_audit_report.md"

print(f"Reading {input_file}...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)

print(f"Total rows: {len(df):,}")
print(f"Total columns: {len(df.columns)}")

# Group columns by category
identity_cols = [c for c in df.columns if any(x in c.lower() for x in ['strain_id', 'seed_bank', 'breeder', 'strain_name', 'source_url', 's3_html_key'])]
botanical_cols = [c for c in df.columns if any(x in c.lower() for x in ['thc', 'cbd', 'cbn', 'flowering', 'yield', 'height', 'effects', 'flavors', 'terpenes', 'climate', 'difficulty'])]
lineage_cols = [c for c in df.columns if any(x in c.lower() for x in ['parent', 'grandparent', 'lineage', 'generation', 'filial', 'backcross', 'selfed', 'genetics'])]
metadata_cols = [c for c in df.columns if any(x in c.lower() for x in ['scraped_at', 'seed_type', 'autoflower', 'hybrid', 'indica', 'sativa', 'ruderalis', 'dominant'])]
validation_cols = [c for c in df.columns if any(x in c.lower() for x in ['validated', 'validation', 'confidence', 'reasoning', 'flagged', 'attempted', 'changes'])]
extraction_cols = [c for c in df.columns if any(x in c.lower() for x in ['_raw', '_extracted', '_clean', '_normalized', '_slug'])]
manual_cols = [c for c in df.columns if '_manual' in c.lower()]

# Remove duplicates across categories
all_categorized = set(identity_cols + botanical_cols + lineage_cols + metadata_cols + validation_cols + extraction_cols + manual_cols)
other_cols = [c for c in df.columns if c not in all_categorized]

# Build report
report = []
report.append("# Column Audit Report")
report.append(f"\n**Date:** {pd.Timestamp.now().strftime('%B %d, %Y')}")
report.append(f"**Total Strains:** {len(df):,}")
report.append(f"**Total Columns:** {len(df.columns)}")
report.append("\n---\n")

def add_category(name, cols):
    if not cols:
        return
    report.append(f"\n## {name} ({len(cols)} columns)\n")
    for col in sorted(cols):
        non_null = df[col].notna().sum()
        coverage = (non_null / len(df)) * 100
        sample = df[col].dropna().head(3).tolist()
        sample_str = ", ".join([str(s)[:50] for s in sample]) if sample else "No data"
        report.append(f"- **{col}**")
        report.append(f"  - Coverage: {non_null:,} / {len(df):,} ({coverage:.1f}%)")
        report.append(f"  - Sample: {sample_str}")
        report.append("")

add_category("Identity Columns", identity_cols)
add_category("Manual Columns (Verified)", manual_cols)
add_category("Lineage Columns", lineage_cols)
add_category("Botanical Columns", botanical_cols)
add_category("Metadata Columns", metadata_cols)
add_category("Validation Columns (Phase 9)", validation_cols)
add_category("Extraction Columns (Raw/Extracted/Clean)", extraction_cols)
add_category("Other Columns", other_cols)

# Write report
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\nReport saved to: {output_file}")
print(f"\nColumn breakdown:")
print(f"  Identity: {len(identity_cols)}")
print(f"  Manual (Verified): {len(manual_cols)}")
print(f"  Lineage: {len(lineage_cols)}")
print(f"  Botanical: {len(botanical_cols)}")
print(f"  Metadata: {len(metadata_cols)}")
print(f"  Validation: {len(validation_cols)}")
print(f"  Extraction: {len(extraction_cols)}")
print(f"  Other: {len(other_cols)}")
