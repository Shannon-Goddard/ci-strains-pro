import boto3
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import time

def extract_mephisto_strain_data(html_content, url):
    """Extract strain data using Mephisto-specific patterns"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    strain_data = {
        'seed_bank': 'Mephisto Genetics',
        'source_url': url,
        'growth_type': 'Autoflower',  # Mephisto specializes in autoflowers
        'seed_type': 'Feminized'
    }
    
    # Method 1: Product title extraction
    h1_tag = soup.find('h1', class_='product-title')
    if not h1_tag:
        h1_tag = soup.find('h1')
    if h1_tag:
        strain_name = h1_tag.get_text().strip()
        # Clean Mephisto naming patterns
        strain_name = re.sub(r'\s*-\s*(Auto|Autoflower|Seeds?)\s*', ' ', strain_name, re.IGNORECASE)
        strain_name = re.sub(r'\s*[0-9]+\s*pack.*$', '', strain_name, re.IGNORECASE)
        strain_data['strain_name'] = strain_name.strip()
    
    # Method 2: Product description mining
    description = soup.find('div', class_='product-description')
    if not description:
        description = soup.find('div', class_='rte')
    if not description:
        description = soup.find('div', class_='product-single__description')
        
    if description:
        desc_text = description.get_text()
        strain_data['about_info'] = desc_text.strip()
        
        # Mephisto-specific patterns
        patterns = {
            'flowering_time': r'(?:flowering|harvest|ready|cycle)[:\s]*([0-9-]+\s*(?:days?|weeks?))',
            'thc_content': r'THC[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)',
            'cbd_content': r'CBD[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)',
            'genetics': r'(?:genetics|cross|lineage|parents?)[:\s]*([^.]+?)(?:\.|$)',
            'effects': r'effects?[:\s]*([^.]+?)(?:\.|$)',
            'yield': r'yield[:\s]*([^.]+?)(?:\.|$)',
            'height': r'(?:height|size)[:\s]*([^.]+?)(?:\.|$)',
            'terpenes': r'terpenes?[:\s]*([^.]+?)(?:\.|$)',
            'flavors': r'(?:flavors?|taste|aroma)[:\s]*([^.]+?)(?:\.|$)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, desc_text, re.IGNORECASE)
            if match:
                strain_data[key] = match.group(1).strip()
    
    # Method 3: Shopify product attributes
    product_form = soup.find('form', class_='product-form')
    if product_form:
        # Look for variant selectors or product options
        selectors = product_form.find_all('select')
        for select in selectors:
            if 'pack' in select.get('name', '').lower():
                options = select.find_all('option')
                if options:
                    # Extract pack sizes available
                    pack_sizes = [opt.get_text().strip() for opt in options if opt.get_text().strip()]
                    if pack_sizes:
                        strain_data['pack_sizes'] = ', '.join(pack_sizes)
    
    # Method 4: Meta and structured data
    # Extract from JSON-LD structured data (common on Shopify)
    json_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                if data.get('@type') == 'Product':
                    if 'name' in data and 'strain_name' not in strain_data:
                        strain_data['strain_name'] = data['name']
                    if 'description' in data and 'about_info' not in strain_data:
                        strain_data['about_info'] = data['description']
                    if 'brand' in data and isinstance(data['brand'], dict):
                        strain_data['breeder_name'] = data['brand'].get('name', 'Mephisto Genetics')
        except:
            continue
    
    # Fallback strain name extraction from URL
    if 'strain_name' not in strain_data:
        path_parts = url.split('/')
        for part in reversed(path_parts):
            if part and 'products' not in part and len(part) > 3:
                strain_name = part.replace('-', ' ').title()
                strain_name = re.sub(r'\s+(Seeds?|Auto|Autoflower)$', '', strain_name, re.IGNORECASE)
                strain_data['strain_name'] = strain_name.strip()
                break
    
    # Default breeder
    if 'breeder_name' not in strain_data:
        strain_data['breeder_name'] = 'Mephisto Genetics'
    
    # Extract generation info (F1, F2, etc.) from strain name
    if 'strain_name' in strain_data:
        generation_match = re.search(r'\b(F[0-9]+)\b', strain_data['strain_name'], re.IGNORECASE)
        if generation_match:
            strain_data['generation'] = generation_match.group(1).upper()
    
    return strain_data

def process_batch(s3_client, metadata_batch, batch_num):
    """Process a batch of Mephisto strains"""
    print(f"Processing batch {batch_num} ({len(metadata_batch)} strains)...")
    
    batch_data = []
    
    for metadata in metadata_batch:
        try:
            # Get HTML file using url_hash
            html_key = f"html/{metadata['url_hash']}.html"
            html_obj = s3_client.get_object(Bucket='ci-strains-html-archive', Key=html_key)
            html_content = html_obj['Body'].read().decode('utf-8', errors='ignore')
            
            # Extract strain data
            strain_data = extract_mephisto_strain_data(html_content, metadata.get('url', ''))
            strain_data['strain_id'] = metadata.get('strain_ids', [None])[0]
            strain_data['url'] = metadata.get('url', '')
            batch_data.append(strain_data)
            
        except Exception as e:
            print(f"Error processing {metadata.get('url_hash', 'unknown')}: {e}")
            continue
    
    # Save batch CSV
    if batch_data:
        df = pd.DataFrame(batch_data)
        batch_file = f'mephisto_strains_batch_{batch_num:03d}.csv'
        df.to_csv(batch_file, index=False, encoding='utf-8')
        print(f"Saved {len(batch_data)} strains to {batch_file}")
    
    return len(batch_data)

def main():
    print("Starting Mephisto Genetics S3 Batch Processor...")
    
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
                
                # Filter for Mephisto Genetics
                url = metadata.get('url', '')
                if 'mephistogenetics.com' in url.lower():
                    all_metadata.append(metadata)
                    
            except Exception as e:
                print(f"Error loading {obj['Key']}: {e}")
                continue
            
            processed_files += 1
            if processed_files % 1000 == 0:
                print(f"Processed {processed_files} metadata files, found {len(all_metadata)} Mephisto strains...")
    
    print(f"\nFound {len(all_metadata)} total Mephisto strain files")
    
    # Process in batches of 25 (smaller batches for premium strains)
    batch_size = 25
    total_processed = 0
    
    for i in range(0, len(all_metadata), batch_size):
        batch = all_metadata[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        
        processed_count = process_batch(s3_client, batch, batch_num)
        total_processed += processed_count
        
        print(f"Batch {batch_num} complete. Total processed: {total_processed}")
        time.sleep(1)
    
    print(f"\nBatch processing complete! Total strains processed: {total_processed}")
    print("Combine batch files with: copy /b mephisto_strains_batch_*.csv mephisto_strains_complete.csv")

if __name__ == "__main__":
    main()