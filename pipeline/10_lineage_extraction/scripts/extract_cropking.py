import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

def extract_lineage_cropking(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='eael-data-table')
    if not table:
        return None
    
    rows = table.find_all('tr')
    for i, row in enumerate(rows):
        cells = row.find_all('td')
        if len(cells) >= 2:
            label_div = cells[0].find('div', class_='td-content')
            value_div = cells[1].find('div', class_='td-content')
            
            if label_div and value_div:
                label = label_div.get_text().strip().lower()
                if 'genetic' in label:
                    value = value_div.get_text().strip()
                    # Handle "and" or "x"
                    match = re.search(r'([^x]+?)\s+(?:and|x)\s+([^x]+)', value, re.IGNORECASE)
                    if match:
                        return {
                            'parent_1': match.group(1).strip(),
                            'parent_2': match.group(2).strip()
                        }
    return None

def create_slug(name):
    if pd.isna(name) or name == '':
        return None
    name = str(name).strip().lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')

df = pd.read_csv('output/all_strains_lineage_barneys.csv', encoding='utf-8', low_memory=False)
cropking = df[df['seed_bank'] == 'crop_king'].copy()
missing = cropking[cropking['parent_1_display'].isna()]

print(f"Crop King: {len(cropking)} total, {len(missing)} missing lineage")

s3 = boto3.client('s3')
extracted = 0

for idx, row in missing.iterrows():
    if pd.isna(row['s3_html_key_raw']):
        continue
    
    try:
        response = s3.get_object(Bucket='ci-strains-html-archive', Key=row['s3_html_key_raw'])
        html = response['Body'].read()
        lineage = extract_lineage_cropking(html)
        
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

df.to_csv('output/all_strains_lineage_cropking.csv', index=False, encoding='utf-8')
print(f"\nCrop King extraction complete: {extracted} lineage extracted")
print(f"Total with lineage: {df['parent_1_display'].notna().sum()} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
