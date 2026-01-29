"""
Phase 8: Quality Report for Strain Name Extraction
Identifies issues: breeder names, seed type keywords, common patterns

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
from pathlib import Path
from collections import Counter

# Paths
INPUT_CSV = Path("../output/02_strain_names_improved.csv")
BREEDER_LIST = Path("../../06_clean_dataset_breeders/BREEDER_LIST_CLEANED.md")
OUTPUT_REPORT = Path("../docs/EXTRACTION_QUALITY_REPORT.md")

# Load data
print("Loading data...")
df = pd.read_csv(INPUT_CSV, low_memory=False)

# Load breeder names
breeder_names = set()
with open(BREEDER_LIST, 'r', encoding='utf-8') as f:
    in_table = False
    for line in f:
        line = line.strip()
        if line.startswith('| Breeder |'):
            in_table = True
            continue
        if line.startswith('|---'):
            continue
        if in_table and not line.startswith('|'):
            break
        if in_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                breeder = parts[1].strip()
                if breeder and breeder != 'Breeder':
                    breeder_names.add(breeder.lower())

# Seed type keywords
SEED_KEYWORDS = ['feminized', 'feminised', 'fem', 'auto', 'autoflower', 'autoflowering', 
                 'regular', 'photoperiod', 'photo', 'fast', 'seeds', 'seed']

# Analysis
print("Analyzing extraction quality...")

# 1. Check for breeder names still in extracted names
breeder_contamination = []
for idx, row in df.iterrows():
    name = str(row['strain_name_extracted']).lower()
    for breeder in breeder_names:
        if breeder in name:
            breeder_contamination.append({
                'seed_bank': row['seed_bank'],
                'strain_name_extracted': row['strain_name_extracted'],
                'breeder_found': breeder
            })
            break

# 2. Check for seed type keywords
seed_keyword_issues = []
for idx, row in df.iterrows():
    name = str(row['strain_name_extracted']).lower()
    for keyword in SEED_KEYWORDS:
        if keyword in name.split():  # Whole word match
            seed_keyword_issues.append({
                'seed_bank': row['seed_bank'],
                'strain_name_extracted': row['strain_name_extracted'],
                'keyword_found': keyword
            })
            break

# 3. Top 50 most common strain names
strain_counts = Counter(df['strain_name_extracted'].dropna())
top_strains = strain_counts.most_common(50)

# 4. Extraction stats by seed bank
bank_stats = df.groupby('seed_bank').agg({
    'strain_name_extracted': 'count',
    'generation_extracted': lambda x: x.notna().sum(),
    'phenotype_marker_extracted': lambda x: x.notna().sum()
}).reset_index()
bank_stats.columns = ['seed_bank', 'total_strains', 'with_generation', 'with_phenotype']

# Generate report
print("Generating report...")
report = []
report.append("# Strain Name Extraction - Quality Report\n")
report.append(f"**Date**: January 25, 2026  ")
report.append(f"**Total Strains**: {len(df):,}  ")
report.append(f"**Extracted**: {df['strain_name_extracted'].notna().sum():,}  ")
report.append(f"**Success Rate**: {(df['strain_name_extracted'].notna().sum() / len(df) * 100):.2f}%\n")
report.append("---\n\n")

# Issue 1: Breeder contamination
report.append(f"## Issue 1: Breeder Names Still in Extracted Names\n\n")
report.append(f"**Count**: {len(breeder_contamination)} strains\n\n")
if breeder_contamination:
    report.append("| Seed Bank | Strain Name Extracted | Breeder Found |\n")
    report.append("|-----------|----------------------|---------------|\n")
    for item in breeder_contamination[:50]:  # Top 50
        report.append(f"| {item['seed_bank']} | {item['strain_name_extracted']} | {item['breeder_found']} |\n")
    if len(breeder_contamination) > 50:
        report.append(f"\n*Showing 50 of {len(breeder_contamination)} issues*\n")
report.append("\n---\n\n")

# Issue 2: Seed type keywords
report.append(f"## Issue 2: Seed Type Keywords Still in Names\n\n")
report.append(f"**Count**: {len(seed_keyword_issues)} strains\n\n")
if seed_keyword_issues:
    report.append("| Seed Bank | Strain Name Extracted | Keyword Found |\n")
    report.append("|-----------|----------------------|---------------|\n")
    for item in seed_keyword_issues[:50]:  # Top 50
        report.append(f"| {item['seed_bank']} | {item['strain_name_extracted']} | {item['keyword_found']} |\n")
    if len(seed_keyword_issues) > 50:
        report.append(f"\n*Showing 50 of {len(seed_keyword_issues)} issues*\n")
report.append("\n---\n\n")

# Top 50 strains
report.append(f"## Top 50 Most Common Strain Names\n\n")
report.append("| Rank | Strain Name | Count |\n")
report.append("|------|-------------|-------|\n")
for i, (strain, count) in enumerate(top_strains, 1):
    report.append(f"| {i} | {strain} | {count} |\n")
report.append("\n---\n\n")

# Stats by seed bank
report.append(f"## Extraction Stats by Seed Bank\n\n")
report.append("| Seed Bank | Total Strains | With Generation | With Phenotype |\n")
report.append("|-----------|---------------|-----------------|----------------|\n")
for _, row in bank_stats.iterrows():
    report.append(f"| {row['seed_bank']} | {row['total_strains']:,} | {row['with_generation']} | {row['with_phenotype']} |\n")
report.append("\n---\n\n")

report.append("**Logic designed by Amazon Q, verified by Shannon Goddard.**\n")

# Save report
OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
    f.writelines(report)

print(f"\nReport saved to: {OUTPUT_REPORT}")
print(f"\nSummary:")
print(f"  - Breeder contamination: {len(breeder_contamination)} strains")
print(f"  - Seed keyword issues: {len(seed_keyword_issues)} strains")
print(f"  - Top strain: {top_strains[0][0]} ({top_strains[0][1]} occurrences)")
