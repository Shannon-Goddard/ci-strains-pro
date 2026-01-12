import boto3
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import time

def extract_attitude_strain_data(html_content):
    """Extract strain data using Attitude's 4-method approach"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Method 1: Title extraction
    title_elem = soup.find('h1') or soup.find('title')
    strain_name = title_elem.get_text().strip() if title_elem else "Unknown"
    
    # Method 2: Genetics extraction
    genetics_text = str(soup)
    sativa_match = re.search(r'(\d+)%\s*Sativa', genetics_text, re.IGNORECASE)
    indica_match = re.search(r'(\d+)%\s*Indica', genetics_text, re.IGNORECASE)
    
    sativa_pct = int(sativa_match.group(1)) if sativa_match else None
    indica_pct = int(indica_match.group(1)) if indica_match else None
    
    # Method 3: THC extraction
    thc_range_match = re.search(r'THC[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%', genetics_text, re.IGNORECASE)
    thc_single_match = re.search(r'THC[:\s]*(\d+(?:\.\d+)?)%', genetics_text, re.IGNORECASE)
    
    if thc_range_match:
        thc_min = float(thc_range_match.group(1))
        thc_max = float(thc_range_match.group(2))
        thc_avg = (thc_min + thc_max) / 2
    elif thc_single_match:
        thc_min = thc_max = thc_avg = float(thc_single_match.group(1))
    else:
        thc_min = thc_max = thc_avg = None
    
    # Method 4: Lineage extraction
    lineage_match = re.search(r'(?:Cross|Genetics|Parents):\s*([^x]+)\s*[xX]\s*([^.]+)', genetics_text, re.IGNORECASE)
    parent1 = lineage_match.group(1).strip() if lineage_match else None
    parent2 = lineage_match.group(2).strip() if lineage_match else None
    
    return {
        'strain_name': strain_name,
        'sativa_percentage': sativa_pct,
        'indica_percentage': indica_pct,
        'thc_min': thc_min,
        'thc_max': thc_max,
        'thc_avg': thc_avg,
        'parent1': parent1,
        'parent2': parent2,
        'seed_bank': 'Attitude Seedbank'
    }

def process_batch(s3_client, metadata_batch, batch_num):
    """Process a batch of strains"""
    print(f"Processing batch {batch_num} ({len(metadata_batch)} strains)...")
    
    batch_data = []
    
    for metadata in metadata_batch:
        try:
            # Get HTML file using url_hash
            html_key = f"html/{metadata['url_hash']}.html"
            html_obj = s3_client.get_object(Bucket='ci-strains-html-archive', Key=html_key)
            html_content = html_obj['Body'].read().decode('utf-8', errors='ignore')
            
            # Extract strain data
            strain_data = extract_attitude_strain_data(html_content)
            strain_data['strain_id'] = metadata.get('strain_ids', [None])[0]  # Get first strain_id
            strain_data['url'] = metadata.get('url', '')
            batch_data.append(strain_data)
            
        except Exception as e:
            print(f"Error processing {metadata.get('url_hash', 'unknown')}: {e}")
            continue
    
    # Save batch CSV
    if batch_data:
        df = pd.DataFrame(batch_data)
        batch_file = f'attitude_strains_batch_{batch_num:03d}.csv'
        df.to_csv(batch_file, index=False, encoding='utf-8')
        print(f"Saved {len(batch_data)} strains to {batch_file}")
    
    return len(batch_data)

def main():
    print("Starting Attitude Seedbank Batch Processor...")
    
    # Initialize S3
    s3_client = boto3.client('s3')
    
    # Get all metadata files with pagination
    print("Loading metadata files...")
    paginator = s3_client.get_paginator('list_objects_v2')
    
    all_metadata = []
    processed_files = 0
    
    # Process all metadata files with pagination
    for page in paginator.paginate(Bucket='ci-strains-html-archive', Prefix='metadata/'):
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            try:
                metadata_obj = s3_client.get_object(Bucket='ci-strains-html-archive', Key=obj['Key'])
                metadata = json.loads(metadata_obj['Body'].read().decode('utf-8'))
                
                # Filter for Attitude Seedbank (cannabis-seeds-bank.co.uk)
                url = metadata.get('url', '')
                if 'cannabis-seeds-bank.co.uk' in url.lower():
                    all_metadata.append(metadata)
                    
            except Exception as e:
                print(f"Error loading {obj['Key']}: {e}")
                continue
            
            processed_files += 1
            if processed_files % 1000 == 0:
                print(f"Processed {processed_files} metadata files, found {len(all_metadata)} Attitude strains...")
    
    print(f"\nFound {len(all_metadata)} total Attitude strain files")
    
    # Process in batches of 50
    batch_size = 50
    total_processed = 0
    
    for i in range(0, len(all_metadata), batch_size):
        batch = all_metadata[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        
        processed_count = process_batch(s3_client, batch, batch_num)
        total_processed += processed_count
        
        print(f"Batch {batch_num} complete. Total processed: {total_processed}")
        time.sleep(1)  # Brief pause between batches
    
    print(f"\nBatch processing complete! Total strains processed: {total_processed}")
    print("Combine batch files with: copy /b attitude_strains_batch_*.csv attitude_strains_complete.csv")

if __name__ == "__main__":
    main()