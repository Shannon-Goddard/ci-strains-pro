import pandas as pd
import boto3
import re

df = pd.read_csv('output/all_strains_genetics_standardized.csv', encoding='latin-1', low_memory=False)
missing = df[df['parent_1_display'].isna()].copy()

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

row = missing.iloc[0]
s3_key = row['s3_html_key_raw']

response = s3.get_object(Bucket=bucket, Key=s3_key)
html = response['Body'].read().decode('utf-8', errors='ignore')

keywords = ['genetic', 'lineage', 'parent', 'cross', 'heritage', 'bred', 'breeding']

print(f"Strain: {row['strain_name_display']}")
print(f"Searching for lineage keywords...\n")

for keyword in keywords:
    matches = re.finditer(rf'.{{0,100}}{keyword}.{{0,100}}', html, re.IGNORECASE)
    for i, match in enumerate(matches):
        if i < 3:  # First 3 matches per keyword
            print(f"{keyword.upper()}: ...{match.group()}...")
