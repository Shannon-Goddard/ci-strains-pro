import pandas as pd
import boto3
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading master dataset...")
master = pd.read_csv(BASE_DIR / "input" / "master_strains_raw.csv", encoding='utf-8', low_memory=False)

seeds_here_now = master[master['seed_bank'] == 'seeds_here_now'].copy()
print(f"Seeds Here Now strains: {len(seeds_here_now)}")

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

results = []
for idx, row in seeds_here_now.iterrows():
    s3_key = row['s3_html_key_raw']
    url = row['source_url_raw']
    
    try:
        obj = s3.get_object(Bucket=bucket, Key=s3_key)
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        breeder = None
        
        # Pattern: <span class="last">Strain Name – Breeder</span>
        last_span = soup.find('span', class_='last')
        if last_span:
            text = last_span.get_text(strip=True)
            if '–' in text:
                breeder = text.split('–')[-1].strip()
            elif ' - ' in text:
                breeder = text.split(' - ')[-1].strip()
        
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
output_path = OUTPUT_DIR / "seeds_here_now_breeders.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

extracted = df['breeder_extracted'].notna().sum()
failed = df['breeder_extracted'].isna().sum()

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(df)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(df)*100:.1f}%)")
print(f"\nOutput: {output_path}")
