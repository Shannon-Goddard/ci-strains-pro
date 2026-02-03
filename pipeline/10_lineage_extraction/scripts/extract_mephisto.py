import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

df = pd.read_csv('output/all_strains_lineage_herbies.csv', encoding='utf-8')
mephisto = df[(df['seed_bank'] == 'mephisto_genetics') & (df['parent_1_display'].isna())].copy()

print(f"Processing {len(mephisto)} Mephisto strains...")

extracted = 0
for idx, row in mephisto.iterrows():
    try:
        obj = s3.get_object(Bucket=bucket, Key=row['s3_html_key_raw'])
        html = obj['Body'].read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find grid with "Genetic Heritage" label
        grid = soup.find('div', class_='w-layout-grid grid')
        if grid:
            divs = grid.find_all('div')
            for i, div in enumerate(divs):
                if 'Genetic Heritage' in div.get_text():
                    if i + 1 < len(divs):
                        genetics = divs[i + 1].get_text(strip=True)
                        if genetics and ' x ' in genetics.lower():
                            parts = genetics.split(' x ')
                            if len(parts) >= 2:
                                df.at[idx, 'parent_1_display'] = parts[0].strip()
                                df.at[idx, 'parent_2_display'] = parts[-1].strip()
                                df.at[idx, 'parent_1_slug'] = re.sub(r'[^a-z0-9]+', '-', parts[0].strip().lower()).strip('-')
                                df.at[idx, 'parent_2_slug'] = re.sub(r'[^a-z0-9]+', '-', parts[-1].strip().lower()).strip('-')
                                df.at[idx, 'is_hybrid'] = 1
                                extracted += 1
                                break
                
                # Check for generation in "Seed Type" field
                if 'Seed Type' in div.get_text():
                    if i + 1 < len(divs):
                        seed_type = divs[i + 1].get_text(strip=True)
                        if 'F1' in seed_type:
                            df.at[idx, 'generation_f'] = 'F1'
                        elif 'F2' in seed_type:
                            df.at[idx, 'generation_f'] = 'F2'
    except Exception as e:
        continue

print(f"Extracted: {extracted}/{len(mephisto)} ({extracted/len(mephisto)*100:.1f}%)")
df.to_csv('output/all_strains_lineage_mephisto.csv', index=False, encoding='utf-8')
print(f"Total coverage: {df['parent_1_display'].notna().sum()}/{len(df)} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
