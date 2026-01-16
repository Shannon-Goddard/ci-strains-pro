#!/usr/bin/env python3
"""
Unified S3 Inventory - Combines html/ and pipeline06/ folders
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import json
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

# Part 1: Get html/ folder with metadata
logger.info("Loading html/ folder inventory...")
df_html = pd.read_csv('s3_html_inventory.csv')
df_html['source_folder'] = 'html'
logger.info(f"Loaded {len(df_html)} strains from html/")

# Part 2: Get pipeline06/ folder
logger.info("Scanning pipeline06/ folder...")
paginator = s3.get_paginator('list_objects_v2')
pipeline06_files = []

for page in paginator.paginate(Bucket=bucket, Prefix='pipeline06/'):
    for obj in page.get('Contents', []):
        if obj['Key'].endswith('.html'):
            url_hash = obj['Key'].split('/')[-1].replace('.html', '')
            pipeline06_files.append({
                'url_hash': url_hash,
                's3_html_key': obj['Key'],
                'html_size': obj['Size'],
                'source_folder': 'pipeline06'
            })

df_pipeline06 = pd.DataFrame(pipeline06_files)
logger.info(f"Found {len(df_pipeline06)} strains in pipeline06/")

# Try to get URLs from database
try:
    db_path = '../../01_html_collection/elite_seedbanks_collection/data/elite_merged_urls.db'
    conn = sqlite3.connect(db_path)
    df_db = pd.read_sql_query("SELECT url_hash, original_url as url, seedbank as seed_bank FROM merged_urls WHERE status = 'success'", conn)
    conn.close()
    df_pipeline06 = df_pipeline06.merge(df_db, on='url_hash', how='left')
    logger.info(f"Mapped {df_pipeline06['url'].notna().sum()} URLs from database")
except Exception as e:
    logger.warning(f"Could not load database: {e}")
    df_pipeline06['url'] = None
    df_pipeline06['seed_bank'] = 'Unknown'

# Combine both
df_unified = pd.concat([df_html, df_pipeline06], ignore_index=True)

# Save unified inventory
df_unified.to_csv('unified_s3_inventory.csv', index=False, encoding='utf-8')

print(f"\nUNIFIED S3 INVENTORY COMPLETE!")
print(f"Total strains: {len(df_unified)}")
print(f"  - html/ folder: {len(df_html)}")
print(f"  - pipeline06/ folder: {len(df_pipeline06)}")
print(f"\nSaved to: unified_s3_inventory.csv")
