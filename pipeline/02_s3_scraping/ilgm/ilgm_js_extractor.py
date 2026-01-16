#!/usr/bin/env python3
"""
ILGM JavaScript-Rendered HTML Extractor
Extracts full product table data from JS-rendered HTML files
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class ILGMJSExtractor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        self.base_url = 'https://ilgm.com'
    
    def extract_strain_data(self, soup, url):
        """Extract comprehensive ILGM strain data from JS-rendered HTML"""
        data = {
            'seed_bank': 'ILGM',
            'source_url': url,
            'scraped_at': datetime.now().isoformat()
        }
        
        # Strain name from h1
        h1 = soup.find('h1')
        if h1:
            data['strain_name'] = h1.get_text().strip().replace(' Seeds', '')
        
        # Extract from product table (flex justify-between structure)
        table_rows = soup.find_all('div', class_='flex justify-between')
        
        for row in table_rows:
            label_elem = row.find('div', class_='text-gray-600')
            value_elem = row.find('div', class_='font-medium')
            
            if label_elem and value_elem:
                label = label_elem.get_text().strip().lower().replace(' ', '_').replace(':', '')
                value = value_elem.get_text().strip()
                
                if value and value != '-':
                    data[f'spec_{label}'] = value
        
        # THC extraction
        html_text = soup.get_text()
        thc_patterns = [
            r'THC[:\s]*([\d.]+)\s*-\s*([\d.]+)%',
            r'([\d.]+)\s*-\s*([\d.]+)%\s*THC',
            r'THC[:\s]*([\d.]+)%'
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
        cbd_match = re.search(r'CBD[:\s]*([\d.]+)%', html_text, re.IGNORECASE)
        if cbd_match:
            data['cbd_content'] = float(cbd_match.group(1))
        
        # Flowering time
        flower_match = re.search(r'(\d+)\s*-\s*(\d+)\s*weeks', html_text, re.IGNORECASE)
        if flower_match:
            data['flowering_time_min'] = int(flower_match.group(1))
            data['flowering_time_max'] = int(flower_match.group(2))
            data['flowering_time'] = f"{flower_match.group(1)}-{flower_match.group(2)} weeks"
        
        # Yield extraction
        yield_patterns = [
            r'(\d+)\s*-\s*(\d+)\s*(?:oz|ounces)',
            r'yield[:\s]*(\d+)\s*-\s*(\d+)'
        ]
        
        for pattern in yield_patterns:
            match = re.search(pattern, html_text, re.IGNORECASE)
            if match:
                data['yield_min'] = int(match.group(1))
                data['yield_max'] = int(match.group(2))
                data['yield_range'] = f"{match.group(1)}-{match.group(2)} oz"
                break
        
        # Height extraction
        height_match = re.search(r'(\d+)\s*-\s*(\d+)\s*(?:inches|in)', html_text, re.IGNORECASE)
        if height_match:
            data['height_min'] = int(height_match.group(1))
            data['height_max'] = int(height_match.group(2))
            data['height_range'] = f"{height_match.group(1)}-{height_match.group(2)} inches"
        
        # Effects extraction
        effects = []
        effect_keywords = ['relaxing', 'euphoric', 'creative', 'uplifting', 'energetic', 'sleepy', 'happy', 'focused']
        for effect in effect_keywords:
            if re.search(rf'\b{effect}\b', html_text, re.IGNORECASE):
                effects.append(effect)
        
        if effects:
            data['effects'] = ', '.join(effects)
            data['primary_effect'] = effects[0]
        
        # Flavors extraction
        flavors = []
        flavor_keywords = ['earthy', 'sweet', 'citrus', 'pine', 'diesel', 'fruity', 'spicy', 'woody']
        for flavor in flavor_keywords:
            if re.search(rf'\b{flavor}\b', html_text, re.IGNORECASE):
                flavors.append(flavor)
        
        if flavors:
            data['flavors'] = ', '.join(flavors)
            data['primary_flavor'] = flavors[0]
        
        # Genetics/lineage
        genetics_match = re.search(r'(?:genetics|lineage|cross)[:\s]*([^\n.]{10,100})', html_text, re.IGNORECASE)
        if genetics_match:
            data['genetics'] = genetics_match.group(1).strip()
        
        # Indica/Sativa ratio
        ratio_match = re.search(r'(\d+)%\s*(?:indica|sativa)[^0-9]*(\d+)%\s*(?:sativa|indica)', html_text, re.IGNORECASE)
        if ratio_match:
            if 'indica' in html_text[ratio_match.start():ratio_match.start()+20].lower():
                data['indica_percentage'] = int(ratio_match.group(1))
                data['sativa_percentage'] = int(ratio_match.group(2))
            else:
                data['sativa_percentage'] = int(ratio_match.group(1))
                data['indica_percentage'] = int(ratio_match.group(2))
        
        # Difficulty level
        difficulty_match = re.search(r'difficulty[:\s]*(easy|moderate|difficult)', html_text, re.IGNORECASE)
        if difficulty_match:
            data['difficulty'] = difficulty_match.group(1).capitalize()
        
        # Climate
        climate_match = re.search(r'climate[:\s]*(indoor|outdoor|both)', html_text, re.IGNORECASE)
        if climate_match:
            data['climate'] = climate_match.group(1).capitalize()
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '')
        
        # Count non-empty fields
        data['total_fields'] = sum(1 for v in data.values() if v and str(v).strip())
        
        return data
    
    def process_ilgm_strains(self):
        """Process all ILGM strains from JS-rendered HTML"""
        logger.info("Starting ILGM JS Extraction")
        
        # Load JS inventory
        inv_path = '../s3_js_html_inventory.csv'
        logger.info(f"Loading JS inventory from {inv_path}")
        inv = pd.read_csv(inv_path)
        
        # ILGM files are marked as 'Unknown' (metadata lookup failed)
        unknown_files = inv[inv['seed_bank'] == 'Unknown']
        logger.info(f"Found {len(unknown_files)} Unknown files (likely ILGM)")
        
        results = []
        processed = 0
        
        for _, row in unknown_files.iterrows():
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
                if processed % 25 == 0:
                    logger.info(f"Processed {processed}/{len(unknown_files)} strains")
                
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                continue
        
        # Create DataFrame
        df_results = pd.DataFrame(results)
        
        # Save results
        output_file = 'ilgm_js_extracted.csv'
        df_results.to_csv(output_file, index=False, encoding='utf-8')
        
        # Generate report
        self.generate_report(df_results, output_file)
        
        logger.info(f"✅ Extraction complete! {len(results)} strains, {len(df_results.columns)} columns")
        logger.info(f"📊 Saved to: {output_file}")
        
        return df_results
    
    def generate_report(self, df, output_file):
        """Generate extraction report"""
        thc_coverage = sum(1 for _, row in df.iterrows() if row.get('thc_min') or row.get('thc_content'))
        
        report = f"""# ILGM JavaScript Extraction Report

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Source:** JS-rendered HTML from S3 `html_js/` folder
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Results
- **Strains Extracted:** {len(df)}
- **Total Columns:** {len(df.columns)}
- **Average Fields per Strain:** {df['total_fields'].mean():.1f}

## Data Coverage
- **THC Data:** {thc_coverage} strains ({thc_coverage/len(df)*100:.1f}%)
- **CBD Data:** {sum(1 for _, row in df.iterrows() if row.get('cbd_content'))} strains
- **Flowering Time:** {sum(1 for _, row in df.iterrows() if row.get('flowering_time'))} strains
- **Yield Data:** {sum(1 for _, row in df.iterrows() if row.get('yield_range'))} strains
- **Effects:** {sum(1 for _, row in df.iterrows() if row.get('effects'))} strains
- **Genetics:** {sum(1 for _, row in df.iterrows() if row.get('genetics'))} strains

## Comparison to Static HTML
- **Previous THC Coverage:** 6.8% (9 strains)
- **New THC Coverage:** {thc_coverage/len(df)*100:.1f}% ({thc_coverage} strains)
- **Improvement:** {(thc_coverage/len(df)*100) - 6.8:.1f} percentage points

## Output
- **File:** {output_file}
- **Format:** CSV, UTF-8 encoding
"""
        
        with open('ILGM_JS_EXTRACTION_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(report)

def main():
    extractor = ILGMJSExtractor()
    df = extractor.process_ilgm_strains()
    
    print(f"\n🎯 ILGM JS EXTRACTION COMPLETE!")
    print(f"📊 {len(df)} strains × {len(df.columns)} columns")
    print(f"💎 Avg fields: {df['total_fields'].mean():.1f}")

if __name__ == "__main__":
    main()
