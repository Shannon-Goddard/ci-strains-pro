#!/usr/bin/env python3
"""
Create metadata for elite seed bank files
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import sqlite3
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

# Load database
db_path = '../01_html_collection/elite_seedbanks_collection/data/elite_merged_urls.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT url_hash, original_url, seedbank FROM merged_urls WHERE status = 'success'")
db_data = {row[0]: {'url': row[1], 'seedbank': row[2]} for row in cursor.fetchall()}
conn.close()

logger.info(f"Loaded {len(db_data)} URLs from database")

# Create metadata files
count = 0
for url_hash, data in db_data.items():
    metadata = {
        'url': data['url'],
        'url_hash': url_hash,
        'seedbank': data['seedbank'],
        'collection_date': '2026-01-14',
        'scrape_method': 'elite_collection',
        'source': 'pipeline06'
    }
    
    s3.put_object(
        Bucket=bucket,
        Key=f'metadata/{url_hash}.json',
        Body=json.dumps(metadata),
        ContentType='application/json'
    )
    
    count += 1
    if count % 100 == 0:
        logger.info(f"Created {count} metadata files...")

logger.info(f"Total metadata files created: {count}")
print(f"\nMETADATA CREATION COMPLETE!")
print(f"Created {count} metadata files for elite seed banks")
