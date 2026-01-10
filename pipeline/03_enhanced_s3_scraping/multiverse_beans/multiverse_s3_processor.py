#!/usr/bin/env python3
"""
Multiverse Beans S3 Processor - Enhanced 4-Method Extraction from S3 HTML
Processes pre-collected HTML files from S3 using proven Multiverse extraction logic
"""

import pandas as pd
import boto3
import hashlib
import re
from bs4 import BeautifulSoup
from decimal import Decimal
from datetime import datetime

class MultiverseS3Processor:
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
        """Retrieve HTML content from S3"""
        try:
            s3_key = f"html/{url_hash}.html"
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            return response['Body'].read().decode('utf-8', errors='ignore')
        except Exception:
            return None

    def method1_structured_extraction(self, soup, url):
        """Method 1: Extract from Multiverse's attribute structure"""
        data = {}
        
        # Multiverse product attributes (.attribute-row structure)
        attributes = soup.find_all('div', class_='attribute-row')
        for attr in attributes:
            label = attr.find('span', class_='attribute-label')
            value = attr.find('span', class_='attribute-value')
            if label and value:
                field_map = {
                    'Flowering Time': 'flowering_time',
                    'Plant Size': 'plant_height',
                    'Yield': 'yield',
                    'THC Content': 'thc_content',
                    'Effects': 'effects',
                    'Flavors': 'flavors',
                    'Genetics': 'genetics',
                    'Breeder': 'breeder_name',
                    'Seed Type': 'seed_type',
                    'Growth Type': 'growth_type'
                }
                label_text = label.get_text().strip().rstrip(':')
                if label_text in field_map:
                    data[field_map[label_text]] = value.get_text().strip()
        
        return data

    def method2_description_mining(self, soup, url):
        """Method 2: Mine product description with autoflower-specific patterns"""
        data = {}
        
        # Find product description
        description = soup.find('div', class_='product-description')
        if not description:
            description = soup.find('div', class_='woocommerce-product-details__short-description')
        if not description:
            description = soup.find('div', id='tab-description')
            
        if description:
            desc_text = description.get_text()
            data['about_info'] = desc_text.strip()
            
            # Autoflower-specific patterns
            patterns = {
                'thc_content': r'THC[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)',
                'cbd_content': r'CBD[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)',
                'flowering_time': r'(?:flowering|flower|harvest|ready)[:\s]*([0-9-]+\s*(?:days?|weeks?))',
                'genetics': r'(?:genetics|cross|lineage)[:\s]*([^.]+?)(?:\.|$)',
                'effects': r'effects?[:\s]*([^.]+?)(?:\.|$)',
                'yield': r'yield[:\s]*([^.]+?)(?:\.|$)'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, desc_text, re.IGNORECASE)
                if match:
                    data[key] = match.group(1).strip()
        
        return data

    def method3_advanced_patterns(self, soup, url):
        """Method 3: Advanced Multiverse-specific patterns"""
        data = {}
        
        data['seed_bank'] = 'Multiverse Beans'
        
        # Extract strain name from product title
        h1_tag = soup.find('h1', class_='product_title')
        if not h1_tag:
            h1_tag = soup.find('h1')
        if h1_tag:
            strain_name = h1_tag.get_text().strip()
            # Clean Multiverse naming patterns
            strain_name = re.sub(r'\s+', ' ', strain_name)
            strain_name = re.sub(r'\s*-\s*(Auto|Fem|Photo|F[0-9]+)\s*', ' ', strain_name, re.IGNORECASE)
            strain_name = re.sub(r'\s*[0-9]+\s*pack.*$', '', strain_name, re.IGNORECASE)
            strain_name = re.sub(r'\s*(Seeds?|Strain)$', '', strain_name, re.IGNORECASE)
            data['strain_name'] = strain_name.strip()
        
        # Extract breeder from product title
        if 'strain_name' in data:
            title_parts = data['strain_name'].split(' - ')
            if len(title_parts) >= 2:
                potential_breeder = title_parts[0].strip()
                # Known Multiverse breeders
                known_breeders = [
                    'Mephisto Genetics', 'Night Owl', 'Cali Connection', 
                    'Ethos Genetics', 'In House Genetics', 'Compound Genetics',
                    'Cannarado Genetics', 'Thug Pug', 'Exotic Genetix'
                ]
                for breeder in known_breeders:
                    if breeder.lower() in potential_breeder.lower():
                        data['breeder_name'] = breeder
                        data['strain_name'] = ' - '.join(title_parts[1:]).strip()
                        break
        
        # Detect autoflower vs photoperiod from URL
        if '/autoflower/' in url or 'auto' in url.lower():
            data['growth_type'] = 'Autoflower'
        elif '/photoperiod/' in url or 'photo' in url.lower():
            data['growth_type'] = 'Photoperiod'
        
        # Extract from WooCommerce product attributes
        woo_attributes = soup.find('table', class_='woocommerce-product-attributes')
        if woo_attributes:
            rows = woo_attributes.find_all('tr')
            for row in rows:
                label_cell = row.find('th')
                value_cell = row.find('td')
                if label_cell and value_cell:
                    label = label_cell.get_text().strip()
                    value = value_cell.get_text().strip()
                    
                    if 'breeder' in label.lower() and not data.get('breeder_name'):
                        data['breeder_name'] = value
                    elif 'genetics' in label.lower():
                        data['genetics'] = value
                    elif 'flowering' in label.lower():
                        data['flowering_time'] = value
        
        return data

    def method4_fallback_extraction(self, soup, url):
        """Method 4: Universal fallback extraction"""
        data = {}
        
        # Extract strain name from URL if not found
        if 'strain_name' not in data:
            path_parts = url.split('/')
            for part in reversed(path_parts):
                if part and 'product' not in part and len(part) > 3:
                    strain_name = part.replace('-', ' ').title()
                    strain_name = re.sub(r'\s+(Seeds?|Feminized|Auto|F[0-9]+|Pack)$', '', strain_name, re.IGNORECASE)
                    data['strain_name'] = strain_name.strip()
                    break
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and not data.get('about_info'):
            data['about_info'] = meta_desc.get('content', '')
        
        # Page title parsing
        title = soup.find('title')
        if title and not data.get('strain_name'):
            title_text = title.get_text().strip()
            title_parts = title_text.split(' - ')
            if title_parts:
                potential_strain = title_parts[0].strip()
                potential_strain = re.sub(r'\s+(Seeds?|Feminized|Auto)$', '', potential_strain, re.IGNORECASE)
                data['strain_name'] = potential_strain
        
        # Default values for Multiverse
        if not data.get('seed_type'):
            data['seed_type'] = 'Feminized'
        
        return data

    def apply_4_methods(self, html_content, url):
        """Apply all 4 extraction methods"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        strain_data = {
            'seed_bank': 'Multiverse Beans',
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
        
        # Set breeder fallback
        if not strain_data.get('breeder_name'):
            strain_data['breeder_name'] = 'Multiverse Beans'
        
        # Quality metrics
        strain_data['data_completeness_score'] = self.calculate_quality_score(strain_data)
        strain_data['quality_tier'] = self.determine_quality_tier(strain_data['data_completeness_score'])
        strain_data['field_count'] = len([v for v in strain_data.values() if v])
        
        # Create strain ID
        strain_name = strain_data.get('strain_name', 'Unknown')
        breeder_name = strain_data.get('breeder_name', 'Multiverse Beans')
        strain_data['strain_id'] = self.create_strain_id(strain_name, breeder_name)
        
        # Timestamps
        now = datetime.utcnow().isoformat() + 'Z'
        strain_data['created_at'] = now
        strain_data['updated_at'] = now
        
        return strain_data

    def calculate_quality_score(self, strain_data):
        """Calculate weighted quality score"""
        field_weights = {
            'strain_name': 10, 'breeder_name': 10, 'seed_bank': 10,
            'genetics': 8, 'flowering_time': 8, 'growth_type': 8,
            'yield': 6, 'plant_height': 6, 'thc_content': 6,
            'effects': 5, 'seed_type': 4, 'about_info': 4,
            'flavors': 4
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
        combined = f"{strain_name}-{breeder_name}-multiverse".lower()
        combined = re.sub(r'[^a-z0-9-]', '', combined.replace(' ', '-'))
        return combined[:50]

    def process_multiverse_urls(self):
        """Main processing function"""
        print("Loading Multiverse URLs from CSV...")
        
        # Load CSV and filter for Multiverse
        df = pd.read_csv('../../pipeline/01_html_collection/data/unique_urls.csv', encoding='latin-1')
        multiverse_df = df[df['url'].str.contains('multiversebeans.com', case=False, na=False)]
        
        print(f"Found {len(multiverse_df)} Multiverse URLs")
        
        for idx, row in multiverse_df.iterrows():
            self.total_processed += 1
            url = row['url']
            url_hash = row['url_hash']
            
            print(f"\n[{self.total_processed}/{len(multiverse_df)}] Processing: {url}")
            
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
                        
                    except Exception as e:
                        print(f"  STORAGE FAILED: {e}")
                else:
                    print(f"  LOW QUALITY: {strain_data['data_completeness_score']:.1f}% - skipped")
            else:
                print(f"  HTML NOT FOUND")
        
        self.print_final_stats()

    def print_final_stats(self):
        """Print final statistics"""
        success_rate = (self.successful_extractions / self.total_processed * 100) if self.total_processed > 0 else 0
        
        print(f"\nMULTIVERSE BEANS S3 PROCESSING COMPLETE!")
        print(f"Total Processed: {self.total_processed}")
        print(f"Successful: {self.successful_extractions}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"\nMethod Usage:")
        for method, count in self.method_stats.items():
            print(f"  {method.title()}: {count} strains")

def main():
    processor = MultiverseS3Processor()
    processor.process_multiverse_urls()

if __name__ == "__main__":
    print("MULTIVERSE BEANS S3 PROCESSOR")
    print("Processing HTML from S3 archive using 4-method extraction")
    print("=" * 60)
    main()