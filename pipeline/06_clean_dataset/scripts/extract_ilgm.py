import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

s3 = boto3.client('s3')
BUCKET = 'ci-strains-html-archive'

print("Loading S3 JS inventory...")
inv = pd.read_csv(BASE_DIR.parent / '03_s3_inventory' / 's3_js_html_inventory.csv')
url_to_key = dict(zip(inv['url'], inv['html_key']))

print("Loading master dataset...")
master = pd.read_csv(BASE_DIR / 'input' / 'master_strains_raw.csv', encoding='utf-8', low_memory=False)
ilgm = master[master['seed_bank'] == 'ilgm_js'].copy()
print(f"ILGM JS strains: {len(ilgm)}")

results = []
for idx, row in ilgm.iterrows():
    url = row['source_url_raw']
    s3_key = url_to_key.get(url)
    
    breeder = None
    if s3_key:
        try:
            response = s3.get_object(Bucket=BUCKET, Key=s3_key)
            html = response['Body'].read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Pattern: <span class="group font-display text-display-xs font-black"><!--[-->Breeder<!--]--></span>
            span = soup.find('span', class_=re.compile('font-display.*font-black', re.I))
            if span:
                text = span.get_text(strip=True)
                text = re.sub(r'<!--.*?-->', '', text)
                if text:
                    breeder = text
        except:
            pass
    
    results.append({
        'strain_name_raw': row['strain_name_raw'],
        'source_url_raw': url,
        's3_html_key_raw': s3_key if s3_key else None,
        'breeder_extracted': breeder
    })

df = pd.DataFrame(results)
output_path = OUTPUT_DIR / 'ilgm_breeders.csv'
df.to_csv(output_path, index=False, encoding='utf-8')

extracted = df['breeder_extracted'].notna().sum()
failed = df['breeder_extracted'].isna().sum()

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(df)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(df)*100:.1f}%)")
print(f"\nOutput: {output_path}")
