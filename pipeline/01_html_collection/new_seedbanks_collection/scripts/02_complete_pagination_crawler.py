#!/usr/bin/env python3
"""
Cannabis Intelligence Database - Complete Pagination Crawler
Gets ALL strain URLs from ALL pages of each seedbank

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import asyncio
import aiohttp
import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompletePaginationCrawler:
    """Crawl ALL pages of each seedbank to get ALL strain URLs"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36']
        
        # Seedbank pagination configurations
        self.seedbanks = {
            "crop_king": {
                "name": "Crop King",
                "base_url": "https://www.cropkingseeds.com/",
                "start_urls": ["https://www.cropkingseeds.com/?s=seeds&post_type=product&dgwt_wcas=1"],
                "pagination_pattern": "page/{page}/",
                "max_pages": 250,  # 3218 results / ~16 per page
                "product_selectors": ["a[href*='/feminized-seeds/']", "a[href*='/autoflower-seeds/']", "a[href*='/regular-seeds/']"]
            },
            "sensi_seeds": {
                "name": "Sensi Seeds", 
                "base_url": "https://sensiseeds.us/",
                "start_urls": [
                    "https://sensiseeds.us/feminized-seeds/",
                    "https://sensiseeds.us/autoflowering-seeds/", 
                    "https://sensiseeds.us/regular-seeds/"
                ],
                "pagination_pattern": "page/{page}/",
                "max_pages": 50,
                "product_selectors": ["a[href*='/feminized-seeds/']", "a[href*='/autoflowering-seeds/']", "a[href*='/regular-seeds/']"]
            },
            "barneys_farm": {
                "name": "Barney's Farm",
                "base_url": "https://www.barneysfarm.com/",
                "start_urls": [
                    "https://www.barneysfarm.com/us/feminized-cannabis-seeds",
                    "https://www.barneysfarm.com/us/autoflowering-cannabis-seeds"
                ],
                "pagination_pattern": "?page={page}",
                "max_pages": 10,
                "product_selectors": ["a[href*='-strain-']", "a[href*='-weed-strain-']"]
            },
            "ilgm": {
                "name": "ILGM",
                "base_url": "https://ilgm.com/",
                "start_urls": ["https://ilgm.com/categories/cannabis-seeds"],
                "pagination_pattern": "?page={page}",
                "max_pages": 20,  # 258 products / ~15 per page
                "product_selectors": ["a[href*='/products/']"]
            },
            "humboldt": {
                "name": "Humboldt Seed Company",
                "base_url": "https://californiahempseeds.com/",
                "start_urls": ["https://californiahempseeds.com/shop-all/"],
                "pagination_pattern": "page/{page}/",
                "max_pages": 10,  # 97 products / ~12 per page
                "product_selectors": ["a[href*='/product/']", ".product-item a"]
            }
        }
    
    def create_database(self):
        """Create database for all discovered URLs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS all_strain_urls (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                seedbank TEXT NOT NULL,
                strain_name TEXT,
                discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_url_hash(self, url: str) -> str:
        """Generate hash for URL"""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """Fetch page with error handling"""
        try:
            headers = {'User-Agent': self.user_agents[0]}
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
        return ""
    
    def extract_strain_urls(self, html: str, base_url: str, selectors: list) -> set:
        """Extract strain URLs from HTML"""
        urls = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        # Clean URL (remove query params for product pages)
                        if '/product' in full_url or '/strain' in full_url or 'seeds/' in full_url:
                            urls.add(full_url.split('?')[0])
        
        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
        
        return urls
    
    async def crawl_all_pages(self, session: aiohttp.ClientSession, seedbank_key: str, config: dict):
        """Crawl ALL pages for a seedbank"""
        
        logger.info(f"Starting complete crawl: {config['name']}")
        all_urls = set()
        
        for start_url in config["start_urls"]:
            logger.info(f"Crawling category: {start_url}")
            
            # Try different pagination patterns
            for page in range(1, config["max_pages"] + 1):
                
                # Build pagination URL
                if "page/{page}/" in config["pagination_pattern"]:
                    page_url = start_url.rstrip('/') + '/' + config["pagination_pattern"].format(page=page)
                elif "?page={page}" in config["pagination_pattern"]:
                    separator = "&" if "?" in start_url else "?"
                    page_url = start_url + separator + config["pagination_pattern"].format(page=page).lstrip('?')
                else:
                    page_url = start_url
                
                logger.info(f"Fetching page {page}: {page_url}")
                
                html = await self.fetch_page(session, page_url)
                if not html:
                    logger.warning(f"No content on page {page}, stopping pagination")
                    break
                
                # Extract strain URLs from this page
                page_urls = self.extract_strain_urls(html, config["base_url"], config["product_selectors"])
                
                if not page_urls:
                    logger.info(f"No more products found on page {page}, stopping pagination")
                    break
                
                all_urls.update(page_urls)
                logger.info(f"Found {len(page_urls)} URLs on page {page} (total: {len(all_urls)})")
                
                # Rate limiting
                await asyncio.sleep(2)
        
        logger.info(f"Completed {config['name']}: {len(all_urls)} total URLs discovered")
        return all_urls
    
    def save_urls_to_db(self, seedbank_name: str, urls: set):
        """Save URLs to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        added_count = 0
        for url in urls:
            url_hash = self.generate_url_hash(url)
            
            # Extract strain name from URL
            strain_name = url.split('/')[-1].replace('-', ' ').replace('_', ' ')
            
            cursor.execute('''
                INSERT OR IGNORE INTO all_strain_urls 
                (url_hash, original_url, seedbank, strain_name)
                VALUES (?, ?, ?, ?)
            ''', (url_hash, url, seedbank_name, strain_name))
            
            if cursor.rowcount > 0:
                added_count += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {added_count} new URLs for {seedbank_name}")
        return added_count
    
    async def crawl_all_seedbanks(self):
        """Crawl ALL seedbanks completely"""
        
        logger.info("Starting COMPLETE seedbank crawling for ALL strain URLs")
        
        connector = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            total_discovered = 0
            
            for seedbank_key, config in self.seedbanks.items():
                try:
                    urls = await self.crawl_all_pages(session, seedbank_key, config)
                    added = self.save_urls_to_db(config["name"], urls)
                    total_discovered += added
                    
                except Exception as e:
                    logger.error(f"Error crawling {config['name']}: {e}")
                
                # Delay between seedbanks
                await asyncio.sleep(5)
        
        logger.info(f"COMPLETE crawling finished! Total URLs discovered: {total_discovered}")
        return total_discovered
    
    def generate_report(self):
        """Generate comprehensive report"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get statistics by seedbank
        cursor.execute('''
            SELECT seedbank, COUNT(*) as url_count
            FROM all_strain_urls 
            GROUP BY seedbank
            ORDER BY url_count DESC
        ''')
        
        seedbank_stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM all_strain_urls')
        total_urls = cursor.fetchone()[0]
        
        conn.close()
        
        # Generate report
        report = f"""
# Cannabis Intelligence Database - COMPLETE URL Discovery Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## COMPLETE Discovery Summary
- **Total Strain URLs Discovered**: {total_urls:,}

## Seedbank Breakdown (ALL Pages Crawled)
"""
        
        for seedbank, count in seedbank_stats:
            report += f"- **{seedbank}**: {count:,} strain URLs\n"
        
        report += f"""
## Expected vs Actual
- **Crop King Expected**: 3,218 → **Actual**: {next((count for name, count in seedbank_stats if 'Crop King' in name), 0):,}
- **Sensi Seeds Expected**: 500+ → **Actual**: {next((count for name, count in seedbank_stats if 'Sensi' in name), 0):,}
- **Barney's Farm Expected**: 115 → **Actual**: {next((count for name, count in seedbank_stats if 'Barney' in name), 0):,}
- **ILGM Expected**: 258 → **Actual**: {next((count for name, count in seedbank_stats if 'ILGM' in name), 0):,}
- **Humboldt Expected**: 97 → **Actual**: {next((count for name, count in seedbank_stats if 'Humboldt' in name), 0):,}

## Next Steps
1. Run bulletproof HTML collection on ALL {total_urls:,} URLs
2. Add to existing S3 archive (13,163 + {total_urls:,} = {13163 + total_urls:,} total pages)
3. Ready for Phase 3: Enhanced Analysis

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'complete_discovery_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved: {report_path}")

async def main():
    """Main execution"""
    
    # Configuration
    db_path = "../data/complete_strain_urls.db"
    
    # Ensure data directory exists
    Path(db_path).parent.mkdir(exist_ok=True)
    
    # Create crawler
    crawler = CompletePaginationCrawler(db_path)
    
    # Create database
    crawler.create_database()
    
    # Crawl ALL seedbanks completely
    total_discovered = await crawler.crawl_all_seedbanks()
    
    # Generate report
    crawler.generate_report()
    
    print("\n" + "="*60)
    print("COMPLETE SEEDBANK CRAWLING FINISHED")
    print("="*60)
    print(f"Total strain URLs discovered: {total_discovered:,}")
    print("ALL pages crawled for each seedbank")
    print("Ready for bulletproof HTML collection!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())