#!/usr/bin/env python3
"""
Precise Seedbank Crawler - Get ALL 4,000+ strain URLs
Based on exact URLs and pagination from chat.txt

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import asyncio
import aiohttp
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PreciseSeedbankCrawler:
    """Get ALL strain URLs using exact URLs from chat.txt"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        # Exact configurations from chat.txt
        self.seedbanks = {
            "humboldt": {
                "name": "Humboldt Seed Company",
                "urls": [
                    "https://humboldtseedcompany.com/feminized-seeds/",
                    "https://humboldtseedcompany.com/regularseeds/", 
                    "https://humboldtseedcompany.com/autoflower-seeds/",
                    "https://humboldtseedcompany.com/triploid-cannabis-seeds/"
                ],
                "selectors": ["a[href*='/product/']", ".product-item a", "a[href*='humboldtseedcompany.com']"],
                "expected": 97
            },
            "ilgm": {
                "name": "ILGM",
                "urls": ["https://ilgm.com/categories/cannabis-seeds"],
                "selectors": ["a[href*='/products/']", ".product-item a"],
                "expected": 258,
                "pagination": True,
                "max_pages": 20
            },
            "crop_king": {
                "name": "Crop King", 
                "base_urls": [
                    "https://www.cropkingseeds.com/feminized-seeds/",  # 3218 results
                    "https://www.cropkingseeds.com/autoflowering-seeds/",  # 196 results  
                    "https://www.cropkingseeds.com/regular-marijuana-seeds/"  # 30 results
                ],
                "selectors": ["a[href*='/feminized-seeds/']", "a[href*='/autoflowering-seeds/']", "a[href*='/regular-marijuana-seeds/']"],
                "expected": 3444,  # 3218 + 196 + 30
                "pagination": True,
                "pages_per_category": [202, 13, 2]  # 3218/16, 196/16, 30/16
            },
            "barneys_farm": {
                "name": "Barney's Farm",
                "urls": [
                    "https://www.barneysfarm.com/us/autoflower-seeds",  # Shows both auto (24) and fem (91) when both checked
                    "https://www.barneysfarm.com/us/feminized-seeds"
                ],
                "selectors": ["a[href*='-strain-']", "a[href*='-weed-strain-']", ".product-item a"],
                "expected": 115  # 24 + 91
            }
        }
    
    def create_database(self):
        """Create database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS precise_urls (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                seedbank TEXT NOT NULL,
                category TEXT,
                discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """Fetch page"""
        try:
            headers = {'User-Agent': self.user_agent}
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
        return ""
    
    def extract_strain_urls(self, html: str, base_url: str, selectors: list) -> set:
        """Extract strain URLs"""
        urls = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        
                        # Filter for actual product pages
                        if self.is_product_url(full_url):
                            urls.add(full_url.split('?')[0])  # Remove query params
        
        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
        
        return urls
    
    def is_product_url(self, url: str) -> bool:
        """Check if URL is a product page"""
        url_lower = url.lower()
        
        # Product indicators
        product_indicators = [
            '/product/',
            '/products/',
            '/feminized-seeds/',
            '/autoflowering-seeds/', 
            '/autoflower-seeds/',
            '/regular-seeds/',
            '/regular-marijuana-seeds/',
            '-strain-',
            '-weed-strain-',
            'humboldtseedcompany.com/' + 'a'  # Any humboldt product page
        ]
        
        # Exclude category/listing pages
        exclude_indicators = [
            '/category/',
            '/categories/',
            '/shop-all/',
            '/cannabis-seeds/',
            '/page/',
            '?page=',
            '/feminized-seeds/?',
            '/autoflowering-seeds/?'
        ]
        
        has_product = any(indicator in url_lower for indicator in product_indicators)
        has_exclude = any(indicator in url_lower for indicator in exclude_indicators)
        
        return has_product and not has_exclude
    
    async def crawl_humboldt(self, session: aiohttp.ClientSession):
        """Crawl Humboldt - all on single pages"""
        config = self.seedbanks["humboldt"]
        logger.info(f"Crawling {config['name']} - Expected: {config['expected']}")
        
        all_urls = set()
        
        for url in config["urls"]:
            logger.info(f"Fetching: {url}")
            html = await self.fetch_page(session, url)
            
            if html:
                page_urls = self.extract_strain_urls(html, url, config["selectors"])
                all_urls.update(page_urls)
                logger.info(f"Found {len(page_urls)} URLs from {url}")
            
            await asyncio.sleep(2)
        
        logger.info(f"Humboldt total: {len(all_urls)} URLs")
        return all_urls
    
    async def crawl_ilgm(self, session: aiohttp.ClientSession):
        """Crawl ILGM with pagination"""
        config = self.seedbanks["ilgm"]
        logger.info(f"Crawling {config['name']} - Expected: {config['expected']}")
        
        all_urls = set()
        base_url = config["urls"][0]
        
        # Try pagination
        for page in range(1, config["max_pages"] + 1):
            page_url = f"{base_url}?page={page}"
            logger.info(f"ILGM page {page}: {page_url}")
            
            html = await self.fetch_page(session, page_url)
            if not html:
                break
            
            page_urls = self.extract_strain_urls(html, page_url, config["selectors"])
            if not page_urls:
                logger.info(f"No more products on page {page}")
                break
            
            all_urls.update(page_urls)
            logger.info(f"Found {len(page_urls)} URLs on page {page}")
            
            await asyncio.sleep(2)
        
        logger.info(f"ILGM total: {len(all_urls)} URLs")
        return all_urls
    
    async def crawl_crop_king(self, session: aiohttp.ClientSession):
        """Crawl Crop King with category pagination"""
        config = self.seedbanks["crop_king"]
        logger.info(f"Crawling {config['name']} - Expected: {config['expected']}")
        
        all_urls = set()
        
        for i, base_url in enumerate(config["base_urls"]):
            max_pages = config["pages_per_category"][i]
            category = base_url.split('/')[-2]
            
            logger.info(f"Crop King {category}: {max_pages} pages expected")
            
            for page in range(1, max_pages + 1):
                page_url = f"{base_url}page/{page}/"
                logger.info(f"{category} page {page}: {page_url}")
                
                html = await self.fetch_page(session, page_url)
                if not html:
                    continue
                
                page_urls = self.extract_strain_urls(html, page_url, config["selectors"])
                all_urls.update(page_urls)
                
                logger.info(f"Found {len(page_urls)} URLs on {category} page {page}")
                
                await asyncio.sleep(2)
        
        logger.info(f"Crop King total: {len(all_urls)} URLs")
        return all_urls
    
    async def crawl_barneys_farm(self, session: aiohttp.ClientSession):
        """Crawl Barney's Farm"""
        config = self.seedbanks["barneys_farm"]
        logger.info(f"Crawling {config['name']} - Expected: {config['expected']}")
        
        all_urls = set()
        
        for url in config["urls"]:
            logger.info(f"Fetching: {url}")
            html = await self.fetch_page(session, url)
            
            if html:
                page_urls = self.extract_strain_urls(html, url, config["selectors"])
                all_urls.update(page_urls)
                logger.info(f"Found {len(page_urls)} URLs from {url}")
            
            await asyncio.sleep(2)
        
        logger.info(f"Barney's Farm total: {len(all_urls)} URLs")
        return all_urls
    
    def save_urls(self, seedbank: str, urls: set, category: str = ""):
        """Save URLs to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        added = 0
        for url in urls:
            url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
            
            cursor.execute('''
                INSERT OR IGNORE INTO precise_urls 
                (url_hash, original_url, seedbank, category)
                VALUES (?, ?, ?, ?)
            ''', (url_hash, url, seedbank, category))
            
            if cursor.rowcount > 0:
                added += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {added} new URLs for {seedbank}")
        return added
    
    async def crawl_all_precise(self):
        """Crawl all seedbanks with precise methods"""
        
        connector = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            results = {}
            
            # Crawl each seedbank with specific method
            results["humboldt"] = await self.crawl_humboldt(session)
            await asyncio.sleep(5)
            
            results["ilgm"] = await self.crawl_ilgm(session)
            await asyncio.sleep(5)
            
            results["crop_king"] = await self.crawl_crop_king(session)
            await asyncio.sleep(5)
            
            results["barneys_farm"] = await self.crawl_barneys_farm(session)
            
            # Save all results
            total_added = 0
            for seedbank_key, urls in results.items():
                config = self.seedbanks[seedbank_key]
                added = self.save_urls(config["name"], urls)
                total_added += added
            
            return total_added, results
    
    def generate_report(self, results: dict):
        """Generate detailed report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT seedbank, COUNT(*) FROM precise_urls GROUP BY seedbank ORDER BY COUNT(*) DESC')
        stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM precise_urls')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        report = f"""
# Precise Seedbank Discovery Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## PRECISE Results Summary
- **Total URLs Discovered**: {total:,}

## Detailed Breakdown
"""
        
        for seedbank_key, config in self.seedbanks.items():
            found = len(results.get(seedbank_key, set()))
            expected = config["expected"]
            percentage = (found / expected * 100) if expected > 0 else 0
            
            report += f"- **{config['name']}**: {found:,} URLs (expected: {expected:,}, {percentage:.1f}%)\n"
        
        report += f"""
## Success Analysis
- **Total Expected**: {sum(config['expected'] for config in self.seedbanks.values()):,}
- **Total Found**: {total:,}
- **Overall Success**: {(total / sum(config['expected'] for config in self.seedbanks.values()) * 100):.1f}%

## Next Steps
1. Run bulletproof HTML collection on ALL {total:,} URLs
2. Add to existing S3 archive: 13,163 + {total:,} = {13163 + total:,} total pages

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'precise_discovery_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved: {report_path}")

async def main():
    """Main execution"""
    
    db_path = "../data/precise_strain_urls.db"
    Path(db_path).parent.mkdir(exist_ok=True)
    
    crawler = PreciseSeedbankCrawler(db_path)
    crawler.create_database()
    
    total_added, results = await crawler.crawl_all_precise()
    crawler.generate_report(results)
    
    print(f"\nPRECISE CRAWLING COMPLETE!")
    print(f"Total URLs discovered: {total_added:,}")
    print("Ready for bulletproof HTML collection!")

if __name__ == "__main__":
    asyncio.run(main())