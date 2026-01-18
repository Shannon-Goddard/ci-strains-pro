import pandas as pd
import json
from pathlib import Path
from schema import CORE_SCHEMA, EXCLUDED_COLUMNS, COLUMN_MAPPINGS

CSV_DIR = Path("../csv")
OUTPUT_DIR = Path("../output")

# Load column analysis
with open(OUTPUT_DIR / "column_analysis.json") as f:
    analysis = json.load(f)

# Analyze all columns and create mapping
mapping_report = []
excluded_report = []
unmapped_report = []

for file_data in analysis:
    seed_bank = file_data['seed_bank']
    columns = file_data['columns']
    
    for col in columns:
        col_lower = col.lower()
        
        # Check if excluded (commercial data)
        if any(excl in col_lower for excl in EXCLUDED_COLUMNS):
            excluded_report.append({
                'seed_bank': seed_bank,
                'original_column': col,
                'reason': 'Commercial data'
            })
            continue
        
        # Check if it maps to core schema
        mapped_to = None
        for unified, keywords in COLUMN_MAPPINGS.items():
            if any(kw in col_lower for kw in keywords):
                mapped_to = unified
                break
        
        if mapped_to:
            mapping_report.append({
                'seed_bank': seed_bank,
                'original_column': col,
                'maps_to': mapped_to
            })
        else:
            unmapped_report.append({
                'seed_bank': seed_bank,
                'original_column': col
            })

# Save mapping report
with open(OUTPUT_DIR / "column_mapping.json", 'w') as f:
    json.dump(mapping_report, f, indent=2)

with open(OUTPUT_DIR / "excluded_columns.json", 'w') as f:
    json.dump(excluded_report, f, indent=2)

with open(OUTPUT_DIR / "unmapped_columns.json", 'w') as f:
    json.dump(unmapped_report, f, indent=2)

# Summary
unique_mapped = set(x['maps_to'] for x in mapping_report)
print(f"Mapped columns: {len(mapping_report)} instances")
print(f"Unique fields: {len(unique_mapped)}")
print(f"Excluded: {len(excluded_report)}")
print(f"Unmapped: {len(unmapped_report)}")
print(f"\nUnique mapped fields:")
for field in sorted(unique_mapped):
    print(f"  - {field}")
