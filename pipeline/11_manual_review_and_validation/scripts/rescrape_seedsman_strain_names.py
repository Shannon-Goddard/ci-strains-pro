import pandas as pd
import boto3
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)

seedsman_mask = df['seed_bank_display'] == 'Seedsman'
seedsman_count = seedsman_mask.sum()
print(f"\nSeedsman strains to fix: {seedsman_count:,}")

def extract_seedsman_strain_name(s3_key):
    """Extract strain name from Seedsman HTML"""
    try:
        response = s3.get_object(Bucket=bucket, Key=s3_key)
        html_content = response['Body'].read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Try multiple selectors (Seedsman is JS-rendered, structure may vary)
        # 1. Try h1
        h1 = soup.find('h1')
        if h1 and 'javascript' not in h1.get_text().lower():
            return h1.get_text(strip=True)
        
        # 2. Try product title class
        product_title = soup.find(class_='product-title')
        if product_title:
            return product_title.get_text(strip=True)
        
        # 3. Try title tag
        title = soup.find('title')
        if title:
            title_text = title.get_text(strip=True)
            if '|' in title_text:
                return title_text.split('|')[0].strip()
            if '-' in title_text and 'seedsman' not in title_text.lower():
                return title_text.split('-')[0].strip()
        
        # 4. Try meta og:title
        meta = soup.find('meta', property='og:title')
        if meta and meta.get('content'):
            return meta['content'].strip()
        
        return None
    except Exception as e:
        return None

print("\nExtracting Seedsman strain names from S3...")
print("(Seedsman is JS-rendered, may have lower success rate)")

seedsman_indices = df[seedsman_mask].index
for idx, row_idx in enumerate(seedsman_indices):
    if idx % 100 == 0:
        print(f"Progress: {idx:,} / {seedsman_count:,} ({(idx/seedsman_count*100):.1f}%)")
    
    s3_key = df.loc[row_idx, 's3_html_key_raw']
    strain_name = extract_seedsman_strain_name(s3_key)
    
    if strain_name:
        df.loc[row_idx, 'strain_name_raw_2'] = strain_name

# Check results
fixed = df[seedsman_mask]['strain_name_raw_2'].notna().sum()
print(f"\nFixed: {fixed:,} / {seedsman_count:,} ({(fixed/seedsman_count*100):.1f}%)")

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")
