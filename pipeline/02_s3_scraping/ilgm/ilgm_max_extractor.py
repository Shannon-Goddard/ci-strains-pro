#!/usr/bin/env python3
"""
ILGM Maximum Value Extractor - Production Grade
Comprehensive data extraction for maximum market value
Logic designed by Amazon Q, verified by Shannon Goddard.

This processor captures 50+ data points per strain including:
- Business Intelligence (pricing, availability, SKUs)
- Cultivation Data (THC/CBD, flowering, yield, genetics)
- Market Intelligence (awards, images, certifications)
- Enhanced Cannabis Data (effects, terpenes, flavors)
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ILGMMaxExtractor:
    def __init__(self, s3_bucket='ci-strains-html-archive'):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        self.processed_count = 0
        self.success_count = 0
        self.extraction_stats = {
            'json_ld': 0, 'meta_tags': 0, 'tables': 0, 'pricing': 0,
            'cannabis_data': 0, 'images': 0, 'awards': 0, 'genetics': 0
        }
        
    def extract_ilgm_strain_profile(self, soup):
        """Extract ILGM Strain Profile table data"""
        data = {}
        
        # Find Strain Profile section
        profile_section = soup.find('h2', id='strain-profile')
        if not profile_section:
            return data
        
        # Find the table after the h2
        table = profile_section.find_next('table')
        if not table:
            return data
        
        # Parse all rows
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].get_text().strip()
                value = cells[1].get_text().strip()
                
                # Map to standardized field names
                field_map = {
                    'Plant Type': 'plant_type',
                    'Genotype': 'genotype',
                    'Lineage': 'genetics_lineage',
                    'Effects': 'effects_all',
                    'Yield Potential': 'yield_potential',
                    'Taste and Aroma': 'flavors_all',
                    'THC Level': 'thc_level',
                    'THC Percentage': 'thc_percentage',
                    'CBD Level': 'cbd_level',
                    'CBD Percentage': 'cbd_percentage',
                    'CBG Level': 'cbg_level',
                    'CBG Percentage': 'cbg_percentage',
                    'Difficulty': 'grow_difficulty',
                    'Climate': 'climate',
                    'Terpenes': 'terpenes',
                    'Bud Structure': 'bud_structure',
                    'Optimal Growing Temperature': 'optimal_temperature',
                    'Optimal Humidity Level': 'optimal_humidity',
                    'Flowering Time Indoor': 'flowering_time_indoor',
                    'Flowering Time Outdoor': 'flowering_time_outdoor',
                    'Vegetative Stage': 'vegetative_stage',
                    'Harvest Height': 'harvest_height',
                    'Original Genetics Developed By': 'original_breeder',
                    'Brand': 'brand',
                    'SKU': 'sku'
                }
                
                if key in field_map:
                    data[field_map[key]] = value
                    
                    # Parse lineage for parent strains
                    if key == 'Lineage' and ' x ' in value:
                        parts = value.split(' x ')
                        if len(parts) == 2:
                            data['parent_1'] = parts[0].strip()
                            data['parent_2'] = parts[1].strip()
                    
                    # Parse flowering time for min/max
                    if key == 'Flowering Time Indoor':
                        match = re.search(r'(\d+)-(\d+)\s*days?', value)
                        if match:
                            data['flowering_min'] = int(match.group(1))
                            data['flowering_max'] = int(match.group(2))
                            data['flowering_time'] = f"{int(match.group(1))//7}-{int(match.group(2))//7} weeks"
                    
                    # Parse THC percentage
                    if key == 'THC Percentage' and value.isdigit():
                        data['thc_content'] = float(value)
                        data['thc_min'] = data['thc_max'] = float(value)
                    
                    # Parse CBD percentage
                    if key == 'CBD Percentage' and value.isdigit():
                        data['cbd_content'] = float(value)
        
        return data
    
    def extract_json_ld_data(self, soup):
        """Extract structured JSON-LD data - Premium business intelligence"""
        data = {}
        json_scripts = soup.find_all('script', type='application/ld+json')
        
        for script in json_scripts:
            if script.string:
                try:
                    json_data = json.loads(script.string)
                    
                    # Product schema extraction
                    if json_data.get('@type') == 'Product':
                        data.update({
                            'jsonld_product_name': json_data.get('name'),
                            'jsonld_description': json_data.get('description'),
                            'jsonld_brand': json_data.get('brand', {}).get('name') if isinstance(json_data.get('brand'), dict) else json_data.get('brand'),
                            'jsonld_sku': json_data.get('sku'),
                            'jsonld_mpn': json_data.get('mpn'),
                            'jsonld_gtin': json_data.get('gtin13') or json_data.get('gtin'),
                            'jsonld_category': json_data.get('category'),
                            'jsonld_image_url': json_data.get('image')
                        })
                        
                        # Offers/pricing extraction
                        offers = json_data.get('offers', {})
                        if isinstance(offers, dict):
                            data.update({
                                'jsonld_price': offers.get('price'),
                                'jsonld_currency': offers.get('priceCurrency'),
                                'jsonld_availability': offers.get('availability'),
                                'jsonld_price_valid_until': offers.get('priceValidUntil'),
                                'jsonld_seller': offers.get('seller', {}).get('name') if isinstance(offers.get('seller'), dict) else None
                            })
                        
                        # Aggregate rating
                        rating = json_data.get('aggregateRating', {})
                        if rating:
                            data.update({
                                'jsonld_rating_value': rating.get('ratingValue'),
                                'jsonld_rating_count': rating.get('ratingCount'),
                                'jsonld_best_rating': rating.get('bestRating'),
                                'jsonld_worst_rating': rating.get('worstRating')
                            })
                    
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    logger.warning(f"JSON-LD parsing error: {e}")
                    continue
        
        if data:
            self.extraction_stats['json_ld'] += 1
        return data
    
    def extract_comprehensive_meta_tags(self, soup):
        """Extract all meta tag data - SEO and social intelligence"""
        data = {}
        meta_tags = soup.find_all('meta')
        
        for meta in meta_tags:
            name = meta.get('name') or meta.get('property') or meta.get('itemprop')
            content = meta.get('content')
            
            if name and content:
                # Clean and standardize field names
                field_name = name.replace(':', '_').replace('og:', '').replace('twitter:', '').lower()
                field_name = re.sub(r'[^a-z0-9_]', '_', field_name)
                data[f'meta_{field_name}'] = content
        
        # Extract title separately
        title_tag = soup.find('title')
        if title_tag:
            data['page_title'] = title_tag.get_text().strip()
        
        if data:
            self.extraction_stats['meta_tags'] += 1
        return data
    
    def extract_structured_tables(self, soup):
        """Extract all table data - Specification intelligence"""
        data = {}
        tables = soup.find_all('table')
        
        for i, table in enumerate(tables):
            rows = table.find_all('tr')
            table_data = {}
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text().strip().lower()
                    value = cells[1].get_text().strip()
                    
                    # Clean and standardize keys
                    key = re.sub(r'[^a-z0-9_]', '_', key).strip('_')
                    if key and value and len(value) < 200:
                        table_data[key] = value
            
            # Add table data with prefixes
            for key, value in table_data.items():
                data[f'spec_{key}'] = value
        
        if data:
            self.extraction_stats['tables'] += 1
        return data
    
    def extract_comprehensive_pricing(self, soup, url):
        """Extract all pricing data - Business intelligence"""
        data = {}
        html_text = soup.get_text()
        
        # Multiple currency extraction
        currency_patterns = {
            'usd': [r'\$(\d+(?:\.\d{2})?)', r'USD\s*(\d+(?:\.\d{2})?)'],
            'eur': [r'€(\d+(?:\.\d{2})?)', r'EUR\s*(\d+(?:\.\d{2})?)'],
            'gbp': [r'£(\d+(?:\.\d{2})?)', r'GBP\s*(\d+(?:\.\d{2})?)']}
        
        for currency, patterns in currency_patterns.items():
            all_prices = []
            for pattern in patterns:
                prices = re.findall(pattern, html_text)
                all_prices.extend([float(p) for p in prices if float(p) > 0.5 and float(p) < 1000])
            
            if all_prices:
                data[f'prices_{currency}'] = ', '.join([str(p) for p in sorted(set(all_prices))])
                data[f'min_price_{currency}'] = min(all_prices)
                data[f'max_price_{currency}'] = max(all_prices)
                data[f'avg_price_{currency}'] = round(sum(all_prices) / len(all_prices), 2)
                data[f'price_count_{currency}'] = len(all_prices)
        
        # Package size extraction
        package_patterns = [
            r'(\d+)\s*seeds?\s*pack',
            r'(\d+)\s*seeds?',
            r'pack\s*of\s*(\d+)',
            r'(\d+)x\s*seeds?'
        ]
        
        package_sizes = []
        for pattern in package_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            package_sizes.extend([int(m) for m in matches if 1 <= int(m) <= 100])
        
        if package_sizes:
            unique_sizes = sorted(set(package_sizes))
            data['package_sizes'] = ', '.join([str(s) for s in unique_sizes])
            data['min_package_size'] = min(unique_sizes)
            data['max_package_size'] = max(unique_sizes)
        
        if any(key.startswith('prices_') for key in data.keys()):
            self.extraction_stats['pricing'] += 1
        return data
    
    def extract_advanced_cannabis_data(self, soup, url):
        """Extract comprehensive cannabis-specific data"""
        data = {}
        html_text = soup.get_text()
        
        # Advanced THC extraction
        thc_patterns = [
            r'THC[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*%',
            r'THC[:\s]*(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*%\s*THC',
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
                    data['thc_average'] = round((float(match[0]) + float(match[1])) / 2, 1)
                else:
                    thc_val = match if isinstance(match, str) else match[0]
                    data['thc_content'] = float(thc_val)
                    data['thc_min'] = data['thc_max'] = float(thc_val)
                break
        
        # Advanced CBD extraction
        cbd_patterns = [
            r'CBD[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*%',
            r'CBD[:\s]*(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*%\s*CBD'
        ]
        
        for pattern in cbd_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2 and match[1]:
                    data['cbd_min'] = float(match[0])
                    data['cbd_max'] = float(match[1])
                    data['cbd_range'] = f"{match[0]}-{match[1]}%"
                else:
                    cbd_val = match if isinstance(match, str) else match[0]
                    data['cbd_content'] = float(cbd_val)
                break
        
        # Flowering time extraction
        flowering_patterns = [
            r'flowering[:\s]*(\d+)\s*[-–]\s*(\d+)\s*weeks?',
            r'(\d+)\s*[-–]\s*(\d+)\s*weeks?\s*(?:flower|bloom)',
            r'flowering[:\s]*(\d+)\s*weeks?',
            r'(\d+)\s*weeks?\s*(?:flower|bloom)'
        ]
        
        for pattern in flowering_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2 and match[1]:
                    data['flowering_min'] = int(match[0])
                    data['flowering_max'] = int(match[1])
                    data['flowering_time'] = f"{match[0]}-{match[1]} weeks"
                else:
                    weeks = match if isinstance(match, str) else match[0]
                    data['flowering_time'] = f"{weeks} weeks"
                    data['flowering_min'] = data['flowering_max'] = int(weeks)
                break
        
        # Yield extraction
        yield_patterns = [
            r'yield[:\s]*(\d+)\s*[-–]\s*(\d+)\s*(g|grams?|oz|ounces?)',
            r'yield[:\s]*(\d+)\s*(g|grams?|oz|ounces?)',
            r'(\d+)\s*[-–]\s*(\d+)\s*(g|grams?|oz).*yield',
            r'(\d+)\s*(g|grams?|oz).*yield'
        ]
        
        for pattern in yield_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if len(match) == 3 and match[1]:  # Range with unit
                    data['yield_min'] = int(match[0])
                    data['yield_max'] = int(match[1])
                    data['yield_unit'] = match[2]
                    data['yield_range'] = f"{match[0]}-{match[1]} {match[2]}"
                elif len(match) == 2:  # Single value with unit
                    data['yield_amount'] = int(match[0])
                    data['yield_unit'] = match[1]
                break
        
        # Effects extraction
        effect_categories = {
            'mental': ['euphoric', 'creative', 'focused', 'uplifting', 'cerebral', 'energetic', 'happy'],
            'physical': ['relaxing', 'sedating', 'body', 'tingly', 'sleepy', 'calming'],
            'appetite': ['hungry', 'munchies'],
            'social': ['talkative', 'sociable']
        }
        
        found_effects = {'all': []}
        for category, effects in effect_categories.items():
            category_effects = []
            for effect in effects:
                if re.search(rf'\b{effect}\b', html_text, re.IGNORECASE):
                    category_effects.append(effect)
                    found_effects['all'].append(effect)
            if category_effects:
                found_effects[category] = category_effects
        
        if found_effects['all']:
            data['effects_all'] = ', '.join(found_effects['all'])
            data['primary_effect'] = found_effects['all'][0]
            
            for category, effects in found_effects.items():
                if category != 'all' and effects:
                    data[f'effects_{category}'] = ', '.join(effects)
        
        if any(key in data for key in ['thc_content', 'cbd_content', 'flowering_time', 'effects_all']):
            self.extraction_stats['cannabis_data'] += 1
        return data
    
    def extract_media_assets(self, soup):
        """Extract comprehensive media and image data"""
        data = {}
        images = soup.find_all('img')
        
        image_urls = []
        for img in images:
            src = img.get('src')
            if src and src.startswith('http'):
                image_urls.append(src)
        
        if image_urls:
            data['product_images'] = ', '.join(image_urls[:10])  # Top 10 images
            data['total_image_count'] = len(image_urls)
        
        if data:
            self.extraction_stats['images'] += 1
        return data
    
    def extract_awards_and_certifications(self, soup, url):
        """Extract comprehensive awards, certifications, and recognition"""
        data = {}
        html_text = soup.get_text()
        
        # Award pattern extraction
        award_patterns = [
            r'(cannabis\s+cup[^.\n]{0,60})',
            r'(high\s+times[^.\n]{0,60})',
            r'(\d{4}\s+(?:winner|champion|award)[^.\n]{0,60})',
            r'(1st\s+(?:place|prize)[^.\n]{0,40})',
            r'(award\s+winner[^.\n]{0,40})'
        ]
        
        awards = []
        for pattern in award_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            for match in matches:
                clean_award = re.sub(r'\s+', ' ', match.strip())
                if len(clean_award) > 5:
                    awards.append(clean_award)
        
        if awards:
            data['awards'] = ' | '.join(awards[:5])  # Top 5 awards
            data['award_count'] = len(awards)
            data['has_awards'] = True
        else:
            data['has_awards'] = False
        
        if data.get('has_awards'):
            self.extraction_stats['awards'] += 1
        return data
    
    def extract_enhanced_genetics(self, soup, url):
        """Extract comprehensive genetics and lineage data"""
        data = {}
        html_text = soup.get_text()
        
        # Enhanced genetics patterns
        genetics_patterns = [
            r'(?:lineage|genetics|cross|parents?)[:\s]*([^.\n]{10,120})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[xX×]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'bred\s+from[:\s]*([^.\n]{10,100})',
            r'combination\s+of[:\s]*([^.\n]{10,100})'
        ]
        
        for pattern in genetics_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple) and len(match) == 2:
                    data['parent_1'] = match[0].strip()
                    data['parent_2'] = match[1].strip()
                    data['genetics_lineage'] = f"{match[0]} × {match[1]}"
                    data['is_hybrid'] = True
                else:
                    genetics_text = match.strip() if isinstance(match, str) else match[0].strip()
                    data['genetics_lineage'] = genetics_text
                    data['is_hybrid'] = 'x' in genetics_text.lower() or '×' in genetics_text
                break
        
        # Indica/Sativa ratio extraction
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
                
                # Determine dominant type
                if data['indica_percentage'] > data['sativa_percentage']:
                    data['dominant_type'] = 'Indica'
                elif data['sativa_percentage'] > data['indica_percentage']:
                    data['dominant_type'] = 'Sativa'
                else:
                    data['dominant_type'] = 'Balanced Hybrid'
                break
        
        if any(key in data for key in ['genetics_lineage', 'parent_1', 'indica_percentage']):
            self.extraction_stats['genetics'] += 1
        return data
    
    def calculate_comprehensive_quality_score(self, strain_data):
        """Calculate weighted quality score based on data completeness and value"""
        
        # Premium data fields (highest weight)
        premium_fields = {
            'thc_min', 'thc_max', 'cbd_content', 'flowering_time', 'yield_range',
            'genetics_lineage', 'jsonld_price', 'awards', 'indica_percentage'
        }
        
        # High value fields
        high_value_fields = {
            'effects_all', 'package_sizes', 'original_breeder', 'product_images'
        }
        
        # Standard fields
        standard_fields = {
            'strain_name', 'page_title', 'meta_description', 'jsonld_description'
        }
        
        # Calculate weighted score
        premium_score = sum(10 for field in premium_fields if strain_data.get(field))
        high_value_score = sum(6 for field in high_value_fields if strain_data.get(field))
        standard_score = sum(3 for field in standard_fields if strain_data.get(field))
        
        total_possible = len(premium_fields) * 10 + len(high_value_fields) * 6 + len(standard_fields) * 3
        actual_score = premium_score + high_value_score + standard_score
        
        return round((actual_score / total_possible) * 100, 1)
    
    def determine_market_tier(self, score, strain_data):
        """Determine market tier based on data completeness"""
        
        # Check for premium indicators
        has_cultivation_data = any(strain_data.get(field) for field in ['thc_min', 'flowering_time', 'yield_range'])
        has_business_data = any(strain_data.get(field) for field in ['jsonld_price', 'package_sizes'])
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
        """Complete extraction pipeline - all methods"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Initialize with core data
        strain_data = {
            'seed_bank': 'ILGM',
            'breeder_name': 'ILGM',
            'source_url': url,
            'scraped_at': datetime.now().isoformat(),
            'url_domain': urlparse(url).netloc,
            'extraction_version': '2.0'
        }
        
        # Apply all extraction methods
        extraction_methods = [
            ('ILGM Strain Profile', self.extract_ilgm_strain_profile),
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
        
        # Fallback strain name extraction
        if not strain_data.get('strain_name') and not strain_data.get('jsonld_product_name'):
            h1 = soup.find('h1')
            if h1:
                strain_name = h1.get_text().strip()
                strain_name = re.sub(r'\s+(Seeds?|Cannabis|Feminized|Auto).*$', '', strain_name, re.IGNORECASE)
                strain_data['strain_name'] = strain_name
        
        # Use JSON-LD name if available
        if strain_data.get('jsonld_product_name') and not strain_data.get('strain_name'):
            strain_data['strain_name'] = strain_data['jsonld_product_name']
        
        # Calculate quality metrics
        strain_data['extraction_methods_used'] = extraction_success
        strain_data['method_count'] = len(extraction_success)
        strain_data['data_completeness_score'] = self.calculate_comprehensive_quality_score(strain_data)
        strain_data['market_tier'] = self.determine_market_tier(strain_data['data_completeness_score'], strain_data)
        
        # Count non-empty fields
        non_empty_fields = sum(1 for v in strain_data.values() if v and str(v).strip() and str(v) != 'nan')
        strain_data['total_fields_captured'] = non_empty_fields
        
        return strain_data
    
    def process_all_ilgm_strains(self):
        """Process all ILGM strains with maximum extraction"""
        
        logger.info("Starting ILGM Maximum Extraction Pipeline")
        
        # Load URL mapping from local file
        df = pd.read_csv('../../01_html_collection/original_html_collection/data/unique_urls.csv', encoding='latin-1')
        logger.info("Loaded URL mapping from local file")
        
        ilgm_urls = df[df['url'].str.contains('ilgm.com', na=False)]
        logger.info(f"Found {len(ilgm_urls)} ILGM URLs")
        
        # Get available HTML files
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
        
        # Process strains
        all_strains = []
        processed = 0
        
        for idx, row in ilgm_urls.iterrows():
            url_hash = row['url_hash']
            url = row['url']
            
            if url_hash not in available_hashes:
                logger.debug(f"HTML not found for {url_hash}")
                continue
            
            try:
                # Get HTML from S3
                html_key = f'html/{url_hash}.html'
                response = self.s3.get_object(Bucket=self.bucket, Key=html_key)
                html_content = response['Body'].read().decode('utf-8')
                
                # Extract strain data
                strain_data = self.maximum_extraction_pipeline(html_content, url)
                all_strains.append(strain_data)
                
                processed += 1
                strain_name = strain_data.get('strain_name') or strain_data.get('jsonld_product_name') or 'Unknown'
                
                if processed % 10 == 0:
                    logger.info(f"Processed {processed}/{len(ilgm_urls)} strains")
                
                logger.debug(f"Extracted {strain_data['total_fields_captured']} fields from {strain_name}")
                
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                continue
        
        # Create comprehensive dataset
        df_results = pd.DataFrame(all_strains)
        
        # Save main dataset
        output_file = 'ilgm_maximum_extraction.csv'
        df_results.to_csv(output_file, index=False, encoding='utf-8')
        
        # Generate summary report
        self.generate_extraction_report(df_results, output_file)
        
        logger.info(f"Maximum extraction complete! Processed {len(all_strains)} strains")
        logger.info(f"Dataset saved to: {output_file}")
        logger.info(f"Total columns captured: {len(df_results.columns)}")
        
        return df_results
    
    def generate_extraction_report(self, df, output_file):
        """Generate comprehensive extraction report"""
        
        report = f"""# ILGM Maximum Extraction Report

**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Processor:** ILGM Maximum Value Extractor  
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

### Extraction Method Success Rates
- **JSON-LD Extraction:** {self.extraction_stats['json_ld']} strains ({self.extraction_stats['json_ld']/len(df)*100:.1f}%)
- **Meta Tags:** {self.extraction_stats['meta_tags']} strains ({self.extraction_stats['meta_tags']/len(df)*100:.1f}%)
- **Table Data:** {self.extraction_stats['tables']} strains ({self.extraction_stats['tables']/len(df)*100:.1f}%)
- **Pricing Data:** {self.extraction_stats['pricing']} strains ({self.extraction_stats['pricing']/len(df)*100:.1f}%)
- **Cannabis Data:** {self.extraction_stats['cannabis_data']} strains ({self.extraction_stats['cannabis_data']/len(df)*100:.1f}%)
- **Media Assets:** {self.extraction_stats['images']} strains ({self.extraction_stats['images']/len(df)*100:.1f}%)
- **Awards:** {self.extraction_stats['awards']} strains ({self.extraction_stats['awards']/len(df)*100:.1f}%)
- **Genetics:** {self.extraction_stats['genetics']} strains ({self.extraction_stats['genetics']/len(df)*100:.1f}%)

## Top Performing Strains (Data Completeness)
{df.nlargest(10, 'data_completeness_score')[['strain_name', 'data_completeness_score', 'market_tier', 'total_fields_captured']].to_string(index=False)}

## File Output
- **Main Dataset:** {output_file}
- **Total Size:** {len(df)} rows × {len(df.columns)} columns
- **Encoding:** UTF-8
- **Format:** CSV with headers

---

**Processing completed with maximum data extraction methodology.**  
**Logic designed by Amazon Q, verified by Shannon Goddard.**
"""
        
        with open('ilgm_extraction_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info("Comprehensive extraction report generated")

def main():
    extractor = ILGMMaxExtractor()
    df = extractor.process_all_ilgm_strains()
    
    print(f"\nILGM MAXIMUM EXTRACTION COMPLETE!")
    print(f"Dataset: {len(df)} strains × {len(df.columns)} columns")
    print(f"Average Quality: {df['data_completeness_score'].mean():.1f}%")
    print(f"Market Tiers: {df['market_tier'].value_counts().to_dict()}")

if __name__ == "__main__":
    main()