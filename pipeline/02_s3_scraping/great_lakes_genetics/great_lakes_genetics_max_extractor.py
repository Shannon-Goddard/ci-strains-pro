#!/usr/bin/env python3
"""
Great Lakes Genetics Maximum Value Extractor - Production Grade
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import csv
import boto3
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GreatLakesGeneticsMaxExtractor:
    def __init__(self, s3_bucket='ci-strains-html-archive'):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.extraction_stats = {
            'json_ld': 0, 'meta_tags': 0, 'tables': 0, 'pricing': 0,
            'cannabis_data': 0, 'images': 0, 'awards': 0, 'genetics': 0
        }
        
    def extract_json_ld_data(self, soup):
        data = {}
        json_scripts = soup.find_all('script', type='application/ld+json')
        
        for script in json_scripts:
            if script.string:
                try:
                    json_data = json.loads(script.string)
                    if json_data.get('@type') == 'Product':
                        data.update({
                            'jsonld_product_name': json_data.get('name'),
                            'jsonld_description': json_data.get('description'),
                            'jsonld_brand': json_data.get('brand', {}).get('name') if isinstance(json_data.get('brand'), dict) else json_data.get('brand'),
                            'jsonld_sku': json_data.get('sku'),
                            'jsonld_price': json_data.get('offers', {}).get('price'),
                            'jsonld_currency': json_data.get('offers', {}).get('priceCurrency')
                        })
                except:
                    continue
        
        if data:
            self.extraction_stats['json_ld'] += 1
        return data
    
    def extract_comprehensive_meta_tags(self, soup):
        data = {}
        meta_tags = soup.find_all('meta')
        
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property') or meta.get('itemprop')
            content = meta.get('content')
            
            if name and content:
                field_name = name.replace(':', '_').replace('og:', '').replace('twitter:', '').lower()
                field_name = re.sub(r'[^a-z0-9_]', '_', field_name)
                data[f'meta_{field_name}'] = content
        
        title_tag = soup.find('title')
        if title_tag:
            data['page_title'] = title_tag.get_text().strip()
        
        if data:
            self.extraction_stats['meta_tags'] += 1
        return data
    
    def extract_structured_tables(self, soup):
        data = {}
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text().strip().lower()
                    value = cells[1].get_text().strip()
                    key = re.sub(r'[^a-z0-9_]', '_', key).strip('_')
                    if key and value and len(value) < 200:
                        data[f'spec_{key}'] = value
        
        if data:
            self.extraction_stats['tables'] += 1
        return data
    
    def extract_comprehensive_pricing(self, soup, url):
        data = {}
        html_text = soup.get_text()
        
        currency_patterns = {
            'usd': [r'\$(\d+(?:\.\d{2})?)', r'USD\s*(\d+(?:\.\d{2})?)'],
            'eur': [r'€(\d+(?:\.\d{2})?)', r'EUR\s*(\d+(?:\.\d{2})?)'],
            'gbp': [r'£(\d+(?:\.\d{2})?)', r'GBP\s*(\d+(?:\.\d{2})?)', r'(\d+(?:\.\d{2})?)\s*GBP']
        }
        
        for currency, patterns in currency_patterns.items():
            all_prices = []
            for pattern in patterns:
                prices = re.findall(pattern, html_text)
                all_prices.extend([float(p) for p in prices if float(p) > 0.5 and float(p) < 1000])
            
            if all_prices:
                data[f'prices_{currency}'] = ', '.join([str(p) for p in sorted(set(all_prices))])
                data[f'min_price_{currency}'] = min(all_prices)
                data[f'max_price_{currency}'] = max(all_prices)
        
        if any(key.startswith('prices_') for key in data.keys()):
            self.extraction_stats['pricing'] += 1
        return data
    
    def extract_advanced_cannabis_data(self, soup, url):
        data = {}
        html_text = soup.get_text()
        
        # THC extraction
        thc_patterns = [
            r'THC[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*%',
            r'THC[:\s]*(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*%\s*THC'
        ]
        
        for pattern in thc_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2 and match[1]:
                    data['thc_min'] = float(match[0])
                    data['thc_max'] = float(match[1])
                    data['thc_range'] = f"{match[0]}-{match[1]}%"
                else:
                    thc_val = match if isinstance(match, str) else match[0]
                    data['thc_content'] = float(thc_val)
                break
        
        # CBD extraction
        cbd_patterns = [
            r'CBD[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*%',
            r'CBD[:\s]*(\d+(?:\.\d+)?)\s*%'
        ]
        
        for pattern in cbd_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2 and match[1]:
                    data['cbd_min'] = float(match[0])
                    data['cbd_max'] = float(match[1])
                else:
                    cbd_val = match if isinstance(match, str) else match[0]
                    data['cbd_content'] = float(cbd_val)
                break
        
        # Flowering time
        flowering_patterns = [
            r'flowering[:\s]*(\d+)\s*[-–]\s*(\d+)\s*weeks?',
            r'(\d+)\s*weeks?\s*(?:flower|bloom)'
        ]
        
        for pattern in flowering_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2 and match[1]:
                    data['flowering_time'] = f"{match[0]}-{match[1]} weeks"
                else:
                    weeks = match if isinstance(match, str) else match[0]
                    data['flowering_time'] = f"{weeks} weeks"
                break
        
        # Effects
        effects = ['euphoric', 'creative', 'focused', 'relaxing', 'sedating', 'happy', 'energetic', 'calming']
        found_effects = []
        for effect in effects:
            if re.search(rf'\b{effect}\b', html_text, re.IGNORECASE):
                found_effects.append(effect)
        
        if found_effects:
            data['effects_all'] = ', '.join(found_effects)
        
        # Flavors
        flavors = ['lemon', 'berry', 'earthy', 'sweet', 'spicy', 'diesel', 'pine', 'citrus']
        found_flavors = []
        for flavor in flavors:
            if re.search(rf'\b{flavor}\b', html_text, re.IGNORECASE):
                found_flavors.append(flavor)
        
        if found_flavors:
            data['flavors_all'] = ', '.join(found_flavors)
        
        if any(key in data for key in ['thc_content', 'cbd_content', 'flowering_time', 'effects_all']):
            self.extraction_stats['cannabis_data'] += 1
        return data
    
    def extract_media_assets(self, soup):
        data = {}
        images = soup.find_all('img')
        
        image_urls = []
        for img in images:
            src = img.get('src')
            if src and src.startswith('http'):
                image_urls.append(src)
        
        if image_urls:
            data['total_image_count'] = len(image_urls)
            data['product_images'] = ', '.join(image_urls[:5])
            self.extraction_stats['images'] += 1
        
        return data
    
    def extract_awards_and_certifications(self, soup, url):
        data = {}
        html_text = soup.get_text()
        
        award_patterns = [
            r'(cannabis\s+cup[^.\n]{0,60})',
            r'(high\s+times[^.\n]{0,60})',
            r'(\d{4}\s+(?:winner|champion|award)[^.\n]{0,60})'
        ]
        
        awards = []
        for pattern in award_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            for match in matches:
                clean_award = re.sub(r'\s+', ' ', match.strip())
                if len(clean_award) > 5:
                    awards.append(clean_award)
        
        if awards:
            data['awards'] = ' | '.join(awards[:3])
            data['has_awards'] = True
            self.extraction_stats['awards'] += 1
        else:
            data['has_awards'] = False
        
        return data
    
    def extract_enhanced_genetics(self, soup, url):
        data = {}
        html_text = soup.get_text()
        
        genetics_patterns = [
            r'(?:lineage|genetics|cross|parents?)[:\s]*([^.\n]{10,120})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[xX×]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in genetics_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2:
                    data['parent_1'] = match[0].strip()
                    data['parent_2'] = match[1].strip()
                    data['genetics_lineage'] = f"{match[0]} × {match[1]}"
                else:
                    data['genetics_lineage'] = match.strip() if isinstance(match, str) else match[0].strip()
                break
        
        if any(key in data for key in ['genetics_lineage', 'parent_1']):
            self.extraction_stats['genetics'] += 1
        return data
    
    def calculate_comprehensive_quality_score(self, strain_data):
        premium_fields = {
            'thc_min', 'thc_max', 'cbd_content', 'flowering_time', 'genetics_lineage', 'jsonld_price', 'awards'
        }
        
        high_value_fields = {
            'effects_all', 'flavors_all', 'product_images'
        }
        
        standard_fields = {
            'strain_name', 'page_title', 'meta_description', 'jsonld_description', 'total_image_count'
        }
        
        premium_score = sum(10 for field in premium_fields if strain_data.get(field))
        high_value_score = sum(6 for field in high_value_fields if strain_data.get(field))
        standard_score = sum(3 for field in standard_fields if strain_data.get(field))
        
        total_possible = len(premium_fields) * 10 + len(high_value_fields) * 6 + len(standard_fields) * 3
        actual_score = premium_score + high_value_score + standard_score
        
        return round((actual_score / total_possible) * 100, 1)
    
    def determine_market_tier(self, score, strain_data):
        has_cultivation_data = any(strain_data.get(field) for field in ['thc_min', 'flowering_time'])
        has_business_data = any(strain_data.get(field) for field in ['jsonld_price'])
        has_genetics_data = strain_data.get('genetics_lineage') or strain_data.get('parent_1')
        
        if score >= 80 and has_cultivation_data and has_business_data:
            return "Enterprise"
        elif score >= 60 and (has_cultivation_data or has_genetics_data):
            return "Professional"
        elif score >= 40:
            return "Standard"
        else:
            return "Basic"
    
    def maximum_extraction_pipeline(self, html_content, url):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        strain_data = {
            'seed_bank': 'Great Lakes Genetics',
            'breeder_name': 'Great Lakes Genetics',
            'source_url': url,
            'scraped_at': datetime.now().isoformat(),
            'url_domain': urlparse(url).netloc,
            'extraction_version': '2.0'
        }
        
        extraction_methods = [
            ('JSON-LD', self.extract_json_ld_data),
            ('Meta Tags', self.extract_comprehensive_meta_tags),
            ('Tables', self.extract_structured_tables),
            ('Pricing', self.extract_comprehensive_pricing),
            ('Cannabis Data', self.extract_advanced_cannabis_data),
            ('Media Assets', self.extract_media_assets),
            ('Awards', self.extract_awards_and_certifications),
            ('Genetics', self.extract_enhanced_genetics)
        ]
        
        extraction_success = []
        
        for method_name, method_func in extraction_methods:
            try:
                if 'url' in method_func.__code__.co_varnames:
                    method_data = method_func(soup, url)
                else:
                    method_data = method_func(soup)
                
                if method_data:
                    strain_data.update(method_data)
                    extraction_success.append(method_name)
            except Exception as e:
                logger.warning(f"Error in {method_name} extraction: {e}")
                continue
        
        # Fallback strain name
        if not strain_data.get('strain_name') and not strain_data.get('jsonld_product_name'):
            h1 = soup.find('h1')
            if h1:
                strain_name = h1.get_text().strip()
                strain_name = re.sub(r'\s+(Seeds?|Cannabis|Feminized|Auto).*$', '', strain_name, re.IGNORECASE)
                strain_data['strain_name'] = strain_name
        
        if strain_data.get('jsonld_product_name') and not strain_data.get('strain_name'):
            strain_data['strain_name'] = strain_data['jsonld_product_name']
        
        strain_data['extraction_methods_used'] = extraction_success
        strain_data['method_count'] = len(extraction_success)
        strain_data['data_completeness_score'] = self.calculate_comprehensive_quality_score(strain_data)
        strain_data['market_tier'] = self.determine_market_tier(strain_data['data_completeness_score'], strain_data)
        
        non_empty_fields = sum(1 for v in strain_data.values() if v and str(v).strip() and str(v) != 'nan')
        strain_data['total_fields_captured'] = non_empty_fields
        
        return strain_data
    
    def process_all_great_lakes_genetics_strains(self):
        logger.info("Starting Great Lakes Genetics Maximum Extraction Pipeline")
        
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key='index/url_mapping.csv')
            df = pd.read_csv(response['Body'])
            logger.info("Loaded URL mapping from S3")
        except Exception as e:
            logger.warning(f"S3 mapping failed, using local file: {e}")
            df = pd.read_csv('../../01_html_collection/data/unique_urls.csv', encoding='latin-1')
        
        great_lakes_genetics_urls = df[df['url'].str.contains('greatlakesgenetics', na=False)]
        logger.info(f"Found {len(great_lakes_genetics_urls)} Great Lakes Genetics URLs")
        
        logger.info("Scanning S3 for available HTML files...")
        paginator = self.s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.bucket, Prefix='html/')
        
        available_hashes = set()
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    if obj['Key'].endswith('.html'):
                        hash_id = obj['Key'].split('/')[-1].replace('.html', '')
                        available_hashes.add(hash_id)
        
        logger.info(f"Found {len(available_hashes)} HTML files in S3")
        
        all_strains = []
        processed = 0
        
        for idx, row in great_lakes_genetics_urls.iterrows():
            url_hash = row['url_hash']
            url = row['url']
            
            if url_hash not in available_hashes:
                continue
            
            try:
                html_key = f'html/{url_hash}.html'
                response = self.s3.get_object(Bucket=self.bucket, Key=html_key)
                html_content = response['Body'].read().decode('utf-8')
                
                strain_data = self.maximum_extraction_pipeline(html_content, url)
                all_strains.append(strain_data)
                
                processed += 1
                if processed % 5 == 0:
                    logger.info(f"Processed {processed}/{len(great_lakes_genetics_urls)} strains")
                
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                continue
        
        df_results = pd.DataFrame(all_strains)
        
        output_file = 'great_lakes_genetics_maximum_extraction.csv'
        df_results.to_csv(output_file, index=False, encoding='utf-8')
        
        self.generate_extraction_report(df_results, output_file)
        
        logger.info(f"Maximum extraction complete! Processed {len(all_strains)} strains")
        logger.info(f"Dataset saved to: {output_file}")
        logger.info(f"Total columns captured: {len(df_results.columns)}")
        
        return df_results
    
    def generate_extraction_report(self, df, output_file):
        report = f"""# Great Lakes Genetics Maximum Extraction Report

**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Processor:** Great Lakes Genetics Maximum Value Extractor  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Extraction Summary

### Success Metrics
- **Total Strains Extracted:** {len(df)}
- **Total Columns Captured:** {len(df.columns)}
- **Average Fields per Strain:** {df['total_fields_captured'].mean():.1f}
- **Maximum Fields Captured:** {df['total_fields_captured'].max()}
- **Average Quality Score:** {df['data_completeness_score'].mean():.1f}%

### Market Tier Distribution
{df['market_tier'].value_counts().to_string()}

---

**Processing completed with maximum data extraction methodology.**  
**Logic designed by Amazon Q, verified by Shannon Goddard.**
"""
        
        with open('great_lakes_genetics_extraction_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info("Comprehensive extraction report generated")

def main():
    extractor = GreatLakesGeneticsMaxExtractor()
    df = extractor.process_all_great_lakes_genetics_strains()
    
    print(f"\nGREAT LAKES GENETICS MAXIMUM EXTRACTION COMPLETE!")
    print(f"Dataset: {len(df)} strains x {len(df.columns)} columns")
    print(f"Average Quality: {df['data_completeness_score'].mean():.1f}%")
    print(f"Market Tiers: {df['market_tier'].value_counts().to_dict()}")
    print(f"Top Quality: {df['data_completeness_score'].max():.1f}%")

if __name__ == "__main__":
    main()