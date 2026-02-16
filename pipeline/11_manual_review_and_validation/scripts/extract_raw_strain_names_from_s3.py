import pandas as pd
import boto3
from bs4 import BeautifulSoup
from io import BytesIO

# AWS S3 setup
s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df):,}")

def extract_strain_name_from_html(s3_key):
    """Extract strain name from S3 HTML archive"""
    try:
        # Download HTML from S3
        response = s3.get_object(Bucket=bucket, Key=s3_key)
        html_content = response['Body'].read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Try multiple extraction methods (seed banks vary)
        # 1. Try <h1> tag (most common)
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        # 2. Try <title> tag
        title = soup.find('title')
        if title:
            # Remove site name (e.g., "Strain Name | Seed Bank")
            title_text = title.get_text(strip=True)
            if '|' in title_text:
                return title_text.split('|')[0].strip()
            if '-' in title_text:
                return title_text.split('-')[0].strip()
            return title_text
        
        # 3. Try product name meta tag
        meta = soup.find('meta', property='og:title')
        if meta and meta.get('content'):
            return meta['content'].strip()
        
        return None
    except Exception as e:
        print(f"Error extracting from {s3_key}: {e}")
        return None

print("\nExtracting strain names from S3 HTML archives...")
print("This will take ~5 minutes for 21,223 strains...")

# Extract strain names
strain_names = []
for idx, row in df.iterrows():
    if idx % 100 == 0:
        print(f"Progress: {idx:,} / {len(df):,} ({(idx/len(df)*100):.1f}%)")
    
    s3_key = row['s3_html_key_raw']
    strain_name = extract_strain_name_from_html(s3_key)
    strain_names.append(strain_name)

# Update dataframe
df['strain_name_raw_2'] = strain_names

# Check coverage
missing = df['strain_name_raw_2'].isna().sum()
print(f"\nCoverage: {len(df) - missing:,} / {len(df):,} ({((len(df) - missing) / len(df) * 100):.1f}%)")

if missing > 0:
    print(f"Warning: {missing} strains missing strain_name_raw_2")
    print("\nSample of missing:")
    print(df[df['strain_name_raw_2'].isna()][['strain_id', 's3_html_key_raw']].head(10))

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")

# Show samples
print("\nSample comparison:")
print(df[['strain_name_raw', 'strain_name_raw_2', 'strain_name_display_manual']].head(10).to_string(index=False))
