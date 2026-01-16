#!/usr/bin/env python3
"""
Seedsman JavaScript-Rendered HTML Extractor
Extracts full product data from ScandiPWA JS-rendered HTML files
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class SeedsmanJSExtractor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        self.base_url = 'https://www.seedsman.com'
    
    def extract_strain_data(self, soup, url):
        """Extract comprehensive Seedsman strain data from JS-rendered HTML"""
        data = {
            'seed_bank': 'Seedsman',
            'source_url': url,
            'scraped_at': datetime.now().isoformat()
        }
        
        # Strain name from h1 or product title
        h1 = soup.find('h1', class_='ProductActions-Title')
        if not h1:
            h1 = soup.find('h1')
        if h1:
            data['strain_name'] = h1.get_text().strip()
        
        # Extract from product attributes table
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text().strip().lower().replace(' ', '_').replace(':', '')
                    value = cells[1].get_text().strip()
                    
                    if value and value != '-' and len(value) < 200:
                        data[f'spec_{key}'] = value
        
        # Extract from attribute divs
        attr_divs = soup.find_all('div', class_='ProductAttribute')
        for div in attr_divs:
            label = div.find('span', class_='ProductAttribute-Label')
            value = div.find('span', class_='ProductAttribute-Value')
            
            if label and value:
                key = label.get_text().strip().lower().replace(' ', '_').replace(':', '')
                val = value.get_text().strip()
                if val and val != '-':
                    data[f'attr_{key}'] = val
        
        html_text = soup.get_text()
        
        # THC extraction
        thc_patterns = [
            r'THC[:\s]*([\d.]+)\s*-\s*([\d.]+)%',
            r'([\d.]+)\s*-\s*([\d.]+)%\s*THC',
            r'THC[:\s]*([\d.]+)%',
            r'THC\s+content[:\s]*([\d.]+)%'
        ]
        
        for pattern in thc_patterns:
            match = re.search(pattern, html_text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    data['thc_min'] = float(match.group(1))
                    data['thc_max'] = float(match.group(2))
                    data['thc_avg'] = round((data['thc_min'] + data['thc_max']) / 2, 1)
                else:
                    data['thc_content'] = float(match.group(1))
                break
        
        # CBD extraction
        cbd_patterns = [
            r'CBD[:\s]*([\d.]+)\s*-\s*([\d.]+)%',
            r'CBD[:\s]*([\d.]+)%'
        ]
        
        for pattern in cbd_patterns:
            match = re.search(pattern, html_text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    data['cbd_min'] = float(match.group(1))
                    data['cbd_max'] = float(match.group(2))
                else:
                    data['cbd_content'] = float(match.group(1))
                break
        
        # Flowering time
        flower_patterns = [
            r'flowering[:\s]*(\d+)\s*-\s*(\d+)\s*(?:weeks|days)',
            r'(\d+)\s*-\s*(\d+)\s*(?:weeks|days)\s*flowering'
        ]
        
        for pattern in flower_patterns:
            match = re.search(pattern, html_text, re.IGNORECASE)
            if match:
                data['flowering_time_min'] = int(match.group(1))
                data['flowering_time_max'] = int(match.group(2))
                data['flowering_time'] = f"{match.group(1)}-{match.group(2)}"
                break
        
        # Yield extraction
        yield_patterns = [
            r'yield[:\s]*(\d+)\s*-\s*(\d+)\s*(?:g|grams?)',
            r'(\d+)\s*-\s*(\d+)\s*g(?:/m2|rams?)'
        ]
        
        for pattern in yield_patterns:
            match = re.search(pattern, html_text, re.IGNORECASE)
            if match:
                data['yield_min'] = int(match.group(1))
                data['yield_max'] = int(match.group(2))
                data['yield_range'] = f"{match.group(1)}-{match.group(2)}g"
                break
        
        # Height extraction
        height_patterns = [
            r'height[:\s]*(\d+)\s*-\s*(\d+)\s*(?:cm|inches?)',
            r'(\d+)\s*-\s*(\d+)\s*cm'
        ]
        
        for pattern in height_patterns:
            match = re.search(pattern, html_text, re.IGNORECASE)
            if match:
                data['height_min'] = int(match.group(1))
                data['height_max'] = int(match.group(2))
                data['height_range'] = f"{match.group(1)}-{match.group(2)}cm"
                break
        
        # Genetics/lineage
        genetics_patterns = [
            r'(?:genetics|lineage|cross|parents?)[:\s]*([^\n.]{10,150})',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[xX×]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in genetics_patterns:
            match = re.search(pattern, html_text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    data['parent_1'] = match.group(1).strip()
                    data['parent_2'] = match.group(2).strip()
                    data['genetics'] = f"{match.group(1)} × {match.group(2)}"
                else:
                    data['genetics'] = match.group(1).strip()
                break
        
        # Indica/Sativa ratio
        ratio_patterns = [
            r'(\d+)%\s*indica[^0-9]*(\d+)%\s*sativa',
            r'(\d+)%\s*sativa[^0-9]*(\d+)%\s*indica'
        ]
        
        for pattern in ratio_patterns:
            match = re.search(pattern, html_text, re.IGNORECASE)
            if match:
                if 'indica' in pattern:
                    data['indica_percentage'] = int(match.group(1))
                    data['sativa_percentage'] = int(match.group(2))
                else:
                    data['sativa_percentage'] = int(match.group(1))
                    data['indica_percentage'] = int(match.group(2))
                
                # Determine type
                if data.get('indica_percentage', 0) > data.get('sativa_percentage', 0):
                    data['strain_type'] = 'Indica Dominant'
                elif data.get('sativa_percentage', 0) > data.get('indica_percentage', 0):
                    data['strain_type'] = 'Sativa Dominant'
                else:
                    data['strain_type'] = 'Balanced Hybrid'
                break
        
        # Effects extraction
        effects = []
        effect_keywords = ['relaxing', 'euphoric', 'creative', 'uplifting', 'energetic', 
                          'sleepy', 'happy', 'focused', 'cerebral', 'body high']
        for effect in effect_keywords:
            if re.search(rf'\b{effect}\b', html_text, re.IGNORECASE):
                effects.append(effect)
        
        if effects:
            data['effects'] = ', '.join(effects)
            data['primary_effect'] = effects[0]
            data['effect_count'] = len(effects)
        
        # Flavors extraction
        flavors = []
        flavor_keywords = ['earthy', 'sweet', 'citrus', 'pine', 'diesel', 'fruity', 
                          'spicy', 'woody', 'lemon', 'berry', 'skunk']
        for flavor in flavor_keywords:
            if re.search(rf'\b{flavor}\b', html_text, re.IGNORECASE):
                flavors.append(flavor)
        
        if flavors:
            data['flavors'] = ', '.join(flavors)
            data['primary_flavor'] = flavors[0]
            data['flavor_count'] = len(flavors)
        
        # Terpenes
        terpenes = []
        terpene_keywords = ['myrcene', 'limonene', 'pinene', 'linalool', 'caryophyllene']
        for terpene in terpene_keywords:
            if re.search(rf'\b{terpene}\b', html_text, re.IGNORECASE):
                terpenes.append(terpene)
        
        if terpenes:
            data['terpenes'] = ', '.join(terpenes)
            data['dominant_terpene'] = terpenes[0]
        
        # Breeder
        breeder_match = re.search(r'breeder[:\s]*([^\n.]{3,50})', html_text, re.IGNORECASE)
        if breeder_match:
            data['breeder'] = breeder_match.group(1).strip()
        
        # Growing difficulty
        difficulty_match = re.search(r'difficulty[:\s]*(easy|moderate|difficult|beginner|intermediate|advanced)', html_text, re.IGNORECASE)
        if difficulty_match:
            data['difficulty'] = difficulty_match.group(1).capitalize()
        
        # Climate
        climate_keywords = ['indoor', 'outdoor', 'greenhouse']
        found_climates = [c for c in climate_keywords if re.search(rf'\b{c}\b', html_text, re.IGNORECASE)]
        if found_climates:
            data['climate'] = ', '.join(found_climates)
        
        # Feminized/Regular/Auto
        if re.search(r'\bfeminized\b', html_text, re.IGNORECASE):
            data['seed_type'] = 'Feminized'
        elif re.search(r'\bautoflower', html_text, re.IGNORECASE):
            data['seed_type'] = 'Autoflower'
        elif re.search(r'\bregular\b', html_text, re.IGNORECASE):
            data['seed_type'] = 'Regular'
        
        # Pricing
        price_patterns = [
            r'[$£€]\s*([\d.]+)',
            r'([\d.]+)\s*[$£€]'
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, html_text)
            prices.extend([float(p) for p in matches if 1 < float(p) < 500])
        
        if prices:
            data['min_price'] = min(prices)
            data['max_price'] = max(prices)
            data['avg_price'] = round(sum(prices) / len(prices), 2)
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '')
        
        # JSON-LD extraction
        json_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_scripts:
            if script.string:
                try:
                    json_data = json.loads(script.string)
                    if json_data.get('@type') == 'Product':
                        data['jsonld_name'] = json_data.get('name')
                        data['jsonld_sku'] = json_data.get('sku')
                        data['jsonld_brand'] = json_data.get('brand', {}).get('name') if isinstance(json_data.get('brand'), dict) else None
                        
                        offers = json_data.get('offers', {})
                        if offers:
                            data['jsonld_price'] = offers.get('price')
                            data['jsonld_currency'] = offers.get('priceCurrency')
                except:
                    pass
        
        # Count non-empty fields
        data['total_fields'] = sum(1 for v in data.values() if v and str(v).strip())
        
        return data
    
    def process_seedsman_strains(self):
        """Process all Seedsman strains from JS-rendered HTML"""
        logger.info("Starting Seedsman JS Extraction")
        
        # Load JS inventory
        inv_path = '../s3_js_html_inventory.csv'
        logger.info(f"Loading JS inventory from {inv_path}")
        inv = pd.read_csv(inv_path)
        
        seedsman_urls = inv[inv['seed_bank'] == 'Seedsman']
        logger.info(f"Found {len(seedsman_urls)} Seedsman URLs")
        
        results = []
        processed = 0
        
        for _, row in seedsman_urls.iterrows():
            url_hash = row['url_hash']
            url = row.get('url', 'Unknown')
            
            try:
                # Get JS-rendered HTML from S3
                html_key = f'html_js/{url_hash}_js.html'
                response = self.s3_client.get_object(Bucket=self.bucket_name, Key=html_key)
                html_content = response['Body'].read().decode('utf-8')
                
                soup = BeautifulSoup(html_content, 'html.parser')
                strain_data = self.extract_strain_data(soup, url)
                results.append(strain_data)
                
                processed += 1
                if processed % 100 == 0:
                    logger.info(f"Processed {processed}/{len(seedsman_urls)} strains")
                
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                continue
        
        # Create DataFrame
        df_results = pd.DataFrame(results)
        
        # Save results
        output_file = 'seedsman_js_extracted.csv'
        df_results.to_csv(output_file, index=False, encoding='utf-8')
        
        # Generate report
        self.generate_report(df_results, output_file)
        
        logger.info(f"✅ Extraction complete! {len(results)} strains, {len(df_results.columns)} columns")
        logger.info(f"📊 Saved to: {output_file}")
        
        return df_results
    
    def generate_report(self, df, output_file):
        """Generate extraction report"""
        thc_coverage = sum(1 for _, row in df.iterrows() if row.get('thc_min') or row.get('thc_content'))
        
        report = f"""# Seedsman JavaScript Extraction Report

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Source:** JS-rendered HTML from S3 `html_js/` folder (ScandiPWA architecture)
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Results
- **Strains Extracted:** {len(df)}
- **Total Columns:** {len(df.columns)}
- **Average Fields per Strain:** {df['total_fields'].mean():.1f}

## Data Coverage
- **THC Data:** {thc_coverage} strains ({thc_coverage/len(df)*100:.1f}%)
- **CBD Data:** {sum(1 for _, row in df.iterrows() if row.get('cbd_content') or row.get('cbd_min'))} strains
- **Flowering Time:** {sum(1 for _, row in df.iterrows() if row.get('flowering_time'))} strains
- **Yield Data:** {sum(1 for _, row in df.iterrows() if row.get('yield_range'))} strains
- **Genetics:** {sum(1 for _, row in df.iterrows() if row.get('genetics'))} strains
- **Effects:** {sum(1 for _, row in df.iterrows() if row.get('effects'))} strains
- **Flavors:** {sum(1 for _, row in df.iterrows() if row.get('flavors'))} strains
- **Terpenes:** {sum(1 for _, row in df.iterrows() if row.get('terpenes'))} strains

## Comparison to Static HTML
- **Previous Status:** JS-blocked (0% extraction)
- **New Status:** Full extraction enabled
- **Improvement:** {thc_coverage} strains with THC data (from 0)

## Output
- **File:** {output_file}
- **Format:** CSV, UTF-8 encoding
"""
        
        with open('SEEDSMAN_JS_EXTRACTION_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(report)

def main():
    extractor = SeedsmanJSExtractor()
    df = extractor.process_seedsman_strains()
    
    print(f"\n🎯 SEEDSMAN JS EXTRACTION COMPLETE!")
    print(f"📊 {len(df)} strains × {len(df.columns)} columns")
    print(f"💎 Avg fields: {df['total_fields'].mean():.1f}")

if __name__ == "__main__":
    main()
