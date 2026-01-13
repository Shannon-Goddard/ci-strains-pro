#!/usr/bin/env python3
"""
Multiverse Beans 4-Method Data Extractor
Processes 799 HTML files from S3 using proven extraction methodology
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
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiverseExtractor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        self.known_breeders = [
            'Mephisto Genetics', 'Night Owl', 'Ethos Genetics',
            'In House Genetics', 'Compound Genetics', 'Cannarado Genetics',
            'Cali Connection', 'Atlas Seeds', 'Multiverse Genetics',
            'Dutch Passion', 'Barney\'s Farm', 'Dinafem', 'Sweet Seeds'
        ]
        self.field_weights = {
            'strain_name': 10, 'breeder_name': 8, 'genetics': 8,
            'flowering_time': 7, 'growth_type': 7, 'thc_content': 6,
            'yield': 6, 'effects': 5, 'seed_type': 4, 'about_info': 4
        }
        
    def discover_multiverse_files(self) -> List[str]:
        """Scan S3 metadata for multiversebeans.com URLs"""
        logger.info("Discovering Multiverse Beans files in S3...")
        multiverse_hashes = []
        
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
                            
                            if 'multiversebeans.com' in metadata.get('url', ''):
                                hash_id = obj['Key'].split('/')[-1].replace('.json', '')
                                multiverse_hashes.append(hash_id)
                                
                        except Exception as e:
                            logger.warning(f"Error reading metadata {obj['Key']}: {e}")
                            
        except Exception as e:
            logger.error(f"Error discovering files: {e}")
            return []
            
        logger.info(f"Found {len(multiverse_hashes)} Multiverse Beans files")
        return multiverse_hashes
    
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
        """Method 1: WooCommerce structured data extraction"""
        data = {}
        
        # Product attributes table
        attrs_table = soup.find('table', class_='woocommerce-product-attributes')
        if attrs_table:
            for row in attrs_table.find_all('tr'):
                label = row.find('td', class_='woocommerce-product-attributes-item__label')
                value = row.find('td', class_='woocommerce-product-attributes-item__value')
                if label and value:
                    key = label.get_text(strip=True).lower().replace(':', '')
                    val = value.get_text(strip=True)
                    
                    if 'breeder' in key or 'brand' in key:
                        data['breeder_name'] = val
                    elif 'flowering' in key or 'flower' in key:
                        data['flowering_time'] = val
                    elif 'genetics' in key or 'lineage' in key:
                        data['genetics'] = val
                    elif 'yield' in key:
                        data['yield'] = val
                    elif 'type' in key:
                        data['seed_type'] = val
        
        # Product meta
        meta_div = soup.find('div', class_='product_meta')
        if meta_div:
            categories = meta_div.find('span', class_='posted_in')
            if categories:
                cat_text = categories.get_text(strip=True)
                if 'auto' in cat_text.lower():
                    data['growth_type'] = 'Autoflower'
                elif 'photo' in cat_text.lower():
                    data['growth_type'] = 'Photoperiod'
        
        # Price
        price_span = soup.find('span', class_='price')
        if price_span:
            data['price'] = price_span.get_text(strip=True)
            
        return data
    
    def method2_description_mining(self, soup: BeautifulSoup) -> Dict:
        """Method 2: Product description text mining"""
        data = {}
        
        # Find description content
        desc_selectors = [
            'div.woocommerce-product-details__short-description',
            'div#tab-description',
            'div.product-description',
            'div.entry-content'
        ]
        
        description_text = ""
        for selector in desc_selectors:
            desc_div = soup.select_one(selector)
            if desc_div:
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
            
            # Effects
            effects_match = re.search(r'effects?[:\s]*([^.]+)', description_text, re.IGNORECASE)
            if effects_match:
                data['effects'] = effects_match.group(1).strip()
            
            # Store full description
            data['about_info'] = description_text.strip()[:500]  # Limit length
            
        return data
    
    def method3_pattern_recognition(self, soup: BeautifulSoup, url: str = "") -> Dict:
        """Method 3: Advanced pattern recognition"""
        data = {}
        
        # Strain name from title
        title_h1 = soup.find('h1', class_='product_title')
        if title_h1:
            raw_title = title_h1.get_text(strip=True)
            # Clean strain name
            strain_name = re.sub(r'\s*-\s*(Auto|Fem|Photo|Feminized|Seeds?|Pack).*$', '', raw_title, flags=re.IGNORECASE)
            strain_name = re.sub(r'\s*\(\d+.*?\).*$', '', strain_name)  # Remove pack info
            
            # Extract breeder if in title
            for breeder in self.known_breeders:
                if breeder.lower() in strain_name.lower():
                    data['breeder_name'] = breeder
                    strain_name = strain_name.replace(breeder, '').strip(' -')
                    break
            
            data['strain_name'] = strain_name.strip()
        
        # Growth type from URL and content
        if url:
            url_lower = url.lower()
            if 'auto' in url_lower:
                data['growth_type'] = 'Autoflower'
            elif 'photo' in url_lower:
                data['growth_type'] = 'Photoperiod'
        
        # Seed type detection
        page_text = soup.get_text().lower()
        if 'feminized' in page_text or 'fem' in page_text:
            data['seed_type'] = 'Feminized'
        elif 'regular' in page_text:
            data['seed_type'] = 'Regular'
        elif 'auto' in page_text:
            data['seed_type'] = 'Autoflower'
            
        return data
    
    def method4_fallback_extraction(self, soup: BeautifulSoup, url: str = "") -> Dict:
        """Method 4: Guaranteed fallback extraction"""
        data = {}
        
        # Strain name from URL as last resort
        if url and not data.get('strain_name'):
            url_parts = urlparse(url).path.strip('/').split('/')
            if url_parts and url_parts[-1] != 'product':
                strain_slug = url_parts[-1].replace('-', ' ').title()
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
            data['seed_type'] = 'Feminized'  # Most common default
            
        return data
    
    def extract_strain_data(self, html_content: str, url: str = "") -> Dict:
        """Apply all 4 extraction methods and combine results"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Apply all methods
        method1_data = self.method1_structured_extraction(soup)
        method2_data = self.method2_description_mining(soup)
        method3_data = self.method3_pattern_recognition(soup, url)
        method4_data = self.method4_fallback_extraction(soup, url)
        
        # Combine results (later methods override earlier ones)
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
        """Process all Multiverse Beans HTML files"""
        logger.info("Starting 4-method extraction process...")
        
        # Discover files
        hash_list = self.discover_multiverse_files()
        if not hash_list:
            logger.error("No Multiverse files found!")
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
                strain_data['source_site'] = 'multiversebeans.com'
                
                results.append(strain_data)
                processed += 1
                
                if processed % 50 == 0:
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
        filename = f"multiverse_beans_extracted_{timestamp}.csv"
        s3_key = f"processed_data/multiverse_beans/{filename}"
        
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
    parser = argparse.ArgumentParser(description='Multiverse Beans 4-Method Extractor')
    parser.add_argument('--discover', action='store_true', help='Discover Multiverse files only')
    parser.add_argument('--extract', action='store_true', help='Run full extraction')
    parser.add_argument('--validate', action='store_true', help='Validate results')
    
    args = parser.parse_args()
    
    extractor = MultiverseExtractor()
    
    if args.discover:
        hash_list = extractor.discover_multiverse_files()
        print(f"Found {len(hash_list)} Multiverse Beans files ready for processing")
        
    elif args.extract:
        # Run full extraction
        df = extractor.process_all_strains()
        
        if not df.empty:
            # Upload to S3
            s3_key = extractor.upload_results_to_s3(df)
            
            # Generate report
            report = extractor.generate_quality_report(df)
            
            print("\n=== EXTRACTION COMPLETE ===")
            print(f"Total Processed: {report['total_processed']}")
            print(f"Average Quality: {report['avg_quality_score']:.1f}%")
            print(f"Success Rate: {report['total_processed']}/799 ({report['total_processed']/799*100:.1f}%)")
            print(f"Results uploaded: {s3_key}")
            
            # Quality distribution
            print("\nQuality Distribution:")
            for tier, count in report['quality_distribution'].items():
                print(f"  {tier}: {count}")
                
        else:
            print("No data extracted!")
            
    elif args.validate:
        print("Validation mode - checking S3 results...")
        # Could add validation logic here
        
    else:
        print("Use --discover, --extract, or --validate")

if __name__ == "__main__":
    main()