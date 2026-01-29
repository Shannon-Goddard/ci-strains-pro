import pandas as pd
import boto3
from bs4 import BeautifulSoup
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
seedsman = master[master['seed_bank'] == 'seedsman_js'].copy()
print(f"Seedsman JS strains: {len(seedsman)}")

results = []
for idx, row in seedsman.iterrows():
    url = row['source_url_raw']
    s3_key = url_to_key.get(url)
    
    breeder = None
    if s3_key:
        try:
            response = s3.get_object(Bucket=BUCKET, Key=s3_key)
            html = response['Body'].read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Pattern: <div class="Brand"><a>Breeder</a></div> OR <h4 class="Product-BrandName">Breeder</h4>
            brand_div = soup.find('div', class_='Brand')
            if brand_div:
                link = brand_div.find('a')
                if link:
                    breeder = link.get_text(strip=True)
                else:
                    h4 = brand_div.find('h4', class_='Product-BrandName')
                    if h4:
                        breeder = h4.get_text(strip=True)
        except:
            pass
    
    # Fallback: If no Brand div found, assume Seedsman self-branded
    if not breeder:
        breeder = 'Seedsman'
    
    results.append({
        'strain_name_raw': row['strain_name_raw'],
        'source_url_raw': url,
        's3_html_key_raw': s3_key if s3_key else None,
        'breeder_extracted': breeder
    })

df = pd.DataFrame(results)
output_path = OUTPUT_DIR / 'seedsman_js_breeders.csv'
df.to_csv(output_path, index=False, encoding='utf-8')

extracted = df['breeder_extracted'].notna().sum()
failed = df['breeder_extracted'].isna().sum()

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(df)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(df)*100:.1f}%)")
print(f"\nOutput: {output_path}")
