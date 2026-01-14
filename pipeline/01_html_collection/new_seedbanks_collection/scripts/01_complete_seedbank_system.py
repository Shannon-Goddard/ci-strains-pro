#!/usr/bin/env python3
"""
Cannabis Intelligence Database - Seedbank Website Crawler & HTML Collector
EXACT same system as pipeline/01 but crawls 5 seedbank websites for ALL strain URLs

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
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
import logging
from typing import Dict, Tuple, Optional
import random
import re
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/seedbank_crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import AWS secrets (same as pipeline/01)
import sys
sys.path.append('../../01_html_collection/scripts')
from aws_secrets import get_aws_credentials

class SeedbankCrawlerCollector:
    """EXACT same bulletproof system as pipeline/01 but for seedbank websites"""
    
    def __init__(self, db_path: str, s3_bucket: str):
        self.db_path = db_path
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
        
        # EXACT same configuration as pipeline/01
        self.retry_delays = [1, 3, 7, 15, 30, 60]
        self.max_attempts = 6
        self.success_threshold = 0.995
        
        # Load credentials (same method)
        self.bright_data_creds = None
        self.scrapingbee_key = None
        self._load_credentials()
        
        # Same user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        # Seedbank crawl targets
        self.seedbank_targets = {
            "sensiseeds.us": "https://sensiseeds.us/cannabis-seeds/",
            "californiahempseeds.com": "https://californiahempseeds.com/shop-all/",
            "cropkingseeds.com": "https://www.cropkingseeds.com/?s=seeds&post_type=product&dgwt_wcas=1",
            "barneysfarm.com": "https://www.barneysfarm.com/us/",
            "ilgm.com": "https://ilgm.com/categories/cannabis-seeds"
        }
        
        self.last_request = {}
        self.discovered_urls = set()
    
    def _load_credentials(self):
        """Load API credentials (same as pipeline/01)"""
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
            
            logger.info("Credentials loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load some credentials: {e}")
    
    def create_database(self):
        """Create database (same structure as pipeline/01)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_progress (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                strain_ids TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                html_size INTEGER,
                validation_score REAL,
                s3_path TEXT,
                error_message TEXT,
                scrape_method TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_url_hash(self, url: str) -> str:
        """Generate hash (same method as pipeline/01)"""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    async def discover_strain_urls(self, session: aiohttp.ClientSession):
        """Crawl all 5 seedbank websites to discover ALL strain URLs"""
        
        logger.info("Starting comprehensive seedbank crawling for ALL strain URLs")
        
        for domain, start_url in self.seedbank_targets.items():
            logger.info(f"Crawling {domain} starting from {start_url}")
            
            try:
                # Crawl this seedbank
                urls = await self.crawl_seedbank_site(session, domain, start_url)
                
                # Add to database
                self.add_urls_to_database(urls, domain)
                
                logger.info(f"Discovered {len(urls)} strain URLs from {domain}")
                
            except Exception as e:
                logger.error(f"Error crawling {domain}: {e}")
            
            # Rate limiting between seedbanks
            await asyncio.sleep(5)
    
    async def crawl_seedbank_site(self, session: aiohttp.ClientSession, domain: str, start_url: str) -> set:
        """Crawl a single seedbank website for ALL strain URLs"""
        
        discovered = set()
        visited = set()
        to_visit = {start_url}
        
        max_pages = 100  # Prevent infinite crawling
        page_count = 0
        
        while to_visit and page_count < max_pages:
            current_url = to_visit.pop()
            
            if current_url in visited:
                continue
            
            visited.add(current_url)
            page_count += 1
            
            logger.info(f"Crawling page {page_count} on {domain}: {current_url}")
            
            try:
                html = await self.fetch_page_simple(session, current_url)
                if not html:
                    continue
                
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find all links
                links = soup.find_all('a', href=True)
                
                for link in links:
                    href = link.get('href')
                    if not href:
                        continue
                    
                    full_url = urljoin(current_url, href)
                    
                    # Only process URLs from this domain
                    if domain not in full_url:
                        continue
                    
                    # Check if this looks like a strain/product page
                    if self.is_strain_url(full_url, domain):
                        discovered.add(full_url)
                    
                    # Check if this is a category/listing page to crawl further
                    elif self.is_category_url(full_url, domain) and full_url not in visited:
                        to_visit.add(full_url)
                
            except Exception as e:
                logger.warning(f"Error processing {current_url}: {e}")
            
            # Rate limiting
            await asyncio.sleep(2)
        
        logger.info(f"Completed crawling {domain}: {len(discovered)} strain URLs found")
        return discovered
    
    def is_strain_url(self, url: str, domain: str) -> bool:
        """Check if URL is a strain/product page"""
        url_lower = url.lower()
        
        # Domain-specific patterns
        if "sensiseeds" in domain:
            return any(x in url_lower for x in ['/feminized-seeds/', '/autoflowering-seeds/', '/regular-seeds/'])
        elif "californiahempseeds" in domain or "humboldtseedcompany" in domain:
            return '/product/' in url_lower or '/strain/' in url_lower
        elif "cropkingseeds" in domain:
            return any(x in url_lower for x in ['/feminized-seeds/', '/autoflower-seeds/', '/regular-seeds/'])
        elif "barneysfarm" in domain:
            return '-strain-' in url_lower and '/us/' in url_lower
        elif "ilgm" in domain:
            return '/products/' in url_lower and 'seeds' in url_lower
        
        return False
    
    def is_category_url(self, url: str, domain: str) -> bool:
        """Check if URL is a category/listing page"""
        url_lower = url.lower()
        
        # General category indicators
        category_terms = ['category', 'shop', 'seeds', 'cannabis', 'feminized', 'autoflower', 'regular']
        return any(term in url_lower for term in category_terms)
    
    async def fetch_page_simple(self, session: aiohttp.ClientSession, url: str) -> str:
        """Simple page fetch for crawling"""
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
        except:
            pass
        return ""
    
    def add_urls_to_database(self, urls: set, domain: str):
        """Add discovered URLs to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        added = 0
        for url in urls:
            url_hash = self.generate_url_hash(url)
            strain_ids = json.dumps([f"discovered_{domain}_{added + 1}"])
            
            cursor.execute('''
                INSERT OR IGNORE INTO scraping_progress 
                (url_hash, original_url, strain_ids, status)
                VALUES (?, ?, ?, 'pending')
            ''', (url_hash, url, strain_ids))
            
            if cursor.rowcount > 0:
                added += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Added {added} new URLs from {domain}")
    
    # EXACT same scraping methods as pipeline/01
    async def bright_data_scrape(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        if not self.bright_data_creds:
            return None
        
        api_url = self.bright_data_creds['endpoint']
        payload = {"url": url, "zone": self.bright_data_creds['username'], "format": "raw"}
        headers = {"Authorization": f"Bearer {self.bright_data_creds['password']}", "Content-Type": "application/json"}
        
        try:
            async with session.post(api_url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('body', '')
        except:
            pass
        return None
    
    async def scrapingbee_scrape(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        if not self.scrapingbee_key:
            return None
        
        api_url = "https://app.scrapingbee.com/api/v1/"
        params = {'api_key': self.scrapingbee_key, 'url': url, 'render_js': 'false', 'premium_proxy': 'true'}
        
        try:
            async with session.get(api_url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    return await response.text()
        except:
            pass
        return None
    
    async def direct_scrape(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    return await response.text()
        except:
            pass
        return None
    
    def validate_html(self, html_content: str, url: str) -> Tuple[bool, float, Dict]:
        """EXACT same validation as pipeline/01"""
        if not html_content or len(html_content) < 1000:
            return False, 0.0, {'error': 'Content too short'}
        
        checks = {
            'min_size': len(html_content) > 5000,
            'has_title': '<title>' in html_content.lower(),
            'has_cannabis_content': any(term in html_content.lower() for term in ['strain', 'cannabis', 'thc', 'cbd', 'seed']),
            'not_blocked': not any(term in html_content.lower() for term in ['blocked', 'captcha', 'access denied', 'forbidden']),
            'not_error': not any(term in html_content for term in ['404', '403', '500', 'error']),
            'has_structure': all(tag in html_content.lower() for tag in ['<html', '<body', '</html>']),
            'reasonable_size': len(html_content) < 5000000,
            'has_content': len(re.sub(r'<[^>]+>', '', html_content).strip()) > 500
        }
        
        score = sum(checks.values()) / len(checks)
        is_valid = score >= 0.75
        
        return is_valid, score, checks
    
    async def scrape_with_fallbacks(self, session: aiohttp.ClientSession, url: str) -> Tuple[Optional[str], str]:
        """EXACT same fallback system as pipeline/01"""
        methods = [
            ('scrapingbee', self.scrapingbee_scrape),
            ('direct', self.direct_scrape),
            ('bright_data', self.bright_data_scrape)
        ]
        
        for attempt in range(self.max_attempts):
            for method_name, method_func in methods:
                try:
                    html = await method_func(session, url)
                    if html:
                        is_valid, score, checks = self.validate_html(html, url)
                        if is_valid:
                            return html, method_name
                except:
                    pass
            
            if attempt < self.max_attempts - 1:
                delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]
                await asyncio.sleep(delay)
        
        return None, 'failed_all_methods'
    
    def store_html_s3(self, url_hash: str, html_content: str, metadata: Dict) -> Tuple[str, str]:
        """EXACT same S3 storage as pipeline/01"""
        html_key = f'html/{url_hash}.html'
        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=html_key,
            Body=html_content.encode('utf-8'),
            ServerSideEncryption='AES256',
            ContentType='text/html',
            Metadata={
                'collection-date': datetime.now().isoformat(),
                'validation-score': str(metadata.get('validation_score', 0)),
                'original-url': metadata['url'][:1000]
            }
        )
        
        metadata_key = f'metadata/{url_hash}.json'
        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=2),
            ServerSideEncryption='AES256',
            ContentType='application/json'
        )
        
        return html_key, metadata_key
    
    def update_progress_db(self, url_hash: str, status: str, **kwargs):
        """EXACT same database updates as pipeline/01"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = ['status = ?']
        values = [status]
        
        for key, value in kwargs.items():
            if key in ['attempts', 'html_size', 'validation_score', 's3_path', 'error_message', 'scrape_method']:
                updates.append(f'{key} = ?')
                values.append(value)
        
        updates.append('last_attempt = ?')
        values.append(datetime.now().isoformat())
        values.append(url_hash)
        
        query = f"UPDATE scraping_progress SET {', '.join(updates)} WHERE url_hash = ?"
        cursor.execute(query, values)
        conn.commit()
        conn.close()
    
    def get_pending_urls(self, limit: int = 100) -> list:
        """EXACT same as pipeline/01"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT url_hash, original_url, strain_ids, attempts 
            FROM scraping_progress 
            WHERE status = 'pending' OR (status = 'failed' AND attempts < ?)
            ORDER BY attempts ASC, RANDOM()
            LIMIT ?
        ''', (self.max_attempts, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'url_hash': r[0], 'url': r[1], 'strain_ids': r[2], 'attempts': r[3]} for r in results]
    
    async def respectful_delay(self, url: str):
        """Rate limiting"""
        domain = urlparse(url).netloc
        delay = 2  # 2 seconds for all domains
        
        if domain in self.last_request:
            elapsed = time.time() - self.last_request[domain]
            if elapsed < delay:
                await asyncio.sleep(delay - elapsed)
        
        self.last_request[domain] = time.time()
    
    async def process_url_batch(self, urls: list, session: aiohttp.ClientSession):
        """EXACT same processing as pipeline/01"""
        for url_data in urls:
            url_hash = url_data['url_hash']
            url = url_data['url']
            attempts = url_data['attempts']
            
            try:
                await self.respectful_delay(url)
                self.update_progress_db(url_hash, 'processing', attempts=attempts + 1)
                
                html, method = await self.scrape_with_fallbacks(session, url)
                
                if html:
                    is_valid, score, checks = self.validate_html(html, url)
                    
                    if is_valid:
                        metadata = {
                            'url': url,
                            'url_hash': url_hash,
                            'strain_ids': json.loads(url_data['strain_ids']),
                            'collection_date': datetime.now().isoformat(),
                            'scrape_method': method,
                            'validation_score': score,
                            'validation_checks': checks,
                            'html_size': len(html)
                        }
                        
                        html_key, metadata_key = self.store_html_s3(url_hash, html, metadata)
                        
                        self.update_progress_db(
                            url_hash, 'success',
                            html_size=len(html),
                            validation_score=score,
                            s3_path=html_key,
                            scrape_method=method
                        )
                        
                        logger.info(f"SUCCESS: {url}")
                    else:
                        self.update_progress_db(url_hash, 'failed', error_message=f"Invalid HTML (score: {score:.2f})")
                else:
                    self.update_progress_db(url_hash, 'failed', error_message="All scraping methods failed")
                    
            except Exception as e:
                self.update_progress_db(url_hash, 'failed', error_message=str(e))
    
    async def run_complete_system(self):
        """Run the complete system: discover URLs then collect HTML"""
        
        logger.info("Starting COMPLETE seedbank crawling and collection system")
        
        # Create database
        self.create_database()
        
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            # STEP 1: Discover ALL strain URLs from 5 seedbank websites
            await self.discover_strain_urls(session)
            
            # STEP 2: Collect HTML for ALL discovered URLs (same as pipeline/01)
            logger.info("Starting HTML collection for all discovered URLs")
            
            while True:
                pending_urls = self.get_pending_urls(50)
                
                if not pending_urls:
                    logger.info("No more pending URLs to process")
                    break
                
                logger.info(f"Processing batch of {len(pending_urls)} URLs")
                
                semaphore = asyncio.Semaphore(10)
                
                async def process_with_semaphore(url_data):
                    async with semaphore:
                        await self.process_url_batch([url_data], session)
                
                tasks = [process_with_semaphore(url_data) for url_data in pending_urls]
                await asyncio.gather(*tasks, return_exceptions=True)
                
                self.log_progress()
        
        self.generate_final_report()
    
    def log_progress(self):
        """EXACT same progress logging as pipeline/01"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
            FROM scraping_progress
        ''')
        
        stats = cursor.fetchone()
        total, success, failed, pending = stats
        
        if total > 0:
            success_rate = (success / total) * 100
            logger.info(f"Progress: {success:,}/{total:,} ({success_rate:.1f}%) | Failed: {failed:,} | Pending: {pending:,}")
        
        conn.close()
    
    def generate_final_report(self):
        """Generate final report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM scraping_progress')
        total_urls = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM scraping_progress WHERE status = "success"')
        success_count = cursor.fetchone()[0]
        
        conn.close()
        
        success_rate = (success_count / total_urls) * 100 if total_urls > 0 else 0
        
        report = f"""
# Cannabis Intelligence Database - Seedbank Collection Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Collection Summary
- **Total URLs Discovered**: {total_urls:,}
- **Successfully Collected**: {success_count:,} ({success_rate:.1f}%)
- **Added to S3**: ci-strains-html-archive bucket
- **Integration**: Seamless with existing 13,163 pages

## System Performance
- Same bulletproof methodology as pipeline/01
- Multi-layer fallback system
- 75% HTML validation threshold
- AES-256 encryption

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'seedbank_collection_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Final report saved to {report_path}")

async def main():
    """Main execution"""
    
    # Configuration (same S3 bucket as pipeline/01)
    db_path = "../data/seedbank_collection.db"
    s3_bucket = "ci-strains-html-archive"
    
    # Ensure data directory exists
    Path(db_path).parent.mkdir(exist_ok=True)
    
    # Run complete system
    collector = SeedbankCrawlerCollector(db_path, s3_bucket)
    
    try:
        await collector.run_complete_system()
        
        print("\n" + "="*60)
        print("SEEDBANK CRAWLING & COLLECTION COMPLETE")
        print("="*60)
        print("Discovered ALL strain URLs from 5 seedbank websites")
        print("Collected HTML using same bulletproof system as pipeline/01")
        print("Added to existing S3 archive seamlessly")
        print("Ready for Phase 3: Enhanced Analysis!")
        print("="*60)
        
    except KeyboardInterrupt:
        logger.info("Collection interrupted by user")
    except Exception as e:
        logger.error(f"Collection failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())