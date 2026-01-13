import boto3
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import time

def extract_north_atlantic_strain_data(html_content, url):
    """Extract strain data using North Atlantic's proven 4-method approach"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    strain_data = {
        'seed_bank': 'North Atlantic Seed Co',
        'source_url': url
    }
    
    # Method 1: Structured extraction from product details
    product_details = soup.find('div', class_='product-details')
    if product_details:
        details_text = product_details.get_text()
        
        # Extract key fields with patterns
        patterns = {
            'flowering_time': r'flowering[:\s]*([0-9-]+\s*(?:days?|weeks?))',
            'thc_content': r'THC[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)',
            'cbd_content': r'CBD[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)',
            'yield': r'yield[:\s]*([^.]+?)(?:\.|$)',
            'genetics': r'(?:genetics|lineage|cross)[:\s]*([^.]+?)(?:\.|$)',
            'effects': r'effects?[:\s]*([^.]+?)(?:\.|$)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, details_text, re.IGNORECASE)
            if match:
                strain_data[key] = match.group(1).strip()
    
    # Method 2: Product title and meta extraction
    h1_tag = soup.find('h1', class_='product_title')
    if not h1_tag:
        h1_tag = soup.find('h1')
    if h1_tag:
        strain_name = h1_tag.get_text().strip()
        # Clean North Atlantic naming patterns
        strain_name = re.sub(r'\s*-\s*(Feminized|Auto|Photo|F[0-9]+)\s*', ' ', strain_name, re.IGNORECASE)
        strain_name = re.sub(r'\s*[0-9]+\s*pack.*$', '', strain_name, re.IGNORECASE)
        strain_name = re.sub(r'\s*(Seeds?|Strain)$', '', strain_name, re.IGNORECASE)
        strain_data['strain_name'] = strain_name.strip()
    
    # Method 3: WooCommerce attributes and tabs
    woo_attributes = soup.find('table', class_='woocommerce-product-attributes')
    if woo_attributes:
        rows = woo_attributes.find_all('tr')
        for row in rows:
            label_cell = row.find('th')
            value_cell = row.find('td')
            if label_cell and value_cell:
                label = label_cell.get_text().strip()
                value = value_cell.get_text().strip()
                
                field_map = {
                    'breeder': 'breeder_name',
                    'genetics': 'genetics',
                    'flowering time': 'flowering_time',
                    'thc': 'thc_content',
                    'cbd': 'cbd_content',
                    'yield': 'yield',
                    'height': 'plant_height',
                    'seed type': 'seed_type',
                    'effects': 'effects'
                }
                
                for key_word, field_name in field_map.items():
                    if key_word in label.lower() and field_name not in strain_data:
                        strain_data[field_name] = value
    
    # Extract from description tab
    description_tab = soup.find('div', id='tab-description')
    if description_tab:
        desc_text = description_tab.get_text()
        strain_data['about_info'] = desc_text.strip()
        
        # Additional pattern extraction from description
        if 'genetics' not in strain_data:
            genetics_match = re.search(r'(?:genetics|cross|lineage)[:\s]*([^.]+?)(?:\.|$)', desc_text, re.IGNORECASE)
            if genetics_match:
                strain_data['genetics'] = genetics_match.group(1).strip()
    
    # Method 4: Fallback extraction
    if 'strain_name' not in strain_data:
        # Extract from URL
        path_parts = url.split('/')
        for part in reversed(path_parts):
            if part and 'product' not in part and len(part) > 3:
                strain_name = part.replace('-', ' ').title()
                strain_name = re.sub(r'\s+(Seeds?|Feminized|Auto|F[0-9]+)$', '', strain_name, re.IGNORECASE)
                strain_data['strain_name'] = strain_name.strip()
                break
    
    # Extract breeder from strain name if not found
    if 'breeder_name' not in strain_data and 'strain_name' in strain_data:
        strain_name = strain_data['strain_name']
        # Check for breeder patterns in strain name
        known_breeders = [
            'Ethos Genetics', 'In House Genetics', 'Compound Genetics',
            'Cannarado Genetics', 'Exotic Genetix', 'Symbiotic Genetics',
            'Clearwater Genetics', 'Thug Pug', 'Jungle Boys'
        ]
        for breeder in known_breeders:
            if breeder.lower() in strain_name.lower():
                strain_data['breeder_name'] = breeder
                # Clean strain name
                strain_data['strain_name'] = strain_name.replace(breeder, '').strip()
                break
    
    # Default seed type for North Atlantic
    if 'seed_type' not in strain_data:
        strain_data['seed_type'] = 'Feminized'
    
    return strain_data

def process_batch(s3_client, metadata_batch, batch_num):
    """Process a batch of North Atlantic strains"""
    print(f"Processing batch {batch_num} ({len(metadata_batch)} strains)...")
    
    batch_data = []
    
    for metadata in metadata_batch:
        try:
            # Get HTML file using url_hash
            html_key = f"html/{metadata['url_hash']}.html"
            html_obj = s3_client.get_object(Bucket='ci-strains-html-archive', Key=html_key)
            html_content = html_obj['Body'].read().decode('utf-8', errors='ignore')
            
            # Extract strain data
            strain_data = extract_north_atlantic_strain_data(html_content, metadata.get('url', ''))
            strain_data['strain_id'] = metadata.get('strain_ids', [None])[0]
            strain_data['url'] = metadata.get('url', '')
            batch_data.append(strain_data)
            
        except Exception as e:
            print(f"Error processing {metadata.get('url_hash', 'unknown')}: {e}")
            continue
    
    # Save batch CSV
    if batch_data:
        df = pd.DataFrame(batch_data)
        batch_file = f'north_atlantic_strains_batch_{batch_num:03d}.csv'
        df.to_csv(batch_file, index=False, encoding='utf-8')
        print(f"Saved {len(batch_data)} strains to {batch_file}")
    
    return len(batch_data)

def main():
    print("Starting North Atlantic Seed Co S3 Batch Processor...")
    
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
                
                # Filter for North Atlantic Seed Co
                url = metadata.get('url', '')
                if 'northatlanticseed.com' in url.lower():
                    all_metadata.append(metadata)
                    
            except Exception as e:
                print(f"Error loading {obj['Key']}: {e}")
                continue
            
            processed_files += 1
            if processed_files % 1000 == 0:
                print(f"Processed {processed_files} metadata files, found {len(all_metadata)} North Atlantic strains...")
    
    print(f"\nFound {len(all_metadata)} total North Atlantic strain files")
    
    # Process in batches of 50
    batch_size = 50
    total_processed = 0
    
    for i in range(0, len(all_metadata), batch_size):
        batch = all_metadata[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        
        processed_count = process_batch(s3_client, batch, batch_num)
        total_processed += processed_count
        
        print(f"Batch {batch_num} complete. Total processed: {total_processed}")
        time.sleep(1)
    
    print(f"\nBatch processing complete! Total strains processed: {total_processed}")
    print("Combine batch files with: copy /b north_atlantic_strains_batch_*.csv north_atlantic_strains_complete.csv")

if __name__ == "__main__":
    main()