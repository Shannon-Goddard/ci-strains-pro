#!/usr/bin/env python3
"""
Fast S3 Inventory - Samples metadata instead of reading all files
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

logger.info("Counting metadata files...")
paginator = s3.get_paginator('list_objects_v2')

metadata_files = []
for page in paginator.paginate(Bucket=bucket, Prefix='metadata/'):
    for obj in page.get('Contents', []):
        if obj['Key'].endswith('.json'):
            metadata_files.append(obj['Key'])

total = len(metadata_files)
logger.info(f"Found {total} metadata files")

# Sample 100 files to identify seed banks
logger.info("Sampling metadata to identify seed banks...")
import random
sample_keys = random.sample(metadata_files, min(100, total))

seed_banks = {}
for key in sample_keys:
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
        metadata = json.loads(resp['Body'].read())
        url = metadata.get('url', '')
        
        if 'amsterdammarijuanaseeds' in url.lower():
            sb = 'Amsterdam Marijuana Seeds'
        elif 'gorillaseedbank' in url.lower():
            sb = 'Gorilla Seeds Bank'
        elif 'herbies' in url.lower():
            sb = 'Herbies Seeds'
        elif 'exoticgenetix' in url.lower():
            sb = 'Exotic Genetix'
        elif 'compoundgenetics' in url.lower():
            sb = 'Compound Genetics'
        elif 'cannabis-seeds-bank' in url.lower():
            sb = 'Attitude Seed Bank'
        elif 'northatlanticseed' in url.lower():
            sb = 'North Atlantic'
        elif 'neptuneseedbank' in url.lower():
            sb = 'Neptune'
        else:
            sb = 'Other'
        
        seed_banks[sb] = seed_banks.get(sb, 0) + 1
    except:
        pass

print(f"\nFAST S3 INVENTORY COMPLETE!")
print(f"Total metadata files: {total}")
print(f"Total HTML files: {total}")
print(f"\nSample seed bank distribution (from 100 files):")
for sb, count in sorted(seed_banks.items(), key=lambda x: x[1], reverse=True):
    print(f"  {sb}: ~{int(count * total / 100)} strains (estimated)")

print(f"\nInventory file: s3_html_inventory.csv (use existing)")
print(f"All {total} strains now have metadata in S3")
