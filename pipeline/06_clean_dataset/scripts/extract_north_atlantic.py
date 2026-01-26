"""
North Atlantic - Breeder Extraction
Extracts breeder from breeder-link span.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd
import boto3
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
BUCKET = 'ci-strains-html-archive'

# Load inventory
print("Loading S3 inventory...")
inv = pd.read_csv('../../03_s3_inventory/s3_html_inventory.csv')
url_to_key = dict(zip(inv['url'], inv['s3_html_key']))

# Load dataset
print("Loading master dataset...")
df = pd.read_csv('../input/master_strains_raw.csv', encoding='latin-1', low_memory=False)
north_atlantic = df[df['seed_bank'] == 'north_atlantic'].copy()
print(f"North Atlantic strains: {len(north_atlantic)}")

# Extract breeders
extracted = 0
failed = 0

print("\nExtracting breeders...")
for idx in north_atlantic.index:
    url = north_atlantic.at[idx, 'source_url_raw']
    s3_key = url_to_key.get(url)
    
    if not s3_key:
        failed += 1
        continue
    
    try:
        response = s3.get_object(Bucket=BUCKET, Key=s3_key)
        html = response['Body'].read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find breeder link
        breeder_span = soup.find('span', class_='breeder-link')
        if breeder_span:
            link = breeder_span.find('a')
            if link:
                north_atlantic.at[idx, 'breeder_extracted'] = link.get_text(strip=True)
                extracted += 1
            else:
                failed += 1
        else:
            # Edge case: check description-content for breeder
            desc = soup.find('div', class_='description-content')
            if desc:
                strong = desc.find('strong')
                if strong:
                    text = strong.get_text(strip=True)
                    if ' >' in text:
                        breeder = text.split(' >')[0].strip()
                        north_atlantic.at[idx, 'breeder_extracted'] = breeder
                        extracted += 1
                    else:
                        failed += 1
                else:
                    failed += 1
            else:
                failed += 1
    except:
        failed += 1
    
    if (extracted + failed) % 500 == 0:
        print(f"Processed: {extracted + failed}, Extracted: {extracted}, Failed: {failed}")

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(north_atlantic)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(north_atlantic)*100:.1f}%)")

# Save
north_atlantic.to_csv('../output/north_atlantic_breeders.csv', index=False, encoding='utf-8')
north_atlantic.head(100).to_csv('../output/north_atlantic_breeders_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: output/north_atlantic_breeders.csv")
