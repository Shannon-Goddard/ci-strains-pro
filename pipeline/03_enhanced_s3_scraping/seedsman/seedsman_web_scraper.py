#!/usr/bin/env python3
"""
Seedsman Web Scraper - HTML Collection Phase
Collects strain HTML pages and stores in S3 ci-strains-html-archive
Following proven methodology from Multiverse Beans success
"""

import requests
import boto3
import json
import hashlib
import time
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SeedsmanScraper:
    def __init__(self):
        self.base_url = "https://www.seedsman.com"
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'ci-strains-html-archive'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def discover_strain_urls(self) -> list:
        """Discover all strain product URLs from Seedsman"""
        logger.info("Discovering Seedsman strain URLs...")
        strain_urls = []
        
        # Seedsman category pages to scrape (updated URLs)
        category_urls = [
            "/us-en/cannabis-seeds/flowering-type/feminized-cannabis-seeds",
            "/us-en/cannabis-seeds/flowering-type/autoflowering-cannabis-seeds", 
            "/us-en/cannabis-seeds/flowering-type/regular-cannabis-seeds",
            "/us-en/cannabis-seeds/thc-cbd-content/cbd-cannabis-seeds"
        ]
        
        for category in category_urls:
            logger.info(f"Scraping category: {category}")
            page = 1
            
            while True:
                try:
                    url = f"{self.base_url}{category}?p={page}"
                    response = self.session.get(url, timeout=30)
                    
                    if response.status_code != 200:
                        logger.warning(f"Failed to fetch {url}: {response.status_code}")
                        break
                        
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find product links - updated pattern for new site structure
                    product_links = soup.find_all('a', href=re.compile(r'/us-en/[^/]+-seeds$'))
                    
                    if not product_links:
                        logger.info(f"No more products found on page {page}")
                        break
                        
                    page_urls = []
                    for link in product_links:
                        href = link.get('href')
                        if href and href not in strain_urls:
                            full_url = urljoin(self.base_url, href)
                            strain_urls.append(full_url)
                            page_urls.append(full_url)
                    
                    logger.info(f"Found {len(page_urls)} strains on page {page}")
                    page += 1
                    time.sleep(1)  # Rate limiting
                    
                    # Safety limit
                    if page > 100:
                        logger.warning("Hit page limit, stopping")
                        break
                        
                except Exception as e:
                    logger.error(f"Error scraping {category} page {page}: {e}")
                    break
        
        logger.info(f"Total strain URLs discovered: {len(strain_urls)}")
        return strain_urls
    
    def generate_hash(self, url: str) -> str:
        """Generate consistent hash for URL"""
        return hashlib.md5(url.encode('utf-8')).hexdigest()
    
    def fetch_strain_html(self, url: str) -> tuple:
        """Fetch HTML content for a strain page"""
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                html_content = response.text
                
                # Basic validation
                if len(html_content) > 5000 and 'seedsman' in html_content.lower():
                    return html_content, True
                else:
                    logger.warning(f"Invalid content for {url}")
                    return None, False
            else:
                logger.warning(f"HTTP {response.status_code} for {url}")
                return None, False
                
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None, False
    
    def upload_to_s3(self, html_content: str, url: str, hash_id: str) -> bool:
        """Upload HTML and metadata to S3"""
        try:
            # Upload HTML
            html_key = f"html/{hash_id}.html"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=html_key,
                Body=html_content.encode('utf-8'),
                ContentType='text/html'
            )
            
            # Create metadata
            metadata = {
                'url': url,
                'hash': hash_id,
                'timestamp': datetime.now().isoformat(),
                'source': 'seedsman.com',
                'collection_method': 'web_scraper',
                'html_size': len(html_content)
            }
            
            # Upload metadata
            metadata_key = f"metadata/{hash_id}.json"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=metadata_key,
                Body=json.dumps(metadata, indent=2).encode('utf-8'),
                ContentType='application/json'
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error uploading to S3: {e}")
            return False
    
    def scrape_all_strains(self):
        """Main scraping process"""
        logger.info("Starting Seedsman HTML collection...")
        
        # Discover URLs
        strain_urls = self.discover_strain_urls()
        
        if not strain_urls:
            logger.error("No strain URLs found!")
            return
        
        # Process each strain
        successful = 0
        failed = 0
        
        for i, url in enumerate(strain_urls, 1):
            try:
                logger.info(f"Processing {i}/{len(strain_urls)}: {url}")
                
                # Generate hash
                hash_id = self.generate_hash(url)
                
                # Fetch HTML
                html_content, success = self.fetch_strain_html(url)
                
                if success and html_content:
                    # Upload to S3
                    if self.upload_to_s3(html_content, url, hash_id):
                        successful += 1
                        logger.info(f"✅ Successfully stored {hash_id}")
                    else:
                        failed += 1
                        logger.error(f"❌ Failed to upload {hash_id}")
                else:
                    failed += 1
                    logger.error(f"❌ Failed to fetch {url}")
                
                # Rate limiting
                time.sleep(2)
                
                # Progress update
                if i % 50 == 0:
                    success_rate = (successful / i) * 100
                    logger.info(f"Progress: {i}/{len(strain_urls)} ({success_rate:.1f}% success)")
                    
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                failed += 1
        
        # Final report
        total = successful + failed
        success_rate = (successful / total) * 100 if total > 0 else 0
        
        logger.info("=== SEEDSMAN COLLECTION COMPLETE ===")
        logger.info(f"Total URLs: {len(strain_urls)}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        
        return {
            'total_urls': len(strain_urls),
            'successful': successful,
            'failed': failed,
            'success_rate': success_rate
        }

def main():
    scraper = SeedsmanScraper()
    results = scraper.scrape_all_strains()
    
    if results:
        print(f"\nSeedsman collection completed:")
        print(f"Success: {results['successful']}/{results['total_urls']} ({results['success_rate']:.1f}%)")

if __name__ == "__main__":
    main()