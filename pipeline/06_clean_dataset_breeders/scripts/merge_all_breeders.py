import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"

# List all breeder CSV files
csv_files = [
    'attitude_breeders.csv',
    'gorilla_breeders.csv',
    'north_atlantic_breeders.csv',
    'neptune_breeders.csv',
    'herbies_breeders.csv',
    'multiverse_beans_breeders.csv',
    'seed_supreme_breeders.csv',
    'seeds_here_now_breeders.csv',
    'great_lakes_breeders.csv',
    'ilgm_breeders.csv',
    'seedsman_js_breeders.csv',
    'self_branded_breeders.csv'
]

print("Merging breeder extraction results...")
all_data = []

for csv_file in csv_files:
    df = pd.read_csv(OUTPUT_DIR / csv_file, encoding='utf-8')
    all_data.append(df)
    print(f"  {csv_file}: {len(df)} strains")

merged = pd.concat(all_data, ignore_index=True)
output_path = OUTPUT_DIR / "all_breeders_extracted.csv"
merged.to_csv(output_path, index=False, encoding='utf-8')

print(f"\nTotal: {len(merged)} strains")
print(f"Output: {output_path}")
