#!/usr/bin/env python3
"""
Exotic Genetix Extractor
Minimal extraction pipeline for limited data structure
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExoticExtractor:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.results = []
        
    def extract_strain_name(self, soup):
        """Extract strain name"""
        data = {}
        title = soup.find('h2', class_='product_title')
        if title:
            data['strain_name'] = title.get_text(strip=True)
        return data
    
    def extract_description(self, soup):
        """Extract genetics from description"""
        data = {}
        desc = soup.find('div', class_='woocommerce-product-details__short-description')
        if desc:
            text = desc.get_text()
            
            mother = re.search(r'Mother[:\s]*([^\n]+)', text, re.I)
            if mother:
                data['mother'] = mother.group(1).strip()
            
            reversal = re.search(r'Reversal[:\s]*([^\n]+)', text, re.I)
            if reversal:
                data['reversal'] = reversal.group(1).strip()
            
            sex = re.search(r'Sex[:\s]*([^\n]+)', text, re.I)
            if sex:
                data['sex'] = sex.group(1).strip()
            
            pack = re.search(r'Pack Size[:\s]*([^\n]+)', text, re.I)
            if pack:
                data['pack_size'] = pack.group(1).strip()
        return data
    
    def extract_meta(self, soup):
        """Extract SKU and category"""
        data = {}
        meta = soup.find('div', class_='product_meta')
        if meta:
            sku = meta.find('span', class_='sku')
            if sku:
                data['sku'] = sku.get_text(strip=True)
            
            category = meta.find('span', class_='posted_in')
            if category:
                link = category.find('a')
                if link:
                    data['category'] = link.get_text(strip=True)
        return data
    
    def extract_strain(self, url, html):
        """Minimal extraction"""
        soup = BeautifulSoup(html, 'html.parser')
        
        data = {
            'seed_bank': 'Exotic Genetix',
            'source_url': url
        }
        
        data.update(self.extract_strain_name(soup))
        data.update(self.extract_description(soup))
        data.update(self.extract_meta(soup))
        
        if data.get('mother') and data.get('reversal'):
            data['genetics_lineage'] = f"{data['mother']} x {data['reversal']}"
        
        return data
    
    def process_exotic(self):
        """Process all Exotic strains from S3"""
        logger.info("Loading S3 inventory...")
        
        inv = pd.read_csv('c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/03_s3_inventory/s3_html_inventory.csv')
        exotic = inv[inv['url'].str.contains('exoticgenetix', na=False)]
        logger.info(f"Found {len(exotic)} Exotic strains")
        
        for idx, row in exotic.iterrows():
            try:
                obj = self.s3.get_object(Bucket=self.bucket, Key=f"html/html/{row['url_hash']}.html")
                html = obj['Body'].read().decode('utf-8')
                
                strain = self.extract_strain(row['url'], html)
                self.results.append(strain)
                
                if len(self.results) % 50 == 0:
                    logger.info(f"Processed {len(self.results)}/{len(exotic)}")
                    
            except Exception as e:
                logger.error(f"Error processing {row['url']}: {e}")
                continue
        
        df = pd.DataFrame(self.results)
        df.to_csv('exotic_extracted.csv', index=False, encoding='utf-8')
        
        logger.info(f"Extraction complete: {len(df)} strains, {len(df.columns)} columns")
        return df

if __name__ == "__main__":
    extractor = ExoticExtractor()
    df = extractor.process_exotic()
    
    print(f"\nExotic Genetix Extraction Complete")
    print(f"Strains: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Genetics: {df['genetics_lineage'].notna().sum() if 'genetics_lineage' in df.columns else 0} with lineage")
