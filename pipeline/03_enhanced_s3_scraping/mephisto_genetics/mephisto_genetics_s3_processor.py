#!/usr/bin/env python3
"""
Mephisto Genetics S3 HTML Processor
Legendary autoflower breeder with unique medicinal effects and growth odour data
Target: Premium autoflower genetics with detailed cultivation specifications
"""

import csv
import boto3
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import json

class MephistoGeneticsS3Processor:
    def __init__(self, s3_bucket='ci-strains-html-archive'):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.processed_count = 0
        self.success_count = 0
        self.method_stats = {'structured': 0, 'description': 0, 'patterns': 0, 'fallback': 0}
        
    def get_mephisto_urls(self):
        """Get all Mephisto Genetics URLs from S3 mapping"""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key='index/url_mapping.csv')
            df = pd.read_csv(response['Body'])
        except:
            df = pd.read_csv('../../01_html_collection/data/unique_urls.csv', encoding='latin-1')
        
        mephisto_urls = df[df['url'].str.contains('mephistogenetics', na=False)]
        return mephisto_urls
    
    def get_all_html_files(self):
        """Get all HTML files from S3 with pagination"""
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.bucket, Prefix='html/')
        
        all_files = []
        for page in page_iterator:
            if 'Contents' in page:
                all_files.extend([obj['Key'] for obj in page['Contents']])
        
        return all_files
    
    def method1_structured_extraction(self, soup, url):
        """Method 1: Mephisto's unique field-based structure"""
        data = {}
        
        # Mephisto's dedicated field classes
        field_classes = {
            'cycle-times-field': 'flowering_time',      # "65 to 75 days from sprout"
            'size-field': 'plant_height',               # "40 to 60cm"
            'yield-field': 'yield',                     # "60 to 90 grams"
            'aroma-flavour-field': 'aroma_flavour',     # "Sour coffee to fruity with hints of bubblegum"
            'effect-field': 'effects',                  # "Narcotic, couchlock"
            'medicinal-effect-field': 'medicinal_effect' # "Insomnia, appetite stimulation" - UNIQUE
        }
        
        for class_name, field_name in field_classes.items():
            element = soup.find('div', class_=class_name)
            if element:
                data[field_name] = element.get_text().strip()
        
        # Handle multiple cannabinoids-field uses
        difficulty_fields = soup.find_all('div', class_='cannabinoids-field')
        if len(difficulty_fields) >= 1:
            data['grow_difficulty'] = difficulty_fields[0].get_text().strip()
        if len(difficulty_fields) >= 2:
            data['growth_odour'] = difficulty_fields[1].get_text().strip()  # UNIQUE
        
        return data

    def method2_description_mining(self, soup, url):
        """Method 2: Mine Mephisto's rich tab content"""
        data = {}
        
        # Extract tab content (Project history + Strain growing info)
        project_tab = soup.find('div', {'data-w-tab': 'Project'})
        strain_tab = soup.find('div', {'data-w-tab': 'Strain'})
        
        about_parts = []
        if project_tab:
            project_content = project_tab.find('div', class_='metafield-rich_text_field')
            if project_content:
                about_parts.append(project_content.get_text().strip())
        
        if strain_tab:
            strain_content = strain_tab.find('div', class_='metafield-rich_text_field')
            if strain_content:
                about_parts.append(strain_content.get_text().strip())
        
        if about_parts:
            data['about_info'] = ' '.join(about_parts)
            
            # Mephisto-specific patterns in descriptions
            desc_text = data['about_info']
            patterns = {
                'genetics': r'(?:genetics|lineage|cross)[:\s]*([^.]+?)(?:\.|$)',
                'indica_sativa': r'([0-9]+)%?\s*(?:indica|sativa)',
                'breeding_notes': r'(?:bred|breeding|selection)[:\s]*([^.]+?)(?:\.|$)',
                'awards': r'(?:award|cup|winner|champion)[:\s]*([^.]+?)(?:\.|$)'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, desc_text, re.IGNORECASE)
                if match:
                    data[key] = match.group(1).strip()
        
        return data

    def method3_advanced_patterns(self, soup, url):
        """Method 3: Mephisto-specific advanced patterns"""
        data = {}
        
        # Extract strain name from product title
        h1_tag = soup.find('h1', class_='product-title')
        if not h1_tag:
            h1_tag = soup.find('h1')
        if h1_tag:
            strain_name = h1_tag.get_text().strip()
            # Clean Mephisto naming patterns
            strain_name = re.sub(r'\s+', ' ', strain_name)
            strain_name = re.sub(r'\s*(Auto|Autoflower|F[0-9]+|BX[0-9]+)\s*', ' ', strain_name, re.IGNORECASE)
            data['strain_name'] = strain_name.strip()
        
        # Detect limited editions and special releases
        if 'strain_name' in data:
            strain_lower = data['strain_name'].lower()
            if any(indicator in strain_lower for indicator in ['limited', 'illuminauto', 'artisanal', 'reserva']):
                data['limited_edition'] = True
            if 'bx' in strain_lower or 'f2' in strain_lower or 'f3' in strain_lower:
                data['breeding_generation'] = True
        
        # Extract from Shopify product JSON-LD
        json_ld = soup.find('script', type='application/ld+json')
        if json_ld:
            try:
                product_data = json.loads(json_ld.get_text())
                if 'offers' in product_data:
                    data['price'] = product_data['offers'].get('price')
                    data['availability'] = product_data['offers'].get('availability')
            except:
                pass
        
        return data

    def method4_fallback_extraction(self, soup, url):
        """Method 4: Universal fallback for Mephisto's Shopify structure"""
        data = {}
        
        # Extract strain name from URL if not found
        if 'strain_name' not in data:
            path_parts = url.split('/')
            for part in reversed(path_parts):
                if part and 'products' not in part and len(part) > 3:
                    strain_name = part.replace('-', ' ').title()
                    # Clean common suffixes
                    strain_name = re.sub(r'\s+(Auto|Bx[0-9]+|F[0-9]+)$', '', strain_name, re.IGNORECASE)
                    data['strain_name'] = strain_name.strip()
                    break
        
        # Shopify meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and not data.get('about_info'):
            data['about_info'] = meta_desc.get('content', '')
        
        # Shopify product title
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            if not data.get('strain_name'):
                # Extract strain name from title
                title_parts = title_text.split(' - ')
                if title_parts:
                    potential_strain = title_parts[0].strip()
                    potential_strain = re.sub(r'\s+(Auto|Autoflower)$', '', potential_strain, re.IGNORECASE)
                    data['strain_name'] = potential_strain
        
        # Shopify product form (availability, variants)
        product_form = soup.find('form', {'action': '/cart/add'})
        if product_form:
            # Check for sold out indicators
            sold_out = soup.find(text=re.compile(r'sold out|unavailable', re.IGNORECASE))
            if sold_out:
                data['availability'] = 'SoldOut'
            else:
                data['availability'] = 'InStock'
        
        return data

    def apply_4_methods(self, html_content, url):
        """Apply all 4 extraction methods"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        strain_data = {
            'seed_bank': 'Mephisto Genetics',
            'breeder_name': 'Mephisto Genetics',  # Always the same for ALL strains
            'seed_type': 'Feminized',            # Always feminized autoflowers
            'growth_type': 'Autoflower',         # Always autoflowers
            'source_url': url,
            'extraction_methods_used': [],
            'scraped_at': datetime.utcnow().isoformat()
        }
        
        # Method 1: Structured extraction
        method1_data = self.method1_structured_extraction(soup, url)
        if method1_data:
            strain_data.update(method1_data)
            strain_data['extraction_methods_used'].append('structured')
            self.method_stats['structured'] += 1
        
        # Method 2: Description mining
        method2_data = self.method2_description_mining(soup, url)
        if method2_data:
            strain_data.update(method2_data)
            strain_data['extraction_methods_used'].append('description')
            self.method_stats['description'] += 1
        
        # Method 3: Advanced patterns
        method3_data = self.method3_advanced_patterns(soup, url)
        if method3_data:
            strain_data.update(method3_data)
            strain_data['extraction_methods_used'].append('patterns')
            self.method_stats['patterns'] += 1
        
        # Method 4: Fallback extraction (always runs)
        method4_data = self.method4_fallback_extraction(soup, url)
        if method4_data:
            strain_data.update(method4_data)
            strain_data['extraction_methods_used'].append('fallback')
            self.method_stats['fallback'] += 1
        
        strain_data['data_completeness_score'] = self.calculate_quality_score(strain_data)
        strain_data['quality_tier'] = self.determine_quality_tier(strain_data['data_completeness_score'])
        
        return strain_data

    def calculate_quality_score(self, strain_data):
        """Calculate weighted quality score with Mephisto-optimized weights"""
        field_weights = {
            # Core fields (required)
            'strain_name': 10,
            'breeder_name': 10,  # Always "Mephisto Genetics"
            
            # Mephisto's strengths (high value)
            'flowering_time': 9,      # Precise "65 to 75 days from sprout"
            'plant_height': 8,        # Exact measurements "40 to 60cm"
            'yield': 8,               # Specific yields "60 to 90 grams"
            'medicinal_effect': 8,    # UNIQUE - Medical applications
            'effects': 7,             # Detailed effect descriptions
            
            # Autoflower specific
            'growth_type': 6,         # Always "Autoflower"
            'seed_type': 6,           # Always "Feminized"
            'grow_difficulty': 6,     # Cultivation difficulty ratings
            'growth_odour': 5,        # UNIQUE - Odor intensity ratings
            
            # Breeding documentation
            'genetics': 7,            # Parent strain lineage
            'about_info': 6,          # Project + Strain tab content
            'breeding_generation': 4, # BX, F2, F3 indicators
            'limited_edition': 3,     # Illuminauto, Artisanal releases
            
            # Sensory data
            'aroma_flavour': 6,       # Combined aroma and flavor
            'availability': 3         # Stock status
        }
        
        total_possible = sum(field_weights.values())
        actual_score = 0
        
        for field, weight in field_weights.items():
            if strain_data.get(field) and len(str(strain_data[field]).strip()) > 2:
                actual_score += weight
        
        return round((actual_score / total_possible) * 100, 1)

    def determine_quality_tier(self, score):
        if score >= 80: return "Premium"
        elif score >= 60: return "High"
        elif score >= 40: return "Medium"
        elif score >= 20: return "Basic"
        else: return "Minimal"

    def process_all_mephisto_strains(self):
        """Process all Mephisto Genetics HTML files and create CSV"""
        print("Getting Mephisto Genetics URLs...")
        mephisto_urls = self.get_mephisto_urls()
        print(f"Found {len(mephisto_urls)} Mephisto Genetics URLs")
        
        # Get all available HTML files with pagination
        print("Getting all HTML files from S3...")
        all_html_files = self.get_all_html_files()
        available_hashes = {f.split('/')[-1].replace('.html', '') for f in all_html_files if f.endswith('.html')}
        print(f"Found {len(available_hashes)} HTML files in S3")
        
        all_strains = []
        
        for idx, row in mephisto_urls.iterrows():
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
                strain_data = self.apply_4_methods(html_content, url)
                all_strains.append(strain_data)
                
                print(f"Processed: {strain_data.get('strain_name', 'Unknown')} ({idx+1}/{len(mephisto_urls)})")
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(all_strains)
        output_file = 'mephisto_genetics.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\nExtracted {len(all_strains)} strains to {output_file}")
        print(f"Available HTML files: {len(available_hashes)}")
        print(f"Processed Mephisto URLs: {len(all_strains)}")
        print(f"Method usage: {self.method_stats}")
        print(f"Columns: {list(df.columns)}")
        
        return df

def main():
    processor = MephistoGeneticsS3Processor()
    df = processor.process_all_mephisto_strains()
    
    # Print summary stats
    print(f"\nSUMMARY:")
    print(f"Total strains: {len(df)}")
    if len(df) > 0:
        print(f"Quality distribution: {df['quality_tier'].value_counts().to_dict()}")
        if 'limited_edition' in df.columns:
            limited_count = df['limited_edition'].sum() if 'limited_edition' in df.columns else 0
            print(f"Limited editions: {limited_count}")

if __name__ == "__main__":
    main()