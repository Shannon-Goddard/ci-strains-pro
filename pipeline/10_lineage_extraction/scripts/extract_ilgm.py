import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

df = pd.read_csv('output/all_strains_lineage_seedsman.csv', encoding='utf-8', low_memory=False)
ilgm = df[(df['seed_bank'] == 'ilgm') & (df['parent_1_display'].isna())].copy()

print(f"Processing {len(ilgm)} ILGM strains...")

extracted = 0
for idx, row in ilgm.iterrows():
    try:
        obj = s3.get_object(Bucket=bucket, Key=row['s3_html_key_raw'])
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        for td in soup.find_all('td', class_='p-0'):
            text = td.get_text(strip=True)
            if text == 'Lineage':
                next_td = td.find_next_sibling('td')
                if next_td:
                    genetics = next_td.get_text(strip=True)
                    # Handle comma or "and" separators
                    if ' x ' in genetics.lower():
                        parts = genetics.split(' x ')
                    elif ',' in genetics:
                        parts = [p.strip() for p in genetics.split(',')]
                    elif ' and ' in genetics.lower():
                        parts = genetics.lower().replace(' and ', ',').split(',')
                        parts = [p.strip() for p in parts]
                    else:
                        continue
                    
                    if len(parts) >= 2:
                        df.at[idx, 'parent_1_display'] = parts[0].strip()
                        df.at[idx, 'parent_2_display'] = parts[-1].strip()
                        df.at[idx, 'parent_1_slug'] = re.sub(r'[^a-z0-9]+', '-', parts[0].strip().lower()).strip('-')
                        df.at[idx, 'parent_2_slug'] = re.sub(r'[^a-z0-9]+', '-', parts[-1].strip().lower()).strip('-')
                        df.at[idx, 'is_hybrid'] = 1
                        extracted += 1
                        break
    except Exception as e:
        continue

print(f"Extracted: {extracted}/{len(ilgm)} ({extracted/len(ilgm)*100:.1f}%)")
df.to_csv('output/all_strains_lineage_ilgm.csv', index=False, encoding='utf-8')
print(f"Total coverage: {df['parent_1_display'].notna().sum()}/{len(df)} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
