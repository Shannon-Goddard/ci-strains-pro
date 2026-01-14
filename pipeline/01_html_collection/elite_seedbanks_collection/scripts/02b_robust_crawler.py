#!/usr/bin/env python3
"""
Robust Elite Seedbank Crawler - Using Pipeline 04 async methodology
Discovers ALL product URLs using proper HTML parsing

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

class RobustEliteCrawler:
    """Robust crawler using async/await and proper HTML parsing"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        # Elite seedbank configurations from chat.txt
        self.seedbanks = {
            "herbies": {
                "name": "Herbies Seeds",
                "base_url": "https://herbiesheadshop.com/cannabis-seeds",
                "pages": 22,
                "selectors": ["a[href*='/seeds/']", ".product-item a", "a.product-link"],
                "expected": 630
            },
            "amsterdam": {
                "name": "Amsterdam Marijuana Seeds",
                "base_url": "https://amsterdammarijuanaseeds.com/feminized",
                "pages": 14,
                "selectors": ["a[href*='/feminized/']", ".product a", "a[href*='amsterdammarijuanaseeds.com']"],
                "expected": 406
            },
            "gorilla": {
                "name": "Gorilla Seeds Bank",
                "urls": [
                    {"base": "https://gorillaseedsbank.com/product-category/cannabis-seeds", "pages": 94},
                    {"base": "https://gorillaseedsbank.com/product-category/bulk-cannabis-seeds", "pages": 34}
                ],
                "selectors": ["a[href*='/product/']", ".product-title a", "a.woocommerce-LoopProduct-link"],
                "expected": 3083
            },
            "zamnesia": {
                "name": "Zamnesia",
                "urls": [
                    {"base": "https://www.zamnesia.com/cannabis-seeds", "pages": 7},
                    {"base": "https://www.zamnesia.com/autoflowering-seeds", "pages": 5}
                ],
                "selectors": ["a[href*='/cannabis-seeds/']", "a[href*='/autoflowering-seeds/']", ".product-item a"],
                "expected": 288
            },
            "exotic": {
                "name": "Exotic Genetix",
                "base_url": "https://exoticgenetix.com/product-category/seeds",
                "pages": 22,
                "selectors": ["a[href*='/product/']", ".product a", "a.woocommerce-LoopProduct-link"],
                "expected": 528
            },
            "original": {
                "name": "Original Seeds Store",
                "base_url": "https://www.originalseeds.org/cannabis-seeds",
                "pages": 2,
                "selectors": ["a[href*='/cannabis-seeds/']", ".product-item a"],
                "expected": 48
            },
            "tiki": {
                "name": "Tiki Madman",
                "base_url": "https://tikimadman.com/product-category/seeds",
                "pages": 1,
                "selectors": ["a[href*='/product/']", ".product a"],
                "expected": 24
            },
            "compound": {
                "name": "Compound Genetics",
                "urls": [
                    "https://compoundgenetics.com/product-category/seeds/feminized-seeds/",
                    "https://compoundgenetics.com/product-category/seeds/regular-seeds/",
                    "https://compoundgenetics.com/product-category/seeds/auto-flower-seeds/",
                    "https://compoundgenetics.com/product-category/seeds/cbd-seeds/"
                ],
                "selectors": ["a[href*='/product/']", ".product-title a"],
                "expected": 76
            }
        }
    
    def create_database(self):
        """Create database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS robust_urls (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                seedbank TEXT NOT NULL,
                discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """Fetch page with retry"""
        for attempt in range(3):
            try:
                headers = {'User-Agent': self.user_agent}
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
            except Exception as e:
                if attempt == 2:
                    logger.warning(f"Failed {url}: {e}")
                await asyncio.sleep(2)
        return ""
    
    def extract_product_urls(self, html: str, base_url: str, selectors: list) -> set:
        """Extract product URLs using multiple selectors"""
        urls = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        if self.is_product_url(full_url):
                            urls.add(full_url.split('?')[0].split('#')[0])
        
        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
        
        return urls
    
    def is_product_url(self, url: str) -> bool:
        """Check if URL is a product page"""
        url_lower = url.lower()
        
        # Product indicators
        product_patterns = [
            '/product/', '/seeds/', '/feminized/', '/autoflowering-seeds/',
            '/cannabis-seeds/', '/regular-seeds/', '/auto-flower-seeds/', '/cbd-seeds/'
        ]
        
        # Exclude patterns
        exclude_patterns = [
            '/category/', '/page/', '?page=', '/cart', '/checkout',
            '/account', '/shop', '/product-category/seeds$'
        ]
        
        has_product = any(p in url_lower for p in product_patterns)
        has_exclude = any(p in url_lower for p in exclude_patterns)
        
        return has_product and not has_exclude
    
    async def crawl_paginated(self, session: aiohttp.ClientSession, base_url: str, 
                             pages: int, selectors: list, name: str) -> set:
        """Crawl paginated catalog"""
        all_urls = set()
        
        for page in range(1, pages + 1):
            # Try multiple pagination formats
            page_urls = [
                f"{base_url}/page/{page}/",
                f"{base_url}?page={page}",
                f"{base_url}/page/{page}"
            ]
            
            for page_url in page_urls:
                html = await self.fetch_page(session, page_url)
                if html:
                    urls = self.extract_product_urls(html, page_url, selectors)
                    if urls:
                        all_urls.update(urls)
                        logger.info(f"{name} page {page}: {len(urls)} products")
                        break
            
            await asyncio.sleep(1)
        
        return all_urls
    
    async def crawl_herbies(self, session: aiohttp.ClientSession):
        """Crawl Herbies"""
        config = self.seedbanks["herbies"]
        logger.info(f"Crawling {config['name']}")
        
        urls = await self.crawl_paginated(
            session, config["base_url"], config["pages"], 
            config["selectors"], config["name"]
        )
        
        logger.info(f"{config['name']}: {len(urls)} URLs")
        return urls
    
    async def crawl_amsterdam(self, session: aiohttp.ClientSession):
        """Crawl Amsterdam"""
        config = self.seedbanks["amsterdam"]
        logger.info(f"Crawling {config['name']}")
        
        urls = await self.crawl_paginated(
            session, config["base_url"], config["pages"],
            config["selectors"], config["name"]
        )
        
        logger.info(f"{config['name']}: {len(urls)} URLs")
        return urls
    
    async def crawl_gorilla(self, session: aiohttp.ClientSession):
        """Crawl Gorilla"""
        config = self.seedbanks["gorilla"]
        logger.info(f"Crawling {config['name']}")
        
        all_urls = set()
        for url_config in config["urls"]:
            urls = await self.crawl_paginated(
                session, url_config["base"], url_config["pages"],
                config["selectors"], config["name"]
            )
            all_urls.update(urls)
        
        logger.info(f"{config['name']}: {len(all_urls)} URLs")
        return all_urls
    
    async def crawl_zamnesia(self, session: aiohttp.ClientSession):
        """Crawl Zamnesia"""
        config = self.seedbanks["zamnesia"]
        logger.info(f"Crawling {config['name']}")
        
        all_urls = set()
        for url_config in config["urls"]:
            urls = await self.crawl_paginated(
                session, url_config["base"], url_config["pages"],
                config["selectors"], config["name"]
            )
            all_urls.update(urls)
        
        logger.info(f"{config['name']}: {len(all_urls)} URLs")
        return all_urls
    
    async def crawl_exotic(self, session: aiohttp.ClientSession):
        """Crawl Exotic Genetix"""
        config = self.seedbanks["exotic"]
        logger.info(f"Crawling {config['name']}")
        
        urls = await self.crawl_paginated(
            session, config["base_url"], config["pages"],
            config["selectors"], config["name"]
        )
        
        logger.info(f"{config['name']}: {len(urls)} URLs")
        return urls
    
    async def crawl_original(self, session: aiohttp.ClientSession):
        """Crawl Original Seeds"""
        config = self.seedbanks["original"]
        logger.info(f"Crawling {config['name']}")
        
        urls = await self.crawl_paginated(
            session, config["base_url"], config["pages"],
            config["selectors"], config["name"]
        )
        
        logger.info(f"{config['name']}: {len(urls)} URLs")
        return urls
    
    async def crawl_tiki(self, session: aiohttp.ClientSession):
        """Crawl Tiki Madman"""
        config = self.seedbanks["tiki"]
        logger.info(f"Crawling {config['name']}")
        
        urls = await self.crawl_paginated(
            session, config["base_url"], config["pages"],
            config["selectors"], config["name"]
        )
        
        logger.info(f"{config['name']}: {len(urls)} URLs")
        return urls
    
    async def crawl_compound(self, session: aiohttp.ClientSession):
        """Crawl Compound Genetics"""
        config = self.seedbanks["compound"]
        logger.info(f"Crawling {config['name']}")
        
        all_urls = set()
        for url in config["urls"]:
            html = await self.fetch_page(session, url)
            if html:
                urls = self.extract_product_urls(html, url, config["selectors"])
                all_urls.update(urls)
                logger.info(f"{config['name']} {url.split('/')[-2]}: {len(urls)} products")
            await asyncio.sleep(2)
        
        logger.info(f"{config['name']}: {len(all_urls)} URLs")
        return all_urls
    
    def save_urls(self, seedbank: str, urls: set):
        """Save URLs to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        added = 0
        for url in urls:
            url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
            
            cursor.execute('''
                INSERT OR IGNORE INTO robust_urls 
                (url_hash, original_url, seedbank)
                VALUES (?, ?, ?)
            ''', (url_hash, url, seedbank))
            
            if cursor.rowcount > 0:
                added += 1
        
        conn.commit()
        conn.close()
        
        return added
    
    async def crawl_all(self):
        """Crawl all seedbanks"""
        connector = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            results = {}
            
            results["herbies"] = await self.crawl_herbies(session)
            await asyncio.sleep(3)
            
            results["amsterdam"] = await self.crawl_amsterdam(session)
            await asyncio.sleep(3)
            
            results["gorilla"] = await self.crawl_gorilla(session)
            await asyncio.sleep(3)
            
            results["zamnesia"] = await self.crawl_zamnesia(session)
            await asyncio.sleep(3)
            
            results["exotic"] = await self.crawl_exotic(session)
            await asyncio.sleep(3)
            
            results["original"] = await self.crawl_original(session)
            await asyncio.sleep(3)
            
            results["tiki"] = await self.crawl_tiki(session)
            await asyncio.sleep(3)
            
            results["compound"] = await self.crawl_compound(session)
            
            # Save all
            total_added = 0
            for key, urls in results.items():
                config = self.seedbanks[key]
                added = self.save_urls(config["name"], urls)
                total_added += added
            
            return total_added, results
    
    def generate_report(self, results: dict):
        """Generate report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT seedbank, COUNT(*) FROM robust_urls GROUP BY seedbank ORDER BY COUNT(*) DESC')
        stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM robust_urls')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        report = f"""
# Robust Elite Seedbank Discovery Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Results Summary
- **Total URLs Discovered**: {total:,}

## Breakdown by Seedbank

"""
        
        for key, config in self.seedbanks.items():
            found = len(results.get(key, set()))
            expected = config["expected"]
            pct = (found / expected * 100) if expected > 0 else 0
            
            report += f"- **{config['name']}**: {found:,} URLs (expected: {expected:,}, {pct:.1f}%)\n"
        
        total_expected = sum(c["expected"] for c in self.seedbanks.values())
        
        report += f"""
## Success Analysis
- **Total Expected**: {total_expected:,}
- **Total Found**: {total:,}
- **Success Rate**: {(total / total_expected * 100):.1f}%

## Next Steps
1. Run bulletproof HTML collection on {total:,} URLs
2. Expand archive: 16,623 + {total:,} = {16623 + total:,} total pages

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'robust_discovery_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved: {report_path}")

async def main():
    """Main execution"""
    
    db_path = "../data/elite_robust_urls.db"
    Path(db_path).parent.mkdir(exist_ok=True)
    
    crawler = RobustEliteCrawler(db_path)
    crawler.create_database()
    
    total_added, results = await crawler.crawl_all()
    crawler.generate_report(results)
    
    print(f"\nROBUST CRAWLING COMPLETE!")
    print(f"Total URLs discovered: {total_added:,}")

if __name__ == "__main__":
    asyncio.run(main())
