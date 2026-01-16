#!/usr/bin/env python3
"""
ILGM Extractor - JSON-LD Schema Parser
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import re
import json
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ILGMExtractor:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.results = []
        
    def extract_json_ld(self, soup):
        """Extract JSON-LD structured data"""
        data = {}
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                json_data = json.loads(script.string)
                if isinstance(json_data, dict) and json_data.get('@type') == 'Product':
                    data['product_name'] = json_data.get('name')
                    data['product_description'] = json_data.get('description')
                    if 'aggregateRating' in json_data:
                        data['rating'] = json_data['aggregateRating'].get('ratingValue')
                        data['review_count'] = json_data['aggregateRating'].get('reviewCount')
                    if 'manufacturer' in json_data:
                        data['breeder'] = json_data['manufacturer'].get('name')
            except:
                continue
        return data
    
    def extract_meta_tags(self, soup):
        """Extract meta tags"""
        data = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                field = name.replace(':', '_').lower()
                data[f'meta_{field}'] = content
        return data
    
    def extract_thc_cbd(self, soup):
        """Extract THC/CBD from meta description"""
        data = {}
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            desc = meta_desc.get('content', '')
            # Pattern: "18-22% THC"
            thc_range = re.search(r'(\d+)[-–](\d+)%\s*THC', desc, re.I)
            if thc_range:
                data['thc_min'] = float(thc_range.group(1))
                data['thc_max'] = float(thc_range.group(2))
                data['thc_avg'] = (float(thc_range.group(1)) + float(thc_range.group(2))) / 2
            else:
                thc_single = re.search(r'(\d+)%\s*THC', desc, re.I)
                if thc_single:
                    data['thc_percentage'] = float(thc_single.group(1))
        return data
    
    def extract_strain(self, url, html):
        """Full extraction"""
        soup = BeautifulSoup(html, 'html.parser')
        
        data = {
            'seed_bank': 'ILGM',
            'source_url': url
        }
        
        data.update(self.extract_json_ld(soup))
        data.update(self.extract_meta_tags(soup))
        data.update(self.extract_thc_cbd(soup))
        
        # Extract strain name from URL
        if not data.get('strain_name'):
            name = url.split('/')[-1].replace('-seeds', '').replace('-', ' ').title()
            data['strain_name'] = name
            
        return data
    
    def process_ilgm(self):
        """Process all ILGM strains from S3"""
        logger.info("Loading S3 inventory...")
        
        inv = pd.read_csv('c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/03_s3_inventory/s3_html_inventory.csv', encoding='latin-1')
        ilgm = inv[inv['url'].str.contains('ilgm.com', na=False)]
        logger.info(f"Found {len(ilgm)} ILGM strains")
        
        for idx, row in ilgm.iterrows():
            try:
                obj = self.s3.get_object(Bucket=self.bucket, Key=f"html/{row['url_hash']}.html")
                html = obj['Body'].read().decode('utf-8')
                
                strain = self.extract_strain(row['url'], html)
                self.results.append(strain)
                
                if len(self.results) % 25 == 0:
                    logger.info(f"Processed {len(self.results)}/{len(ilgm)}")
                    
            except Exception as e:
                logger.error(f"Error processing {row['url']}: {e}")
                continue
        
        df = pd.DataFrame(self.results)
        df.to_csv('ilgm_extracted.csv', index=False, encoding='utf-8')
        
        logger.info(f"Extraction complete: {len(df)} strains, {len(df.columns)} columns")
        return df

if __name__ == "__main__":
    extractor = ILGMExtractor()
    df = extractor.process_ilgm()
    
    print(f"\nILGM Extraction Complete")
    print(f"Strains: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"THC Coverage: {df['thc_min'].notna().sum() + df['thc_percentage'].notna().sum()}")
