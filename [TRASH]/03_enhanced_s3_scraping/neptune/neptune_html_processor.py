#!/usr/bin/env python3
"""
Neptune Seed Bank HTML Processor
Processes stored HTML files from S3 to extract strain data into CSV
"""

import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json

class NeptuneHTMLProcessor:
    def __init__(self, s3_bucket='ci-strains-html-archive'):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        
    def get_neptune_urls(self):
        """Get all Neptune URLs from S3 mapping"""
        try:
            # Try S3 first
            response = self.s3.get_object(Bucket=self.bucket, Key='index/url_mapping.csv')
            df = pd.read_csv(response['Body'])
        except:
            # Fallback to local file
            df = pd.read_csv('../06_html_collection/data/unique_urls.csv', encoding='latin-1')
        
        neptune_urls = df[df['url'].str.contains('neptuneseedbank.com', na=False)]
        return neptune_urls
    
    def get_all_html_files(self):
        """Get all HTML files from S3 with pagination"""
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.bucket, Prefix='html/')
        
        all_files = []
        for page in page_iterator:
            if 'Contents' in page:
                all_files.extend([obj['Key'] for obj in page['Contents']])
        
        return all_files
    
    def extract_strain_data(self, html_content, url):
        """Extract strain data using 4-method approach"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        data = {
            'source_url': url,
            'seed_bank': 'Neptune Seed Bank',
            'scraped_at': datetime.utcnow().isoformat()
        }
        
        # Method 1: Structured WooCommerce table
        table = soup.find('table', class_='woocommerce-product-attributes')
        if table:
            for row in table.find_all('tr', class_='woocommerce-product-attributes-item'):
                label = row.find('th', class_='woocommerce-product-attributes-item__label')
                value = row.find('td', class_='woocommerce-product-attributes-item__value')
                
                if label and value:
                    label_text = label.get_text().strip()
                    value_p = value.find('p')
                    if value_p and value_p.get_text().strip() != '#REF!':
                        value_text = value_p.get_text().strip()
                        
                        field_map = {
                            'Yield': 'yield',
                            'Harvest Time': 'flowering_time', 
                            'Cannabis Type': 'strain_type',
                            'Feelings': 'feelings',
                            'Grow Difficulty': 'grow_difficulty',
                            'Height': 'plant_height',
                            'Flowering Type': 'seed_type'
                        }
                        
                        if label_text in field_map:
                            data[field_map[label_text]] = value_text
        
        # Method 2: Extract strain name from H1
        h1_tag = soup.find('h1')
        if h1_tag:
            strain_name = h1_tag.get_text().strip()
            strain_name = re.sub(r'\s+', ' ', strain_name)
            data['strain_name'] = strain_name
        
        # Method 3: Extract breeder
        breeder_link = soup.find('a', class_='breeder-link')
        if breeder_link:
            data['breeder_name'] = breeder_link.get_text().strip()
        
        # Method 4: Description mining
        description = soup.find('div', id='description')
        if description:
            desc_text = description.get_text()
            data['description'] = desc_text.strip()
            
            # Extract THC/CBD with regex
            thc_match = re.search(r'THC[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)', desc_text, re.IGNORECASE)
            if thc_match:
                data['thc_content'] = thc_match.group(1).strip()
                
            cbd_match = re.search(r'CBD[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)', desc_text, re.IGNORECASE)
            if cbd_match:
                data['cbd_content'] = cbd_match.group(1).strip()
        
        return data
    
    def process_all_neptune_strains(self):
        """Process all Neptune HTML files and create CSV"""
        print("Getting Neptune URLs...")
        neptune_urls = self.get_neptune_urls()
        print(f"Found {len(neptune_urls)} Neptune URLs")
        
        # Get all available HTML files with pagination
        print("Getting all HTML files from S3...")
        all_html_files = self.get_all_html_files()
        available_hashes = {f.split('/')[-1].replace('.html', '') for f in all_html_files if f.endswith('.html')}
        print(f"Found {len(available_hashes)} HTML files in S3")
        
        all_strains = []
        
        for idx, row in neptune_urls.iterrows():
            url_hash = row['url_hash']
            url = row['url']
            
            # Check if HTML file exists
            if url_hash not in available_hashes:
                print(f"HTML not found for {url_hash}")
                continue
            
            try:
                # Get HTML from S3
                html_key = f'html/{url_hash}.html'
                response = self.s3.get_object(Bucket=self.bucket, Key=html_key)
                html_content = response['Body'].read().decode('utf-8')
                
                # Extract strain data
                strain_data = self.extract_strain_data(html_content, url)
                all_strains.append(strain_data)
                
                print(f"Processed: {strain_data.get('strain_name', 'Unknown')} ({idx+1}/{len(neptune_urls)})")
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(all_strains)
        output_file = 'neptune.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\nExtracted {len(all_strains)} strains to {output_file}")
        print(f"Available HTML files: {len(available_hashes)}")
        print(f"Processed Neptune URLs: {len(all_strains)}")
        print(f"Columns: {list(df.columns)}")
        
        return df

def main():
    processor = NeptuneHTMLProcessor()
    df = processor.process_all_neptune_strains()
    
    # Print summary stats
    print(f"\nSUMMARY:")
    print(f"Total strains: {len(df)}")
    print(f"Unique breeders: {df['breeder_name'].nunique()}")
    print(f"Strain types: {df['strain_type'].value_counts().to_dict()}")

if __name__ == "__main__":
    main()