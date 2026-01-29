"""
Gorilla Seed Bank - Breeder Extraction
Extracts breeder from product-manufacturer h3.
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
gorilla = df[df['seed_bank'] == 'gorilla'].copy()
print(f"Gorilla strains: {len(gorilla)}")

extracted = 0
failed = 0

print("\nExtracting breeders...")
for idx in gorilla.index:
    url = gorilla.at[idx, 'source_url_raw']
    s3_key = url_to_key.get(url)
    
    if not s3_key:
        failed += 1
        continue
    
    try:
        response = s3.get_object(Bucket=BUCKET, Key=s3_key)
        html = response['Body'].read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find product-manufacturer h3
        h3 = soup.find('h3', class_='product-manufacturer')
        if h3:
            link = h3.find('a')
            if link:
                gorilla.at[idx, 'breeder_extracted'] = link.get_text(strip=True)
                extracted += 1
                continue
        
        # Edge case: check breadcrumb
        breadcrumb = soup.find('nav', class_='g-breadcrumbs')
        if breadcrumb:
            items = breadcrumb.find_all('li', class_='item')
            # Second item (index 1) is breeder
            if len(items) > 1:
                link = items[1].find('a')
                if link:
                    gorilla.at[idx, 'breeder_extracted'] = link.get_text(strip=True)
                    extracted += 1
                    continue
        
        # Fallback: extract from URL pattern
        # https://www.gorilla-cannabis-seeds.co.uk/blimburn/feminized/narkosis.html
        if 'gorilla-cannabis-seeds.co.uk/' in url:
            parts = url.split('gorilla-cannabis-seeds.co.uk/')[1].split('/')
            if len(parts) > 0 and parts[0]:
                breeder = parts[0].replace('-', ' ').title()
                gorilla.at[idx, 'breeder_extracted'] = breeder
                extracted += 1
                continue
        
        failed += 1
    except:
        failed += 1
    
    if (extracted + failed) % 500 == 0:
        print(f"Processed: {extracted + failed}, Extracted: {extracted}, Failed: {failed}")

print(f"\nResults:")
print(f"  Extracted: {extracted} ({extracted/len(gorilla)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(gorilla)*100:.1f}%)")

gorilla.to_csv('../output/gorilla_breeders.csv', index=False, encoding='utf-8')
gorilla.head(100).to_csv('../output/gorilla_breeders_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: output/gorilla_breeders.csv")
