#!/usr/bin/env python3
"""
Amsterdam Marijuana Seeds Maximum Data Extractor
9-method extraction pipeline for comprehensive data capture
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
from datetime import datetime
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AmsterdamMaxExtractor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
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
                            'jsonld_sku': json_data.get('sku')
                        })
                        offers = json_data.get('offers', {})
                        if isinstance(offers, dict):
                            data.update({
                                'jsonld_price': offers.get('price'),
                                'jsonld_currency': offers.get('priceCurrency'),
                                'jsonld_availability': offers.get('availability')
                            })
                except:
                    continue
        if data:
            self.extraction_stats['json_ld'] += 1
        return data
    
    def extract_meta_tags(self, soup):
        data = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                field_name = re.sub(r'[^a-z0-9_]', '_', name.lower())
                data[f'meta_{field_name}'] = content
        title_tag = soup.find('title')
        if title_tag:
            data['page_title'] = title_tag.get_text().strip()
        if data:
            self.extraction_stats['meta_tags'] += 1
        return data
    
    def extract_amsterdam_specific_data(self, soup):
        """Extract Amsterdam-specific ams-attr-table data"""
        data = {}
        ams_table = soup.find('div', class_='ams-attr-table')
        if ams_table:
            rows = ams_table.find_all('div', class_='ams-attr-row')
            for row in rows:
                label_div = row.find('div', class_='ams-attr-label')
                value_div = row.find('div', class_='ams-attr-value')
                if label_div and value_div:
                    key = re.sub(r'[^a-z0-9_]', '_', label_div.get_text().strip().lower()).strip('_')
                    value = value_div.get_text().strip()
                    if key and value:
                        data[f'spec_{key}'] = value
        if data:
            self.extraction_stats['tables'] += 1
        return data
    
    def extract_tables(self, soup):
        data = {}
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = re.sub(r'[^a-z0-9_]', '_', cells[0].get_text().strip().lower()).strip('_')
                    value = cells[1].get_text().strip()
                    if key and value and len(value) < 200:
                        data[f'spec_{key}'] = value
        if data:
            self.extraction_stats['tables'] += 1
        return data
    
    def extract_pricing(self, soup):
        data = {}
        html_text = soup.get_text()
        currency_patterns = {
            'usd': [r'\$(\d+(?:\.\d{2})?)', r'USD\s*(\d+(?:\.\d{2})?)'],
            'eur': [r'€(\d+(?:\.\d{2})?)', r'EUR\s*(\d+(?:\.\d{2})?)']
        }
        for currency, patterns in currency_patterns.items():
            all_prices = []
            for pattern in patterns:
                prices = re.findall(pattern, html_text)
                all_prices.extend([float(p) for p in prices if 0.5 < float(p) < 1000])
            if all_prices:
                data[f'prices_{currency}'] = ', '.join([str(p) for p in sorted(set(all_prices))])
                data[f'min_price_{currency}'] = min(all_prices)
                data[f'max_price_{currency}'] = max(all_prices)
                data[f'avg_price_{currency}'] = round(sum(all_prices) / len(all_prices), 2)
        if any(key.startswith('prices_') for key in data.keys()):
            self.extraction_stats['pricing'] += 1
        return data
    
    def extract_cannabis_data(self, soup):
        data = {}
        html_text = soup.get_text()
        
        # THC
        thc_patterns = [
            r'THC[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*%',
            r'THC[:\s]*(\d+(?:\.\d+)?)\s*%'
        ]
        for pattern in thc_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2 and match[1]:
                    data['thc_min'] = float(match[0])
                    data['thc_max'] = float(match[1])
                    data['thc_range'] = f"{match[0]}-{match[1]}%"
                    data['thc_average'] = round((float(match[0]) + float(match[1])) / 2, 1)
                else:
                    thc_val = match if isinstance(match, str) else match[0]
                    data['thc_content'] = float(thc_val)
                break
        
        # CBD
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
        
        # Effects
        effects = ['euphoric', 'creative', 'focused', 'uplifting', 'relaxing', 'sedating', 'happy', 'energetic']
        found_effects = [e for e in effects if re.search(rf'\b{e}\b', html_text, re.IGNORECASE)]
        if found_effects:
            data['effects_all'] = ', '.join(found_effects)
            data['primary_effect'] = found_effects[0]
        
        # Flavors
        flavors = ['lemon', 'berry', 'earthy', 'sweet', 'spicy', 'diesel', 'pine', 'citrus']
        found_flavors = [f for f in flavors if re.search(rf'\b{f}\b', html_text, re.IGNORECASE)]
        if found_flavors:
            data['flavors_all'] = ', '.join(found_flavors)
            data['primary_flavor'] = found_flavors[0]
        
        if any(key in data for key in ['thc_content', 'effects_all']):
            self.extraction_stats['cannabis_data'] += 1
        return data
    
    def extract_media(self, soup):
        data = {}
        images = soup.find_all('img')
        product_images = []
        for img in images:
            src = img.get('src')
            if src and any(term in src.lower() for term in ['product', 'seed', 'strain']):
                product_images.append(src)
        if product_images:
            data['product_images'] = ', '.join(product_images[:5])
            data['total_image_count'] = len(product_images)
            self.extraction_stats['images'] += 1
        return data
    
    def extract_awards(self, soup):
        data = {}
        html_text = soup.get_text()
        award_patterns = [
            r'(cannabis\s+cup[^.\n]{0,60})',
            r'(high\s+times[^.\n]{0,60})',
            r'(\d{4}\s+(?:winner|award)[^.\n]{0,60})'
        ]
        awards = []
        for pattern in award_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            awards.extend([re.sub(r'\s+', ' ', m.strip()) for m in matches if len(m.strip()) > 5])
        if awards:
            data['awards'] = ' | '.join(awards[:5])
            data['has_awards'] = True
            self.extraction_stats['awards'] += 1
        else:
            data['has_awards'] = False
        return data
    
    def extract_genetics(self, soup):
        data = {}
        html_text = soup.get_text()
        genetics_patterns = [
            r'(?:lineage|genetics|cross)[:\s]*([^.\n]{10,120})',
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
        
        # Indica/Sativa
        ratio_patterns = [
            r'(\d+)%\s*indica[^0-9]*(\d+)%\s*sativa',
            r'(\d+)%\s*sativa[^0-9]*(\d+)%\s*indica'
        ]
        for pattern in ratio_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if 'indica' in pattern.split(')')[0]:
                    data['indica_percentage'] = int(match[0])
                    data['sativa_percentage'] = int(match[1])
                else:
                    data['sativa_percentage'] = int(match[0])
                    data['indica_percentage'] = int(match[1])
                
                if data['indica_percentage'] > data['sativa_percentage']:
                    data['dominant_type'] = 'Indica'
                elif data['sativa_percentage'] > data['indica_percentage']:
                    data['dominant_type'] = 'Sativa'
                else:
                    data['dominant_type'] = 'Balanced Hybrid'
                break
        
        if any(key in data for key in ['genetics_lineage', 'indica_percentage']):
            self.extraction_stats['genetics'] += 1
        return data
    
    def calculate_quality_score(self, strain_data):
        premium_fields = {'thc_min', 'thc_max', 'genetics_lineage', 'jsonld_price', 'indica_percentage'}
        high_value_fields = {'effects_all', 'flavors_all', 'product_images'}
        standard_fields = {'strain_name', 'page_title', 'meta_description'}
        
        premium_score = sum(10 for field in premium_fields if strain_data.get(field))
        high_value_score = sum(6 for field in high_value_fields if strain_data.get(field))
        standard_score = sum(3 for field in standard_fields if strain_data.get(field))
        
        total_possible = len(premium_fields) * 10 + len(high_value_fields) * 6 + len(standard_fields) * 3
        actual_score = premium_score + high_value_score + standard_score
        
        return round((actual_score / total_possible) * 100, 1)
    
    def determine_market_tier(self, score):
        if score >= 80:
            return "Enterprise"
        elif score >= 60:
            return "Professional"
        elif score >= 40:
            return "Standard"
        else:
            return "Basic"
    
    def maximum_extraction_pipeline(self, html_content, url):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        strain_data = {
            'seed_bank': 'Amsterdam Marijuana Seeds',
            'source_url': url,
            'scraped_at': datetime.now().isoformat(),
            'url_domain': urlparse(url).netloc,
            'extraction_version': '1.0'
        }
        
        extraction_methods = [
            ('Amsterdam Specific', self.extract_amsterdam_specific_data),
            ('JSON-LD', self.extract_json_ld_data),
            ('Meta Tags', self.extract_meta_tags),
            ('Tables', self.extract_tables),
            ('Pricing', self.extract_pricing),
            ('Cannabis Data', self.extract_cannabis_data),
            ('Media Assets', self.extract_media),
            ('Awards', self.extract_awards),
            ('Genetics', self.extract_genetics)
        ]
        
        extraction_success = []
        for method_name, method_func in extraction_methods:
            try:
                method_data = method_func(soup)
                if method_data:
                    strain_data.update(method_data)
                    extraction_success.append(method_name)
            except Exception as e:
                logger.warning(f"Error in {method_name}: {e}")
                continue
        
        # Extract strain name
        if not strain_data.get('strain_name'):
            h1 = soup.find('h1')
            title_elem = soup.find('title')
            for elem in [h1, title_elem]:
                if elem:
                    strain_name = elem.get_text().strip()
                    strain_name = re.sub(r'\s+(Seeds?|Cannabis|Feminized|Auto).*$', '', strain_name, re.IGNORECASE)
                    if len(strain_name) > 3:
                        strain_data['strain_name'] = strain_name
                        break
        
        if strain_data.get('jsonld_product_name') and not strain_data.get('strain_name'):
            strain_data['strain_name'] = strain_data['jsonld_product_name']
        
        strain_data['extraction_methods_used'] = extraction_success
        strain_data['method_count'] = len(extraction_success)
        strain_data['data_completeness_score'] = self.calculate_quality_score(strain_data)
        strain_data['market_tier'] = self.determine_market_tier(strain_data['data_completeness_score'])
        strain_data['total_fields_captured'] = sum(1 for v in strain_data.values() if v and str(v).strip())
        
        return strain_data
    
    def process_amsterdam_strains(self, limit: Optional[int] = None):
        logger.info("Starting Amsterdam Marijuana Seeds extraction")
        
        # Load URLs from existing CSV
        csv_path = '../../../csv/amsterdam_marijuana_maximum_extraction.csv'
        try:
            df_urls = pd.read_csv(csv_path, encoding='utf-8')
            logger.info(f"Loaded {len(df_urls)} URLs from CSV")
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            return pd.DataFrame()
        
        if limit:
            df_urls = df_urls.head(limit)
        
        # Get available HTML files
        paginator = self.s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix='html/')
        
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
        
        for idx, row in df_urls.iterrows():
            url = row['url']
            # Generate hash from URL
            import hashlib
            url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
            
            if url_hash not in available_hashes:
                continue
            
            try:
                html_key = f'html/{url_hash}.html'
                response = self.s3_client.get_object(Bucket=self.bucket_name, Key=html_key)
                html_content = response['Body'].read().decode('utf-8')
                
                strain_data = self.maximum_extraction_pipeline(html_content, url)
                all_strains.append(strain_data)
                
                processed += 1
                if processed % 50 == 0:
                    logger.info(f"Processed {processed}/{len(df_urls)} strains")
                
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                continue
        
        df_results = pd.DataFrame(all_strains)
        
        # Handle empty dataframe
        if len(df_results) == 0:
            logger.warning("No strains extracted - check URL pattern")
            return df_results
        
        output_file = 'amsterdam_maximum_extraction.csv'
        df_results.to_csv(output_file, index=False, encoding='utf-8')
        
        # Generate sample
        sample_file = 'amsterdam_maximum_extraction_sample.csv'
        df_results.head(10).to_csv(sample_file, index=False, encoding='utf-8')
        
        self.generate_report(df_results, output_file)
        
        logger.info(f"Extraction complete! Processed {len(all_strains)} strains")
        logger.info(f"Dataset saved to: {output_file}")
        
        return df_results
    
    def generate_report(self, df, output_file):
        if len(df) == 0:
            logger.warning("Empty dataframe - skipping report generation")
            return
        
        report = f"""# Amsterdam Marijuana Seeds Maximum Extraction Report

**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Extraction Summary

### Success Metrics
- **Total Strains Extracted:** {len(df)}
- **Total Columns Captured:** {len(df.columns)}
- **Average Fields per Strain:** {df['total_fields_captured'].mean():.1f}
- **Average Quality Score:** {df['data_completeness_score'].mean():.1f}%

### Market Tier Distribution
{df['market_tier'].value_counts().to_string()}

### Extraction Method Success Rates
- **JSON-LD:** {self.extraction_stats['json_ld']} strains ({self.extraction_stats['json_ld']/len(df)*100:.1f}%)
- **Meta Tags:** {self.extraction_stats['meta_tags']} strains ({self.extraction_stats['meta_tags']/len(df)*100:.1f}%)
- **Tables:** {self.extraction_stats['tables']} strains ({self.extraction_stats['tables']/len(df)*100:.1f}%)
- **Pricing:** {self.extraction_stats['pricing']} strains ({self.extraction_stats['pricing']/len(df)*100:.1f}%)
- **Cannabis Data:** {self.extraction_stats['cannabis_data']} strains ({self.extraction_stats['cannabis_data']/len(df)*100:.1f}%)
- **Media Assets:** {self.extraction_stats['images']} strains ({self.extraction_stats['images']/len(df)*100:.1f}%)
- **Awards:** {self.extraction_stats['awards']} strains ({self.extraction_stats['awards']/len(df)*100:.1f}%)
- **Genetics:** {self.extraction_stats['genetics']} strains ({self.extraction_stats['genetics']/len(df)*100:.1f}%)

## Top Performing Strains
{df.nlargest(10, 'data_completeness_score')[['strain_name', 'data_completeness_score', 'market_tier']].to_string(index=False)}

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
"""
        
        with open('amsterdam_extraction_report.md', 'w', encoding='utf-8') as f:
            f.write(report)

def main():
    extractor = AmsterdamMaxExtractor()
    df = extractor.process_amsterdam_strains()
    
    if len(df) > 0:
        print(f"\nAMSTERDAM MARIJUANA SEEDS EXTRACTION COMPLETE!")
        print(f"Dataset: {len(df)} strains x {len(df.columns)} columns")
        print(f"Average Quality: {df['data_completeness_score'].mean():.1f}%")
        print(f"Market Tiers: {df['market_tier'].value_counts().to_dict()}")
    else:
        print("\nNo strains extracted - check logs for errors")

if __name__ == "__main__":
    main()
