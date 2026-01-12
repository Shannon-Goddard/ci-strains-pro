import boto3
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import time

def extract_seeds_supreme_data(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    data = {
        'seed_bank': 'Seeds Supreme',
        'source_url': url
    }
    
    # Extract strain name
    h1 = soup.find('h1')
    if h1:
        name = h1.get_text().strip()
        name = re.sub(r'\s+(Seeds?|Feminized|Auto)$', '', name, re.IGNORECASE)
        data['strain_name'] = name
    
    # Extract from description
    desc = soup.find('div', class_='product-description') or soup.find('div', class_='description')
    if desc:
        text = desc.get_text()
        data['about_info'] = text.strip()
        
        # Extract key data
        thc_match = re.search(r'THC[:\s]*([0-9.-]+%?)', text, re.IGNORECASE)
        if thc_match:
            data['thc_content'] = thc_match.group(1)
            
        flowering_match = re.search(r'flowering[:\s]*([0-9-]+\s*(?:days?|weeks?))', text, re.IGNORECASE)
        if flowering_match:
            data['flowering_time'] = flowering_match.group(1)
    
    # Fallback strain name from URL
    if 'strain_name' not in data:
        parts = url.split('/')
        for part in reversed(parts):
            if part and len(part) > 3:
                data['strain_name'] = part.replace('-', ' ').title()
                break
    
    return data

def main():
    s3_client = boto3.client('s3')
    paginator = s3_client.get_paginator('list_objects_v2')
    
    all_data = []
    
    for page in paginator.paginate(Bucket='ci-strains-html-archive', Prefix='metadata/'):
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            try:
                metadata_obj = s3_client.get_object(Bucket='ci-strains-html-archive', Key=obj['Key'])
                metadata = json.loads(metadata_obj['Body'].read().decode('utf-8'))
                
                url = metadata.get('url', '')
                if 'seedsupreme.com' in url.lower():
                    html_key = f"html/{metadata['url_hash']}.html"
                    html_obj = s3_client.get_object(Bucket='ci-strains-html-archive', Key=html_key)
                    html_content = html_obj['Body'].read().decode('utf-8', errors='ignore')
                    
                    strain_data = extract_seeds_supreme_data(html_content, url)
                    strain_data['strain_id'] = metadata.get('strain_ids', [None])[0]
                    all_data.append(strain_data)
                    
            except Exception as e:
                continue
    
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('seeds_supreme_complete.csv', index=False, encoding='utf-8')
        print(f"Seeds Supreme: {len(all_data)} strains extracted")
    else:
        print("No Seeds Supreme strains found")

if __name__ == "__main__":
    main()