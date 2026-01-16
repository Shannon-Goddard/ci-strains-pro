#!/usr/bin/env python3
"""
Create inventory of JS-rendered HTML files from S3
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import json
from datetime import datetime

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

print("Scanning S3 html_js/ folder...")

# Get all JS HTML files
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix='html_js/')

inventory = []

for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            key = obj['Key']
            if key.endswith('_js.html'):
                # Extract hash
                url_hash = key.replace('html_js/', '').replace('_js.html', '')
                
                # Get corresponding metadata
                try:
                    meta_key = f'metadata/{url_hash}.json'
                    meta_obj = s3.get_object(Bucket=bucket, Key=meta_key)
                    metadata = json.loads(meta_obj['Body'].read())
                    url = metadata['url']
                except:
                    url = 'Unknown'
                
                inventory.append({
                    'url_hash': url_hash,
                    'url': url,
                    'html_key': key,
                    'html_size': obj['Size']
                })
                
                if len(inventory) % 100 == 0:
                    print(f"Processed {len(inventory)} files...")

# Create DataFrame
df = pd.DataFrame(inventory)

# Add seed bank column
df['seed_bank'] = df['url'].apply(lambda x: 'ILGM' if 'ilgm.com' in str(x) else ('Seedsman' if 'seedsman.com' in str(x) else 'Unknown'))

# Save inventory
output_file = 's3_js_html_inventory.csv'
df.to_csv(output_file, index=False, encoding='utf-8')

print("\nInventory complete!")
print(f"Total files: {len(df)}")
print(f"ILGM: {len(df[df['seed_bank']=='ILGM'])}")
print(f"Seedsman: {len(df[df['seed_bank']=='Seedsman'])}")
print(f"Saved to: {output_file}")
