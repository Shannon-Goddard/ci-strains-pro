#!/usr/bin/env python3
"""
Seedsman S3 Processor - Enhanced 4-Method Extraction from S3 HTML
Processes pre-collected HTML files from S3 using proven Seedsman extraction logic
"""

import pandas as pd
import boto3
import hashlib
import re
from bs4 import BeautifulSoup
from decimal import Decimal
from datetime import datetime

class SeedsmanS3Processor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table('cannabis-strains-universal')
        self.bucket_name = 'ci-strains-html-archive'
        
        # Success tracking
        self.total_processed = 0
        self.successful_extractions = 0
        self.method_stats = {'structured': 0, 'description': 0, 'patterns': 0, 'fallback': 0}

    def url_to_hash(self, url):
        """Convert URL to hash for S3 file lookup"""
        return hashlib.md5(url.encode()).hexdigest()

    def get_html_from_s3(self, url_hash):
        """Retrieve HTML content from S3 with pagination support"""
        try:
            s3_key = f"html/{url_hash}.html"
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            return response['Body'].read().decode('utf-8', errors='ignore')
        except Exception as e:
            return None

    def method1_structured_extraction(self, soup, url):
        """Method 1: Seedsman specifications table extraction"""
        data = {}
        
        table = soup.find('table', id='product-attribute-specs-table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                label_th = row.find('th', class_='col label')
                data_td = row.find('td', class_='col data')
                
                if label_th and data_td:
                    label_h4 = label_th.find('h4')
                    if label_h4:
                        label = label_h4.get_text().strip()
                        
                        spans = data_td.find_all('span')
                        if spans:
                            values = [span.get_text().strip() for span in spans if span.get_text().strip()]
                            value = ' | '.join(values) if len(values) > 1 else values[0] if values else ''
                        else:
                            h3 = data_td.find('h3')
                            value = h3.get_text().strip() if h3 else data_td.get_text().strip()
                        
                        field_map = {
                            'SKU': 'sku',
                            'Brand/breeder': 'brand_breeder',
                            'Parental lines': 'parental_lines',
                            'Variety': 'variety',
                            'THC content': 'thc_content',
                            'CBD content': 'cbd_content',
                            'Yield outdoor': 'yield_outdoor',
                            'Yield indoor': 'yield_indoor',
                            'Photoperiod flowering time': 'photoperiod_flowering_time',
                            'Suitable climates': 'suitable_climates',
                            'Aroma': 'aroma'
                        }
                        
                        if label in field_map and value:
                            data[field_map[label]] = value
        
        return data

    def method2_description_mining(self, soup, url):
        """Method 2: Mine Seedsman product descriptions"""
        data = {}
        
        desc_selectors = [
            'div.ProductActions-ShortDescription',
            'div.ProductPageDescription',
            'div.product-description',
            'div.description'
        ]
        
        about_parts = []
        for selector in desc_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if text and len(text) > 100:
                    about_parts.append(text)
        
        if about_parts:
            full_text = ' '.join(about_parts)
            data['about_info'] = full_text
            
            patterns = {
                'genetics_pattern': r'(?:genetics|lineage|cross|bred from)[:\s]*([^.]+?)(?:\.|$)',
                'effects_pattern': r'(?:effect|high|buzz)[s]?[:\s]*([^.]+?)(?:\.|$)',
                'flavor_pattern': r'(?:flavor|taste|aroma)[s]?[:\s]*([^.]+?)(?:\.|$)'
            }
            
            for key, pattern in patterns.items():
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                if matches:
                    data[key] = '; '.join(matches[:2])
        
        return data

    def method3_advanced_patterns(self, soup, url):
        """Method 3: Seedsman specific patterns"""
        data = {}
        
        data['seed_bank'] = 'Seedsman'
        
        # Extract strain name
        title_selectors = ['h1.page-title', 'h1', '.product-name h1', '.page-title']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                strain_name = title_elem.get_text().strip()
                strain_name = re.sub(r'\s+', ' ', strain_name)
                strain_name = re.sub(r'\s*(Feminized|Auto|Autoflower|Seeds?|Regular)\s*', ' ', strain_name, re.IGNORECASE)
                strain_name = re.sub(r'\s*-\s*Seedsman\s*', '', strain_name, re.IGNORECASE)
                data['strain_name'] = strain_name.strip()
                break
        
        # Extract from URL if not found
        if 'strain_name' not in data:
            path_parts = url.split('/')
            for part in reversed(path_parts):
                if part and len(part) > 5 and 'seedsman' not in part.lower():
                    strain_name = part.replace('-', ' ').title()
                    strain_name = re.sub(r'\s+(Auto|Feminized|Regular|Seeds?)$', '', strain_name, re.IGNORECASE)
                    data['strain_name'] = strain_name.strip()
                    break
        
        # Detect seed type
        url_lower = url.lower()
        page_text = soup.get_text().lower()
        
        if 'autoflower' in url_lower or 'auto' in url_lower:
            data['growth_type'] = 'Autoflower'
            data['seed_type'] = 'Feminized'
        elif 'feminized' in url_lower or 'fem' in url_lower:
            data['seed_type'] = 'Feminized'
            data['growth_type'] = 'Photoperiod'
        elif 'regular' in url_lower:
            data['seed_type'] = 'Regular'
            data['growth_type'] = 'Photoperiod'
        
        return data

    def method4_fallback_extraction(self, soup, url):
        """Method 4: Universal fallback for Seedsman"""
        data = {}
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['about_info'] = meta_desc.get('content', '')
        
        title = soup.find('title')
        if title and not data.get('strain_name'):
            title_text = title.get_text().strip()
            title_parts = title_text.split(' - ')
            if title_parts:
                potential_strain = title_parts[0].strip()
                potential_strain = re.sub(r'\s+(Auto|Feminized|Regular|Seeds?)$', '', potential_strain, re.IGNORECASE)
                data['strain_name'] = potential_strain
        
        return data

    def apply_4_methods(self, html_content, url):
        """Apply all 4 extraction methods"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        strain_data = {
            'seed_bank': 'Seedsman',
            'source_url': url,
            'extraction_methods_used': []
        }
        
        # Apply methods
        for method_name, method_func in [
            ('structured', self.method1_structured_extraction),
            ('description', self.method2_description_mining),
            ('patterns', self.method3_advanced_patterns),
            ('fallback', self.method4_fallback_extraction)
        ]:
            method_data = method_func(soup, url)
            if method_data:
                strain_data.update(method_data)
                strain_data['extraction_methods_used'].append(method_name)
                self.method_stats[method_name] += 1
        
        # Set breeder
        if strain_data.get('brand_breeder') and strain_data['brand_breeder'] != 'Seedsman':
            strain_data['breeder_name'] = strain_data['brand_breeder']
        else:
            strain_data['breeder_name'] = 'Seedsman'
        
        # Quality metrics
        strain_data['data_completeness_score'] = self.calculate_quality_score(strain_data)
        strain_data['quality_tier'] = self.determine_quality_tier(strain_data['data_completeness_score'])
        strain_data['field_count'] = len([v for v in strain_data.values() if v])
        
        # Create strain ID
        strain_name = strain_data.get('strain_name', 'Unknown')
        breeder_name = strain_data.get('breeder_name', 'Seedsman')
        strain_data['strain_id'] = self.create_strain_id(strain_name, breeder_name)
        
        # Timestamps
        now = datetime.utcnow().isoformat() + 'Z'
        strain_data['created_at'] = now
        strain_data['updated_at'] = now
        
        return strain_data

    def calculate_quality_score(self, strain_data):
        """Calculate weighted quality score"""
        field_weights = {
            'strain_name': 10, 'seed_bank': 10, 'brand_breeder': 10,
            'thc_content': 9, 'yield_indoor': 9, 'yield_outdoor': 9,
            'photoperiod_flowering_time': 8, 'suitable_climates': 8,
            'parental_lines': 7, 'aroma': 7, 'about_info': 6,
            'variety': 6, 'breeder_name': 8
        }
        
        total_possible = sum(field_weights.values())
        actual_score = sum(weight for field, weight in field_weights.items() 
                          if strain_data.get(field) and len(str(strain_data[field]).strip()) > 2)
        
        return round((actual_score / total_possible) * 100, 1)

    def determine_quality_tier(self, score):
        if score >= 80: return "Premium"
        elif score >= 60: return "High"
        elif score >= 40: return "Medium"
        elif score >= 20: return "Basic"
        else: return "Minimal"

    def create_strain_id(self, strain_name, breeder_name):
        combined = f"{strain_name}-{breeder_name}-seedsman".lower()
        combined = re.sub(r'[^a-z0-9-]', '', combined.replace(' ', '-'))
        return combined[:50]

    def process_seedsman_urls(self):
        """Main processing function"""
        print("Loading Seedsman URLs from CSV...")
        
        # Load CSV and filter for Seedsman
        df = pd.read_csv('../../pipeline/01_html_collection/data/unique_urls.csv', encoding='latin-1')
        
        seedsman_df = df[df['url'].str.contains('seedsman.com', case=False, na=False)]
        print(f"Found {len(seedsman_df)} Seedsman URLs")
        
        for idx, row in seedsman_df.iterrows():
            self.total_processed += 1
            url = row['url']
            url_hash = row['url_hash']
            
            print(f"\n[{self.total_processed}/{len(seedsman_df)}] Processing: {url}")
            print(f"  Hash: {url_hash}")
            
            html_content = self.get_html_from_s3(url_hash)
            if html_content:
                strain_data = self.apply_4_methods(html_content, url)
                
                if strain_data['data_completeness_score'] >= 20:
                    try:
                        strain_data['data_completeness_score'] = Decimal(str(strain_data['data_completeness_score']))
                        self.table.put_item(Item=strain_data)
                        self.successful_extractions += 1
                        
                        print(f"  SUCCESS: {strain_data.get('strain_name', 'Unknown')} - {strain_data.get('breeder_name', 'Unknown')}")
                        print(f"    Quality: {strain_data['quality_tier']} ({float(strain_data['data_completeness_score']):.1f}%)")
                        print(f"    Methods: {', '.join(strain_data['extraction_methods_used'])}")
                        
                    except Exception as e:
                        print(f"  STORAGE FAILED: {e}")
                else:
                    print(f"  LOW QUALITY: {strain_data['data_completeness_score']:.1f}% - skipped")
        
        self.print_final_stats()

    def print_final_stats(self):
        """Print final statistics"""
        success_rate = (self.successful_extractions / self.total_processed * 100) if self.total_processed > 0 else 0
        
        print(f"\nSEEDSMAN S3 PROCESSING COMPLETE!")
        print(f"Total Processed: {self.total_processed}")
        print(f"Successful: {self.successful_extractions}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"\nMethod Usage:")
        for method, count in self.method_stats.items():
            print(f"  {method.title()}: {count} strains")

def main():
    processor = SeedsmanS3Processor()
    processor.process_seedsman_urls()

if __name__ == "__main__":
    print("SEEDSMAN S3 PROCESSOR")
    print("Processing HTML from S3 archive using 4-method extraction")
    print("=" * 60)
    main()