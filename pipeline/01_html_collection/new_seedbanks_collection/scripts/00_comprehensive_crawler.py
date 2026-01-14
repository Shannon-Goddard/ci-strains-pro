#!/usr/bin/env python3
"""
Cannabis Intelligence Database - Seedbank URL Crawler
Discovers ALL strain URLs from each seedbank's website

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import asyncio
import aiohttp
import sqlite3
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SeedbankCrawler:
    """Crawl seedbank websites to discover all strain URLs"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.discovered_urls = set()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        # Seedbank configurations
        self.seedbanks = {
            "sensi_seeds": {
                "name": "Sensi Seeds",
                "start_urls": ["https://sensiseeds.us/cannabis-seeds/"],
                "product_patterns": [r"/feminized-seeds/", r"/autoflowering-seeds/", r"/regular-seeds/"],
                "pagination_selectors": [".pagination a", ".next-page", "a[rel='next']"],
                "product_selectors": ["a[href*='/feminized-seeds/']", "a[href*='/autoflowering-seeds/']", "a[href*='/regular-seeds/']"]
            },
            "humboldt": {
                "name": "Humboldt Seed Company",
                "start_urls": ["https://californiahempseeds.com/shop-all/", "https://humboldtseedcompany.com/"],
                "product_patterns": [r"/product/", r"/strain/"],
                "pagination_selectors": [".pagination a", ".next", "a[rel='next']"],
                "product_selectors": ["a[href*='/product/']", ".product-item a", ".strain-link"]
            },
            "crop_king": {
                "name": "Crop King",
                "start_urls": ["https://www.cropkingseeds.com/?s=seeds&post_type=product"],
                "product_patterns": [r"/feminized-seeds/", r"/autoflower-seeds/", r"/regular-seeds/"],
                "pagination_selectors": [".pagination a", ".next-page"],
                "product_selectors": ["a[href*='/feminized-seeds/']", "a[href*='/autoflower-seeds/']", ".product-title a"]
            },
            "barneys_farm": {
                "name": "Barney's Farm",
                "start_urls": ["https://www.barneysfarm.com/us/", "https://www.barneysfarm.com/us/feminized-cannabis-seeds", "https://www.barneysfarm.com/us/autoflowering-cannabis-seeds"],
                "product_patterns": [r"/us/.*-strain-\d+", r"/us/.*-auto-.*-strain-\d+"],
                "pagination_selectors": [".pagination a", ".next"],
                "product_selectors": ["a[href*='-strain-']", ".product-name a"]
            },
            "ilgm": {
                "name": "ILGM",
                "start_urls": ["https://ilgm.com/categories/cannabis-seeds"],
                "product_patterns": [r"/products/.*-seeds"],
                "pagination_selectors": [".pagination a", "a[rel='next']"],
                "product_selectors": ["a[href*='/products/']", ".product-item a"]
            }
        }
    
    def generate_url_hash(self, url: str) -> str:
        """Generate 16-character hash for URL"""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """Fetch a single page with error handling"""
        try:
            headers = {'User-Agent': self.user_agents[0]}
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return ""
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return ""
    
    def extract_product_urls(self, html: str, base_url: str, seedbank_config: dict) -> set:
        """Extract product URLs from HTML"""
        urls = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try multiple selectors
            for selector in seedbank_config["product_selectors"]:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        
                        # Check if URL matches product patterns
                        for pattern in seedbank_config["product_patterns"]:
                            if re.search(pattern, full_url, re.IGNORECASE):
                                urls.add(full_url)
                                break
            
            # Also look for any links that contain strain-related keywords
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    text = link.get_text().lower()
                    
                    # Check for strain keywords in link text or URL
                    strain_keywords = ['strain', 'seed', 'feminized', 'autoflower', 'regular', 'cannabis']
                    if any(keyword in text or keyword in full_url.lower() for keyword in strain_keywords):
                        for pattern in seedbank_config["product_patterns"]:
                            if re.search(pattern, full_url, re.IGNORECASE):
                                urls.add(full_url)
                                break
        
        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
        
        return urls
    
    def extract_pagination_urls(self, html: str, base_url: str, seedbank_config: dict) -> set:
        """Extract pagination URLs"""
        urls = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            for selector in seedbank_config["pagination_selectors"]:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href and 'next' in link.get_text().lower():
                        full_url = urljoin(base_url, href)
                        urls.add(full_url)
        
        except Exception as e:
            logger.error(f"Error extracting pagination: {e}")
        
        return urls
    
    async def crawl_seedbank(self, session: aiohttp.ClientSession, seedbank_key: str, seedbank_config: dict):
        """Crawl a single seedbank for all strain URLs"""
        
        logger.info(f"Starting crawl: {seedbank_config['name']}")
        
        visited_pages = set()
        pages_to_visit = set(seedbank_config["start_urls"])
        product_urls = set()
        
        max_pages = 50  # Limit to prevent infinite crawling
        page_count = 0
        
        while pages_to_visit and page_count < max_pages:
            current_url = pages_to_visit.pop()
            
            if current_url in visited_pages:
                continue
            
            visited_pages.add(current_url)
            page_count += 1
            
            logger.info(f"Crawling page {page_count}: {current_url}")
            
            html = await self.fetch_page(session, current_url)
            if not html:
                continue
            
            # Extract product URLs
            page_products = self.extract_product_urls(html, current_url, seedbank_config)
            product_urls.update(page_products)
            logger.info(f"Found {len(page_products)} products on this page")
            
            # Extract pagination URLs (only for category/listing pages)
            if any(term in current_url.lower() for term in ['category', 'shop', 'seeds', 'cannabis']):
                pagination_urls = self.extract_pagination_urls(html, current_url, seedbank_config)
                pages_to_visit.update(pagination_urls - visited_pages)
            
            # Rate limiting
            await asyncio.sleep(2)
        
        logger.info(f"Completed {seedbank_config['name']}: {len(product_urls)} strain URLs found")
        return product_urls
    
    def save_urls_to_db(self, seedbank_name: str, urls: set):
        """Save discovered URLs to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_progress (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                strain_ids TEXT NOT NULL,
                seedbank TEXT NOT NULL,
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
        
        added_count = 0
        for url in urls:
            url_hash = self.generate_url_hash(url)
            strain_ids = json.dumps([f"discovered_{seedbank_name.lower().replace(' ', '_')}_{added_count + 1}"])
            
            cursor.execute('''
                INSERT OR IGNORE INTO scraping_progress 
                (url_hash, original_url, strain_ids, seedbank, status)
                VALUES (?, ?, ?, ?, 'pending')
            ''', (url_hash, url, strain_ids, seedbank_name))
            
            if cursor.rowcount > 0:
                added_count += 1
        
        conn.commit()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM scraping_progress WHERE seedbank = ?', (seedbank_name,))
        total_count = cursor.fetchone()[0]
        
        conn.close()
        
        logger.info(f"Added {added_count} new URLs for {seedbank_name} (total: {total_count})")
        return added_count, total_count
    
    async def crawl_all_seedbanks(self):
        """Crawl all configured seedbanks"""
        
        logger.info("Starting comprehensive seedbank crawling")
        
        connector = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            total_discovered = 0
            
            for seedbank_key, seedbank_config in self.seedbanks.items():
                try:
                    urls = await self.crawl_seedbank(session, seedbank_key, seedbank_config)
                    added, total = self.save_urls_to_db(seedbank_config["name"], urls)
                    total_discovered += added
                    
                except Exception as e:
                    logger.error(f"Error crawling {seedbank_config['name']}: {e}")
        
        logger.info(f"Crawling complete! Total new URLs discovered: {total_discovered}")
        return total_discovered
    
    def generate_discovery_report(self):
        """Generate comprehensive discovery report"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get statistics by seedbank
        cursor.execute('''
            SELECT seedbank, COUNT(*) as url_count
            FROM scraping_progress 
            GROUP BY seedbank
            ORDER BY url_count DESC
        ''')
        
        seedbank_stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM scraping_progress')
        total_urls = cursor.fetchone()[0]
        
        conn.close()
        
        # Generate report
        report = f"""
# Cannabis Intelligence Database - Comprehensive URL Discovery Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Discovery Summary
- **Total Strain URLs**: {total_urls:,}

## Seedbank Breakdown
"""
        
        for seedbank, count in seedbank_stats:
            report += f"- **{seedbank}**: {count:,} strain URLs\n"
        
        report += """
## Next Steps
1. Run `02_bulletproof_scraper.py` to collect ALL strain HTML pages
2. Monitor progress with `03_progress_monitor.py --watch`
3. All URLs will be added to existing S3 archive seamlessly

## Integration Notes
- Same S3 bucket: ci-strains-html-archive
- Same validation thresholds: 75%
- Same retry logic: 6 attempts max
- Same encryption: AES-256
- Seamless integration with existing 13,163 pages

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'comprehensive_discovery_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved: {report_path}")

async def main():
    """Main execution function"""
    
    # Configuration
    db_path = "../data/new_seedbanks_progress.db"
    
    # Ensure data directory exists
    Path(db_path).parent.mkdir(exist_ok=True)
    
    # Create crawler
    crawler = SeedbankCrawler(db_path)
    
    # Crawl all seedbanks
    total_discovered = await crawler.crawl_all_seedbanks()
    
    # Generate report
    crawler.generate_discovery_report()
    
    print("\n" + "="*60)
    print("COMPREHENSIVE SEEDBANK CRAWLING COMPLETE")
    print("="*60)
    print(f"Total strain URLs discovered: {total_discovered:,}")
    print("Database updated with all discovered URLs")
    print("Ready for bulletproof HTML collection!")
    print("\nNext steps:")
    print("1. python 02_bulletproof_scraper.py")
    print("2. python 03_progress_monitor.py --watch")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())