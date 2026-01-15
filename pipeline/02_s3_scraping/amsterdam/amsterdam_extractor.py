#!/usr/bin/env python3
"""
Amsterdam Marijuana Seeds Extractor
9-method extraction pipeline for ams-attr-table structure
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmsterdamExtractor:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.results = []
        
    def extract_ams_table(self, soup):
        """Extract ams-attr-table data"""
        data = {}
        table = soup.find('div', class_='ams-attr-table')
        if not table:
            return data
            
        for row in table.find_all('div', class_='ams-attr-row'):
            label = row.find('div', class_='ams-attr-label')
            value = row.find('div', class_='ams-attr-value')
            if label and value:
                key = label.get_text(strip=True).lower().replace(' ', '_')
                val = value.get_text(strip=True)
                data[f'ams_{key}'] = val
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
    
    def extract_description(self, soup):
        """Extract product description"""
        data = {}
        desc = soup.find('div', class_='woocommerce-product-details__short-description')
        if desc:
            data['description'] = desc.get_text(strip=True)
        return data
    
    def extract_thc_cbd(self, soup):
        """Extract THC/CBD from text"""
        data = {}
        text = soup.get_text()
        
        # THC patterns
        thc = re.search(r'THC.*?(\d+(?:\.\d+)?)\s*%', text, re.I)
        if thc:
            data['thc_content'] = float(thc.group(1))
            
        thc_range = re.search(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*%', text)
        if thc_range:
            data['thc_min'] = float(thc_range.group(1))
            data['thc_max'] = float(thc_range.group(2))
            
        # CBD patterns
        cbd = re.search(r'CBD.*?(\d+(?:\.\d+)?)\s*%', text, re.I)
        if cbd:
            data['cbd_content'] = float(cbd.group(1))
            
        return data
    
    def extract_genetics(self, soup):
        """Extract genetics/lineage"""
        data = {}
        text = soup.get_text()
        
        # Indica/Sativa ratio
        ratio = re.search(r'(\d+)%\s*/\s*(\d+)%', text)
        if ratio:
            data['indica_percentage'] = int(ratio.group(1))
            data['sativa_percentage'] = int(ratio.group(2))
            
        # Lineage patterns
        lineage = re.search(r'(?:cross|genetics|lineage)[:\s]*([^.]{10,100})', text, re.I)
        if lineage:
            data['genetics_lineage'] = lineage.group(1).strip()
            
        return data
    
    def extract_flowering(self, soup):
        """Extract flowering time"""
        data = {}
        text = soup.get_text()
        
        flower = re.search(r'(\d+)\s*-\s*(\d+)\s*weeks', text, re.I)
        if flower:
            data['flowering_time_min'] = int(flower.group(1))
            data['flowering_time_max'] = int(flower.group(2))
            data['flowering_time'] = f"{flower.group(1)}-{flower.group(2)} weeks"
            
        return data
    
    def extract_yield(self, soup):
        """Extract yield data"""
        data = {}
        text = soup.get_text()
        
        # Indoor yield
        indoor = re.search(r'(\d+)\s*-\s*(\d+)\s*(?:gr|g)(?:/m2|/m²)', text, re.I)
        if indoor:
            data['indoor_yield_min'] = int(indoor.group(1))
            data['indoor_yield_max'] = int(indoor.group(2))
            
        # Outdoor yield
        outdoor = re.search(r'(\d+)\s*-\s*(\d+)\s*(?:gr|g)(?:/plant)', text, re.I)
        if outdoor:
            data['outdoor_yield_min'] = int(outdoor.group(1))
            data['outdoor_yield_max'] = int(outdoor.group(2))
            
        return data
    
    def extract_effects(self, soup):
        """Extract effects"""
        data = {}
        text = soup.get_text().lower()
        
        effects = ['energetic', 'relaxed', 'uplifting', 'euphoric', 'creative', 
                   'happy', 'focused', 'sleepy', 'hungry', 'talkative']
        found = [e for e in effects if e in text]
        if found:
            data['effects_all'] = ', '.join(found)
            data['primary_effect'] = found[0]
            
        return data
    
    def extract_flavors(self, soup):
        """Extract flavor profile"""
        data = {}
        text = soup.get_text().lower()
        
        flavors = ['berries', 'herbs', 'pine', 'citrus', 'lemon', 'sweet', 
                   'earthy', 'diesel', 'fruity', 'spicy']
        found = [f for f in flavors if f in text]
        if found:
            data['flavors_all'] = ', '.join(found)
            data['primary_flavor'] = found[0]
            
        return data
    
    def extract_strain(self, url, html):
        """Full 9-method extraction"""
        soup = BeautifulSoup(html, 'html.parser')
        
        data = {
            'seed_bank': 'Amsterdam Marijuana Seeds',
            'source_url': url
        }
        
        # Apply all 9 methods
        data.update(self.extract_ams_table(soup))
        data.update(self.extract_meta_tags(soup))
        data.update(self.extract_description(soup))
        data.update(self.extract_thc_cbd(soup))
        data.update(self.extract_genetics(soup))
        data.update(self.extract_flowering(soup))
        data.update(self.extract_yield(soup))
        data.update(self.extract_effects(soup))
        data.update(self.extract_flavors(soup))
        
        # Extract strain name from URL
        if not data.get('strain_name'):
            name = url.split('/')[-2].replace('-', ' ').title()
            data['strain_name'] = name
            
        return data
    
    def process_amsterdam(self):
        """Process all Amsterdam strains from S3"""
        logger.info("Loading S3 inventory...")
        
        # Load inventory
        inv = pd.read_csv('c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/03_s3_inventory/s3_html_inventory.csv')
        
        # Filter Amsterdam URLs
        ams = inv[inv['url'].str.contains('amsterdammarijuanaseeds.com', na=False)]
        logger.info(f"Found {len(ams)} Amsterdam strains")
        
        for idx, row in ams.iterrows():
            try:
                # Get HTML from S3
                obj = self.s3.get_object(Bucket=self.bucket, Key=f"html/html/{row['url_hash']}.html")
                html = obj['Body'].read().decode('utf-8')
                
                # Extract data
                strain = self.extract_strain(row['url'], html)
                self.results.append(strain)
                
                if len(self.results) % 50 == 0:
                    logger.info(f"Processed {len(self.results)}/{len(ams)}")
                    
            except Exception as e:
                logger.error(f"Error processing {row['url']}: {e}")
                continue
        
        # Save results
        df = pd.DataFrame(self.results)
        df.to_csv('amsterdam_extracted.csv', index=False, encoding='utf-8')
        
        logger.info(f"Extraction complete: {len(df)} strains, {len(df.columns)} columns")
        return df

if __name__ == "__main__":
    extractor = AmsterdamExtractor()
    df = extractor.process_amsterdam()
    
    print(f"\nAmsterdam Extraction Complete")
    print(f"Strains: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Quality: {df['ams_thc'].notna().sum() if 'ams_thc' in df.columns else 0} with THC data")
