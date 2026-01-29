import pandas as pd
import boto3
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading master dataset...")
master = pd.read_csv(BASE_DIR / "input" / "master_strains_raw.csv", encoding='utf-8', low_memory=False)

great_lakes = master[master['seed_bank'] == 'great_lakes_genetics'].copy()
print(f"Great Lakes strains: {len(great_lakes)}")

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

results = []
for idx, row in great_lakes.iterrows():
    s3_key = row['s3_html_key_raw']
    url = row['source_url_raw']
    
    try:
        obj = s3.get_object(Bucket=bucket, Key=s3_key)
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        breeder = None
        
        # Pattern 1: <h3>Breeder - Strain Name</h3>
        h3 = soup.find('h3')
        if h3:
            text = h3.get_text(strip=True)
            if ' - ' in text:
                breeder = text.split(' - ')[0].strip()
            elif '-' in text:
                breeder = text.split('-')[0].strip()
        
        # Pattern 2: Title fallback
        if not breeder:
            title = soup.find('title')
            if title:
                text = title.get_text(strip=True)
                if ' - ' in text:
                    breeder = text.split(' - ')[0].strip()
        
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
output_path = OUTPUT_DIR / "great_lakes_breeders.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

extracted = df['breeder_extracted'].notna().sum()
failed = df['breeder_extracted'].isna().sum()

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(df)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(df)*100:.1f}%)")
print(f"\nOutput: {output_path}")
