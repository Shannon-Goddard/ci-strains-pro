import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

def extract_lineage_gorilla(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = row.find_all(['th', 'td'])
            if len(cells) >= 2:
                label = cells[0].get_text().strip().lower()
                if 'genetic' in label:
                    value = cells[1].get_text().strip()
                    parts = re.split(r'\s+x\s+', value, flags=re.IGNORECASE)
                    if len(parts) >= 2:
                        return {
                            'parent_1': ' x '.join(parts[:-1]).strip(),
                            'parent_2': parts[-1].strip()
                        }
    return None

def create_slug(name):
    if pd.isna(name) or name == '':
        return None
    name = str(name).strip().lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')

df = pd.read_csv('output/all_strains_lineage_exotic.csv', encoding='utf-8', low_memory=False)
gorilla = df[df['seed_bank'] == 'gorilla'].copy()
missing = gorilla[gorilla['parent_1_display'].isna()]

print(f"Gorilla: {len(gorilla)} total, {len(missing)} missing lineage")

s3 = boto3.client('s3')
extracted = 0

for idx, row in missing.iterrows():
    if pd.isna(row['s3_html_key_raw']):
        continue
    
    try:
        response = s3.get_object(Bucket='ci-strains-html-archive', Key=row['s3_html_key_raw'])
        html = response['Body'].read()
        lineage = extract_lineage_gorilla(html)
        
        if lineage:
            p1 = lineage['parent_1']
            p2 = lineage['parent_2']
            
            df.at[idx, 'parent_1_display'] = p1
            df.at[idx, 'parent_2_display'] = p2
            df.at[idx, 'parent_1_slug'] = create_slug(p1)
            df.at[idx, 'parent_2_slug'] = create_slug(p2)
            df.at[idx, 'parent_1_is_hybrid'] = ' x ' in p1.lower()
            df.at[idx, 'parent_2_is_hybrid'] = ' x ' in p2.lower()
            df.at[idx, 'has_nested_cross'] = (' x ' in p1.lower()) or (' x ' in p2.lower())
            
            if pd.notna(df.at[idx, 'parent_1_slug']) and pd.notna(df.at[idx, 'parent_2_slug']):
                df.at[idx, 'lineage_formula'] = f"{df.at[idx, 'parent_1_slug']} x {df.at[idx, 'parent_2_slug']}"
            
            extracted += 1
            if extracted % 100 == 0:
                print(f"Extracted: {extracted}")
    except:
        continue

df.to_csv('output/all_strains_lineage_gorilla.csv', index=False, encoding='utf-8')
print(f"\nGorilla extraction complete: {extracted} lineage extracted")
print(f"Total with lineage: {df['parent_1_display'].notna().sum()} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
