import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

def extract_lineage_exotic(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', id='tab-description')
    if not div:
        return None
    
    mother = None
    reversal = None
    
    for p in div.find_all('p'):
        text = p.get_text()
        if text.lower().startswith('mother:'):
            mother = text.split(':', 1)[1].strip()
        elif text.lower().startswith('reversal:'):
            # Get text before <br> tag
            reversal_text = ''
            for content in p.contents:
                if content.name == 'br':
                    break
                reversal_text += str(content)
            if ':' in reversal_text:
                reversal = reversal_text.split(':', 1)[1].strip()
    
    if mother and reversal:
        return {'parent_1': mother, 'parent_2': reversal}
    return None

def create_slug(name):
    if pd.isna(name) or name == '':
        return None
    name = str(name).strip().lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')

df = pd.read_csv('output/all_strains_lineage_cropking.csv', encoding='utf-8', low_memory=False)
exotic = df[df['seed_bank'] == 'exotic'].copy()
missing = exotic[exotic['parent_1_display'].isna()]

print(f"Exotic Genetics: {len(exotic)} total, {len(missing)} missing lineage")

s3 = boto3.client('s3')
extracted = 0

for idx, row in missing.iterrows():
    if pd.isna(row['s3_html_key_raw']):
        continue
    
    try:
        response = s3.get_object(Bucket='ci-strains-html-archive', Key=row['s3_html_key_raw'])
        html = response['Body'].read()
        lineage = extract_lineage_exotic(html)
        
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
            if extracted % 50 == 0:
                print(f"Extracted: {extracted}")
    except:
        continue

df.to_csv('output/all_strains_lineage_exotic.csv', index=False, encoding='utf-8')
print(f"\nExotic Genetics extraction complete: {extracted} lineage extracted")
print(f"Total with lineage: {df['parent_1_display'].notna().sum()} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
