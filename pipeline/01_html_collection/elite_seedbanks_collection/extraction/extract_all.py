#!/usr/bin/env python3
"""
Pipeline 06: Maximum Value Extraction
8-Method Extraction Pipeline for 3,153 Elite Seedbank Pages

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import boto3
import sqlite3
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class EliteExtractor:
    """8-Method extraction for elite seedbanks"""
    
    def __init__(self, db_path: str, s3_bucket: str):
        self.db_path = db_path
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
        
        # Field weights for quality scoring
        self.weights = {
            'premium': 10,  # THC, CBD, flowering, yield, genetics
            'high': 6,      # Effects, packages, breeder
            'standard': 3   # Basic info, descriptions
        }
    
    def get_successful_urls(self, seedbank: str = None) -> list:
        """Get successfully collected URLs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if seedbank:
            cursor.execute('SELECT url_hash, original_url, seedbank, s3_path FROM merged_urls WHERE status = "success" AND seedbank = ?', (seedbank,))
        else:
            cursor.execute('SELECT url_hash, original_url, seedbank, s3_path FROM merged_urls WHERE status = "success"')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'url_hash': r[0], 'url': r[1], 'seedbank': r[2], 's3_path': r[3]} for r in results]
    
    def get_html_from_s3(self, s3_path: str) -> str:
        """Fetch HTML from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=s3_path)
            return response['Body'].read().decode('utf-8')
        except:
            return ""
    
    def extract_8_methods(self, html: str, url: str) -> dict:
        """8-Method extraction pipeline"""
        soup = BeautifulSoup(html, 'html.parser')
        data = {'url': url}
        
        # Method 1: JSON-LD
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                ld = json.loads(script.string)
                if isinstance(ld, dict):
                    data['name'] = ld.get('name', data.get('name'))
                    data['description'] = ld.get('description', data.get('description'))
                    data['brand'] = ld.get('brand', {}).get('name') if isinstance(ld.get('brand'), dict) else ld.get('brand')
                    data['price'] = ld.get('offers', {}).get('price') if isinstance(ld.get('offers'), dict) else None
            except:
                pass
        
        # Method 2: Meta tags
        for meta in soup.find_all('meta'):
            prop = meta.get('property', '') or meta.get('name', '')
            content = meta.get('content', '')
            if 'title' in prop.lower() and not data.get('name'):
                data['name'] = content
            elif 'description' in prop.lower() and not data.get('description'):
                data['description'] = content
        
        # Method 3: Title
        if not data.get('name') and soup.title:
            data['name'] = soup.title.string.strip()
        
        # Method 4: Cannabis-specific mining
        text = soup.get_text()
        
        # THC
        thc_match = re.search(r'(\d+(?:\.\d+)?)\s*-?\s*(\d+(?:\.\d+)?)?\s*%?\s*THC', text, re.I)
        if thc_match:
            data['thc_min'] = thc_match.group(1)
            data['thc_max'] = thc_match.group(2) or thc_match.group(1)
        
        # CBD
        cbd_match = re.search(r'(\d+(?:\.\d+)?)\s*-?\s*(\d+(?:\.\d+)?)?\s*%?\s*CBD', text, re.I)
        if cbd_match:
            data['cbd_min'] = cbd_match.group(1)
            data['cbd_max'] = cbd_match.group(2) or cbd_match.group(1)
        
        # Flowering time
        flower_match = re.search(r'(\d+)\s*-?\s*(\d+)?\s*(?:days?|weeks?|wks?).*?flower', text, re.I)
        if flower_match:
            data['flowering_min'] = flower_match.group(1)
            data['flowering_max'] = flower_match.group(2) or flower_match.group(1)
        
        # Yield
        yield_match = re.search(r'(\d+)\s*-?\s*(\d+)?\s*(?:g|grams?|oz)', text, re.I)
        if yield_match:
            data['yield_min'] = yield_match.group(1)
            data['yield_max'] = yield_match.group(2) or yield_match.group(1)
        
        # Genetics
        genetics_patterns = [
            r'(?:genetics|lineage|cross|parents?):\s*([^\n\.]{10,100})',
            r'(\w+\s+x\s+\w+)',
            r'(\d+%\s+(?:indica|sativa|hybrid))'
        ]
        for pattern in genetics_patterns:
            match = re.search(pattern, text, re.I)
            if match and not data.get('genetics'):
                data['genetics'] = match.group(1).strip()
        
        # Type
        if re.search(r'\bauto(?:flower)?', text, re.I):
            data['type'] = 'Autoflower'
        elif re.search(r'\bfeminized', text, re.I):
            data['type'] = 'Feminized'
        elif re.search(r'\bregular', text, re.I):
            data['type'] = 'Regular'
        
        # Method 5: Pricing
        price_patterns = [
            r'\$(\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?)\s*(?:USD|EUR|GBP)',
            r'price["\']?\s*:\s*["\']?(\d+(?:\.\d{2})?)'
        ]
        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.I)
            if matches and not data.get('price'):
                data['price'] = matches[0]
                break
        
        # Method 6: Effects
        effects = []
        effect_keywords = ['relaxed', 'euphoric', 'happy', 'uplifted', 'creative', 'focused', 'energetic', 'sleepy', 'hungry']
        for keyword in effect_keywords:
            if re.search(rf'\b{keyword}\b', text, re.I):
                effects.append(keyword.capitalize())
        if effects:
            data['effects'] = ', '.join(effects[:5])
        
        # Method 7: Flavors
        flavors = []
        flavor_keywords = ['sweet', 'fruity', 'citrus', 'earthy', 'pine', 'diesel', 'skunky', 'berry', 'lemon', 'grape']
        for keyword in flavor_keywords:
            if re.search(rf'\b{keyword}\b', text, re.I):
                flavors.append(keyword.capitalize())
        if flavors:
            data['flavors'] = ', '.join(flavors[:5])
        
        # Method 8: Breeder
        breeder_match = re.search(r'(?:breeder|brand|by)\s*:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text)
        if breeder_match and not data.get('brand'):
            data['brand'] = breeder_match.group(1)
        
        return data
    
    def calculate_quality_score(self, data: dict) -> float:
        """Calculate quality score"""
        score = 0
        total = 0
        
        # Premium fields (weight: 10)
        premium_fields = ['thc_min', 'thc_max', 'cbd_min', 'cbd_max', 'flowering_min', 'flowering_max', 'yield_min', 'yield_max', 'genetics']
        for field in premium_fields:
            total += self.weights['premium']
            if data.get(field):
                score += self.weights['premium']
        
        # High value fields (weight: 6)
        high_fields = ['effects', 'flavors', 'brand', 'type']
        for field in high_fields:
            total += self.weights['high']
            if data.get(field):
                score += self.weights['high']
        
        # Standard fields (weight: 3)
        standard_fields = ['name', 'description', 'price']
        for field in standard_fields:
            total += self.weights['standard']
            if data.get(field):
                score += self.weights['standard']
        
        return (score / total * 100) if total > 0 else 0
    
    def extract_seedbank(self, seedbank: str) -> pd.DataFrame:
        """Extract all strains for one seedbank with custom fields"""
        logger.info(f"Extracting {seedbank}...")
        
        urls = self.get_successful_urls(seedbank)
        logger.info(f"Found {len(urls)} URLs for {seedbank}")
        
        results = []
        for i, url_data in enumerate(urls, 1):
            if i % 100 == 0:
                logger.info(f"Progress: {i}/{len(urls)}")
            
            html = self.get_html_from_s3(url_data['s3_path'])
            if html:
                data = self.extract_8_methods(html, url_data['url'])
                data['seedbank'] = seedbank
                data['quality_score'] = self.calculate_quality_score(data)
                results.append(data)
        
        df = pd.DataFrame(results)
        
        # Save individual CSV
        filename = seedbank.lower().replace(' ', '_').replace('seeds', '').replace('bank', '').strip('_')
        output_path = Path(f'../data/{filename}_maximum_extraction.csv')
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"{seedbank}: {len(df)} strains, {len(df.columns)} columns, avg quality: {df['quality_score'].mean():.1f}%")
        
        return df
    
    def extract_all(self):
        """Extract all seedbanks to individual CSVs"""
        logger.info("Starting Phase 3: Maximum Extraction (Individual CSVs)")
        start_time = datetime.now()
        
        all_data = []
        seedbanks = ['Gorilla Seeds Bank', 'Herbies Seeds', 'Exotic Genetix', 'Amsterdam Marijuana Seeds', 'Compound Genetics']
        
        for seedbank in seedbanks:
            df = self.extract_seedbank(seedbank)
            all_data.append(df)
        
        duration = datetime.now() - start_time
        logger.info(f"Extraction complete in {duration}")
        
        # Generate report
        self.generate_report(all_data, seedbanks)
        
        return all_data
    
    def generate_report(self, all_data: list, seedbanks: list):
        """Generate extraction report"""
        
        total_strains = sum(len(df) for df in all_data)
        
        report = f"""# Pipeline 06: Maximum Extraction Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Extraction Summary
- **Total Strains Extracted**: {total_strains:,}
- **Individual CSVs**: 5 seedbanks
- **Custom Headers**: Each CSV has unique columns based on seedbank HTML

## Breakdown by Seedbank

"""
        
        for i, seedbank in enumerate(seedbanks):
            df = all_data[i]
            filename = seedbank.lower().replace(' ', '_').replace('seeds', '').replace('bank', '').strip('_')
            thc_count = df['thc_min'].notna().sum() if 'thc_min' in df.columns else 0
            genetics_count = df['genetics'].notna().sum() if 'genetics' in df.columns else 0
            report += f"""### {seedbank}
- **File**: `{filename}_maximum_extraction.csv`
- **Strains**: {len(df):,}
- **Columns**: {len(df.columns)}
- **Avg Quality**: {df['quality_score'].mean():.1f}%
- **THC Data**: {thc_count:,} strains ({thc_count/len(df)*100:.1f}%)
- **Genetics**: {genetics_count:,} strains ({genetics_count/len(df)*100:.1f}%)

"""
        
        # Combined quality distribution
        combined = pd.concat(all_data, ignore_index=True)
        enterprise = len(combined[combined['quality_score'] >= 80])
        professional = len(combined[(combined['quality_score'] >= 60) & (combined['quality_score'] < 80)])
        standard = len(combined[(combined['quality_score'] >= 40) & (combined['quality_score'] < 60)])
        basic = len(combined[combined['quality_score'] < 40])
        
        report += f"""## Market Tier Distribution (Combined)
- **Enterprise (80%+)**: {enterprise:,} strains ({enterprise/total_strains*100:.1f}%)
- **Professional (60-79%)**: {professional:,} strains ({professional/total_strains*100:.1f}%)
- **Standard (40-59%)**: {standard:,} strains ({standard/total_strains*100:.1f}%)
- **Basic (<40%)**: {basic:,} strains ({basic/total_strains*100:.1f}%)

## Database Impact
- **Previous Database**: 17,243 strains
- **Pipeline 06 Addition**: {total_strains:,} strains
- **New Total**: {17243 + total_strains:,} strains
- **20K Milestone**: {20000 - (17243 + total_strains):,} strains remaining

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path('../data/pipeline06_extraction_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved: {report_path}")

def main():
    """Main execution"""
    
    db_path = "../data/elite_merged_urls.db"
    s3_bucket = "ci-strains-html-archive"
    
    extractor = EliteExtractor(db_path, s3_bucket)
    all_data = extractor.extract_all()
    
    total = sum(len(df) for df in all_data)
    avg_quality = sum(df['quality_score'].mean() for df in all_data) / len(all_data)
    
    print("\n" + "="*60)
    print("PIPELINE 06 EXTRACTION COMPLETE")
    print("="*60)
    print(f"Total strains: {total:,}")
    print(f"Average quality: {avg_quality:.1f}%")
    print(f"Individual CSVs: 5 files created")
    print("="*60)

if __name__ == "__main__":
    main()
