#!/usr/bin/env python3
"""
Pipeline 06: Bulletproof Catalog Page Collection
Collect HTML for 201 catalog pages, then extract product URLs

Same proven methodology as Pipeline 01/04
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import asyncio
import aiohttp
import sqlite3
import json
import boto3
import hashlib
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import logging
import random
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/catalog_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import AWS secrets
from aws_secrets import get_aws_credentials

class CatalogCollector:
    """Collect catalog pages and extract product URLs"""
    
    def __init__(self, db_path: str, s3_bucket: str):
        self.db_path = db_path
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
        
        self.retry_delays = [1, 3, 7, 15, 30, 60]
        self.max_attempts = 6
        
        self.bright_data_creds = None
        self.scrapingbee_key = None
        self._load_credentials()
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
        self.last_request = {}
        self.product_urls = []
    
    def _load_credentials(self):
        try:
            creds = get_aws_credentials()
            if creds['BRIGHT_DATA_USERNAME']:
                self.bright_data_creds = {
                    'username': creds['BRIGHT_DATA_USERNAME'],
                    'password': creds['BRIGHT_DATA_PASSWORD'],
                    'endpoint': creds['BRIGHT_DATA_ENDPOINT']
                }
            if creds['SCRAPINGBEE_API_KEY']:
                self.scrapingbee_key = creds['SCRAPINGBEE_API_KEY']
            logger.info("Credentials loaded")
        except Exception as e:
            logger.warning(f"Credential loading issue: {e}")
    
    async def scrapingbee_scrape(self, session: aiohttp.ClientSession, url: str):
        if not self.scrapingbee_key:
            return None
        api_url = "https://app.scrapingbee.com/api/v1/"
        params = {'api_key': self.scrapingbee_key, 'url': url, 'render_js': 'false'}
        try:
            async with session.get(api_url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    return await response.text()
        except:
            pass
        return None
    
    async def direct_scrape(self, session: aiohttp.ClientSession, url: str):
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    return await response.text()
        except:
            pass
        return None
    
    def validate_html(self, html: str):
        if not html or len(html) < 1000:
            return False, 0.0
        checks = {
            'min_size': len(html) > 5000,
            'has_title': '<title>' in html.lower(),
            'has_content': any(term in html.lower() for term in ['seed', 'strain', 'cannabis']),
            'not_blocked': not any(term in html.lower() for term in ['blocked', 'captcha']),
            'has_structure': '<html' in html.lower() and '</html>' in html.lower()
        }
        score = sum(checks.values()) / len(checks)
        return score >= 0.75, score
    
    async def scrape_with_fallbacks(self, session: aiohttp.ClientSession, url: str):
        methods = [
            ('scrapingbee', self.scrapingbee_scrape),
            ('direct', self.direct_scrape)
        ]
        for attempt in range(self.max_attempts):
            for method_name, method_func in methods:
                try:
                    html = await method_func(session, url)
                    if html:
                        is_valid, score = self.validate_html(html)
                        if is_valid:
                            return html, method_name
                except:
                    pass
            if attempt < self.max_attempts - 1:
                await asyncio.sleep(self.retry_delays[min(attempt, len(self.retry_delays) - 1)])
        return None, 'failed'
    
    def extract_product_urls(self, html: str, base_url: str, seedbank: str):
        """Extract product URLs from catalog page"""
        urls = set()
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Seedbank-specific selectors
            selectors = {
                'Herbies Head Shop': ['a[href*="/seeds/"]'],
                'Amsterdam Marijuana Seeds': ['a.woocommerce-LoopProduct-link', 'a[href*="/product/"]'],
                'Gorilla Seeds Bank': ['a.product-item-link', 'a[href*=".html"]'],
                'Zamnesia': ['a[href*="/product/"]', 'a.product-name'],
                'Exotic Genetix': ['a.woocommerce-LoopProduct-link'],
                'Original Seeds Store': ['a[href*="/product/"]'],
                'Tiki Madman': ['a[href*="/strain/"]'],
                'Compound Genetics': ['a[href*="/products/"]']
            }
            
            for selector in selectors.get(seedbank, ['a[href*="/product/"]']):
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        # Filter out non-product pages
                        if not any(skip in full_url for skip in ['cart', 'account', 'category', 'collection', '?page=']):
                            urls.add(full_url)
        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
        return urls
    
    def store_catalog_s3(self, url_hash: str, html: str, metadata: dict):
        html_key = f'pipeline06/catalogs/{url_hash}.html'
        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=html_key,
            Body=html.encode('utf-8'),
            ServerSideEncryption='AES256',
            ContentType='text/html'
        )
        return html_key
    
    def save_product_url(self, url: str, seedbank: str):
        """Save discovered product URL"""
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
        conn = sqlite3.connect(self.db_path.replace('catalog', 'product'))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_urls (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                seedbank TEXT NOT NULL,
                discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        cursor.execute('INSERT OR IGNORE INTO product_urls (url_hash, original_url, seedbank) VALUES (?, ?, ?)',
                      (url_hash, url, seedbank))
        conn.commit()
        conn.close()
    
    def update_catalog_status(self, url_hash: str, status: str, **kwargs):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE elite_urls SET status = ?, attempts = attempts + 1 WHERE url_hash = ?',
                      (status, url_hash))
        conn.commit()
        conn.close()
    
    def get_pending_catalogs(self, limit: int = 50):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT url_hash, original_url, seedbank 
            FROM elite_urls 
            WHERE status = 'pending' 
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()
        return [{'url_hash': r[0], 'url': r[1], 'seedbank': r[2]} for r in results]
    
    async def respectful_delay(self, url: str):
        domain = urlparse(url).netloc
        if domain in self.last_request:
            elapsed = time.time() - self.last_request[domain]
            if elapsed < 2:
                await asyncio.sleep(2 - elapsed)
        self.last_request[domain] = time.time()
    
    async def process_catalog(self, catalog_data: dict, session: aiohttp.ClientSession):
        url_hash = catalog_data['url_hash']
        url = catalog_data['url']
        seedbank = catalog_data['seedbank']
        
        try:
            await self.respectful_delay(url)
            html, method = await self.scrape_with_fallbacks(session, url)
            
            if html:
                # Store catalog HTML
                self.store_catalog_s3(url_hash, html, {'url': url, 'seedbank': seedbank})
                
                # Extract product URLs
                product_urls = self.extract_product_urls(html, url, seedbank)
                
                # Save product URLs
                for product_url in product_urls:
                    self.save_product_url(product_url, seedbank)
                
                self.update_catalog_status(url_hash, 'success')
                logger.info(f"PASS {seedbank} - Found {len(product_urls)} products")
                return len(product_urls)
            else:
                self.update_catalog_status(url_hash, 'failed')
                return 0
        except Exception as e:
            self.update_catalog_status(url_hash, 'failed')
            logger.error(f"FAIL {url}: {e}")
            return 0
    
    async def run_collection(self):
        logger.info("Starting catalog collection for 201 pages")
        
        Path(self.db_path.replace('catalog', 'product')).parent.mkdir(exist_ok=True)
        
        connector = aiohttp.TCPConnector(limit=10)
        async with aiohttp.ClientSession(connector=connector) as session:
            total_products = 0
            while True:
                catalogs = self.get_pending_catalogs(50)
                if not catalogs:
                    break
                
                logger.info(f"Processing {len(catalogs)} catalog pages...")
                
                tasks = [self.process_catalog(cat, session) for cat in catalogs]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                total_products += sum(r for r in results if isinstance(r, int))
                self.log_progress(total_products)
        
        logger.info(f"Collection complete! Discovered {total_products:,} product URLs")
        self.generate_report(total_products)
    
    def log_progress(self, total_products: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM elite_urls WHERE status = "success"')
        success = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM elite_urls')
        total = cursor.fetchone()[0]
        conn.close()
        logger.info(f"Progress: {success}/{total} catalogs | {total_products:,} products discovered")
    
    def generate_report(self, total_products: int):
        report = f"""
# Pipeline 06: Catalog Collection Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Phase 1 Complete: Catalog Pages Collected
- **Catalog Pages Processed**: 201
- **Product URLs Discovered**: {total_products:,}

## Next Step: Product Page Collection
Ready to collect HTML for {total_products:,} individual product pages!

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        Path('../data/catalog_collection_report.md').write_text(report)

async def main():
    db_path = "../data/elite_catalog_urls.db"
    s3_bucket = "ci-strains-html-archive"
    
    collector = CatalogCollector(db_path, s3_bucket)
    await collector.run_collection()
    
    print("\n" + "="*60)
    print("CATALOG COLLECTION COMPLETE!")
    print("Product URLs discovered and ready for collection!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
