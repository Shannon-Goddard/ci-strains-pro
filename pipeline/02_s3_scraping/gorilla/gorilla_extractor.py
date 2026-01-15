#!/usr/bin/env python3
"""
Gorilla Seed Bank Extractor
9-method extraction pipeline for product-topattributes table
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GorillaExtractor:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.results = []
        
    def extract_topattributes_table(self, soup):
        """Extract product-topattributes table"""
        data = {}
        table = soup.find('table', class_='product-topattributes')
        if table:
            for row in table.find_all('tr'):
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    key = th.get_text(strip=True).lower().replace(' ', '_')
                    val = td.get_text(strip=True)
                    data[f'spec_{key}'] = val
        return data
    
    def extract_product_features(self, soup):
        """Extract product-features list"""
        data = {}
        features = soup.find('div', class_='product-features')
        if features:
            items = [li.get_text(strip=True) for li in features.find_all('li')]
            data['features_all'] = ' | '.join(items)
            for item in items:
                if 'THC' in item:
                    thc = re.search(r'(\d+(?:\.\d+)?)\s*%', item)
                    if thc:
                        data['thc_content'] = float(thc.group(1))
                if 'flowering' in item.lower():
                    data['flowering_time'] = item
        return data
    
    def extract_overview(self, soup):
        """Extract product overview"""
        data = {}
        overview = soup.find('div', class_='product attribute overview')
        if overview:
            val = overview.find('div', class_='value')
            if val:
                data['overview'] = val.get_text(strip=True)
        return data
    
    def extract_description(self, soup):
        """Extract main description"""
        data = {}
        desc = soup.find('div', class_='description-main')
        if desc:
            data['description'] = desc.get_text(strip=True)
        return data
    
    def extract_strain_name(self, soup):
        """Extract strain name and breeder"""
        data = {}
        title = soup.find('h1', class_='page-title')
        if title:
            span = title.find('span', class_='base')
            if span:
                data['strain_name'] = span.get_text(strip=True)
        
        breeder = soup.find('h3', class_='product-manufacturer')
        if breeder:
            link = breeder.find('a')
            if link:
                data['breeder_name'] = link.get_text(strip=True)
        return data
    
    def extract_thc_cbd(self, soup):
        """Extract THC/CBD from text"""
        data = {}
        text = soup.get_text()
        
        thc_range = re.search(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*%', text)
        if thc_range:
            data['thc_min'] = float(thc_range.group(1))
            data['thc_max'] = float(thc_range.group(2))
        
        cbd = re.search(r'CBD.*?(\d+(?:\.\d+)?)\s*%', text, re.I)
        if cbd:
            data['cbd_content'] = float(cbd.group(1))
        return data
    
    def extract_yield(self, soup):
        """Extract yield data"""
        data = {}
        text = soup.get_text()
        
        indoor = re.search(r'(\d+)\s*-\s*(\d+)\s*gr/m2', text)
        if indoor:
            data['indoor_yield_min'] = int(indoor.group(1))
            data['indoor_yield_max'] = int(indoor.group(2))
            data['indoor_yield_range'] = f"{indoor.group(1)}-{indoor.group(2)} gr/m2"
        
        outdoor = re.search(r'(\d+)\s*-\s*(\d+)\s*gr/plant', text)
        if outdoor:
            data['outdoor_yield_min'] = int(outdoor.group(1))
            data['outdoor_yield_max'] = int(outdoor.group(2))
        return data
    
    def extract_effects(self, soup):
        """Extract effects"""
        data = {}
        text = soup.get_text().lower()
        effects = ['relaxing', 'euphoric', 'uplifting', 'energetic', 'creative', 
                   'happy', 'focused', 'sleepy', 'hungry', 'calming']
        found = [e for e in effects if e in text]
        if found:
            data['effects_all'] = ', '.join(found)
            data['primary_effect'] = found[0]
        return data
    
    def extract_flavors(self, soup):
        """Extract flavors"""
        data = {}
        text = soup.get_text().lower()
        flavors = ['cheese', 'earthy', 'sweet', 'citrus', 'pine', 'diesel', 
                   'fruity', 'spicy', 'herbal', 'woody']
        found = [f for f in flavors if f in text]
        if found:
            data['flavors_all'] = ', '.join(found)
            data['primary_flavor'] = found[0]
        return data
    
    def extract_strain(self, url, html):
        """Full 9-method extraction"""
        soup = BeautifulSoup(html, 'html.parser')
        
        data = {
            'seed_bank': 'Gorilla Seed Bank',
            'source_url': url
        }
        
        data.update(self.extract_strain_name(soup))
        data.update(self.extract_topattributes_table(soup))
        data.update(self.extract_product_features(soup))
        data.update(self.extract_overview(soup))
        data.update(self.extract_description(soup))
        data.update(self.extract_thc_cbd(soup))
        data.update(self.extract_yield(soup))
        data.update(self.extract_effects(soup))
        data.update(self.extract_flavors(soup))
        
        return data
    
    def process_gorilla(self):
        """Process all Gorilla strains from S3"""
        logger.info("Loading S3 inventory...")
        
        inv = pd.read_csv('c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/03_s3_inventory/s3_html_inventory.csv')
        gorilla = inv[inv['url'].str.contains('gorilla-cannabis-seeds', na=False)]
        logger.info(f"Found {len(gorilla)} Gorilla strains")
        
        for idx, row in gorilla.iterrows():
            try:
                obj = self.s3.get_object(Bucket=self.bucket, Key=f"html/html/{row['url_hash']}.html")
                html = obj['Body'].read().decode('utf-8')
                
                strain = self.extract_strain(row['url'], html)
                self.results.append(strain)
                
                if len(self.results) % 100 == 0:
                    logger.info(f"Processed {len(self.results)}/{len(gorilla)}")
                    
            except Exception as e:
                logger.error(f"Error processing {row['url']}: {e}")
                continue
        
        df = pd.DataFrame(self.results)
        df.to_csv('gorilla_extracted.csv', index=False, encoding='utf-8')
        
        logger.info(f"Extraction complete: {len(df)} strains, {len(df.columns)} columns")
        return df

if __name__ == "__main__":
    extractor = GorillaExtractor()
    df = extractor.process_gorilla()
    
    print(f"\nGorilla Extraction Complete")
    print(f"Strains: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Quality: {df['thc_content'].notna().sum() if 'thc_content' in df.columns else 0} with THC data")
