#!/usr/bin/env python3
"""
Find URLs that don't have HTML files in S3 archive
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import json
from pathlib import Path

def find_missing_html():
    """Compare master URL list against S3 metadata to find missing HTML files"""
    
    # Read the complete CSV (just URL column to avoid memory issues)
    csv_path = Path(__file__).parent / "s3_complete_inventory.csv"
    print(f"Reading URLs from: {csv_path}")
    
    df = pd.read_csv(csv_path, usecols=['url'], encoding='latin-1')
    master_urls = set(df['url'])
    print(f"Total URLs in master list: {len(master_urls)}")
    
    # Initialize S3 client
    s3_client = boto3.client('s3')
    bucket_name = 'ci-strains-html-archive'
    
    # Get URLs from S3 metadata
    print("Reading URLs from S3 metadata...")
    s3_urls = set()
    paginator = s3_client.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket_name, Prefix='metadata/'):
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['Key'].endswith('.json'):
                    content = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])['Body'].read()
                    metadata = json.loads(content)
                    if 'url' in metadata:
                        s3_urls.add(metadata['url'])
    
    print(f"URLs found in S3: {len(s3_urls)}")
    
    # Find missing URLs
    missing_urls = master_urls - s3_urls
    
    print(f"\nResults:")
    print(f"Total URLs in master: {len(master_urls)}")
    print(f"URLs with HTML in S3: {len(s3_urls)}")
    print(f"URLs missing HTML: {len(missing_urls)}")
    
    if missing_urls:
        missing_list = list(missing_urls)
        for url in missing_list[:10]:
            print(f"  - {url}")
        if len(missing_list) > 10:
            print(f"  ... and {len(missing_list) - 10} more")
        
        pd.DataFrame({'missing_url': missing_list}).to_csv(
            Path(__file__).parent / "missing_html_urls.csv", index=False)
    
    return list(missing_urls)

if __name__ == "__main__":
    missing = find_missing_html()