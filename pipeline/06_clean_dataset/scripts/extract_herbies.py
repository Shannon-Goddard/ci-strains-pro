import pandas as pd
import boto3
from bs4 import BeautifulSoup
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load datasets
print("Loading master dataset...")
master = pd.read_csv(BASE_DIR / "input" / "master_strains_raw.csv", encoding='utf-8')

# Filter Herbies strains
herbies = master[master['seed_bank'] == 'herbies'].copy()
print(f"Herbies strains: {len(herbies)}")

# Initialize S3
s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

results = []
for idx, row in herbies.iterrows():
    s3_key = row['s3_html_key_raw']
    url = row['source_url_raw']
    
    try:
        obj = s3.get_object(Bucket=bucket, Key=s3_key)
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        breeder = None
        
        # Pattern 1: <a href="https://herbiesheadshop.com/producers/...">
        link = soup.find('a', href=lambda x: x and '/producers/' in x)
        if link:
            breeder = link.get_text(strip=True)
        
        # Pattern 2: Strain brand in properties table
        if not breeder:
            for tr in soup.find_all('tr', class_='properties-list__item'):
                text = tr.get_text(' | ', strip=True)
                if 'Strain brand' in text:
                    parts = text.split('|')
                    if len(parts) >= 2:
                        breeder = parts[1].strip()
                    break
        
        results.append({
            'strain_name_raw': row['strain_name_raw'],
            'source_url_raw': url,
            's3_html_key_raw': s3_key,
            'breeder_extracted': breeder
        })
        
    except Exception as e:
        results.append({
            'strain_name_raw': row['strain_name_raw'],
            'source_url_raw': url,
            's3_html_key_raw': s3_key,
            'breeder_extracted': None
        })

# Save results
df = pd.DataFrame(results)
output_path = OUTPUT_DIR / "herbies_breeders.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

# Stats
extracted = df['breeder_extracted'].notna().sum()
failed = df['breeder_extracted'].isna().sum()

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(df)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(df)*100:.1f}%)")
print(f"\nOutput: {output_path}")
