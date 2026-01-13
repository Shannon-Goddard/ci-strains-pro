#!/usr/bin/env python3
"""
Dutch Passion S3 HTML Processor
Based on North Atlantic's S3 pattern with Dutch Passion's 4-method extraction system
Target: Legacy genetics from original seed company (1987)
"""

import csv
import boto3
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

class DutchPassionS3Processor:
    def __init__(self, s3_bucket='ci-strains-html-archive'):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.processed_count = 0
        self.success_count = 0
        self.method_stats = {'structured': 0, 'description': 0, 'patterns': 0, 'fallback': 0}
        
    def get_dutch_passion_urls(self):
        """Get all Dutch Passion URLs from S3 mapping"""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key='index/url_mapping.csv')
            df = pd.read_csv(response['Body'])
        except:
            df = pd.read_csv('../../01_html_collection/data/unique_urls.csv', encoding='latin-1')
        
        dutch_passion_urls = df[df['url'].str.contains('dutch-passion', na=False)]
        return dutch_passion_urls
    
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
        """Method 1: Extract from Dutch Passion's specification tables"""
        data = {}
        
        # Extract from specification tables
        table_patterns = {
            'genetics': r'<td[^>]*>Genetics[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'flowering_time': r'<td[^>]*>Flowering[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'thc_content': r'<td[^>]*>THC[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'cbd_content': r'<td[^>]*>CBD[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'yield': r'<td[^>]*>Yield[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'height': r'<td[^>]*>Height[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'seed_type': r'<td[^>]*>Type[^<]*</td>\s*<td[^>]*>([^<]+)</td>'
        }
        
        html_content = str(soup)
        for field, pattern in table_patterns.items():
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                data[field] = match.group(1).strip()
        
        # Look for structured data in divs/spans
        spec_items = soup.find_all(['div', 'span'], class_=re.compile(r'spec|detail|info'))
        for item in spec_items:
            text = item.get_text().strip()
            if 'genetics' in text.lower() and ':' in text:
                genetics_match = re.search(r'genetics[:\s]*([^,\n]+)', text, re.IGNORECASE)
                if genetics_match:
                    data['genetics'] = genetics_match.group(1).strip()
        
        return data

    def method2_description_mining(self, soup, url):
        """Method 2: Mine description content with regex patterns"""
        data = {}
        
        # Find description areas
        description_selectors = [
            'div.description-content', 'div.product-description', 
            'div.strain-description', 'p.description'
        ]
        
        description_text = ""
        for selector in description_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                description_text = desc_elem.get_text()
                break
        
        if not description_text:
            # Fallback to any div with substantial text
            divs = soup.find_all('div')
            for div in divs:
                text = div.get_text().strip()
                if len(text) > 200 and ('strain' in text.lower() or 'cannabis' in text.lower()):
                    description_text = text
                    break
        
        if description_text:
            data['about_info'] = description_text.strip()
            
            # Extract flowering time
            flowering_match = re.search(r'(\d+)[-\s]*(\d+)?\s*weeks?\s*flower', description_text, re.IGNORECASE)
            if flowering_match:
                if flowering_match.group(2):
                    data['flowering_time'] = f"{flowering_match.group(1)}-{flowering_match.group(2)} weeks"
                else:
                    data['flowering_time'] = f"{flowering_match.group(1)} weeks"
            
            # Extract THC content
            thc_patterns = [
                r'(\d+(?:\.\d+)?)[-\s]*(\d+(?:\.\d+)?)?\s*%\s*THC',
                r'THC[:\s]*(\d+(?:\.\d+)?)[-\s]*(\d+(?:\.\d+)?)?\s*%'
            ]
            for pattern in thc_patterns:
                thc_match = re.search(pattern, description_text, re.IGNORECASE)
                if thc_match:
                    if thc_match.group(2):
                        data['thc_content'] = f"{thc_match.group(1)}-{thc_match.group(2)}%"
                    else:
                        data['thc_content'] = f"{thc_match.group(1)}%"
                    break
            
            # Extract effects
            effect_keywords = ['euphoric', 'relaxing', 'energetic', 'creative', 'uplifting', 'calming', 'cerebral', 'body']
            effects = []
            for keyword in effect_keywords:
                if re.search(rf'\b{keyword}\b', description_text, re.IGNORECASE):
                    effects.append(keyword)
            if effects:
                data['effects'] = ', '.join(effects)
        
        return data

    def method3_advanced_patterns(self, soup, url):
        """Method 3: Advanced Dutch Passion specific patterns"""
        data = {}
        
        # Extract strain name from title or h1
        h1_tag = soup.find('h1')
        if h1_tag:
            strain_name = h1_tag.get_text().strip()
            strain_name = re.sub(r'\s+', ' ', strain_name)
            strain_name = strain_name.replace(' Seeds', '').replace(' Feminized', '').replace(' Auto', '')
            data['strain_name'] = strain_name.strip()
        
        # Detect seed type from URL and content
        html_content = str(soup).lower()
        if '/autoflower-seeds' in url or 'auto-' in html_content:
            data['seed_type'] = 'Autoflower'
            data['growth_type'] = 'Autoflower'
        elif '/feminized-seeds' in url or 'feminized' in html_content:
            data['seed_type'] = 'Feminized'
            data['growth_type'] = 'Photoperiod'
        elif '/regular-seeds' in url:
            data['seed_type'] = 'Regular'
            data['growth_type'] = 'Photoperiod'
        
        # Extract terpene profiles
        terpene_pattern = r'terpene[^:]*:\s*([^<\n]+)'
        terpene_match = re.search(terpene_pattern, str(soup), re.IGNORECASE)
        if terpene_match:
            data['terpene_profile'] = terpene_match.group(1).strip()
        
        # Extract awards
        award_pattern = r'(cup|award|winner|champion)[^<\n]*([^<\n]{10,50})'
        award_match = re.search(award_pattern, str(soup), re.IGNORECASE)
        if award_match:
            data['awards'] = award_match.group(0).strip()
        
        return data

    def method4_fallback_extraction(self, soup, url):
        """Method 4: Universal fallback extraction"""
        data = {}
        
        # Extract strain name from URL if not found
        if 'strain_name' not in data:
            strain_match = re.search(r'/cannabis-seeds/([^/?]+)', url)
            if strain_match:
                strain_name = strain_match.group(1).replace('-', ' ').title()
                data['strain_name'] = strain_name
            else:
                # Fallback to URL path parsing
                path_parts = url.split('/')
                for part in reversed(path_parts):
                    if part and 'product' not in part and len(part) > 3:
                        strain_name = part.replace('-', ' ').title()
                        strain_name = re.sub(r'\s+(Seeds?|Feminized|Auto|Drop)$', '', strain_name, re.IGNORECASE)
                        data['strain_name'] = strain_name.strip()
                        break
        
        # Extract title
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            if 'Dutch Passion' in title_text:
                data['page_title'] = title_text
            
            # Use title for strain name if still missing
            if not data.get('strain_name'):
                title_parts = title_text.split(' - ')
                if title_parts:
                    potential_strain = title_parts[0].strip()
                    potential_strain = re.sub(r'\s+(Seeds?|Feminized|Auto)$', '', potential_strain, re.IGNORECASE)
                    data['strain_name'] = potential_strain
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and not data.get('about_info'):
            data['about_info'] = meta_desc.get('content', '')
        
        # Set hardcoded values
        data['seed_bank'] = 'Dutch Passion'
        data['breeder_name'] = 'Dutch Passion'
        
        return data

    def apply_4_methods(self, html_content, url):
        """Apply all 4 extraction methods"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        strain_data = {
            'seed_bank': 'Dutch Passion',
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
        """Calculate weighted quality score"""
        field_weights = {
            'strain_name': 10, 'breeder_name': 10,
            'genetics': 8, 'flowering_time': 8, 'seed_type': 8,
            'thc_content': 6, 'yield': 6, 'height': 6,
            'effects': 5, 'terpene_profile': 5, 'about_info': 4,
            'growth_type': 4, 'cbd_content': 4, 'awards': 3
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

    def process_all_dutch_passion_strains(self):
        """Process all Dutch Passion HTML files and create CSV"""
        print("Getting Dutch Passion URLs...")
        dutch_passion_urls = self.get_dutch_passion_urls()
        print(f"Found {len(dutch_passion_urls)} Dutch Passion URLs")
        
        # Get all available HTML files with pagination
        print("Getting all HTML files from S3...")
        all_html_files = self.get_all_html_files()
        available_hashes = {f.split('/')[-1].replace('.html', '') for f in all_html_files if f.endswith('.html')}
        print(f"Found {len(available_hashes)} HTML files in S3")
        
        all_strains = []
        
        for idx, row in dutch_passion_urls.iterrows():
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
                
                print(f"Processed: {strain_data.get('strain_name', 'Unknown')} ({idx+1}/{len(dutch_passion_urls)})")
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(all_strains)
        output_file = 'dutch_passion.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\nExtracted {len(all_strains)} strains to {output_file}")
        print(f"Available HTML files: {len(available_hashes)}")
        print(f"Processed Dutch Passion URLs: {len(all_strains)}")
        print(f"Method usage: {self.method_stats}")
        print(f"Columns: {list(df.columns)}")
        
        return df

def main():
    processor = DutchPassionS3Processor()
    df = processor.process_all_dutch_passion_strains()
    
    # Print summary stats
    print(f"\nSUMMARY:")
    print(f"Total strains: {len(df)}")
    if len(df) > 0:
        print(f"Quality distribution: {df['quality_tier'].value_counts().to_dict()}")
        print(f"Seed types: {df['seed_type'].value_counts().to_dict()}")

if __name__ == "__main__":
    main()