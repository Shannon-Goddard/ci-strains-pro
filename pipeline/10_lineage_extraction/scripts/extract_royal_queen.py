import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

df = pd.read_csv('output/all_strains_lineage_north_atlantic.csv', encoding='utf-8', low_memory=False)
royal_queen = df[(df['seed_bank'] == 'royal_queen_seeds') & (df['parent_1_display'].isna())].copy()

print(f"Processing {len(royal_queen)} Royal Queen strains...")

extracted = 0
for idx, row in royal_queen.iterrows():
    try:
        obj = s3.get_object(Bucket=bucket, Key=row['s3_html_key_raw'])
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        h2 = soup.find('h2', class_='product-keywords')
        if h2:
            genetics = h2.get_text(strip=True)
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

print(f"Extracted: {extracted}/{len(royal_queen)} ({extracted/len(royal_queen)*100:.1f}%)")
df.to_csv('output/all_strains_lineage_royal_queen.csv', index=False, encoding='utf-8')
print(f"Total coverage: {df['parent_1_display'].notna().sum()}/{len(df)} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
