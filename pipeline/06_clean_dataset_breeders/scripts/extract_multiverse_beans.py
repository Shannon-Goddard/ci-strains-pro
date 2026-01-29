import pandas as pd
import boto3
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading master dataset...")
master = pd.read_csv(BASE_DIR / "input" / "master_strains_raw.csv", encoding='utf-8', low_memory=False)

multiverse = master[master['seed_bank'] == 'multiverse_beans'].copy()
print(f"Multiverse Beans strains: {len(multiverse)}")

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

results = []
for idx, row in multiverse.iterrows():
    s3_key = row['s3_html_key_raw']
    url = row['source_url_raw']
    
    try:
        obj = s3.get_object(Bucket=bucket, Key=s3_key)
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        breeder = None
        
        # Pattern: <a href="https://multiversebeans.com/brand/.../" rel="tag">Breeder</a>
        link = soup.find('a', href=lambda x: x and '/brand/' in x, rel='tag')
        if link:
            breeder = link.get_text(strip=True)
        
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

df = pd.DataFrame(results)
output_path = OUTPUT_DIR / "multiverse_beans_breeders.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

extracted = df['breeder_extracted'].notna().sum()
failed = df['breeder_extracted'].isna().sum()

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(df)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(df)*100:.1f}%)")
print(f"\nOutput: {output_path}")
