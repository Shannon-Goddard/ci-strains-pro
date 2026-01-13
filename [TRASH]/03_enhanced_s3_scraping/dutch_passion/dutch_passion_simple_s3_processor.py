#!/usr/bin/env python3
"""
Dutch Passion Simple S3 Processor - Testing Proven Approach
Uses the exact same regex patterns that achieved 71.7% success
"""

import json
import boto3
import pandas as pd
import re
from datetime import datetime

class DutchPassionSimpleS3Processor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        
        # Success tracking
        self.total_processed = 0
        self.successful_extractions = 0
        self.method_stats = {'structured': 0, 'description': 0, 'patterns': 0, 'fallback': 0}
        self.extracted_strains = []

    def method1_structured_extraction(self, html):
        """Method 1: Extract from structured HTML tables - Dutch Passion proven patterns"""
        data = {}
        
        # Extract from specification tables
        table_patterns = {
            'genetics': r'<td[^>]*>Genetics[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'flowering_time': r'<td[^>]*>Flowering[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'thc_content': r'<td[^>]*>THC[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'cbd_content': r'<td[^>]*>CBD[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'yield': r'<td[^>]*>Yield[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'height': r'<td[^>]*>Height[^<]*</td>\s*<td[^>]*>([^<]+)</td>',
            'seed_type': r'<td[^>]*>Type[^<]*</td>\s*<td[^>]*>([^<]+)</td>'
        }
        
        for field, pattern in table_patterns.items():
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                data[field] = match.group(1).strip()
        
        if data:
            self.method_stats['structured'] += 1
        
        return data

    def method2_description_mining(self, html):
        """Method 2: Mine data from product descriptions - Dutch Passion proven patterns"""
        data = {}
        
        # Extract description text
        desc_patterns = [
            r'<div[^>]*class="[^"]*description[^"]*"[^>]*>(.*?)</div>',
            r'<p[^>]*class="[^"]*product-description[^"]*"[^>]*>(.*?)</p>'
        ]
        
        description = ""
        for pattern in desc_patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                description = match.group(1)
                break
        
        if description:
            # Extract flowering time
            flowering_match = re.search(r'(\d+)[-\s]*(\d+)?\s*weeks?\s*flower', description, re.IGNORECASE)
            if flowering_match:
                if flowering_match.group(2):
                    data['flowering_time'] = f"{flowering_match.group(1)}-{flowering_match.group(2)} weeks"
                else:
                    data['flowering_time'] = f"{flowering_match.group(1)} weeks"
            
            # Extract THC content
            thc_match = re.search(r'(\d+(?:\.\d+)?)[-\s]*(\d+(?:\.\d+)?)?\s*%\s*THC', description, re.IGNORECASE)
            if thc_match:
                if thc_match.group(2):
                    data['thc_content'] = f"{thc_match.group(1)}-{thc_match.group(2)}%"
                else:
                    data['thc_content'] = f"{thc_match.group(1)}%"
            
            # Extract effects
            effect_keywords = ['euphoric', 'relaxing', 'energetic', 'creative', 'uplifting', 'calming']
            effects = []
            for keyword in effect_keywords:
                if re.search(rf'\b{keyword}\b', description, re.IGNORECASE):
                    effects.append(keyword)
            if effects:
                data['effects'] = ', '.join(effects)
        
        if data:
            self.method_stats['description'] += 1
        
        return data

    def method3_advanced_patterns(self, html, url):
        """Method 3: Advanced pattern matching - Dutch Passion proven patterns"""
        data = {}
        
        # Detect seed type from URL and content
        if '/autoflower-seeds' in url or 'auto-' in html.lower():
            data['seed_type'] = 'Autoflower'
            data['growth_type'] = 'Autoflower'
        elif '/feminized-seeds' in url or 'feminized' in html.lower():
            data['seed_type'] = 'Feminized'
            data['growth_type'] = 'Photoperiod'
        elif '/regular-seeds' in url:
            data['seed_type'] = 'Regular'
            data['growth_type'] = 'Photoperiod'
        
        # Extract terpene profiles
        terpene_pattern = r'terpene[^:]*:\s*([^<\n]+)'
        terpene_match = re.search(terpene_pattern, html, re.IGNORECASE)
        if terpene_match:
            data['terpene_profile'] = terpene_match.group(1).strip()
        
        # Extract awards
        award_pattern = r'(cup|award|winner|champion)[^<\n]*([^<\n]{10,50})'
        award_match = re.search(award_pattern, html, re.IGNORECASE)
        if award_match:
            data['awards'] = award_match.group(0).strip()
        
        if data:
            self.method_stats['patterns'] += 1
        
        return data

    def method4_fallback_extraction(self, html, url):
        """Method 4: Universal fallback - Dutch Passion proven patterns"""
        data = {}
        
        # Extract strain name from URL
        strain_match = re.search(r'/cannabis-seeds/([^/?]+)', url)
        if strain_match:
            strain_name = strain_match.group(1).replace('-', ' ').title()
            data['strain_name'] = strain_name
        
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            if 'Dutch Passion' in title:
                data['page_title'] = title
        
        # Set hardcoded values - Dutch Passion proven approach
        data['seed_bank'] = 'Dutch Passion'
        data['breeder_name'] = 'Dutch Passion'
        data['source_url'] = url
        data['scraped_at'] = datetime.utcnow().isoformat()
        
        self.method_stats['fallback'] += 1
        return data

    def extract_strain_data(self, html_content, s3_key):
        """Extract strain data using Dutch Passion's proven 4-method approach"""
        
        # Apply all 4 methods
        strain_data = {}
        
        # Method 1: Structured extraction
        structured_data = self.method1_structured_extraction(html_content)
        strain_data.update(structured_data)
        
        # Method 2: Description mining
        description_data = self.method2_description_mining(html_content)
        strain_data.update(description_data)
        
        # Method 3: Advanced patterns
        pattern_data = self.method3_advanced_patterns(html_content, s3_key)
        strain_data.update(pattern_data)
        
        # Method 4: Universal fallback (always runs)
        fallback_data = self.method4_fallback_extraction(html_content, s3_key)
        strain_data.update(fallback_data)
        
        # Calculate quality score - Dutch Passion proven method
        quality_score = self._calculate_quality_score(strain_data)
        strain_data['quality_score'] = quality_score
        
        return strain_data

    def _calculate_quality_score(self, data):
        """Calculate quality score (0-100) - Dutch Passion proven method"""
        core_fields = ['strain_name', 'genetics', 'flowering_time', 'thc_content', 'seed_type']
        bonus_fields = ['cbd_content', 'yield', 'height', 'effects', 'terpene_profile', 'awards']
        
        score = 0
        
        # Core fields (20 points each)
        for field in core_fields:
            if field in data and data[field]:
                score += 20
        
        # Bonus fields (5 points each, max 30)
        bonus_score = 0
        for field in bonus_fields:
            if field in data and data[field]:
                bonus_score += 5
        score += min(bonus_score, 30)
        
        return min(score, 100)

    def process_s3_files(self):
        """Process Dutch Passion HTML files from S3 archive"""
        print("DUTCH PASSION SIMPLE S3 PROCESSOR")
        print("Testing proven regex-based approach...")
        
        # List Dutch Passion files in S3
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='dutch-passion/'
            )
            
            if 'Contents' not in response:
                print("No Dutch Passion files found in S3 archive")
                return
            
            html_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.html')]
            print(f"Found {len(html_files)} HTML files to process")
            
            for i, s3_key in enumerate(html_files, 1):
                self.total_processed += 1
                print(f"\n[{i}/{len(html_files)}] Processing: {s3_key}")
                
                try:
                    # Download HTML from S3
                    obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
                    html_content = obj['Body'].read().decode('utf-8', errors='ignore')
                    
                    # Apply 4-method extraction
                    strain_data = self.extract_strain_data(html_content, s3_key)
                    
                    # Quality validation (minimum 40% score like original Dutch Passion)
                    if strain_data['quality_score'] >= 40:
                        self.extracted_strains.append(strain_data)
                        self.successful_extractions += 1
                        
                        print(f"  SUCCESS: {strain_data.get('strain_name', 'Unknown')}")
                        print(f"     Quality: {strain_data['quality_score']:.1f}%")
                        
                        # Show key fields if present
                        if strain_data.get('genetics'):
                            print(f"     Genetics: {strain_data['genetics'][:50]}...")
                        if strain_data.get('thc_content'):
                            print(f"     THC: {strain_data['thc_content']}")
                        
                    else:
                        print(f"  LOW QUALITY: {strain_data['quality_score']:.1f}% - skipped")
                        
                except Exception as e:
                    print(f"  ERROR processing {s3_key}: {e}")
            
            # Save results to CSV
            if self.extracted_strains:
                df = pd.DataFrame(self.extracted_strains)
                csv_filename = f"dutch_passion_simple_extracted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(csv_filename, index=False, encoding='utf-8')
                print(f"\nResults saved to: {csv_filename}")
            
            self.print_final_stats()
            
        except Exception as e:
            print(f"S3 processing error: {e}")

    def print_final_stats(self):
        """Print final statistics - Dutch Passion proven style"""
        success_rate = (self.successful_extractions / self.total_processed * 100) if self.total_processed > 0 else 0
        
        print(f"\nDUTCH PASSION SIMPLE PROCESSING COMPLETE")
        print(f"Total Processed: {self.total_processed}")
        print(f"Successful: {self.successful_extractions}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"\nMethod Usage:")
        for method, count in self.method_stats.items():
            print(f"  {method.title()}: {count}")

def main():
    processor = DutchPassionSimpleS3Processor()
    processor.process_s3_files()

if __name__ == "__main__":
    main()