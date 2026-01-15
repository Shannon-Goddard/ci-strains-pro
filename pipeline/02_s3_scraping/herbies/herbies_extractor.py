#!/usr/bin/env python3
"""
Herbies Seeds Extractor
9-method extraction pipeline for properties-list table
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HerbiesExtractor:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.results = []
        
    def extract_properties_table(self, soup):
        """Extract properties-list table"""
        data = {}
        table = soup.find('table', class_='properties-list')
        if table:
            for row in table.find_all('tr', class_='properties-list__item'):
                name_td = row.find('td', class_='properties-list__name')
                value_td = row.find('td', class_='value') or row.find_all('td')[1] if len(row.find_all('td')) > 1 else None
                
                if name_td and value_td:
                    key = name_td.get_text(strip=True).lower().replace(' ', '_').replace('%', 'pct').replace('/', '_')
                    val = value_td.get_text(strip=True)
                    data[f'herb_{key}'] = val
        return data
    
    def extract_thc_cbd(self, soup):
        """Extract THC/CBD from properties"""
        data = {}
        text = soup.get_text()
        
        thc = re.search(r'THC.*?(\d+(?:\.\d+)?)\s*%', text, re.I)
        if thc:
            data['thc_content'] = float(thc.group(1))
        
        cbd = re.search(r'CBD.*?(\d+(?:\.\d+)?)\s*%', text, re.I)
        if cbd:
            data['cbd_content'] = float(cbd.group(1))
        return data
    
    def extract_yield(self, soup):
        """Extract yield data"""
        data = {}
        text = soup.get_text()
        
        indoor = re.search(r'(\d+(?:\.\d+)?)\s*oz/ft', text)
        if indoor:
            data['indoor_yield_oz_ft2'] = float(indoor.group(1))
        
        outdoor = re.search(r'(\d+(?:\.\d+)?)\s*oz/plant', text)
        if outdoor:
            data['outdoor_yield_oz_plant'] = float(outdoor.group(1))
        return data
    
    def extract_flowering(self, soup):
        """Extract flowering time"""
        data = {}
        text = soup.get_text()
        
        flower = re.search(r'(\d+)\s*-\s*(\d+)\s*days', text)
        if flower:
            data['flowering_time_min'] = int(flower.group(1))
            data['flowering_time_max'] = int(flower.group(2))
            data['flowering_time'] = f"{flower.group(1)}-{flower.group(2)} days"
        return data
    
    def extract_height(self, soup):
        """Extract height data"""
        data = {}
        text = soup.get_text()
        
        indoor_h = re.search(r'(\d+(?:\.\d+)?)\s*inches indoors', text)
        if indoor_h:
            data['indoor_height_inches'] = float(indoor_h.group(1))
        
        outdoor_h = re.search(r'(\d+(?:\.\d+)?)\s*inches outdoors', text)
        if outdoor_h:
            data['outdoor_height_inches'] = float(outdoor_h.group(1))
        return data
    
    def extract_genetics(self, soup):
        """Extract genetics"""
        data = {}
        text = soup.get_text()
        
        genetics = re.search(r'Genetics[:\s]*([^\n]{10,100})', text, re.I)
        if genetics:
            data['genetics_lineage'] = genetics.group(1).strip()
        
        ratio = re.search(r'(\d+)%\s*Sativa.*?(\d+)%\s*Indica', text, re.I)
        if ratio:
            data['sativa_percentage'] = int(ratio.group(1))
            data['indica_percentage'] = int(ratio.group(2))
        return data
    
    def extract_effects(self, soup):
        """Extract effects"""
        data = {}
        text = soup.get_text().lower()
        effects = ['happy', 'relaxed', 'euphoric', 'uplifting', 'creative', 
                   'energetic', 'focused', 'sleepy', 'hungry', 'calming']
        found = [e for e in effects if e in text]
        if found:
            data['effects_all'] = ', '.join(found)
            data['primary_effect'] = found[0]
        return data
    
    def extract_flavors(self, soup):
        """Extract flavors"""
        data = {}
        text = soup.get_text().lower()
        flavors = ['berry', 'sweet', 'earthy', 'citrus', 'pine', 'diesel', 
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
            'seed_bank': 'Herbies Seeds',
            'source_url': url
        }
        
        data.update(self.extract_properties_table(soup))
        data.update(self.extract_thc_cbd(soup))
        data.update(self.extract_yield(soup))
        data.update(self.extract_flowering(soup))
        data.update(self.extract_height(soup))
        data.update(self.extract_genetics(soup))
        data.update(self.extract_effects(soup))
        data.update(self.extract_flavors(soup))
        
        if not data.get('strain_name'):
            name = url.split('/')[-1].replace('-', ' ').title()
            data['strain_name'] = name
        
        return data
    
    def process_herbies(self):
        """Process all Herbies strains from S3"""
        logger.info("Loading S3 inventory...")
        
        inv = pd.read_csv('c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/03_s3_inventory/s3_html_inventory.csv')
        herbies = inv[inv['url'].str.contains('herbiesheadshop', na=False)]
        logger.info(f"Found {len(herbies)} Herbies strains")
        
        for idx, row in herbies.iterrows():
            try:
                obj = self.s3.get_object(Bucket=self.bucket, Key=f"html/html/{row['url_hash']}.html")
                html = obj['Body'].read().decode('utf-8')
                
                strain = self.extract_strain(row['url'], html)
                self.results.append(strain)
                
                if len(self.results) % 100 == 0:
                    logger.info(f"Processed {len(self.results)}/{len(herbies)}")
                    
            except Exception as e:
                logger.error(f"Error processing {row['url']}: {e}")
                continue
        
        df = pd.DataFrame(self.results)
        df.to_csv('herbies_extracted.csv', index=False, encoding='utf-8')
        
        logger.info(f"Extraction complete: {len(df)} strains, {len(df.columns)} columns")
        return df

if __name__ == "__main__":
    extractor = HerbiesExtractor()
    df = extractor.process_herbies()
    
    print(f"\nHerbies Extraction Complete")
    print(f"Strains: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Quality: {df['thc_content'].notna().sum() if 'thc_content' in df.columns else 0} with THC data")
