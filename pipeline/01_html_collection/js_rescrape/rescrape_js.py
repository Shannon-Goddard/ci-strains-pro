#!/usr/bin/env python3
"""
JavaScript Rescrape: ILGM & Seedsman
Designed and executed by Amazon Q, funded by Shannon Goddard
"""

import requests
import boto3
import pandas as pd
import time
import hashlib
import json
from datetime import datetime
import logging
import argparse
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class SecretsManager:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)
    
    def get_secret(self, secret_name):
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            raise e
    
    def get_scrapingbee_key(self):
        secret = self.get_secret('cannabis_scrapingbee_api')
        return secret['api_key']

class JSRescraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.s3 = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.results = []
        self.success_count = 0
        self.fail_count = 0
        
    def scrape_url(self, url, retries=3):
        """Scrape URL with JavaScript rendering"""
        params = {
            'api_key': self.api_key,
            'url': url,
            'render_js': 'true',
            'wait': 5000,
            'premium_proxy': 'true',
            'country_code': 'us'
        }
        
        for attempt in range(retries):
            try:
                response = requests.get('https://app.scrapingbee.com/api/v1/', params=params, timeout=60)
                
                if response.status_code == 200:
                    return response.text, True
                else:
                    logger.warning(f"Attempt {attempt+1} failed for {url}: {response.status_code}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
            except Exception as e:
                logger.error(f"Attempt {attempt+1} error for {url}: {e}")
                time.sleep(2 ** attempt)
        
        return None, False
    
    def upload_to_s3(self, url_hash, html, seed_bank):
        """Upload HTML to S3"""
        key = f"html_js/{url_hash}_js.html"
        
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=html.encode('utf-8'),
                Metadata={
                    'scrape_method': 'javascript_render',
                    'scrape_date': datetime.now().isoformat(),
                    'seed_bank': seed_bank,
                    'tool': 'scrapingbee'
                }
            )
            return True
        except Exception as e:
            logger.error(f"S3 upload failed for {url_hash}: {e}")
            return False
    
    def process_urls(self, urls, seed_bank, upload_s3=True):
        """Process list of URLs"""
        logger.info(f"Starting {seed_bank} scrape: {len(urls)} URLs")
        
        for idx, url in enumerate(urls, 1):
            # Generate hash (first 16 chars to match S3 inventory)
            url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
            
            # Scrape
            html, success = self.scrape_url(url)
            
            if success and html:
                # Validate content
                has_content = len(html) > 50000  # Basic size check
                
                if has_content:
                    # Upload to S3
                    if upload_s3:
                        s3_success = self.upload_to_s3(url_hash, html, seed_bank)
                    else:
                        s3_success = True
                    
                    if s3_success:
                        self.success_count += 1
                        logger.info(f"✅ [{idx}/{len(urls)}] {seed_bank}: {url[:60]}...")
                    else:
                        self.fail_count += 1
                        logger.error(f"❌ S3 upload failed: {url}")
                else:
                    self.fail_count += 1
                    logger.warning(f"⚠️ Content too small: {url}")
            else:
                self.fail_count += 1
                logger.error(f"❌ Scrape failed: {url}")
            
            # Log result
            self.results.append({
                'url': url,
                'url_hash': url_hash,
                'seed_bank': seed_bank,
                'success': success,
                'timestamp': datetime.now().isoformat()
            })
            
            # Rate limiting
            time.sleep(0.1)  # 10 requests/second
            
            # Progress update every 25
            if idx % 25 == 0:
                logger.info(f"Progress: {idx}/{len(urls)} | Success: {self.success_count} | Failed: {self.fail_count}")
        
        logger.info(f"✅ {seed_bank} complete: {self.success_count}/{len(urls)} successful")
    
    def save_results(self):
        """Save results to CSV"""
        df = pd.DataFrame(self.results)
        df.to_csv('results/scrape_log.csv', index=False)
        
        with open('results/success_count.txt', 'w') as f:
            f.write(f"Success: {self.success_count}\n")
            f.write(f"Failed: {self.fail_count}\n")
            f.write(f"Total: {len(self.results)}\n")
            f.write(f"Success Rate: {self.success_count/len(self.results)*100:.1f}%\n")
        
        failed = df[~df['success']]
        if len(failed) > 0:
            failed['url'].to_csv('results/failed_urls.txt', index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description='JavaScript Rescrape for ILGM & Seedsman')
    parser.add_argument('--seed-bank', choices=['ilgm', 'seedsman', 'all'], default='all')
    parser.add_argument('--upload-s3', type=bool, default=True)
    args = parser.parse_args()
    
    # Get API key from AWS Secrets Manager
    logger.info("Fetching ScrapingBee API key from AWS Secrets Manager...")
    secrets = SecretsManager()
    api_key = secrets.get_scrapingbee_key()
    logger.info("✅ API key retrieved")
    
    # Load S3 inventory
    logger.info("Loading S3 inventory...")
    inv = pd.read_csv('../../03_s3_inventory/s3_html_inventory.csv', encoding='latin-1')
    
    # Initialize scraper
    scraper = JSRescraper(api_key)
    
    # Process ILGM
    if args.seed_bank in ['ilgm', 'all']:
        ilgm_urls = inv[inv['url'].str.contains('ilgm.com', na=False)]['url'].tolist()
        logger.info(f"Loaded {len(ilgm_urls)} ILGM URLs")
        scraper.process_urls(ilgm_urls, 'ILGM', args.upload_s3)
    
    # Process Seedsman
    if args.seed_bank in ['seedsman', 'all']:
        seedsman_urls = inv[inv['url'].str.contains('seedsman.com', na=False)]['url'].tolist()
        logger.info(f"Loaded {len(seedsman_urls)} Seedsman URLs")
        scraper.process_urls(seedsman_urls, 'Seedsman', args.upload_s3)
    
    # Save results
    scraper.save_results()
    
    logger.info(f"""
    ╔══════════════════════════════════════╗
    ║   JavaScript Rescrape Complete! 🎉   ║
    ╠══════════════════════════════════════╣
    ║  Success: {scraper.success_count:4d}                       ║
    ║  Failed:  {scraper.fail_count:4d}                       ║
    ║  Total:   {len(scraper.results):4d}                       ║
    ║  Rate:    {scraper.success_count/len(scraper.results)*100:5.1f}%                     ║
    ╚══════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
