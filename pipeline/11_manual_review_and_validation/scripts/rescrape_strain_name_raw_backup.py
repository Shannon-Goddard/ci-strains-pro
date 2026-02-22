import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

# S3 setup
s3_client = boto3.client('s3')
bucket_name = 'strains-data-raw'

input_file = 'output/pipeline_11_clean.csv'
output_file = 'output/pipeline_11_clean_rescraped.csv'

print("Reading backup CSV...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df):,}\n")

print("Sample of current strain_name_raw:")
print(df[['strain_name_display', 'strain_name_raw', 'seed_bank_display']].head(10))
print()

proceed = input("Proceed with rescraping strain_name_raw from S3? (yes/no): ")
if proceed.lower() != 'yes':
    print("Aborted.")
    exit()

def extract_strain_name_from_html(html_content, seed_bank):
    """Extract strain name from HTML based on seed bank"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Attitude - use h2.productHeading
    if seed_bank == 'Attitude':
        heading = soup.find('h2', class_='productHeading')
        if heading:
            return heading.get_text(strip=True)
    
    # Try common patterns for all seed banks
    # 1. h1 tag
    h1 = soup.find('h1')
    if h1:
        text = h1.get_text(strip=True)
        if text and len(text) < 200:  # Reasonable length
            return text
    
    # 2. title tag
    title = soup.find('title')
    if title:
        text = title.get_text(strip=True)
        # Remove common suffixes
        text = re.sub(r'\s*[-|]\s*(Buy|Shop|Seeds|Seed Bank).*$', '', text, flags=re.IGNORECASE)
        if text and len(text) < 200:
            return text
    
    # 3. meta og:title
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        text = og_title['content'].strip()
        if text and len(text) < 200:
            return text
    
    return None

# Rescrape
print("\nRescraping strain_name_raw from S3...\n")
success_count = 0
fail_count = 0

for idx, row in df.iterrows():
    s3_key = row['s3_html_key_raw']
    seed_bank = row['seed_bank_display']
    
    if pd.isna(s3_key):
        fail_count += 1
        continue
    
    try:
        # Fetch from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        html_content = response['Body'].read().decode('utf-8', errors='ignore')
        
        # Extract strain name
        strain_name = extract_strain_name_from_html(html_content, seed_bank)
        
        if strain_name:
            df.at[idx, 'strain_name_raw'] = strain_name
            success_count += 1
        else:
            fail_count += 1
        
        # Progress
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1:,}/{len(df):,} - Success: {success_count:,}, Failed: {fail_count:,}")
    
    except Exception as e:
        fail_count += 1
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1:,}/{len(df):,} - Success: {success_count:,}, Failed: {fail_count:,}")

print(f"\nRescraping complete!")
print(f"Success: {success_count:,}/{len(df):,} ({success_count/len(df)*100:.1f}%)")
print(f"Failed: {fail_count:,}/{len(df):,} ({fail_count/len(df)*100:.1f}%)")

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")

print("\nSample of rescraped strain_name_raw:")
print(df[['strain_name_display', 'strain_name_raw', 'seed_bank_display']].head(20))
