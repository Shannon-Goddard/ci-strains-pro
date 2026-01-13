#!/usr/bin/env python3

import boto3
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class S3SeedsmanProcessor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        self.results = []
        
    def get_seedsman_metadata(self):
        """Get all metadata files for Seedsman URLs"""
        logger.info("Fetching Seedsman metadata from S3...")
        
        paginator = self.s3_client.get_paginator('list_objects_v2')
        seedsman_files = []
        
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix='metadata/'):
            if 'Contents' in page:
                for obj in page['Contents']:
                    try:
                        # Get metadata file
                        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=obj['Key'])
                        metadata = json.loads(response['Body'].read().decode('utf-8'))
                        
                        # Check if it's a Seedsman URL
                        if 'seedsman.com' in metadata.get('url', ''):
                            seedsman_files.append(metadata)
                            
                    except Exception as e:
                        logger.warning(f"Error processing {obj['Key']}: {e}")
                        
        logger.info(f"Found {len(seedsman_files)} Seedsman files in S3")
        return seedsman_files
    
    def extract_strain_data(self, html_content, url):
        """Extract strain data using 4-method approach"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for JavaScript dependency
        text_content = soup.get_text().lower()
        if 'javascript' in text_content and 'enable' in text_content:
            return None
            
        data = {
            'url': url,
            'strain_name': '',
            'genetics_sativa': '',
            'genetics_indica': '',
            'thc_min': '',
            'thc_max': '',
            'cbd_min': '',
            'cbd_max': '',
            'flowering_time': '',
            'yield_info': '',
            'breeder': '',
            'description': ''
        }
        
        # Extract strain name from title
        title = soup.find('title')
        if title:
            title_text = title.get_text()
            # Remove "Seedsman" and common suffixes
            strain_name = re.sub(r'(Seedsman|Cannabis Seeds|Buy Online).*', '', title_text).strip()
            data['strain_name'] = strain_name
        
        # Extract genetics percentages
        text = soup.get_text()
        sativa_match = re.search(r'(\d+)%\s*[Ss]ativa', text)
        indica_match = re.search(r'(\d+)%\s*[Ii]ndica', text)
        
        if sativa_match:
            data['genetics_sativa'] = sativa_match.group(1)
        if indica_match:
            data['genetics_indica'] = indica_match.group(1)
            
        # Extract THC content
        thc_match = re.search(r'THC[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)%', text)
        if thc_match:
            data['thc_min'] = thc_match.group(1)
            data['thc_max'] = thc_match.group(2)
        else:
            single_thc = re.search(r'THC[:\s]*(\d+(?:\.\d+)?)%', text)
            if single_thc:
                data['thc_min'] = data['thc_max'] = single_thc.group(1)
        
        # Extract CBD content
        cbd_match = re.search(r'CBD[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)%', text)
        if cbd_match:
            data['cbd_min'] = cbd_match.group(1)
            data['cbd_max'] = cbd_match.group(2)
        else:
            single_cbd = re.search(r'CBD[:\s]*(\d+(?:\.\d+)?)%', text)
            if single_cbd:
                data['cbd_min'] = data['cbd_max'] = single_cbd.group(1)
        
        # Extract flowering time
        flowering_match = re.search(r'flowering[:\s]*(\d+)\s*[-–]\s*(\d+)\s*weeks?', text, re.IGNORECASE)
        if flowering_match:
            data['flowering_time'] = f"{flowering_match.group(1)}-{flowering_match.group(2)} weeks"
        
        # Calculate quality score
        filled_fields = sum(1 for v in data.values() if v and v != url)
        quality_score = (filled_fields / (len(data) - 1)) * 100
        
        return data, quality_score
    
    def process_seedsman_files(self):
        """Process all Seedsman HTML files from S3"""
        metadata_files = self.get_seedsman_metadata()
        
        if not metadata_files:
            logger.error("No Seedsman files found in S3 archive")
            return
            
        logger.info(f"Processing {len(metadata_files)} Seedsman HTML files...")
        
        for i, metadata in enumerate(metadata_files, 1):
            try:
                url_hash = metadata['url_hash']
                url = metadata['url']
                
                # Get HTML file from S3
                html_key = f'html/{url_hash}.html'
                response = self.s3_client.get_object(Bucket=self.bucket_name, Key=html_key)
                html_content = response['Body'].read().decode('utf-8', errors='ignore')
                
                # Extract strain data
                result = self.extract_strain_data(html_content, url)
                
                if result:
                    strain_data, quality_score = result
                    strain_data['quality_score'] = quality_score
                    strain_data['url_hash'] = url_hash
                    self.results.append(strain_data)
                    
                    if i % 50 == 0:
                        logger.info(f"Processed {i}/{len(metadata_files)} files, avg quality: {sum(r['quality_score'] for r in self.results)/len(self.results):.1f}%")
                else:
                    logger.warning(f"JavaScript dependency detected in {url}")
                    
            except Exception as e:
                logger.error(f"Error processing {metadata.get('url', 'unknown')}: {e}")
        
        logger.info(f"Extraction complete! Processed {len(self.results)} valid Seedsman strains")
        
    def save_results(self):
        """Save results to CSV"""
        if not self.results:
            logger.error("No results to save")
            return
            
        df = pd.DataFrame(self.results)
        output_file = 'seedsman_s3_extraction.csv'
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        # Calculate statistics
        avg_quality = df['quality_score'].mean()
        high_quality = len(df[df['quality_score'] > 50])
        
        logger.info(f"Results saved to {output_file}")
        logger.info(f"Total strains: {len(df)}")
        logger.info(f"Average quality: {avg_quality:.1f}%")
        logger.info(f"High quality (>50%): {high_quality}")

def main():
    processor = S3SeedsmanProcessor()
    processor.process_seedsman_files()
    processor.save_results()

if __name__ == "__main__":
    main()