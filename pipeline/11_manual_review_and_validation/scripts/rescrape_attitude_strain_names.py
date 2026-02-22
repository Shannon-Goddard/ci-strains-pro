import pandas as pd
import boto3
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)

attitude_mask = df['seed_bank_display'] == 'The Attitude Seedbank'
attitude_count = attitude_mask.sum()
print(f"\nAttitude strains to fix: {attitude_count:,}")

def extract_attitude_strain_name(s3_key):
    """Extract strain name from Attitude HTML using h2.productHeading"""
    try:
        response = s3.get_object(Bucket=bucket, Key=s3_key)
        html_content = response['Body'].read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find h2 with class="productHeading"
        h2 = soup.find('h2', class_='productHeading')
        if h2:
            return h2.get_text(strip=True)
        
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

print("\nExtracting Attitude strain names from S3...")
attitude_indices = df[attitude_mask].index

for idx, row_idx in enumerate(attitude_indices):
    if idx % 500 == 0:
        print(f"Progress: {idx:,} / {attitude_count:,} ({(idx/attitude_count*100):.1f}%)")
    
    s3_key = df.loc[row_idx, 's3_html_key_raw']
    strain_name = extract_attitude_strain_name(s3_key)
    
    if strain_name:
        df.loc[row_idx, 'strain_name_raw'] = strain_name

# Check results
fixed = df[attitude_mask]['strain_name_raw'].notna().sum()
print(f"\nFixed: {fixed:,} / {attitude_count:,} ({(fixed/attitude_count*100):.1f}%)")

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")
