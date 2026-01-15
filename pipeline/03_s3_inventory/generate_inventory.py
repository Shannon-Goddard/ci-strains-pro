#!/usr/bin/env python3
"""
S3 HTML Archive Inventory Generator
Creates complete hash-to-URL mapping from S3 metadata
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def identify_seed_bank(url):
    if pd.isna(url) or not url:
        return 'Unknown'
    url_lower = url.lower()
    if 'amsterdammarijuanaseeds' in url_lower:
        return 'Amsterdam Marijuana Seeds'
    elif 'gorillaseedbank' in url_lower:
        return 'Gorilla Seeds Bank'
    elif 'herbiesheadshop' in url_lower or 'herbies' in url_lower:
        return 'Herbies Seeds'
    elif 'exoticgenetix' in url_lower:
        return 'Exotic Genetix'
    elif 'compoundgenetics' in url_lower:
        return 'Compound Genetics'
    else:
        return 'Other'

def generate_s3_inventory():
    """Generate complete inventory from S3 metadata folder"""
    
    s3_client = boto3.client('s3')
    bucket_name = 'ci-strains-html-archive'
    
    logger.info("Scanning S3 metadata for URL mappings...")
    
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix='metadata/')
    
    inventory_data = []
    processed = 0
    
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['Key'].endswith('.json'):
                    try:
                        response = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])
                        metadata = json.loads(response['Body'].read())
                        
                        url_hash = metadata.get('url_hash')
                        url = metadata.get('url')
                        seed_bank = identify_seed_bank(url)
                        
                        inventory_data.append({
                            'url_hash': url_hash,
                            's3_html_key': f'html/{url_hash}.html',
                            's3_metadata_key': obj['Key'],
                            'url': url,
                            'seed_bank': seed_bank,
                            'collection_date': metadata.get('collection_date'),
                            'scrape_method': metadata.get('scrape_method'),
                            'html_size': metadata.get('html_size'),
                            'validation_score': metadata.get('validation_score')
                        })
                        
                        processed += 1
                        if processed % 1000 == 0:
                            logger.info(f"Processed {processed} metadata files...")
                        
                    except Exception as e:
                        logger.warning(f"Error processing {obj['Key']}: {e}")
                        continue
    
    logger.info(f"Found {len(inventory_data)} HTML files with metadata")
    
    df_final = pd.DataFrame(inventory_data)
    
    output_file = 's3_html_inventory.csv'
    df_final.to_csv(output_file, index=False, encoding='utf-8')
    
    total_size_mb = df_final['html_size'].sum() / (1024**2)
    
    report = f"""# S3 HTML Archive Inventory

**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Inventory Summary

- **Total HTML Files:** {len(df_final)}
- **Total Storage Size:** {total_size_mb:.2f} MB
- **Average File Size:** {df_final['html_size'].mean() / 1024:.1f} KB

## Seed Bank Distribution

{df_final['seed_bank'].value_counts().to_string()}

## Elite Seed Banks (5 banks for extraction)

- **Amsterdam Marijuana Seeds:** {len(df_final[df_final['seed_bank'] == 'Amsterdam Marijuana Seeds'])} strains
- **Gorilla Seeds Bank:** {len(df_final[df_final['seed_bank'] == 'Gorilla Seeds Bank'])} strains
- **Herbies Seeds:** {len(df_final[df_final['seed_bank'] == 'Herbies Seeds'])} strains
- **Exotic Genetix:** {len(df_final[df_final['seed_bank'] == 'Exotic Genetix'])} strains
- **Compound Genetics:** {len(df_final[df_final['seed_bank'] == 'Compound Genetics'])} strains

## Output Files

- **Complete Inventory:** {output_file}
- **Total Records:** {len(df_final)}

---

**This inventory enables extraction of all seed banks with complete URL-to-hash mapping.**

**Logic designed by Amazon Q, verified by Shannon Goddard.**
"""
    
    with open('s3_inventory_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"Inventory saved to: {output_file}")
    logger.info(f"Report saved to: s3_inventory_report.md")
    
    print(f"\nS3 INVENTORY COMPLETE!")
    print(f"Total HTML files: {len(df_final)}")
    print(f"Total size: {total_size_mb:.2f} MB")
    print(f"\nSeed Bank Distribution:")
    print(df_final['seed_bank'].value_counts())
    print(f"\nElite Seed Banks:")
    for bank in ['Amsterdam Marijuana Seeds', 'Gorilla Seeds Bank', 'Herbies Seeds', 'Exotic Genetix', 'Compound Genetics']:
        count = len(df_final[df_final['seed_bank'] == bank])
        print(f"  {bank}: {count} strains")

if __name__ == "__main__":
    generate_s3_inventory()
