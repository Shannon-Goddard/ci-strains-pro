import pandas as pd
import numpy as np
from pathlib import Path

# Paths
input_file = Path('../output/02_unit_normalized.csv')
output_file = Path('../output/03_placeholders_removed.csv')
report_file = Path('../output/03_placeholder_removal_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

# Placeholder patterns
placeholders = [
    'n/a', 'na', 'not available', 'not specified', 'unknown', 
    'tbd', 'tba', 'coming soon', 'contact us', 'varies',
    'see description', 'variable', 'depends', 'multiple',
    '-', '--', '---', 'none', 'null', 'nil'
]

replacements = 0
affected_columns = {}

# Replace placeholders with NULL
for col in df.columns:
    if col.endswith('_raw') or col.endswith('_clean'):
        before = df[col].notna().sum()
        
        # Convert to string for comparison
        df[col] = df[col].apply(lambda x: None if pd.notna(x) and str(x).strip().lower() in placeholders else x)
        
        after = df[col].notna().sum()
        removed = before - after
        
        if removed > 0:
            replacements += removed
            affected_columns[col] = removed

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 03: Placeholder Removal Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n")
    f.write(f"Total placeholders removed: {replacements}\n")
    f.write(f"Affected columns: {len(affected_columns)}\n\n")
    f.write("Placeholders removed by column:\n")
    for col, count in sorted(affected_columns.items(), key=lambda x: x[1], reverse=True)[:20]:
        f.write(f"  {col}: {count}\n")
    if len(affected_columns) > 20:
        f.write(f"  ... and {len(affected_columns) - 20} more columns\n")

print(f"\n[SUCCESS] Step 03 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Placeholders removed: {replacements}")
