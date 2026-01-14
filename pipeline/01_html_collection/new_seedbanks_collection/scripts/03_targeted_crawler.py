#!/usr/bin/env python3
"""
Complete Seedbank Crawler - Get ALL 4,000+ strain URLs
Based on actual pagination patterns from each site

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

class TargetedSeedbankCrawler:
    """Get ALL strain URLs using specific pagination patterns"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        # Specific configurations based on actual site structures
        self.targets = {
            "crop_king": {
                "name": "Crop King",
                "expected": 3218,
                "urls": [f"https://www.cropkingseeds.com/page/{page}/?s=seeds&post_type=product" for page in range(1, 201)],  # 3218/16 = ~200 pages
                "selectors": ["a[href*='/feminized-seeds/']", "a[href*='/autoflower-seeds/']"]
            },
            "sensi_seeds": {
                "name": "Sensi Seeds", 
                "expected": 500,
                "urls": [
                    *[f"https://sensiseeds.us/feminized-seeds/page/{page}/" for page in range(1, 26)],
                    *[f"https://sensiseeds.us/autoflowering-seeds/page/{page}/" for page in range(1, 26)],
                    *[f"https://sensiseeds.us/regular-seeds/page/{page}/" for page in range(1, 11)]
                ],
                "selectors": ["a[href*='/feminized-seeds/']", "a[href*='/autoflowering-seeds/']", "a[href*='/regular-seeds/']"]
            },
            "barneys_farm": {
                "name": "Barney's Farm",
                "expected": 115,
                "urls": [f"https://www.barneysfarm.com/us/feminized-cannabis-seeds?page={page}" for page in range(1, 8)] + 
                        [f"https://www.barneysfarm.com/us/autoflowering-cannabis-seeds?page={page}" for page in range(1, 8)],
                "selectors": ["a[href*='-strain-']", "a[href*='-weed-strain-']"]
            },
            "ilgm": {
                "name": "ILGM",
                "expected": 258,
                "urls": [f"https://ilgm.com/categories/cannabis-seeds?page={page}" for page in range(1, 18)],  # 258/15 = ~17 pages
                "selectors": ["a[href*='/products/']"]
            },
            "humboldt": {
                "name": "Humboldt Seed Company",
                "expected": 97,
                "urls": [f"https://californiahempseeds.com/shop-all/page/{page}/" for page in range(1, 9)],  # 97/12 = ~8 pages
                "selectors": ["a[href*='/product/']"]
            }
        }
    
    def create_database(self):
        """Create database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS discovered_urls (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                seedbank TEXT NOT NULL,
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
        except:
            pass
        return ""
    
    def extract_urls(self, html: str, base_url: str, selectors: list) -> set:
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
                        # Only product pages, not category pages
                        if any(term in full_url for term in ['/product/', '/strain', 'seeds/', '/products/']):
                            urls.add(full_url.split('?')[0])  # Remove query params
        except:
            pass
        
        return urls
    
    async def crawl_seedbank(self, session: aiohttp.ClientSession, key: str, config: dict):
        """Crawl all pages for one seedbank"""
        
        logger.info(f"Crawling {config['name']} - Expected: {config['expected']} strains")
        
        all_urls = set()
        
        for i, url in enumerate(config['urls'], 1):
            logger.info(f"Page {i}/{len(config['urls'])}: {url}")
            
            html = await self.fetch_page(session, url)
            if not html:
                continue
            
            page_urls = self.extract_urls(html, url, config['selectors'])
            all_urls.update(page_urls)
            
            logger.info(f"Found {len(page_urls)} URLs (total: {len(all_urls)})")
            
            # Rate limiting
            await asyncio.sleep(2)
        
        logger.info(f"COMPLETED {config['name']}: {len(all_urls)} URLs (expected: {config['expected']})")
        return all_urls
    
    def save_urls(self, seedbank: str, urls: set):
        """Save URLs to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        added = 0
        for url in urls:
            url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
            
            cursor.execute('''
                INSERT OR IGNORE INTO discovered_urls 
                (url_hash, original_url, seedbank)
                VALUES (?, ?, ?)
            ''', (url_hash, url, seedbank))
            
            if cursor.rowcount > 0:
                added += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {added} new URLs for {seedbank}")
        return added
    
    async def crawl_all(self):
        """Crawl all seedbanks"""
        
        connector = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            total = 0
            
            for key, config in self.targets.items():
                urls = await self.crawl_seedbank(session, key, config)
                added = self.save_urls(config['name'], urls)
                total += added
                
                await asyncio.sleep(5)  # Delay between seedbanks
        
        return total
    
    def generate_report(self):
        """Generate report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT seedbank, COUNT(*) FROM discovered_urls GROUP BY seedbank ORDER BY COUNT(*) DESC')
        stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM discovered_urls')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        report = f"""
# Complete Seedbank Discovery Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Results Summary
- **Total URLs Discovered**: {total:,}

## Seedbank Breakdown
"""
        
        for seedbank, count in stats:
            expected = next((config['expected'] for config in self.targets.values() if config['name'] == seedbank), 0)
            percentage = (count / expected * 100) if expected > 0 else 0
            report += f"- **{seedbank}**: {count:,} URLs (expected: {expected:,}, {percentage:.1f}%)\n"
        
        report += f"""
## Next Steps
1. Run bulletproof HTML collection on ALL {total:,} URLs
2. Add to existing S3 archive (13,163 + {total:,} = {13163 + total:,} total)

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'targeted_discovery_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

async def main():
    """Main execution"""
    
    db_path = "../data/targeted_strain_urls.db"
    Path(db_path).parent.mkdir(exist_ok=True)
    
    crawler = TargetedSeedbankCrawler(db_path)
    crawler.create_database()
    
    total = await crawler.crawl_all()
    crawler.generate_report()
    
    print(f"\nCOMPLETE! Discovered {total:,} strain URLs")
    print("Ready for bulletproof HTML collection!")

if __name__ == "__main__":
    asyncio.run(main())