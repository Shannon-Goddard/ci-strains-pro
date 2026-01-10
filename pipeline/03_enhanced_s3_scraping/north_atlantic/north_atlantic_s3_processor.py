#!/usr/bin/env python3
"""
North Atlantic Seed Company S3 HTML Processor
Based on Neptune's successful pattern with 4-method extraction system
Target: 2,876 URLs with 97%+ success rate
"""

import csv
import boto3
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

class NorthAtlanticS3Processor:
    def __init__(self, s3_bucket='ci-strains-html-archive'):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.processed_count = 0
        self.success_count = 0
        self.method_stats = {'structured': 0, 'description': 0, 'patterns': 0, 'fallback': 0}
        
    def get_north_atlantic_urls(self):
        """Get all North Atlantic URLs from S3 mapping"""
        try:
            # Try S3 first
            response = self.s3.get_object(Bucket=self.bucket, Key='index/url_mapping.csv')
            df = pd.read_csv(response['Body'])
        except:
            # Fallback to local file
            df = pd.read_csv('../01_html_collection/data/unique_urls.csv', encoding='latin-1')
        
        north_atlantic_urls = df[df['url'].str.contains('northatlanticseed.com', na=False)]
        return north_atlantic_urls
    
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
        """Method 1: Extract from North Atlantic's specifications table"""
        data = {}
        
        spec_items = soup.find_all('div', class_='spec-item')
        for item in spec_items:
            label = item.find('dt', class_='spec-label')
            value = item.find('dd', class_='spec-value')
            if label and value:
                field_map = {
                    'Seed Type': 'seed_type',
                    'Growth Type': 'growth_type', 
                    'Strain Type': 'strain_type',
                    'Genetics': 'genetics',
                    'Cannabis Type': 'cannabis_type',
                    'Indica / Sativa / CBD': 'indica_sativa_cbd',
                    'Flowering Time': 'flowering_time',
                    'Height': 'plant_height',
                    'Yield': 'yield',
                    'Terpene Profile': 'terpene_profile'
                }
                label_text = label.get_text().strip()
                if label_text in field_map:
                    data[field_map[label_text]] = value.get_text().strip()
        
        breeder_link = soup.find('span', class_='breeder-link')
        if breeder_link:
            breeder_a = breeder_link.find('a')
            if breeder_a:
                data['breeder_name'] = breeder_a.get_text().strip()
        
        return data

    def method2_description_mining(self, soup, url):
        """Method 2: Mine description content with regex patterns"""
        data = {}
        
        description = soup.find('div', class_='description-content')
        if description:
            desc_text = description.get_text()
            data['about_info'] = desc_text.strip()
            
            patterns = {
                'thc_content': r'THC[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)',
                'cbd_content': r'CBD[:\s]*([0-9.-]+%?(?:\s*-\s*[0-9.-]+%?)?)',
                'flowering_time': r'(?:flowering|flower|harvest)[:\s]*([0-9-]+\s*(?:days?|weeks?))',
                'genetics': r'(?:genetics|cross|lineage)[:\s]*([^.]+?)(?:\.|$)',
                'effects': r'effects?[:\s]*([^.]+?)(?:\.|$)',
                'yield': r'yield[:\s]*([^.]+?)(?:\.|$)',
                'height': r'height[:\s]*([^.]+?)(?:\.|$)'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, desc_text, re.IGNORECASE)
                if match:
                    data[key] = match.group(1).strip()
        
        return data

    def method3_advanced_patterns(self, soup, url):
        """Method 3: Advanced North Atlantic specific patterns"""
        data = {}
        
        h1_tag = soup.find('h1', class_='product-title')
        if not h1_tag:
            h1_tag = soup.find('h1')
        if h1_tag:
            strain_name = h1_tag.get_text().strip()
            strain_name = re.sub(r'\s+', ' ', strain_name)
            strain_name = strain_name.replace(' Seeds', '').replace(' Feminized', '').replace(' Auto', '')
            data['strain_name'] = strain_name.strip()
        
        meta_specs = soup.find_all('div', class_='product-meta')
        for meta in meta_specs:
            text = meta.get_text()
            if 'Breeder:' in text:
                breeder_match = re.search(r'Breeder:\s*([^,\n]+)', text)
                if breeder_match:
                    data['breeder_name'] = breeder_match.group(1).strip()
        
        return data

    def method4_fallback_extraction(self, soup, url):
        """Method 4: Universal fallback extraction"""
        data = {}
        
        if 'strain_name' not in data:
            path_parts = url.split('/')
            for part in reversed(path_parts):
                if part and 'product' not in part and len(part) > 3:
                    strain_name = part.replace('-', ' ').title()
                    strain_name = re.sub(r'\s+(Seeds?|Feminized|Auto|Drop)$', '', strain_name, re.IGNORECASE)
                    data['strain_name'] = strain_name.strip()
                    break
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and not data.get('about_info'):
            data['about_info'] = meta_desc.get('content', '')
        
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            if not data.get('strain_name'):
                title_parts = title_text.split(' - ')
                if title_parts:
                    potential_strain = title_parts[0].strip()
                    potential_strain = re.sub(r'\s+(Seeds?|Feminized|Auto)$', '', potential_strain, re.IGNORECASE)
                    data['strain_name'] = potential_strain
        
        return data

    def apply_4_methods(self, html_content, url):
        """Apply all 4 extraction methods"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        strain_data = {
            'seed_bank': 'North Atlantic Seed Company',
            'source_url': url,
            'extraction_methods_used': [],
            'scraped_at': datetime.utcnow().isoformat()
        }
        
        method1_data = self.method1_structured_extraction(soup, url)
        if method1_data:
            strain_data.update(method1_data)
            strain_data['extraction_methods_used'].append('structured')
            self.method_stats['structured'] += 1
        
        method2_data = self.method2_description_mining(soup, url)
        if method2_data:
            strain_data.update(method2_data)
            strain_data['extraction_methods_used'].append('description')
            self.method_stats['description'] += 1
        
        method3_data = self.method3_advanced_patterns(soup, url)
        if method3_data:
            strain_data.update(method3_data)
            strain_data['extraction_methods_used'].append('patterns')
            self.method_stats['patterns'] += 1
        
        method4_data = self.method4_fallback_extraction(soup, url)
        if method4_data:
            strain_data.update(method4_data)
            strain_data['extraction_methods_used'].append('fallback')
            self.method_stats['fallback'] += 1
        
        strain_data['data_completeness_score'] = self.calculate_quality_score(strain_data)
        strain_data['quality_tier'] = self.determine_quality_tier(strain_data['data_completeness_score'])
        
        return strain_data

    def calculate_quality_score(self, strain_data):
        """Calculate weighted quality score"""
        field_weights = {
            'strain_name': 10, 'breeder_name': 10,
            'genetics': 8, 'flowering_time': 8, 'strain_type': 8,
            'yield': 6, 'plant_height': 6, 'terpene_profile': 6,
            'effects': 5, 'seed_type': 4, 'about_info': 4,
            'growth_type': 4, 'cannabis_type': 4
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

    def process_all_north_atlantic_strains(self):
        """Process all North Atlantic HTML files and create CSV"""
        print("Getting North Atlantic URLs...")
        north_atlantic_urls = self.get_north_atlantic_urls()
        print(f"Found {len(north_atlantic_urls)} North Atlantic URLs")
        
        # Get all available HTML files with pagination
        print("Getting all HTML files from S3...")
        all_html_files = self.get_all_html_files()
        available_hashes = {f.split('/')[-1].replace('.html', '') for f in all_html_files if f.endswith('.html')}
        print(f"Found {len(available_hashes)} HTML files in S3")
        
        all_strains = []
        
        for idx, row in north_atlantic_urls.iterrows():
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
                
                print(f"Processed: {strain_data.get('strain_name', 'Unknown')} ({idx+1}/{len(north_atlantic_urls)})")
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(all_strains)
        output_file = 'north_atlantic.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\nExtracted {len(all_strains)} strains to {output_file}")
        print(f"Available HTML files: {len(available_hashes)}")
        print(f"Processed North Atlantic URLs: {len(all_strains)}")
        print(f"Columns: {list(df.columns)}")
        
        return df

def main():
    processor = NorthAtlanticS3Processor()
    df = processor.process_all_north_atlantic_strains()
    
    # Print summary stats
    print(f"\nSUMMARY:")
    print(f"Total strains: {len(df)}")
    if len(df) > 0:
        print(f"Unique breeders: {df['breeder_name'].nunique()}")
        print(f"Strain types: {df['strain_type'].value_counts().to_dict()}")

if __name__ == "__main__":
    main()