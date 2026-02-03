import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

df = pd.read_csv('output/all_strains_lineage_royal_queen.csv', encoding='utf-8', low_memory=False)
seeds_here_now = df[(df['seed_bank'] == 'seeds_here_now') & (df['parent_1_display'].isna())].copy()

print(f"Processing {len(seeds_here_now)} Seeds Here Now strains...")

extracted = 0
for idx, row in seeds_here_now.iterrows():
    try:
        obj = s3.get_object(Bucket=bucket, Key=row['s3_html_key_raw'])
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        for th in soup.find_all('th'):
            if 'Genetics' in th.get_text():
                td = th.find_next_sibling('td')
                if td:
                    genetics = td.get_text(strip=True)
                    if ' x ' in genetics.lower():
                        parts = genetics.split(' x ')
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

print(f"Extracted: {extracted}/{len(seeds_here_now)} ({extracted/len(seeds_here_now)*100:.1f}%)")
df.to_csv('output/all_strains_lineage_seeds_here_now.csv', index=False, encoding='utf-8')
print(f"Total coverage: {df['parent_1_display'].notna().sum()}/{len(df)} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
