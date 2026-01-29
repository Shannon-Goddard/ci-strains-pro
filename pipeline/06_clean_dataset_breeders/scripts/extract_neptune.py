"""
Neptune - Breeder Extraction
Extracts breeder from breeder-link in product-breeder div.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd
import boto3
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
BUCKET = 'ci-strains-html-archive'

print("Loading S3 inventory...")
inv = pd.read_csv('../../03_s3_inventory/s3_html_inventory.csv')
url_to_key = dict(zip(inv['url'], inv['s3_html_key']))

print("Loading master dataset...")
df = pd.read_csv('../input/master_strains_raw.csv', encoding='latin-1', low_memory=False)
neptune = df[df['seed_bank'] == 'neptune'].copy()
print(f"Neptune strains: {len(neptune)}")

extracted = 0
failed = 0

print("\nExtracting breeders...")
for idx in neptune.index:
    url = neptune.at[idx, 'source_url_raw']
    s3_key = url_to_key.get(url)
    
    if not s3_key:
        failed += 1
        continue
    
    try:
        response = s3.get_object(Bucket=BUCKET, Key=s3_key)
        html = response['Body'].read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find breeder link
        link = soup.find('a', class_='breeder-link')
        if link:
            neptune.at[idx, 'breeder_extracted'] = link.get_text(strip=True)
            extracted += 1
        else:
            # Fallback: extract from h1 title (e.g., "Sin City Seeds – Coconut Cloud (F)")
            h1 = soup.find('h1', class_='product_title')
            if h1:
                title = h1.get_text(strip=True)
                # Split on em dash or hyphen with spaces
                if ' – ' in title:
                    breeder = title.split(' – ')[0].strip()
                    neptune.at[idx, 'breeder_extracted'] = breeder
                    extracted += 1
                elif ' - ' in title:
                    breeder = title.split(' - ')[0].strip()
                    neptune.at[idx, 'breeder_extracted'] = breeder
                    extracted += 1
                else:
                    failed += 1
            else:
                failed += 1
    except:
        failed += 1
    
    if (extracted + failed) % 500 == 0:
        print(f"Processed: {extracted + failed}, Extracted: {extracted}, Failed: {failed}")

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(neptune)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(neptune)*100:.1f}%)")

neptune.to_csv('../output/neptune_breeders.csv', index=False, encoding='utf-8')
neptune.head(100).to_csv('../output/neptune_breeders_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: output/neptune_breeders.csv")
