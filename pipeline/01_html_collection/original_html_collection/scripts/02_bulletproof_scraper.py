#!/usr/bin/env python3
"""
Cannabis Intelligence Database - Bulletproof HTML Scraper
Multi-layer fallback system with 99.5% success rate target

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
from urllib.parse import urlparse
import logging
from typing import Dict, Tuple, Optional
import random
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/bulletproof_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecretsManager:
    """AWS Secrets Manager integration"""
    
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)
    
    def get_secret(self, secret_name):
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except Exception as e:
            logger.error(f"Failed to get secret {secret_name}: {e}")
            raise
    
    def get_bright_data_creds(self):
        return self.get_secret('cannabis_bright_data_api')
    
    def get_scrapingbee_key(self):
        return self.get_secret('cannabis_scrapingbee_api')['api_key']

class HTMLValidator:
    """Comprehensive HTML quality validation"""
    
    @staticmethod
    def validate_html(html_content: str, url: str) -> Tuple[bool, float, Dict]:
        """
        Validate HTML quality with comprehensive checks
        Returns: (is_valid, score, detailed_checks)
        """
        
        if not html_content or len(html_content) < 1000:
            return False, 0.0, {'error': 'Content too short'}
        
        checks = {
            'min_size': len(html_content) > 5000,
            'has_title': '<title>' in html_content.lower(),
            'has_cannabis_content': any(term in html_content.lower() 
                                      for term in ['strain', 'cannabis', 'thc', 'cbd', 'seed']),
            'not_blocked': not any(term in html_content.lower() 
                                 for term in ['blocked', 'captcha', 'access denied', 'forbidden']),
            'not_error': not any(term in html_content 
                               for term in ['404', '403', '500', 'error']),
            'has_structure': all(tag in html_content.lower() 
                               for tag in ['<html', '<body', '</html>']),
            'reasonable_size': len(html_content) < 5000000,  # < 5MB
            'has_content': len(re.sub(r'<[^>]+>', '', html_content).strip()) > 500
        }
        
        score = sum(checks.values()) / len(checks)
        is_valid = score >= 0.75  # 75% threshold
        
        return is_valid, score, checks

class PolitenessMixin:
    """Rate limiting and politeness controls"""
    
    def __init__(self):
        self.last_request = {}
        self.request_counts = {}
        self.domain_delays = {
            'seedsman.com': 3,
            'leafly.com': 2,
            'allbud.com': 4,
            'attitude.co.uk': 2,
            'northatlanticseed.com': 2,
            'default': 2
        }
    
    async def respectful_delay(self, url: str):
        """Implement respectful delays between requests"""
        domain = urlparse(url).netloc
        delay = self.domain_delays.get(domain, self.domain_delays['default'])
        
        if domain in self.last_request:
            elapsed = time.time() - self.last_request[domain]
            if elapsed < delay:
                sleep_time = delay - elapsed
                logger.debug(f"Sleeping {sleep_time:.1f}s for {domain}")
                await asyncio.sleep(sleep_time)
        
        self.last_request[domain] = time.time()

class BulletproofScraper(PolitenessMixin):
    """Multi-layer bulletproof scraping system"""
    
    def __init__(self, db_path: str, s3_bucket: str):
        super().__init__()
        self.db_path = db_path
        self.s3_bucket = s3_bucket
        self.s3_client = boto3.client('s3')
        self.secrets = SecretsManager()
        self.validator = HTMLValidator()
        
        # Retry configuration
        self.retry_delays = [1, 3, 7, 15, 30, 60]  # Exponential backoff
        self.max_attempts = 6
        self.success_threshold = 0.995  # 99.5% target
        
        # Load credentials
        self.bright_data_creds = None
        self.scrapingbee_key = None
        self._load_credentials()
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
    
    def _load_credentials(self):
        """Load API credentials from AWS Secrets Manager"""
        try:
            from aws_secrets import get_aws_credentials
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
    
    async def bright_data_scrape(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Primary scraping method using Bright Data API"""
        
        if not self.bright_data_creds:
            return None
        
        api_url = self.bright_data_creds['endpoint']
        
        payload = {
            "url": url,
            "zone": self.bright_data_creds['username'],  # zone name
            "format": "raw"  # Changed from "html" to "raw"
        }
        
        headers = {
            "Authorization": f"Bearer {self.bright_data_creds['password']}",  # API key
            "Content-Type": "application/json"
        }
        
        try:
            async with session.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    # For "raw" format, the HTML is in the "body" field
                    html = result.get('body', '')
                    if html:
                        logger.debug(f"Bright Data API success for {url}")
                        return html
                    else:
                        logger.warning(f"Bright Data API returned empty HTML for {url}")
                        return None
                else:
                    logger.warning(f"Bright Data API HTTP {response.status} for {url}")
                    return None
                    
        except Exception as e:
            logger.warning(f"Bright Data API failed for {url}: {e}")
            return None
    
    async def scrapingbee_scrape(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fallback method using ScrapingBee API"""
        
        if not self.scrapingbee_key:
            return None
        
        api_url = "https://app.scrapingbee.com/api/v1/"
        params = {
            'api_key': self.scrapingbee_key,
            'url': url,
            'render_js': 'false',
            'premium_proxy': 'true'
        }
        
        try:
            async with session.get(api_url, params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    html = await response.text()
                    logger.debug(f"ScrapingBee success for {url}")
                    return html
                else:
                    logger.warning(f"ScrapingBee HTTP {response.status} for {url}")
                    return None
                    
        except Exception as e:
            logger.warning(f"ScrapingBee failed for {url}: {e}")
            return None
    
    async def direct_scrape(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Direct scraping with rotating user agents"""
        
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            async with session.get(
                url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    html = await response.text()
                    logger.debug(f"Direct scrape success for {url}")
                    return html
                else:
                    logger.warning(f"Direct scrape HTTP {response.status} for {url}")
                    return None
                    
        except Exception as e:
            logger.warning(f"Direct scrape failed for {url}: {e}")
            return None
    
    async def scrape_with_fallbacks(self, session: aiohttp.ClientSession, url: str) -> Tuple[Optional[str], str]:
        """
        Attempt scraping with all fallback methods
        Returns: (html_content, method_used)
        """
        
        # Define scraping methods in priority order (ScrapingBee first while Bright Data is being debugged)
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
                        is_valid, score, checks = self.validator.validate_html(html, url)
                        if is_valid:
                            logger.info(f"Success: {url} via {method_name} (score: {score:.2f})")
                            return html, method_name
                        else:
                            logger.warning(f"Invalid HTML from {method_name} for {url} (score: {score:.2f})")
                    
                except Exception as e:
                    logger.error(f"Method {method_name} error for {url}: {e}")
            
            # Exponential backoff before retry
            if attempt < self.max_attempts - 1:
                delay = self.retry_delays[min(attempt, len(self.retry_delays) - 1)]
                logger.info(f"Retrying {url} in {delay}s (attempt {attempt + 1})")
                await asyncio.sleep(delay)
        
        logger.error(f"All methods failed for {url}")
        return None, 'failed_all_methods'
    
    def store_html_s3(self, url_hash: str, html_content: str, metadata: Dict) -> Tuple[str, str]:
        """Store HTML and metadata in S3 with encryption"""
        
        # Store HTML file
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
                'original-url': metadata['url'][:1000]  # S3 metadata limit
            }
        )
        
        # Store metadata JSON
        metadata_key = f'metadata/{url_hash}.json'
        self.s3_client.put_object(
            Bucket=self.s3_bucket,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=2),
            ServerSideEncryption='AES256',
            ContentType='application/json'
        )
        
        logger.debug(f"Stored to S3: {html_key}")
        return html_key, metadata_key
    
    def update_progress_db(self, url_hash: str, status: str, **kwargs):
        """Update progress in SQLite database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build update query dynamically
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
        """Get pending URLs from database"""
        
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
    
    async def process_url_batch(self, urls: list, session: aiohttp.ClientSession):
        """Process a batch of URLs with rate limiting"""
        
        for url_data in urls:
            url_hash = url_data['url_hash']
            url = url_data['url']
            attempts = url_data['attempts']
            
            try:
                # Respectful delay
                await self.respectful_delay(url)
                
                # Update attempt count
                self.update_progress_db(url_hash, 'processing', attempts=attempts + 1)
                
                # Attempt scraping
                html, method = await self.scrape_with_fallbacks(session, url)
                
                if html:
                    # Validate HTML
                    is_valid, score, checks = self.validator.validate_html(html, url)
                    
                    if is_valid:
                        # Store in S3
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
                        
                        # Update database
                        self.update_progress_db(
                            url_hash, 'success',
                            html_size=len(html),
                            validation_score=score,
                            s3_path=html_key,
                            scrape_method=method
                        )
                        
                        logger.info(f"SUCCESS: Collected: {url}")
                    else:
                        # Invalid HTML
                        self.update_progress_db(
                            url_hash, 'failed',
                            error_message=f"Invalid HTML (score: {score:.2f})"
                        )
                        logger.warning(f"❌ Invalid HTML: {url}")
                else:
                    # All methods failed
                    self.update_progress_db(
                        url_hash, 'failed',
                        error_message="All scraping methods failed"
                    )
                    logger.error(f"FAILED: {url}")
                    
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                self.update_progress_db(
                    url_hash, 'failed',
                    error_message=str(e)
                )
    
    async def run_collection(self, batch_size: int = 50, max_concurrent: int = 10):
        """Run the complete HTML collection process"""
        
        logger.info("Starting bulletproof HTML collection")
        start_time = datetime.now()
        
        # Create aiohttp session with connection pooling
        connector = aiohttp.TCPConnector(
            limit=max_concurrent,
            limit_per_host=5,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        async with aiohttp.ClientSession(connector=connector) as session:
            
            while True:
                # Get pending URLs
                pending_urls = self.get_pending_urls(batch_size)
                
                if not pending_urls:
                    logger.info("No more pending URLs to process")
                    break
                
                logger.info(f"Processing batch of {len(pending_urls)} URLs")
                
                # Process batch with concurrency control
                semaphore = asyncio.Semaphore(max_concurrent)
                
                async def process_with_semaphore(url_data):
                    async with semaphore:
                        await self.process_url_batch([url_data], session)
                
                # Process URLs concurrently
                tasks = [process_with_semaphore(url_data) for url_data in pending_urls]
                await asyncio.gather(*tasks, return_exceptions=True)
                
                # Progress update
                self.log_progress()
        
        duration = datetime.now() - start_time
        logger.info(f"Collection completed in {duration}")
        self.generate_final_report()
    
    def log_progress(self):
        """Log current progress statistics"""
        
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
        """Generate final collection report"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get detailed statistics
        cursor.execute('''
            SELECT 
                status,
                COUNT(*) as count,
                AVG(html_size) as avg_size,
                AVG(validation_score) as avg_score
            FROM scraping_progress 
            GROUP BY status
        ''')
        
        status_stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM scraping_progress')
        total_urls = cursor.fetchone()[0]
        
        conn.close()
        
        # Generate report
        report = f"""
# Cannabis Intelligence Database - HTML Collection Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Collection Summary
- **Total URLs**: {total_urls:,}

"""
        
        for status, count, avg_size, avg_score in status_stats:
            percentage = (count / total_urls) * 100
            report += f"- **{status.title()}**: {count:,} ({percentage:.1f}%)\n"
            if avg_size:
                report += f"  - Average HTML size: {int(avg_size):,} bytes\n"
            if avg_score:
                report += f"  - Average validation score: {avg_score:.3f}\n"
        
        report += """
## Quality Metrics
✅ Multi-layer fallback system deployed
✅ HTML validation with 75% threshold
✅ S3 storage with encryption
✅ Progress tracking and recovery

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'collection_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Final report saved to {report_path}")

def main():
    """Main execution function"""
    
    # Configuration
    db_path = "../data/scraping_progress.db"
    s3_bucket = "ci-strains-html-archive"  # Update with actual bucket name
    
    # Verify database exists
    if not Path(db_path).exists():
        logger.error(f"Database not found: {db_path}")
        logger.error("Please run 01_url_deduplication.py first")
        return
    
    # Run collection
    scraper = BulletproofScraper(db_path, s3_bucket)
    
    try:
        asyncio.run(scraper.run_collection(batch_size=50, max_concurrent=10))
        
        print("\n" + "="*60)
        print("🌿 CANNABIS INTELLIGENCE - HTML COLLECTION COMPLETE")
        print("="*60)
        print("✅ Bulletproof scraping completed")
        print("📊 Check collection_report.md for details")
        print("🗄️  HTML stored in S3 with encryption")
        print("\n🎯 Ready for Phase 3: Enhanced Analysis!")
        print("="*60)
        
    except KeyboardInterrupt:
        logger.info("Collection interrupted by user")
    except Exception as e:
        logger.error(f"Collection failed: {e}")
        raise

if __name__ == "__main__":
    main()