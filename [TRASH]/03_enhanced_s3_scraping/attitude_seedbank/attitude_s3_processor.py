#!/usr/bin/env python3
"""
Attitude Seedbank S3 Processor
Uses metadata mapping to process HTML files with Attitude's proven 4-method extraction
Target: 7,734 strains (99.5% success rate) - LARGEST COLLECTION
"""

import json
import boto3
import pandas as pd
import re
from datetime import datetime

class AttitudeSeedbankS3Processor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        
        # Success tracking
        self.total_processed = 0
        self.successful_extractions = 0
        self.extracted_strains = []

    def load_attitude_urls(self):
        """Load Attitude URLs from metadata files"""
        print("Loading Attitude Seedbank URLs from metadata...")
        
        attitude_files = []
        
        # List all metadata files
        paginator = self.s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix='metadata/')
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    if obj['Key'].endswith('.json'):
                        try:
                            # Download metadata
                            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=obj['Key'])
                            metadata = json.loads(response['Body'].read().decode('utf-8'))
                            
                            url = metadata.get('url', '')
                            url_hash = metadata.get('url_hash', '')
                            
                            # Check if it's Attitude Seedbank
                            if 'cannabis-seeds-bank.co.uk' in url.lower():
                                attitude_files.append((url, url_hash))
                                
                        except Exception as e:
                            continue
        
        print(f"Found {len(attitude_files)} Attitude Seedbank files")
        return attitude_files

    def extract_strain_data(self, html, url):
        """Extract strain data using Attitude's proven 4-method approach"""
        data = {
            'bank_name': 'The Attitude Seed Bank',
            'url': url,
            'scraped_at': datetime.utcnow().isoformat()
        }
        
        # Extract strain name from product title
        title_match = re.search(r'<h2[^>]*class="productHeading"[^>]*>([^<]+)</h2>', html)
        if title_match:
            data['strain_name'] = title_match.group(1).strip()
        
        # Extract characteristics from structured list
        char_patterns = {
            'genetics': r'Genetics[^>]*>([^<]+)</span>',
            'sex': r'Sex[^>]*>([^<]+)</span>',
            'flowering': r'Flowering[^>]*>([^<]+)</span>',
            'type': r'Type[^>]*>([^<]+)</span>',
            'flowering_time': r'Flowering Time[^>]*>([^<]+)</span>',
            'height': r'Height[^>]*>([^<]+)</span>',
            'area': r'Area[^>]*>([^<]+)</span>'
        }
        
        for field, pattern in char_patterns.items():
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                data[field] = match.group(1).strip()
        
        # Extract detailed information from description
        desc_match = re.search(r'<div[^>]*id="tabDesc"[^>]*>(.*?)</div>', html, re.DOTALL)
        if desc_match:
            desc_text = desc_match.group(1)
            data['about_info'] = desc_text.strip()
            
            # Extract breeder using pattern matching
            breeder_match = re.search(r'Cannabis Seeds by ([^\n]+?)(?:\s|$)', desc_text)
            if breeder_match:
                data['breeder_name'] = breeder_match.group(1).strip()
            
            # Extract specific cultivation data using regex
            cultivation_patterns = {
                'thc_content': r'THC:\s*(\d+%)',
                'yield_indoor': r'Yield:\s*([\d\s-]+gr/m2)',
                'height_indoor': r'Height:\s*([\d\s-]+cm)',
                'cultivation_time': r'Total Cultivation:\s*([\d\s-]+days)',
                'harvest_period': r'Harvest:\s*(From [^\n]+)'
            }
            
            for field, pattern in cultivation_patterns.items():
                match = re.search(pattern, desc_text)
                if match:
                    data[field] = match.group(1).strip()
            
            # Outdoor height - second height match is usually outdoor
            height_matches = re.findall(r'Height:\s*(\d+\s*-\s*\d+\s*cm)', desc_text)
            if len(height_matches) > 1:
                data['height_outdoor'] = height_matches[1].strip()
        
        return data

    def process_attitude_strains(self):
        """Process all Attitude Seedbank strains"""
        print("ATTITUDE SEEDBANK S3 PROCESSOR")
        print("Target: 7,734 strains (99.5% success rate)")
        print("=" * 60)
        
        # Load Attitude URLs
        attitude_files = self.load_attitude_urls()
        
        if not attitude_files:
            print("No Attitude files found!")
            return
        
        # Process each strain
        for i, (url, url_hash) in enumerate(attitude_files, 1):
            self.total_processed += 1
            print(f"\n[{i}/{len(attitude_files)}] Processing: {url_hash}")
            
            try:
                # Download HTML from S3
                response = self.s3_client.get_object(Bucket=self.bucket_name, Key=f'html/{url_hash}.html')
                html_content = response['Body'].read().decode('utf-8', errors='ignore')
                
                # Extract strain data
                strain_data = self.extract_strain_data(html_content, url)
                
                # Validate required fields
                if strain_data.get('strain_name'):
                    self.extracted_strains.append(strain_data)
                    self.successful_extractions += 1
                    
                    print(f"  SUCCESS: {strain_data.get('strain_name')} - {strain_data.get('breeder_name', 'Unknown Breeder')}")
                    
                    # Show key fields if present
                    if strain_data.get('genetics'):
                        print(f"     Genetics: {strain_data['genetics'][:50]}...")
                    if strain_data.get('thc_content'):
                        print(f"     THC: {strain_data['thc_content']}")
                    
                else:
                    print(f"  SKIPPED: No strain name found")
                    
            except Exception as e:
                print(f"  ERROR processing {url_hash}: {e}")
        
        # Save results to CSV
        if self.extracted_strains:
            df = pd.DataFrame(self.extracted_strains)
            csv_filename = f"attitude_seedbank_commercial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(csv_filename, index=False, encoding='utf-8')
            print(f"\nCOMMERCIAL CSV SAVED: {csv_filename}")
            print(f"READY FOR SALE: {len(self.extracted_strains)} strains")
        
        self.print_final_stats()

    def print_final_stats(self):
        """Print final statistics"""
        success_rate = (self.successful_extractions / self.total_processed * 100) if self.total_processed > 0 else 0
        
        print(f"\nATTITUDE SEEDBANK PROCESSING COMPLETE!")
        print(f"Total Processed: {self.total_processed}")
        print(f"Successful: {self.successful_extractions}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.successful_extractions > 0:
            print(f"\nTarget: 7,734 strains (original success)")
            print(f"Current: {self.successful_extractions} strains")
            coverage = (self.successful_extractions / 7734) * 100
            print(f"Coverage: {coverage:.1f}% of original collection")

def main():
    processor = AttitudeSeedbankS3Processor()
    processor.process_attitude_strains()

if __name__ == "__main__":
    main()