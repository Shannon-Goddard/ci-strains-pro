#!/usr/bin/env python3
"""
Compound Genetics Extractor
Minimal extraction pipeline for accordion structure
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompoundExtractor:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.results = []
        
    def extract_description(self, soup):
        """Extract description"""
        data = {}
        desc = soup.find('div', class_='collapsible__content')
        if desc:
            data['description'] = desc.get_text(strip=True)
        return data
    
    def extract_agronomic_traits(self, soup):
        """Extract agronomic traits from accordion"""
        data = {}
        accordions = soup.find_all('div', class_='collapsible__content')
        
        for acc in accordions:
            text = acc.get_text()
            
            lineage = re.search(r'Lineage[:\s]*([^\n]+)', text, re.I)
            if lineage:
                data['genetics_lineage'] = lineage.group(1).strip()
            
            potency = re.search(r'Potency[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*%', text, re.I)
            if potency:
                data['thc_min'] = float(potency.group(1))
                data['thc_max'] = float(potency.group(2))
                data['thc_range'] = f"{potency.group(1)}-{potency.group(2)}%"
            
            flower = re.search(r'Flower Time[:\s]*(\d+)\s*-\s*(\d+)\s*Weeks', text, re.I)
            if flower:
                data['flowering_time_min'] = int(flower.group(1))
                data['flowering_time_max'] = int(flower.group(2))
                data['flowering_time'] = f"{flower.group(1)}-{flower.group(2)} weeks"
            
            veg = re.search(r'Vegetative Time[:\s]*([^\n]+)', text, re.I)
            if veg:
                data['vegetative_time'] = veg.group(1).strip()
            
            aroma = re.search(r'Aroma[:\s]*([^\n]+)', text, re.I)
            if aroma:
                data['aroma'] = aroma.group(1).strip()
        
        return data
    
    def extract_strain(self, url, html):
        """Minimal extraction"""
        soup = BeautifulSoup(html, 'html.parser')
        
        data = {
            'seed_bank': 'Compound Genetics',
            'source_url': url
        }
        
        data.update(self.extract_description(soup))
        data.update(self.extract_agronomic_traits(soup))
        
        if not data.get('strain_name'):
            name = url.split('/')[-1].replace('-', ' ').title()
            data['strain_name'] = name
        
        return data
    
    def process_compound(self):
        """Process all Compound strains from S3"""
        logger.info("Loading S3 inventory...")
        
        inv = pd.read_csv('c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/03_s3_inventory/s3_html_inventory.csv')
        compound = inv[inv['url'].str.contains('compound-genetics', na=False)]
        logger.info(f"Found {len(compound)} Compound strains")
        
        for idx, row in compound.iterrows():
            try:
                obj = self.s3.get_object(Bucket=self.bucket, Key=f"html/html/{row['url_hash']}.html")
                html = obj['Body'].read().decode('utf-8')
                
                strain = self.extract_strain(row['url'], html)
                self.results.append(strain)
                
            except Exception as e:
                logger.error(f"Error processing {row['url']}: {e}")
                continue
        
        df = pd.DataFrame(self.results)
        df.to_csv('compound_extracted.csv', index=False, encoding='utf-8')
        
        logger.info(f"Extraction complete: {len(df)} strains, {len(df.columns)} columns")
        return df

if __name__ == "__main__":
    extractor = CompoundExtractor()
    df = extractor.process_compound()
    
    print(f"\nCompound Genetics Extraction Complete")
    print(f"Strains: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"THC: {df['thc_range'].notna().sum() if 'thc_range' in df.columns else 0} with potency data")
