import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading master dataset...")
master = pd.read_csv(BASE_DIR / "input" / "master_strains_raw.csv", encoding='utf-8', low_memory=False)

# Self-branded seed banks (bank = breeder)
self_branded = {
    'crop_king': 'Crop King Seeds',
    'sensi_seeds': 'Sensi Seeds',
    'mephisto_genetics': 'Mephisto Genetics',
    'exotic': 'Exotic Genetix',
    'amsterdam': 'Amsterdam Marijuana Seeds',
    'dutch_passion': 'Dutch Passion',
    'barneys_farm': "Barney's Farm",
    'royal_queen_seeds': 'Royal Queen Seeds'
}

results = []
for bank_code, breeder_name in self_branded.items():
    bank_strains = master[master['seed_bank'] == bank_code].copy()
    print(f"{bank_code}: {len(bank_strains)} strains")
    
    for idx, row in bank_strains.iterrows():
        results.append({
            'strain_name_raw': row['strain_name_raw'],
            'source_url_raw': row['source_url_raw'],
            's3_html_key_raw': row['s3_html_key_raw'],
            'breeder_extracted': breeder_name
        })

df = pd.DataFrame(results)
output_path = OUTPUT_DIR / "self_branded_breeders.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"\nTotal: {len(df)} strains")
print(f"Output: {output_path}")
