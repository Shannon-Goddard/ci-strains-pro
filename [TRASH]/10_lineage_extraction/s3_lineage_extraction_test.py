import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re
from botocore.exceptions import ClientError

def extract_lineage_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try table
    for row in soup.find_all('tr'):
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 2:
            label = cells[0].get_text().strip().lower()
            value = cells[1].get_text().strip()
            if any(k in label for k in ['genetic', 'lineage', 'parent', 'cross']):
                match = re.search(r'([^x]+)\s+x\s+([^x]+)', value, re.IGNORECASE)
                if match:
                    return {'parent_1': match.group(1).strip(), 'parent_2': match.group(2).strip()}
    
    # Try meta
    for meta in soup.find_all('meta'):
        content = meta.get('content', '')
        match = re.search(r'cross(?:ed)?\s+(?:of|between)?\s*([^x]+?)\s+(?:and|with|x)\s+([^.]+)', content, re.IGNORECASE)
        if match:
            return {'parent_1': match.group(1).strip(), 'parent_2': match.group(2).strip()}
    
    return None

# Load dataset
print("Loading dataset...")
df = pd.read_csv('output/all_strains_genetics_standardized.csv', encoding='latin-1', low_memory=False)
print(f"Total: {len(df)}")

missing = df[df['parent_1_display'].isna()].copy()
print(f"Missing lineage: {len(missing)}")

# Test first 10
s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

print("\nTesting first 10 strains...")
for i, (idx, row) in enumerate(missing.head(10).iterrows()):
    if pd.isna(row['s3_html_key_raw']):
        print(f"{i+1}. SKIP - No S3 key")
        continue
    
    try:
        print(f"{i+1}. Fetching {row['s3_html_key_raw'][:50]}...")
        response = s3.get_object(Bucket=bucket, Key=row['s3_html_key_raw'])
        html = response['Body'].read()
        
        lineage = extract_lineage_from_html(html)
        if lineage:
            print(f"   FOUND: {lineage['parent_1']} x {lineage['parent_2']}")
        else:
            print(f"   NOT FOUND")
    except Exception as e:
        print(f"   ERROR: {str(e)[:50]}")

print("\nTest complete. Check if S3 access is working.")
