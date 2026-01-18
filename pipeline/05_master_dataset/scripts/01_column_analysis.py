import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

# Paths
CSV_DIR = Path("../csv")
OUTPUT_DIR = Path("../output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Scan all CSVs
csv_files = sorted(CSV_DIR.glob("*.csv"))
print(f"Found {len(csv_files)} CSV files\n")

# Collect column data
column_data = []
all_columns = defaultdict(list)

for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file, encoding='latin-1', nrows=0)
        columns = list(df.columns)
        
        seed_bank = csv_file.stem.replace('_extracted', '').replace('_maximum_extraction', '').replace('_js_extracted', '')
        
        column_data.append({
            'seed_bank': seed_bank,
            'file': csv_file.name,
            'column_count': len(columns),
            'columns': columns
        })
        
        for col in columns:
            all_columns[col].append(seed_bank)
        
        print(f"[OK] {seed_bank}: {len(columns)} columns")
    except Exception as e:
        print(f"[ERROR] {csv_file.name}: {e}")

# Save detailed analysis
with open(OUTPUT_DIR / "column_analysis.json", 'w') as f:
    json.dump(column_data, f, indent=2)

# Create column frequency report
column_freq = {col: len(banks) for col, banks in all_columns.items()}
sorted_cols = sorted(column_freq.items(), key=lambda x: x[1], reverse=True)

with open(OUTPUT_DIR / "column_frequency.txt", 'w') as f:
    f.write("COLUMN FREQUENCY ACROSS SEED BANKS\n")
    f.write("=" * 80 + "\n\n")
    for col, count in sorted_cols:
        f.write(f"{col:<50} {count:>2} seed banks\n")

# Summary stats
print(f"\nSUMMARY")
print(f"Total unique columns: {len(all_columns)}")
print(f"Universal columns (in all files): {sum(1 for c in column_freq.values() if c == len(csv_files))}")
print(f"Common columns (in 10+ files): {sum(1 for c in column_freq.values() if c >= 10)}")
print(f"\nAnalysis saved to output/")
