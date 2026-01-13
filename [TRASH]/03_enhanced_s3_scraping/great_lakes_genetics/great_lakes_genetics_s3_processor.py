#!/usr/bin/env python3
"""
Great Lakes Genetics S3 HTML Processor
Based on successful S3 pattern with Great Lakes Genetics 4-method extraction
Target: US boutique breeder strains with detailed cultivation data
"""

import csv
import boto3
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

class GreatLakesGeneticsS3Processor:
    def __init__(self, s3_bucket='ci-strains-html-archive'):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.processed_count = 0
        self.success_count = 0
        self.method_stats = {'structured': 0, 'description': 0, 'patterns': 0, 'fallback': 0}
        
    def get_great_lakes_urls(self):
        """Get all Great Lakes Genetics URLs from S3 mapping"""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key='index/url_mapping.csv')
            df = pd.read_csv(response['Body'])
        except:
            df = pd.read_csv('../../01_html_collection/data/unique_urls.csv', encoding='latin-1')
        
        great_lakes_urls = df[df['url'].str.contains('greatlakesgenetics', na=False)]
        return great_lakes_urls
    
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
        """Method 1: Great Lakes Genetics .et_pb_module_inner container extraction"""
        data = {}
        
        # Target the main container
        container = soup.find('div', class_='et_pb_module_inner')
        if container:
            # Extract strain name and breeder from H3
            h3_tag = container.find('h3')
            if h3_tag:
                h3_text = h3_tag.get_text().strip()
                # Parse format: "Breeder - Strain Name (pack info)"
                if ' - ' in h3_text:
                    breeder_part, strain_part = h3_text.split(' - ', 1)
                    data['breeder_name'] = breeder_part.strip()
                    # Remove pack info from strain name
                    strain_name = strain_part.split(' (')[0].strip()
                    data['strain_name'] = strain_name
            
            # Extract structured fields from paragraphs
            paragraphs = container.find_all('p')
            for p in paragraphs:
                # Find all strong tags (field labels)
                strong_tags = p.find_all('strong')
                for strong in strong_tags:
                    label = strong.get_text().strip().rstrip(':')
                    
                    # Get the value after the strong tag
                    next_sibling = strong.next_sibling
                    value = ""
                    
                    # Handle different sibling types
                    if next_sibling:
                        if hasattr(next_sibling, 'get_text'):
                            value = next_sibling.get_text().strip()
                        else:
                            value = str(next_sibling).strip()
                        
                        # Clean up the value
                        value = value.lstrip(': ').strip()
                        
                        # If value is empty, look for span after strong
                        if not value:
                            next_span = strong.find_next_sibling('span')
                            if next_span:
                                value = next_span.get_text().strip()
                    
                    # Map Great Lakes Genetics fields
                    field_map = {
                        'Genetics': 'genetics',
                        'Seeds in pack': 'seeds_in_pack',
                        'Sex': 'sex',
                        'Type': 'strain_type',
                        'Yield': 'yield',
                        'Flowering Time': 'flowering_time',
                        'Area (Indoor, Outdoor, Both)': 'growing_area',
                        'Notes': 'cultivation_notes'
                    }
                    
                    if label in field_map and value:
                        data[field_map[label]] = value
        
        return data

    def method2_description_mining(self, soup, url):
        """Method 2: Mine Great Lakes Genetics Notes section for detailed information"""
        data = {}
        
        # Look for Notes section and other descriptive content
        desc_selectors = [
            'div.et_pb_module_inner',
            'div.product-description',
            'div.strain-info'
        ]
        
        about_parts = []
        for selector in desc_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if text and len(text) > 100:  # Substantial content
                    about_parts.append(text)
        
        if about_parts:
            full_text = ' '.join(about_parts)
            data['about_info'] = full_text
            
            # Extract specific patterns from Notes section
            patterns = {
                'effects_pattern': r'(?:euphoric|creative|stoned|relaxing|uplifting|energetic|calming)[^.]*',
                'aroma_pattern': r'(?:nose|aroma|smell)[^.]*?(?:spicy|hash|lemon|fuel|sweet|earthy|pine)[^.]*',
                'structure_pattern': r'(?:structure|tree|bush|plant)[^.]*?(?:christmas|uniform|branching)[^.]*',
                'resin_pattern': r'(?:resin|sticky|trichome)[^.]*?(?:production|impressive|coverage)[^.]*'
            }
            
            for key, pattern in patterns.items():
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                if matches:
                    data[key] = '; '.join(matches[:3])  # Limit to 3 matches
        
        return data

    def method3_advanced_patterns(self, soup, url):
        """Method 3: Great Lakes Genetics specific patterns"""
        data = {}
        
        # Extract strain name from URL if not found
        if 'strain_name' not in data:
            path_parts = url.split('/')
            for part in reversed(path_parts):
                if part and 'product' in url and len(part) > 5:
                    strain_name = part.replace('-', ' ').title()
                    # Clean common suffixes
                    strain_name = re.sub(r'\s+(Auto|Autoflower|Fem|Feminized|Regular|Seeds?)$', '', strain_name, re.IGNORECASE)
                    data['strain_name'] = strain_name.strip()
                    break
        
        # Detect seed type from content
        page_text = soup.get_text().lower()
        if 'autoflower' in page_text or 'auto' in page_text:
            data['growth_type'] = 'Autoflower'
            data['seed_type'] = 'Feminized'  # Most autos are feminized
        elif 'feminized' in page_text or 'fem' in page_text:
            data['seed_type'] = 'Feminized'
            data['growth_type'] = 'Photoperiod'
        elif 'regular' in page_text or 'reg' in page_text:
            data['seed_type'] = 'Regular'
            data['growth_type'] = 'Photoperiod'
        
        # Extract US breeder indicators
        us_breeders = [
            'forest', 'jaws', 'cannarado', 'ethos', 'in house', 'compound',
            'thug pug', 'exotic genetix', 'oni seed', 'clearwater', 'bloom'
        ]
        
        page_text_lower = soup.get_text().lower()
        for breeder in us_breeders:
            if breeder in page_text_lower:
                data['us_genetics'] = True
                break
        
        return data

    def method4_fallback_extraction(self, soup, url):
        """Method 4: Universal fallback for Great Lakes Genetics"""
        data = {}
        
        # Extract strain name from page title if not found
        if 'strain_name' not in data:
            title = soup.find('title')
            if title:
                title_text = title.get_text().strip()
                title_parts = title_text.split(' - ')
                if title_parts:
                    potential_strain = title_parts[0].strip()
                    potential_strain = re.sub(r'\s+(Auto|Feminized|Regular|Seeds?)$', '', potential_strain, re.IGNORECASE)
                    data['strain_name'] = potential_strain
        
        # Meta description fallback
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and not data.get('about_info'):
            data['about_info'] = meta_desc.get('content', '')
        
        # Extract any H1-H6 headings for additional context
        headings = []
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            for h in h_tags:
                heading_text = h.get_text().strip()
                if heading_text and len(heading_text) > 5:
                    headings.append(heading_text)
        
        if headings and not data.get('strain_name'):
            # Use first substantial heading as strain name
            data['strain_name'] = headings[0]
        
        return data

    def apply_4_methods(self, html_content, url):
        """Apply all 4 extraction methods"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        strain_data = {
            'seed_bank': 'Great Lakes Genetics',
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
        """Calculate weighted quality score optimized for Great Lakes Genetics"""
        field_weights = {
            # Core fields (required)
            'strain_name': 10,
            'seed_bank': 10,
            
            # Great Lakes Genetics strengths
            'breeder_name': 10,              # Clear breeder attribution
            'genetics': 9,                   # Parent strain lineage
            'cultivation_notes': 9,          # Comprehensive growing info
            'flowering_time': 8,             # Cultivation timing
            'yield': 8,                      # Production data
            'strain_type': 7,                # Cannabis classification
            'sex': 7,                        # Seed type
            'growing_area': 6,               # Indoor/Outdoor suitability
            'seeds_in_pack': 5,              # Pack information
            
            # Enhanced fields from Notes mining
            'effects_pattern': 7,            # Experience profiles
            'aroma_pattern': 6,              # Scent profiles
            'structure_pattern': 5,          # Growth patterns
            'resin_pattern': 5,              # Quality indicators
            
            # Additional info
            'about_info': 6,                 # Detailed descriptions
            'growth_type': 5,                # Auto/Photo classification
            'seed_type': 5,                  # Feminized/Regular
            'us_genetics': 3                 # US breeder indicator
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

    def process_all_great_lakes_strains(self):
        """Process all Great Lakes Genetics HTML files and create CSV"""
        print("Getting Great Lakes Genetics URLs...")
        great_lakes_urls = self.get_great_lakes_urls()
        print(f"Found {len(great_lakes_urls)} Great Lakes Genetics URLs")
        
        # Get all available HTML files with pagination
        print("Getting all HTML files from S3...")
        all_html_files = self.get_all_html_files()
        available_hashes = {f.split('/')[-1].replace('.html', '') for f in all_html_files if f.endswith('.html')}
        print(f"Found {len(available_hashes)} HTML files in S3")
        
        all_strains = []
        
        for idx, row in great_lakes_urls.iterrows():
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
                
                print(f"Processed: {strain_data.get('strain_name', 'Unknown')} - {strain_data.get('breeder_name', 'Unknown')} ({idx+1}/{len(great_lakes_urls)})")
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(all_strains)
        output_file = 'great_lakes_genetics.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\nExtracted {len(all_strains)} strains to {output_file}")
        print(f"Available HTML files: {len(available_hashes)}")
        print(f"Processed Great Lakes URLs: {len(all_strains)}")
        print(f"Method usage: {self.method_stats}")
        print(f"Columns: {list(df.columns)}")
        
        return df

def main():
    processor = GreatLakesGeneticsS3Processor()
    df = processor.process_all_great_lakes_strains()
    
    # Print summary stats
    print(f"\nSUMMARY:")
    print(f"Total strains: {len(df)}")
    if len(df) > 0:
        print(f"Quality distribution: {df['quality_tier'].value_counts().to_dict()}")
        if 'breeder_name' in df.columns:
            print(f"Top breeders: {df['breeder_name'].value_counts().head().to_dict()}")

if __name__ == "__main__":
    main()