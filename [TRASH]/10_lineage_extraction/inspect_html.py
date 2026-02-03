import pandas as pd
import boto3

df = pd.read_csv('output/all_strains_genetics_standardized.csv', encoding='latin-1', low_memory=False)
missing = df[df['parent_1_display'].isna()].copy()

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

row = missing.iloc[0]
s3_key = row['s3_html_key_raw']

print(f"Strain: {row['strain_name_display']}")
print(f"Breeder: {row['breeder_display']}")
print(f"\nFetching HTML from S3...")

response = s3.get_object(Bucket=bucket, Key=s3_key)
html = response['Body'].read().decode('utf-8', errors='ignore')

print(f"\nHTML length: {len(html)} chars")
print("\nFirst 3000 chars:")
print(html[:3000])
