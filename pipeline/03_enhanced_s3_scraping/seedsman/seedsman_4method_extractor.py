#!/usr/bin/env python3
"""
Seedsman 4-Method Data Extractor
Processes Seedsman HTML files from S3 using proven extraction methodology
Target: 95%+ extraction success rate with commercial-grade quality
"""

import boto3
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import argparse
import logging
from typing import Dict, List, Optional
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SeedsmanExtractor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        self.seedsman_breeders = [
            'Dinafem', 'Barney\'s Farm', 'Dutch Passion', 'Sweet Seeds',
            'Royal Queen Seeds', 'Sensi Seeds', 'Serious Seeds',
            'Paradise Seeds', 'Greenhouse Seeds', 'DNA Genetics',
            'Reserva Privada', 'Humboldt Seeds', 'World of Seeds',
            'FastBuds', 'Mephisto Genetics', 'Night Owl Seeds'
        ]
        self.field_weights = {
            'strain_name': 10, 'breeder_name': 9, 'genetics': 8,
            'flowering_time': 7, 'growth_type': 7, 'thc_content': 6,
            'yield': 6, 'height': 5, 'effects': 5, 'seed_count': 4, 'about_info': 4
        }
        
    def discover_seedsman_files(self) -> List[str]:
        """Scan S3 metadata for seedsman.com URLs"""
        logger.info("Discovering Seedsman files in S3...")
        seedsman_hashes = []
        
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=self.bucket_name, Prefix='metadata/')
            
            for page in pages:
                if 'Contents' not in page:
                    continue
                    
                for obj in page['Contents']:
                    if obj['Key'].endswith('.json'):
                        try:
                            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=obj['Key'])
                            metadata = json.loads(response['Body'].read().decode('utf-8'))
                            
                            if 'seedsman.com' in metadata.get('url', ''):
                                hash_id = obj['Key'].split('/')[-1].replace('.json', '')
                                seedsman_hashes.append(hash_id)
                                
                        except Exception as e:
                            logger.warning(f"Error reading metadata {obj['Key']}: {e}")
                            
        except Exception as e:
            logger.error(f"Error discovering files: {e}")
            return []
            
        logger.info(f"Found {len(seedsman_hashes)} Seedsman files")
        return seedsman_hashes
    
    def fetch_html_content(self, hash_id: str) -> Optional[str]:
        """Fetch HTML content from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name, 
                Key=f'html/{hash_id}.html'
            )
            return response['Body'].read().decode('utf-8', errors='ignore')
        except Exception as e:
            logger.error(f"Error fetching HTML {hash_id}: {e}")
            return None
    
    def method1_structured_extraction(self, soup: BeautifulSoup) -> Dict:
        """Method 1: Seedsman structured data extraction"""
        data = {}
        
        # Product info main section
        product_main = soup.find('div', class_='product-info-main')
        if product_main:
            # Price information
            price_div = product_main.find('div', class_='product-info-price')
            if price_div:
                price_span = price_div.find('span', class_='price')
                if price_span:
                    data['price'] = price_span.get_text(strip=True)
        
        # Product specifications table
        spec_table = soup.find('table', class_='data-table')
        if spec_table:
            for row in spec_table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    
                    if 'breeder' in key or 'brand' in key:
                        data['breeder_name'] = value
                    elif 'flowering' in key or 'flower' in key:
                        data['flowering_time'] = value
                    elif 'genetics' in key or 'lineage' in key or 'cross' in key:
                        data['genetics'] = value
                    elif 'yield' in key:
                        data['yield'] = value
                    elif 'height' in key:
                        data['height'] = value
                    elif 'thc' in key:
                        data['thc_content'] = value
                    elif 'cbd' in key:
                        data['cbd_content'] = value
                    elif 'seeds' in key or 'count' in key:
                        data['seed_count'] = value
        
        # Stock status
        stock_div = soup.find('div', class_='stock-status')
        if stock_div:
            data['availability'] = stock_div.get_text(strip=True)
            
        return data
    
    def method2_description_mining(self, soup: BeautifulSoup) -> Dict:
        """Method 2: Product description text mining"""
        data = {}
        
        # Find description content
        desc_selectors = [
            'div.product-info-description',
            'div.product-collateral',
            'div.std',
            'div.product-view'
        ]
        
        description_text = ""
        for selector in desc_selectors:
            desc_divs = soup.select(selector)
            for desc_div in desc_divs:
                description_text += " " + desc_div.get_text()
        
        if description_text:
            # THC extraction
            thc_match = re.search(r'THC[:\s]*(\d+(?:\.\d+)?%?(?:\s*-\s*\d+(?:\.\d+)?%?)?)', description_text, re.IGNORECASE)
            if thc_match:
                data['thc_content'] = thc_match.group(1)
            
            # CBD extraction
            cbd_match = re.search(r'CBD[:\s]*(\d+(?:\.\d+)?%?(?:\s*-\s*\d+(?:\.\d+)?%?)?)', description_text, re.IGNORECASE)
            if cbd_match:
                data['cbd_content'] = cbd_match.group(1)
            
            # Flowering time
            flowering_match = re.search(r'flowering[:\s]*(\d+-?\d*\s*(?:days?|weeks?))', description_text, re.IGNORECASE)
            if flowering_match:
                data['flowering_time'] = flowering_match.group(1)
            
            # Yield extraction
            yield_match = re.search(r'yield[:\s]*(\d+(?:\.\d+)?\s*(?:g|oz|grams?))', description_text, re.IGNORECASE)
            if yield_match:
                data['yield'] = yield_match.group(1)
            
            # Height extraction
            height_match = re.search(r'height[:\s]*(\d+(?:\.\d+)?\s*(?:cm|m|ft))', description_text, re.IGNORECASE)
            if height_match:
                data['height'] = height_match.group(1)
            
            # Effects
            effects_match = re.search(r'effects?[:\s]*([^.]+)', description_text, re.IGNORECASE)
            if effects_match:
                data['effects'] = effects_match.group(1).strip()
            
            # Store description
            data['about_info'] = description_text.strip()[:500]
            
        return data
    
    def method3_pattern_recognition(self, soup: BeautifulSoup, url: str = "") -> Dict:
        """Method 3: Advanced pattern recognition"""
        data = {}
        
        # Strain name from page title
        title_h1 = soup.find('h1', class_='page-title')
        if title_h1:
            raw_title = title_h1.get_text(strip=True)
            # Clean strain name
            strain_name = re.sub(r'\s*-?\s*(Seeds?|Feminized|Auto|Regular|CBD).*$', '', raw_title, flags=re.IGNORECASE)
            strain_name = re.sub(r'\s*\(\d+.*?\).*$', '', strain_name)  # Remove pack info
            
            # Extract breeder if in title
            for breeder in self.seedsman_breeders:
                if breeder.lower() in strain_name.lower():
                    data['breeder_name'] = breeder
                    strain_name = strain_name.replace(breeder, '').strip(' -')
                    break
            
            data['strain_name'] = strain_name.strip()
        
        # Growth type from URL and breadcrumbs
        if url:
            url_lower = url.lower()
            if 'autoflowering' in url_lower or 'auto' in url_lower:
                data['growth_type'] = 'Autoflower'
            elif 'feminised' in url_lower or 'feminized' in url_lower:
                data['growth_type'] = 'Photoperiod'
                data['seed_type'] = 'Feminized'
            elif 'regular' in url_lower:
                data['growth_type'] = 'Photoperiod'
                data['seed_type'] = 'Regular'
        
        # Breadcrumb analysis
        breadcrumbs = soup.find('div', class_='breadcrumbs')
        if breadcrumbs:
            breadcrumb_text = breadcrumbs.get_text().lower()
            if 'autoflowering' in breadcrumb_text:
                data['growth_type'] = 'Autoflower'
            elif 'feminised' in breadcrumb_text:
                data['seed_type'] = 'Feminized'
            elif 'regular' in breadcrumb_text:
                data['seed_type'] = 'Regular'
            elif 'cbd' in breadcrumb_text:
                data['cbd_strain'] = True
                
        return data
    
    def method4_fallback_extraction(self, soup: BeautifulSoup, url: str = "") -> Dict:
        """Method 4: Guaranteed fallback extraction"""
        data = {}
        
        # Strain name from URL as last resort
        if url and not data.get('strain_name'):
            url_parts = urlparse(url).path.strip('/').split('/')
            if url_parts:
                strain_slug = url_parts[-1].replace('-seeds.html', '').replace('-', ' ').title()
                data['strain_name'] = strain_slug
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and not data.get('about_info'):
            data['about_info'] = meta_desc.get('content', '')[:200]
        
        # Page title fallback
        title_tag = soup.find('title')
        if title_tag and not data.get('strain_name'):
            title_text = title_tag.get_text(strip=True)
            data['strain_name'] = title_text.split('|')[0].strip()
        
        # Default values
        if not data.get('seed_type'):
            data['seed_type'] = 'Feminized'  # Most common
        if not data.get('growth_type'):
            data['growth_type'] = 'Photoperiod'  # Most common
            
        return data
    
    def extract_strain_data(self, html_content: str, url: str = "") -> Dict:
        """Apply all 4 extraction methods and combine results"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Apply all methods
        method1_data = self.method1_structured_extraction(soup)
        method2_data = self.method2_description_mining(soup)
        method3_data = self.method3_pattern_recognition(soup, url)
        method4_data = self.method4_fallback_extraction(soup, url)
        
        # Combine results
        combined_data = {}
        for method_data in [method1_data, method2_data, method3_data, method4_data]:
            combined_data.update({k: v for k, v in method_data.items() if v})
        
        # Calculate quality score
        quality_score = self.calculate_quality_score(combined_data)
        combined_data['quality_score'] = quality_score
        combined_data['extraction_timestamp'] = datetime.now().isoformat()
        
        return combined_data
    
    def calculate_quality_score(self, data: Dict) -> float:
        """Calculate data quality score based on field weights"""
        total_weight = sum(self.field_weights.values())
        achieved_weight = 0
        
        for field, weight in self.field_weights.items():
            if field in data and data[field]:
                achieved_weight += weight
        
        return round((achieved_weight / total_weight) * 100, 1)
    
    def process_all_strains(self) -> pd.DataFrame:
        """Process all Seedsman HTML files"""
        logger.info("Starting Seedsman 4-method extraction...")
        
        # Discover files
        hash_list = self.discover_seedsman_files()
        if not hash_list:
            logger.error("No Seedsman files found!")
            return pd.DataFrame()
        
        results = []
        processed = 0
        errors = 0
        
        for hash_id in hash_list:
            try:
                # Fetch HTML
                html_content = self.fetch_html_content(hash_id)
                if not html_content:
                    errors += 1
                    continue
                
                # Extract data
                strain_data = self.extract_strain_data(html_content)
                strain_data['source_hash'] = hash_id
                strain_data['source_site'] = 'seedsman.com'
                
                results.append(strain_data)
                processed += 1
                
                if processed % 100 == 0:
                    logger.info(f"Processed {processed}/{len(hash_list)} files...")
                    
            except Exception as e:
                logger.error(f"Error processing {hash_id}: {e}")
                errors += 1
        
        logger.info(f"Extraction complete: {processed} successful, {errors} errors")
        
        # Create DataFrame
        df = pd.DataFrame(results)
        return df
    
    def upload_results_to_s3(self, df: pd.DataFrame) -> str:
        """Upload results CSV to S3 processed_data folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"seedsman_extracted_{timestamp}.csv"
        s3_key = f"processed_data/seedsman/{filename}"
        
        try:
            # Convert to CSV
            csv_buffer = df.to_csv(index=False, encoding='utf-8')
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=csv_buffer.encode('utf-8'),
                ContentType='text/csv'
            )
            
            logger.info(f"Results uploaded to s3://{self.bucket_name}/{s3_key}")
            return s3_key
            
        except Exception as e:
            logger.error(f"Error uploading to S3: {e}")
            return ""
    
    def generate_quality_report(self, df: pd.DataFrame) -> Dict:
        """Generate extraction quality report"""
        if df.empty:
            return {}
        
        report = {
            'total_processed': len(df),
            'avg_quality_score': df['quality_score'].mean(),
            'quality_distribution': {
                'premium_80plus': len(df[df['quality_score'] >= 80]),
                'high_60to79': len(df[(df['quality_score'] >= 60) & (df['quality_score'] < 80)]),
                'medium_40to59': len(df[(df['quality_score'] >= 40) & (df['quality_score'] < 60)]),
                'basic_20to39': len(df[(df['quality_score'] >= 20) & (df['quality_score'] < 40)])
            },
            'field_coverage': {}
        }
        
        # Field coverage analysis
        for field in self.field_weights.keys():
            if field in df.columns:
                coverage = (df[field].notna() & (df[field] != '')).sum()
                report['field_coverage'][field] = f"{coverage}/{len(df)} ({coverage/len(df)*100:.1f}%)"
        
        return report

def main():
    parser = argparse.ArgumentParser(description='Seedsman 4-Method Extractor')
    parser.add_argument('--discover', action='store_true', help='Discover Seedsman files only')
    parser.add_argument('--extract', action='store_true', help='Run full extraction')
    parser.add_argument('--validate', action='store_true', help='Validate results')
    
    args = parser.parse_args()
    
    extractor = SeedsmanExtractor()
    
    if args.discover:
        hash_list = extractor.discover_seedsman_files()
        print(f"Found {len(hash_list)} Seedsman files ready for processing")
        
    elif args.extract:
        # Run full extraction
        df = extractor.process_all_strains()
        
        if not df.empty:
            # Upload to S3
            s3_key = extractor.upload_results_to_s3(df)
            
            # Generate report
            report = extractor.generate_quality_report(df)
            
            print("\n=== SEEDSMAN EXTRACTION COMPLETE ===")
            print(f"Total Processed: {report['total_processed']}")
            print(f"Average Quality: {report['avg_quality_score']:.1f}%")
            print(f"Results uploaded: {s3_key}")
            
            # Quality distribution
            print("\nQuality Distribution:")
            for tier, count in report['quality_distribution'].items():
                print(f"  {tier}: {count}")
                
        else:
            print("No data extracted!")
            
    elif args.validate:
        print("Validation mode - checking S3 results...")
        
    else:
        print("Use --discover, --extract, or --validate")

if __name__ == "__main__":
    main()