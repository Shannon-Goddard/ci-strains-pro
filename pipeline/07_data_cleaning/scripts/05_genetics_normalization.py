import pandas as pd
import numpy as np
import re
from pathlib import Path

# Paths
input_file = Path('../output/04_data_types_standardized.csv')
output_file = Path('../output/05_genetics_normalized.csv')
report_file = Path('../output/05_genetics_normalization_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

stats = {
    'ruderalis_calculated': 0,
    'filial_extracted': 0,
    'breeding_status_identified': 0
}

# Calculate ruderalis percentage
def calculate_ruderalis(row):
    indica = row.get('indica_percentage_raw')
    sativa = row.get('sativa_percentage_raw')
    
    if pd.notna(indica) and pd.notna(sativa):
        total = indica + sativa
        if total < 100:
            stats['ruderalis_calculated'] += 1
            return 100 - total
    return None

df['ruderalis_percentage_clean'] = df.apply(calculate_ruderalis, axis=1)

# Extract filial generation (F1, F2, S1, IBL, etc.)
def extract_filial(val):
    if pd.isna(val): return None
    val = str(val).upper()
    
    patterns = [
        r'\b(F[1-9]\d*)\b',  # F1, F2, F3, etc.
        r'\b(S[1-9]\d*)\b',  # S1, S2, etc.
        r'\b(BX[1-9]\d*)\b', # BX1, BX2, etc.
        r'\b(P[1-9]\d*)\b',  # P1, P2, etc.
        r'\b(IBL)\b',        # IBL
        r'\b(F1\s*FAST)\b'   # F1 Fast
    ]
    
    for pattern in patterns:
        match = re.search(pattern, val)
        if match:
            stats['filial_extracted'] += 1
            return match.group(1)
    return None

if 'generation_raw' in df.columns:
    df['filial_type_clean'] = df['generation_raw'].apply(extract_filial)
else:
    df['filial_type_clean'] = None

# Identify breeding status
def identify_breeding_status(row):
    lineage = str(row.get('genetics_lineage_raw', '')).lower()
    name = str(row.get('strain_name_raw', '')).lower()
    
    if 'landrace' in lineage or 'landrace' in name:
        stats['breeding_status_identified'] += 1
        return 'Landrace'
    elif 'heirloom' in lineage or 'heirloom' in name:
        stats['breeding_status_identified'] += 1
        return 'Heirloom'
    elif 'ibl' in lineage or 'ibl' in name:
        stats['breeding_status_identified'] += 1
        return 'IBL'
    elif 'polyhybrid' in lineage or 'polyhybrid' in name:
        stats['breeding_status_identified'] += 1
        return 'Polyhybrid'
    elif pd.notna(row.get('genetics_lineage_raw')) and 'x' in lineage:
        stats['breeding_status_identified'] += 1
        return 'Hybrid'
    return None

df['breeding_status_clean'] = df.apply(identify_breeding_status, axis=1)

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 05: Genetics Normalization Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n\n")
    f.write("Genetics calculations:\n")
    f.write(f"  Ruderalis percentage calculated: {stats['ruderalis_calculated']}\n")
    f.write(f"  Filial generation extracted: {stats['filial_extracted']}\n")
    f.write(f"  Breeding status identified: {stats['breeding_status_identified']}\n")
    f.write(f"\nTotal genetics enhancements: {sum(stats.values())}\n")

print(f"\n[SUCCESS] Step 05 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Genetics enhancements: {sum(stats.values())}")
