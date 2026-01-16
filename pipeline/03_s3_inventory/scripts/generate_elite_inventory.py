#!/usr/bin/env python3
"""
Elite Seed Banks S3 Inventory (pipeline06)
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_elite_inventory():
    """Generate inventory for elite seed banks in pipeline06 folder"""
    
    s3_client = boto3.client('s3')
    bucket_name = 'ci-strains-html-archive'
    
    logger.info("Scanning pipeline06 folder...")
    
    # Get all HTML files from pipeline06
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix='pipeline06/')
    
    html_files = []
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['Key'].endswith('.html'):
                    url_hash = obj['Key'].split('/')[-1].replace('.html', '')
                    html_files.append({
                        'url_hash': url_hash,
                        's3_key': obj['Key'],
                        'size_bytes': obj['Size'],
                        'last_modified': obj['LastModified']
                    })
    
    logger.info(f"Found {len(html_files)} HTML files in pipeline06")
    
    # Try to load database for URL mappings
    db_path = '../../01_html_collection/elite_seedbanks_collection/data/elite_merged_urls.db'
    try:
        conn = sqlite3.connect(db_path)
        df_db = pd.read_sql_query("SELECT url_hash, original_url as url, seedbank FROM merged_urls WHERE status = 'success'", conn)
        conn.close()
        logger.info(f"Loaded {len(df_db)} URLs from database")
        
        # Merge with HTML files
        df_inventory = pd.DataFrame(html_files)
        df_final = df_inventory.merge(df_db, on='url_hash', how='left')
        
    except Exception as e:
        logger.warning(f"Could not load database: {e}")
        df_final = pd.DataFrame(html_files)
        df_final['url'] = None
        df_final['seedbank'] = 'Unknown'
    
    # Save inventory
    output_file = 'elite_s3_inventory.csv'
    df_final.to_csv(output_file, index=False, encoding='utf-8')
    
    # Generate report
    total_size_mb = df_final['size_bytes'].sum() / (1024**2)
    
    seedbank_counts = df_final['seedbank'].value_counts() if 'seedbank' in df_final.columns else {}
    
    report = f"""# Elite Seed Banks S3 Inventory (pipeline06)

**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Inventory Summary

- **Total HTML Files:** {len(df_final)}
- **Total Storage Size:** {total_size_mb:.2f} MB
- **Average File Size:** {df_final['size_bytes'].mean() / 1024:.1f} KB
- **S3 Location:** `ci-strains-html-archive/pipeline06/`

## Seed Bank Distribution

{seedbank_counts.to_string() if len(seedbank_counts) > 0 else 'No seedbank data available'}

## Files

- **Inventory CSV:** {output_file}
- **Total Records:** {len(df_final)}

---

**These are the 5 elite seed banks collected separately:**
- Amsterdam Marijuana Seeds
- Gorilla Seeds Bank
- Herbies Seeds
- Exotic Genetix
- Compound Genetics

**Logic designed by Amazon Q, verified by Shannon Goddard.**
"""
    
    with open('elite_s3_inventory_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"Inventory saved to: {output_file}")
    logger.info(f"Report saved to: elite_s3_inventory_report.md")
    
    print(f"\nELITE S3 INVENTORY COMPLETE!")
    print(f"Total HTML files: {len(df_final)}")
    print(f"Total size: {total_size_mb:.2f} MB")
    if len(seedbank_counts) > 0:
        print(f"\nSeed Bank Distribution:")
        print(seedbank_counts)

if __name__ == "__main__":
    generate_elite_inventory()
