"""
Attitude Seed Bank - Breeder Extraction
Extracts breeder names from breadcrumb pattern.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

s3 = boto3.client('s3')
BUCKET = 'ci-strains-html-archive'

# Load inventory
print("Loading S3 inventory...")
inv = pd.read_csv('../../03_s3_inventory/s3_html_inventory.csv')
url_to_key = dict(zip(inv['url'], inv['s3_html_key']))

# Load dataset
print("Loading master dataset...")
df = pd.read_csv('../input/master_strains_raw.csv', encoding='latin-1', low_memory=False)
attitude = df[df['seed_bank'] == 'attitude'].copy()
print(f"Attitude strains: {len(attitude)}")

# Extract breeders
extracted = 0
failed = 0

print("\nExtracting breeders...")
for idx in attitude.index:
    url = attitude.at[idx, 'source_url_raw']
    s3_key = url_to_key.get(url)
    
    if not s3_key:
        failed += 1
        continue
    
    try:
        response = s3.get_object(Bucket=BUCKET, Key=s3_key)
        html = response['Body'].read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find breeder link in breadcrumb: <a href="/00-seeds/cat_195">00 Seeds</a> OR <a href="/bulk-seeds">Bulk Seeds</a>
        breadcrumb = soup.find('div', class_=re.compile('breadcrumb', re.I))
        if breadcrumb:
            # Try pattern with cat_ first, then without
            link = breadcrumb.find('a', href=re.compile(r'^/[^/]+(/cat_\d+)?$'))
            if link:
                attitude.at[idx, 'breeder_extracted'] = link.get_text(strip=True)
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
print(f"  Extracted: {extracted} ({extracted/len(attitude)*100:.1f}%)")
print(f"  Failed: {failed} ({failed/len(attitude)*100:.1f}%)")

# Save
attitude.to_csv('../output/attitude_breeders.csv', index=False, encoding='utf-8')
attitude.head(100).to_csv('../output/attitude_breeders_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: output/attitude_breeders.csv")
