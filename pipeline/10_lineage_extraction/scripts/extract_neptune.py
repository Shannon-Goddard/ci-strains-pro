import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

df = pd.read_csv('output/all_strains_lineage_mephisto.csv', encoding='utf-8', low_memory=False)
neptune = df[(df['seed_bank'] == 'neptune') & (df['parent_1_display'].isna())].copy()

print(f"Processing {len(neptune)} Neptune strains...")

extracted = 0
for idx, row in neptune.iterrows():
    try:
        obj = s3.get_object(Bucket=bucket, Key=row['s3_html_key_raw'])
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        desc = soup.find('div', class_='woocommerce-product-details__short-description')
        if desc:
            text = desc.get_text()
            match = re.search(r'Lineage:\s*([^\n<]+)', text)
            if match:
                genetics = match.group(1).strip()
                if ' x ' in genetics.lower():
                    parts = genetics.split(' x ')
                    if len(parts) >= 2:
                        df.at[idx, 'parent_1_display'] = parts[0].strip()
                        df.at[idx, 'parent_2_display'] = parts[-1].strip()
                        df.at[idx, 'parent_1_slug'] = re.sub(r'[^a-z0-9]+', '-', parts[0].strip().lower()).strip('-')
                        df.at[idx, 'parent_2_slug'] = re.sub(r'[^a-z0-9]+', '-', parts[-1].strip().lower()).strip('-')
                        df.at[idx, 'is_hybrid'] = 1
                        extracted += 1
    except Exception as e:
        continue

print(f"Extracted: {extracted}/{len(neptune)} ({extracted/len(neptune)*100:.1f}%)")
df.to_csv('output/all_strains_lineage_neptune.csv', index=False, encoding='utf-8')
print(f"Total coverage: {df['parent_1_display'].notna().sum()}/{len(df)} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
