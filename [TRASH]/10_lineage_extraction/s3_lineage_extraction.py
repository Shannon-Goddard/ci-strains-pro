import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re
from botocore.exceptions import ClientError

def extract_generation_from_html(soup):
    """Extract F1, S1, BX1 from HTML"""
    text = soup.get_text()
    f_gen = re.search(r'\bF(\d+)\b', text, re.IGNORECASE)
    s_gen = re.search(r'\bS(\d+)\b', text, re.IGNORECASE)
    bx_gen = re.search(r'\bBX(\d+)\b', text, re.IGNORECASE)
    
    filial = f"F{f_gen.group(1)}" if f_gen else None
    selfed = f"S{s_gen.group(1)}" if s_gen else None
    backcross = f"BX{bx_gen.group(1)}" if bx_gen else None
    
    generation = filial or selfed or backcross
    return generation, filial, selfed, backcross

def extract_from_table(soup):
    """Extract lineage from product tables"""
    for row in soup.find_all('tr'):
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 2:
            label = cells[0].get_text().strip().lower()
            value = cells[1].get_text().strip()
            
            if any(keyword in label for keyword in ['genetic', 'lineage', 'parent', 'cross', 'heritage']):
                # Look for X x Y pattern
                match = re.search(r'([^x]+)\s+x\s+([^x]+)', value, re.IGNORECASE)
                if match:
                    return {
                        'parent_1': match.group(1).strip(),
                        'parent_2': match.group(2).strip(),
                        'source': 'table'
                    }
    return None

def extract_from_meta(soup):
    """Extract lineage from meta tags"""
    meta_tags = soup.find_all('meta', attrs={'property': 'og:description'})
    meta_tags += soup.find_all('meta', attrs={'name': 'description'})
    
    for meta in meta_tags:
        content = meta.get('content', '')
        match = re.search(r'cross(?:ed)?\s+(?:of|between)?\s*([^x]+?)\s+(?:and|with|x)\s+([^.]+)', content, re.IGNORECASE)
        if match:
            return {
                'parent_1': match.group(1).strip(),
                'parent_2': match.group(2).strip(),
                'source': 'meta'
            }
    return None

def extract_from_spans(soup):
    """Extract from span/div with genetics classes"""
    for tag in soup.find_all(['span', 'div'], class_=re.compile(r'genetic|lineage|parent', re.IGNORECASE)):
        text = tag.get_text().strip()
        match = re.search(r'([^x]+)\s+x\s+([^x]+)', text, re.IGNORECASE)
        if match:
            return {
                'parent_1': match.group(1).strip(),
                'parent_2': match.group(2).strip(),
                'source': 'span'
            }
    return None

def extract_lineage_from_html(html_content):
    """Main extraction logic"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try table first (most reliable)
    lineage = extract_from_table(soup)
    if lineage:
        return lineage
    
    # Try meta tags
    lineage = extract_from_meta(soup)
    if lineage:
        return lineage
    
    # Try spans/divs
    lineage = extract_from_spans(soup)
    if lineage:
        return lineage
    
    return None

def create_slug(name):
    """Create slug for matching"""
    if pd.isna(name) or name == '':
        return None
    name = str(name).strip().lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')

# Load dataset
print("Loading dataset...")
df = pd.read_csv('output/all_strains_genetics_standardized.csv', encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df)}")

# Filter strains missing lineage
missing_lineage = df[df['parent_1_display'].isna()].copy()
print(f"Strains missing lineage: {len(missing_lineage)}")

# S3 setup
s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

# Process strains
extracted_count = 0
error_count = 0

print("\nExtracting lineage from S3 HTML files...")
for idx, row in missing_lineage.iterrows():
    if pd.isna(row['s3_html_key_raw']):
        continue
    
    s3_key = row['s3_html_key_raw']
    
    try:
        # Fetch HTML from S3
        response = s3.get_object(Bucket=bucket, Key=s3_key)
        html_content = response['Body'].read()
        
        # Extract lineage
        lineage_data = extract_lineage_from_html(html_content)
        
        if lineage_data:
            p1 = lineage_data['parent_1']
            p2 = lineage_data['parent_2']
            
            # Check if parent is nested
            p1_nested = ' x ' in p1.lower()
            p2_nested = ' x ' in p2.lower()
            
            # Update dataframe
            df.at[idx, 'parent_1_display'] = p1
            df.at[idx, 'parent_2_display'] = p2
            df.at[idx, 'parent_1_slug'] = create_slug(p1)
            df.at[idx, 'parent_2_slug'] = create_slug(p2)
            df.at[idx, 'parent_1_is_hybrid'] = p1_nested
            df.at[idx, 'parent_2_is_hybrid'] = p2_nested
            df.at[idx, 'has_nested_cross'] = p1_nested or p2_nested
            
            # Create lineage formula
            if pd.notna(df.at[idx, 'parent_1_slug']) and pd.notna(df.at[idx, 'parent_2_slug']):
                df.at[idx, 'lineage_formula'] = f"{df.at[idx, 'parent_1_slug']} x {df.at[idx, 'parent_2_slug']}"
            
            # Extract grandparents if nested
            if p1_nested:
                gp = re.split(r'\s+x\s+', p1, flags=re.IGNORECASE)
                if len(gp) >= 2:
                    df.at[idx, 'grandparent_1_display'] = gp[0].strip()
                    df.at[idx, 'grandparent_2_display'] = gp[1].strip()
                    df.at[idx, 'grandparent_1_slug'] = create_slug(gp[0])
                    df.at[idx, 'grandparent_2_slug'] = create_slug(gp[1])
            
            extracted_count += 1
            
            if extracted_count % 100 == 0:
                print(f"Processed: {extracted_count} extracted")
    
    except ClientError as e:
        error_count += 1
        if error_count % 100 == 0:
            print(f"Errors: {error_count}")
        continue
    except Exception as e:
        error_count += 1
        continue

# Save enriched dataset
output_path = 'output/all_strains_lineage_s3_enriched.csv'
df.to_csv(output_path, index=False, encoding='latin-1')

print(f"\nS3 lineage extraction complete: {output_path}")
print(f"New lineage extracted: {extracted_count}")
print(f"Errors: {error_count}")
print(f"Total with lineage: {df['parent_1_display'].notna().sum()} ({df['parent_1_display'].notna().sum()/len(df)*100:.1f}%)")
