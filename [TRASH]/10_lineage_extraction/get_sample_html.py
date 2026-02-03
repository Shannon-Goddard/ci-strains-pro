import pandas as pd
import boto3
import sys

if len(sys.argv) < 2:
    print("Usage: python get_sample_html.py <seed_bank_name>")
    print("\nAvailable seed banks:")
    print("  attitude, crop_king, north_atlantic, gorilla, seedsman_js,")
    print("  herbies, neptune, multiverse_beans, seed_supreme, exotic,")
    print("  mephisto_genetics, amsterdam, ilgm, sensi_seeds, barneys_farm,")
    print("  royal_queen_seeds, dutch_passion, seeds_here_now, great_lakes_genetics")
    sys.exit(1)

seed_bank = sys.argv[1]

df = pd.read_csv('output/all_strains_genetics_standardized.csv', encoding='latin-1', low_memory=False)
bank_strains = df[df['seed_bank'] == seed_bank]
missing = bank_strains[bank_strains['parent_1_display'].isna()]

if len(missing) == 0:
    print(f"No strains missing lineage for {seed_bank}")
    sys.exit(0)

row = missing.iloc[0]

s3 = boto3.client('s3')
response = s3.get_object(Bucket='ci-strains-html-archive', Key=row['s3_html_key_raw'])
html = response['Body'].read().decode('utf-8', errors='ignore')

print(f"Seed Bank: {seed_bank}")
print(f"Strain: {row['strain_name_display']}")
print(f"Breeder: {row['breeder_display']}")
print(f"S3 Key: {row['s3_html_key_raw']}")
print(f"\nHTML Length: {len(html)} chars")
print("\n" + "="*70)
print("FULL HTML:")
print("="*70)
print(html)
