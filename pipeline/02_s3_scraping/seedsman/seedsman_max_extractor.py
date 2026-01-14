#!/usr/bin/env python3
"""
Seedsman Maximum Data Extractor - THE BEAR (Final Bank)
Logic designed by Amazon Q, verified by Shannon Goddard.

8-Method Pipeline: JSON-LD, Meta Tags, Tables, Pricing, Cannabis Data, Media, Awards, Genetics
Target: 878 strains with maximum data capture and quality scoring
"""

import pandas as pd
import json
import re
from bs4 import BeautifulSoup
from pathlib import Path
import boto3
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SeedsmanMaxExtractor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        self.base_url = 'https://www.seedsman.com'
        
        # Quality scoring weights
        self.field_weights = {
            'premium': 3.0,  # THC/CBD, genetics, flowering_time
            'high': 2.0,     # price, yield, height, effects
            'standard': 1.0  # description, images, basic info
        }
        
    def extract_json_ld(self, soup):
        """Method 1: Extract JSON-LD structured data"""
        data = {}
        json_scripts = soup.find_all('script', type='application/ld+json')
        
        for script in json_scripts:
            try:
                json_data = json.loads(script.string)
                if isinstance(json_data, dict):
                    if json_data.get('@type') == 'Product':
                        data.update({
                            'jsonld_name': json_data.get('name'),
                            'jsonld_description': json_data.get('description'),
                            'jsonld_brand': json_data.get('brand', {}).get('name') if isinstance(json_data.get('brand'), dict) else json_data.get('brand'),
                            'jsonld_sku': json_data.get('sku'),
                            'jsonld_price': json_data.get('offers', {}).get('price') if isinstance(json_data.get('offers'), dict) else None,
                            'jsonld_currency': json_data.get('offers', {}).get('priceCurrency') if isinstance(json_data.get('offers'), dict) else None,
                            'jsonld_availability': json_data.get('offers', {}).get('availability') if isinstance(json_data.get('offers'), dict) else None,
                            'jsonld_image': json_data.get('image'),
                            'jsonld_rating': json_data.get('aggregateRating', {}).get('ratingValue') if isinstance(json_data.get('aggregateRating'), dict) else None,
                            'jsonld_review_count': json_data.get('aggregateRating', {}).get('reviewCount') if isinstance(json_data.get('aggregateRating'), dict) else None
                        })
            except (json.JSONDecodeError, AttributeError):
                continue
                
        return data
    
    def extract_meta_tags(self, soup):
        """Method 2: Extract meta tag data"""
        data = {}
        
        # Standard meta tags
        meta_mappings = {
            'title': 'meta_title',
            'description': 'meta_description',
            'keywords': 'meta_keywords',
            'og:title': 'og_title',
            'og:description': 'og_description',
            'og:image': 'og_image',
            'og:price:amount': 'og_price',
            'og:price:currency': 'og_currency',
            'product:brand': 'product_brand',
            'product:availability': 'product_availability',
            'product:condition': 'product_condition',
            'product:price:amount': 'product_price',
            'product:price:currency': 'product_currency'
        }
        
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name in meta_mappings and content:
                data[meta_mappings[name]] = content
                
        # Title tag
        title_tag = soup.find('title')
        if title_tag:
            data['page_title'] = title_tag.get_text().strip()
            
        return data
    
    def extract_tables(self, soup):
        """Method 3: Extract Seedsman's structured specification table"""
        data = {}
        
        # Seedsman's specific product attribute table
        spec_table = soup.find('table', id='product-attribute-specs-table')
        if spec_table:
            rows = spec_table.find_all('tr')
            for row in rows:
                label_th = row.find('th', class_='col label')
                data_td = row.find('td', class_='col data')
                
                if label_th and data_td:
                    label_h4 = label_th.find('h4')
                    if label_h4:
                        label = label_h4.get_text().strip()
                        
                        # Extract value from nested spans or h3
                        spans = data_td.find_all('span')
                        if spans:
                            values = [span.get_text().strip() for span in spans if span.get_text().strip()]
                            value = ' | '.join(values) if len(values) > 1 else values[0] if values else ''
                        else:
                            h3 = data_td.find('h3')
                            value = h3.get_text().strip() if h3 else data_td.get_text().strip()
                        
                        # Map Seedsman's specific fields
                        field_map = {
                            'Brand/breeder': 'breeder_name',
                            'THC content': 'thc_content',
                            'CBD content': 'cbd_content', 
                            'Yield indoor': 'yield_indoor',
                            'Yield outdoor': 'yield_outdoor',
                            'Photoperiod flowering time': 'flowering_time',
                            'Autoflower flowering time': 'auto_flowering_time',
                            'Suitable climates': 'suitable_climates',
                            'Aroma': 'aroma',
                            'Variety': 'variety',
                            'Sex': 'sex',
                            'Flowering type': 'flowering_type',
                            'Height indoor': 'height_indoor',
                            'Height outdoor': 'height_outdoor',
                            'Effects': 'effects',
                            'Genetics': 'genetics_info',
                            'Medical': 'medical_uses'
                        }
                        
                        if label in field_map and value:
                            data[field_map[label]] = value
                        
                        # Also store raw field for analysis
                        clean_label = re.sub(r'[^a-z0-9_]', '_', label.lower())
                        data[f'seedsman_{clean_label}'] = value
        
        # Look for other specification tables
        other_tables = soup.find_all('table')
        for i, table in enumerate(other_tables):
            if table.get('id') != 'product-attribute-specs-table':  # Skip the main one
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        key = cells[0].get_text().strip().lower().replace(' ', '_').replace(':', '')
                        value = cells[1].get_text().strip()
                        if key and value:
                            data[f'table_{i}_{key}'] = value
        
        # Product description sections
        desc_div = soup.find('div', class_='ProductActions-ShortDescription')
        if desc_div:
            data['product_description'] = desc_div.get_text().strip()
            
        return data
    
    def extract_pricing(self, soup):
        """Method 4: Extract pricing and package information"""
        data = {}
        
        # Price patterns
        price_patterns = [
            r'[\$£€¥]\s*(\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?)\s*[\$£€¥]',
            r'Price[:\s]*[\$£€¥]?\s*(\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?)\s*(?:USD|GBP|EUR|CAD)'
        ]
        
        page_text = soup.get_text()
        for i, pattern in enumerate(price_patterns):
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                data[f'price_match_{i}'] = matches[0]
        
        # Package options
        package_elements = soup.find_all(['select', 'div'], class_=re.compile(r'(package|option|variant)', re.I))
        for element in package_elements:
            options = element.find_all(['option', 'div', 'span'])
            for j, option in enumerate(options):
                text = option.get_text().strip()
                if any(word in text.lower() for word in ['seed', 'pack', 'fem', 'auto', 'reg']):
                    data[f'package_option_{j}'] = text
                    
        return data
    
    def extract_cannabis_data(self, soup):
        """Method 5: Extract cannabis-specific data"""
        data = {}
        page_text = soup.get_text()
        
        # THC/CBD patterns
        thc_patterns = [
            r'THC[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%',
            r'THC[:\s]*(\d+(?:\.\d+)?)%',
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%\s*THC'
        ]
        
        cbd_patterns = [
            r'CBD[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%',
            r'CBD[:\s]*(\d+(?:\.\d+)?)%',
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%\s*CBD'
        ]
        
        for i, pattern in enumerate(thc_patterns):
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                if len(matches[0]) == 2:  # Range
                    data[f'thc_min_{i}'] = matches[0][0]
                    data[f'thc_max_{i}'] = matches[0][1]
                else:  # Single value
                    data[f'thc_value_{i}'] = matches[0]
        
        for i, pattern in enumerate(cbd_patterns):
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                if len(matches[0]) == 2:  # Range
                    data[f'cbd_min_{i}'] = matches[0][0]
                    data[f'cbd_max_{i}'] = matches[0][1]
                else:  # Single value
                    data[f'cbd_value_{i}'] = matches[0]
        
        # Flowering time
        flowering_patterns = [
            r'flowering[:\s]*(\d+)\s*-\s*(\d+)\s*(?:days?|weeks?)',
            r'(\d+)\s*-\s*(\d+)\s*(?:days?|weeks?)\s*flowering',
            r'flowering[:\s]*(\d+)\s*(?:days?|weeks?)'
        ]
        
        for i, pattern in enumerate(flowering_patterns):
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                data[f'flowering_time_{i}'] = matches[0] if isinstance(matches[0], str) else '-'.join(matches[0])
        
        # Yield patterns
        yield_patterns = [
            r'yield[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:g|oz|kg)',
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:g|oz|kg)\s*yield',
            r'yield[:\s]*(\d+(?:\.\d+)?)\s*(?:g|oz|kg)'
        ]
        
        for i, pattern in enumerate(yield_patterns):
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                data[f'yield_{i}'] = matches[0] if isinstance(matches[0], str) else '-'.join(matches[0])
        
        # Height patterns
        height_patterns = [
            r'height[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:cm|m|ft|in)',
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:cm|m|ft|in)\s*(?:tall|high)',
            r'height[:\s]*(\d+(?:\.\d+)?)\s*(?:cm|m|ft|in)'
        ]
        
        for i, pattern in enumerate(height_patterns):
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                data[f'height_{i}'] = matches[0] if isinstance(matches[0], str) else '-'.join(matches[0])
        
        # Genetics/Type
        genetics_keywords = ['indica', 'sativa', 'hybrid', 'autoflower', 'feminized', 'regular']
        for keyword in genetics_keywords:
            if re.search(rf'\b{keyword}\b', page_text, re.IGNORECASE):
                data[f'genetics_{keyword}'] = True
        
        return data
    
    def extract_media(self, soup):
        """Method 6: Extract images and media"""
        data = {}
        
        # Product images
        img_tags = soup.find_all('img')
        image_urls = []
        for img in img_tags:
            src = img.get('src') or img.get('data-src')
            if src:
                full_url = urljoin(self.base_url, src)
                image_urls.append(full_url)
        
        data['image_count'] = len(image_urls)
        for i, url in enumerate(image_urls[:10]):  # Limit to first 10
            data[f'image_{i}'] = url
        
        # Video content
        video_tags = soup.find_all(['video', 'iframe'])
        for i, video in enumerate(video_tags):
            src = video.get('src')
            if src:
                data[f'video_{i}'] = src
        
        return data
    
    def extract_awards(self, soup):
        """Method 7: Extract awards and certifications"""
        data = {}
        page_text = soup.get_text().lower()
        
        # Award keywords
        award_keywords = [
            'cup winner', 'award', 'champion', 'winner', 'prize', 'medal',
            'cannabis cup', 'high times', 'spannabis', 'emerald cup',
            'certified', 'organic', 'tested', 'lab tested'
        ]
        
        for keyword in award_keywords:
            if keyword in page_text:
                data[f'award_{keyword.replace(" ", "_")}'] = True
        
        # Look for award sections
        award_sections = soup.find_all(['div', 'section'], class_=re.compile(r'(award|prize|winner|cert)', re.I))
        for i, section in enumerate(award_sections):
            data[f'award_section_{i}'] = section.get_text().strip()[:200]  # Limit length
        
        return data
    
    def extract_genetics(self, soup):
        """Method 8: Extract genetics and lineage information"""
        data = {}
        page_text = soup.get_text()
        
        # Genetics patterns
        genetics_patterns = [
            r'genetics[:\s]*([^.]+)',
            r'lineage[:\s]*([^.]+)',
            r'parents[:\s]*([^.]+)',
            r'cross[:\s]*([^.]+)',
            r'bred from[:\s]*([^.]+)'
        ]
        
        for i, pattern in enumerate(genetics_patterns):
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                data[f'genetics_info_{i}'] = matches[0].strip()[:100]  # Limit length
        
        # Sativa/Indica percentages
        ratio_patterns = [
            r'(\d+)%\s*sativa[^0-9]*(\d+)%\s*indica',
            r'(\d+)%\s*indica[^0-9]*(\d+)%\s*sativa',
            r'sativa[:\s]*(\d+)%',
            r'indica[:\s]*(\d+)%'
        ]
        
        for i, pattern in enumerate(ratio_patterns):
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            if matches:
                data[f'ratio_match_{i}'] = matches[0] if isinstance(matches[0], str) else '/'.join(matches[0])
        
        return data
    
    def calculate_quality_score(self, row_data):
        """Calculate quality score based on field completeness and importance"""
        premium_fields = ['thc_min_0', 'thc_max_0', 'cbd_min_0', 'flowering_time_0', 'genetics_info_0', 'yield_0']
        high_fields = ['jsonld_price', 'price_match_0', 'height_0', 'genetics_indica', 'genetics_sativa']
        standard_fields = ['jsonld_name', 'meta_description', 'image_0', 'page_title']
        
        score = 0
        max_score = 0
        
        # Premium fields
        for field in premium_fields:
            max_score += self.field_weights['premium']
            if field in row_data and pd.notna(row_data[field]) and str(row_data[field]).strip():
                score += self.field_weights['premium']
        
        # High importance fields
        for field in high_fields:
            max_score += self.field_weights['high']
            if field in row_data and pd.notna(row_data[field]) and str(row_data[field]).strip():
                score += self.field_weights['high']
        
        # Standard fields
        for field in standard_fields:
            max_score += self.field_weights['standard']
            if field in row_data and pd.notna(row_data[field]) and str(row_data[field]).strip():
                score += self.field_weights['standard']
        
        return (score / max_score * 100) if max_score > 0 else 0
    
    def classify_market_tier(self, quality_score, row_data):
        """Classify strain into market tier based on quality score and data richness"""
        if quality_score >= 70:
            return 'Enterprise'
        elif quality_score >= 50:
            return 'Professional'
        elif quality_score >= 30:
            return 'Standard'
        else:
            return 'Basic'
    
    def process_strain(self, s3_key):
        """Process a single strain HTML file"""
        try:
            # Download HTML from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            html_content = response['Body'].read().decode('utf-8', errors='ignore')
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Apply 8-method extraction pipeline
            strain_data = {'s3_key': s3_key}
            strain_data.update(self.extract_json_ld(soup))
            strain_data.update(self.extract_meta_tags(soup))
            strain_data.update(self.extract_tables(soup))
            strain_data.update(self.extract_pricing(soup))
            strain_data.update(self.extract_cannabis_data(soup))
            strain_data.update(self.extract_media(soup))
            strain_data.update(self.extract_awards(soup))
            strain_data.update(self.extract_genetics(soup))
            
            # Calculate quality metrics
            quality_score = self.calculate_quality_score(strain_data)
            market_tier = self.classify_market_tier(quality_score, strain_data)
            
            strain_data['quality_score'] = quality_score
            strain_data['market_tier'] = market_tier
            strain_data['extraction_method'] = '8_method_pipeline'
            strain_data['field_count'] = len([k for k, v in strain_data.items() if pd.notna(v) and str(v).strip()])
            
            return strain_data
            
        except Exception as e:
            logger.error(f"Error processing {s3_key}: {str(e)}")
            return {'s3_key': s3_key, 'error': str(e)}
    
    def run_extraction(self):
        """Run the complete extraction process using direct URL mappings"""
        logger.info("Starting Seedsman maximum extraction - THE BEAR!")
        
        # Read the complete inventory CSV to get Seedsman URLs
        inventory_path = Path('../../02_source_of_truth/s3_complete_inventory.csv')
        if not inventory_path.exists():
            logger.error(f"Inventory file not found: {inventory_path}")
            return None
            
        import pandas as pd
        inventory_df = pd.read_csv(inventory_path)
        seedsman_df = inventory_df[inventory_df['seed_bank'] == 'Seedsman']
        
        logger.info(f"Found {len(seedsman_df)} Seedsman strains in inventory")
        
        # Process all Seedsman strains
        all_data = []
        for i, row in seedsman_df.iterrows():
            if i % 50 == 0:
                logger.info(f"Processing strain {i+1}/{len(seedsman_df)}")
            
            s3_key = f"html/{row['url_hash']}.html"
            strain_data = self.process_strain(s3_key)
            strain_data['original_url'] = row['url']
            strain_data['url_hash'] = row['url_hash']
            all_data.append(strain_data)
        
        # Create DataFrame and save
        df = pd.DataFrame(all_data)
        
        # Generate summary statistics
        total_strains = len(df)
        avg_quality = df['quality_score'].mean() if 'quality_score' in df.columns else 0
        total_columns = len(df.columns)
        
        tier_distribution = df['market_tier'].value_counts().to_dict() if 'market_tier' in df.columns else {}
        
        logger.info(f"Extraction complete!")
        logger.info(f"Total strains: {total_strains}")
        logger.info(f"Average quality: {avg_quality:.1f}%")
        logger.info(f"Total columns: {total_columns}")
        logger.info(f"Market tiers: {tier_distribution}")
        
        # Save results
        output_file = Path(__file__).parent / 'seedsman_maximum_extraction.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        logger.info(f"Results saved to {output_file}")
        
        return df

if __name__ == "__main__":
    extractor = SeedsmanMaxExtractor()
    results = extractor.run_extraction()