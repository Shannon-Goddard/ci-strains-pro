import pandas as pd
import boto3
from bs4 import BeautifulSoup

s3_client = boto3.client('s3')
bucket_name = 'strains-data-raw'

input_file = 'output/pipeline_11_clean.csv'
output_file = 'output/pipeline_11_clean.csv'

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df):,}\n")

# Filter Attitude only
attitude_mask = df['seed_bank_display'] == 'Attitude'
attitude_count = attitude_mask.sum()
print(f"Attitude strains to rescrape: {attitude_count:,}\n")

success = 0
failed = 0

for idx in df[attitude_mask].index:
    s3_key = df.at[idx, 's3_html_key_raw']
    
    if pd.isna(s3_key):
        failed += 1
        continue
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        html_content = response['Body'].read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Attitude uses h2.productHeading
        heading = soup.find('h2', class_='productHeading')
        if heading:
            strain_name = heading.get_text(strip=True)
            df.at[idx, 'strain_name_raw'] = strain_name
            success += 1
        else:
            failed += 1
        
        if (success + failed) % 100 == 0:
            print(f"Progress: {success + failed:,}/{attitude_count:,} - Success: {success:,}, Failed: {failed:,}")
    
    except Exception as e:
        failed += 1

print(f"\nComplete!")
print(f"Success: {success:,}/{attitude_count:,} ({success/attitude_count*100:.1f}%)")
print(f"Failed: {failed:,}")

df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")
