#!/usr/bin/env python3
"""
Pipeline 06: Elite Seedbanks Precise Crawler
Target: 8 Premium Seedbanks | ~3,083 Strains | Breaking 20K Total

Based on proven Pipeline 04 methodology
Logic designed by Amazon Q, verified by Shannon Goddard.
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

class EliteSeedbankCrawler:
    """Precise crawler for 8 elite seedbanks"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        # Exact configurations from chat.txt research
        self.seedbanks = {
            "herbies": {
                "name": "Herbies Head Shop",
                "base_urls": [
                    "https://herbiesheadshop.com/collections/feminized-seeds",
                    "https://herbiesheadshop.com/collections/regular-cannabis-seeds"
                ],
                "pagination": "/page/{page}",
                "pages_per_category": [21, 1],
                "selectors": ["a[href*='/seeds/']", "a.product-card__name"],
                "expected": 440
            },
            "amsterdam": {
                "name": "Amsterdam Marijuana Seeds",
                "base_urls": ["https://amsterdammarijuanaseeds.com/all-seeds/"],
                "pagination": "page/{page}/",
                "pages_per_category": [14],
                "selectors": ["a.woocommerce-LoopProduct-link", "a[href*='/product/']"],
                "expected": 168
            },
            "gorilla": {
                "name": "Gorilla Seeds Bank",
                "base_urls": [
                    "https://www.gorilla-cannabis-seeds.co.uk/feminized-seeds",
                    "https://www.gorilla-cannabis-seeds.co.uk/autoflowering-seeds"
                ],
                "pagination": "?page={page}",
                "pages_per_category": [93, 33],
                "selectors": ["a.product-item-link", "a[href*='.html']"],
                "expected": 1260
            },
            "zamnesia": {
                "name": "Zamnesia",
                "base_urls": [
                    "https://www.zamnesia.com/us/295-feminized-seeds",
                    "https://www.zamnesia.com/us/294-autoflower-seeds"
                ],
                "pagination": "?p={page}",
                "pages_per_category": [6, 4],
                "selectors": ["a.product-name", "a[href*='/product/']"],
                "expected": 759
            },
            "exotic": {
                "name": "Exotic Genetix",
                "base_urls": ["https://exoticgenetix.com/shop/"],
                "pagination": "page/{page}/",
                "pages_per_category": [22],
                "selectors": ["a.woocommerce-LoopProduct-link", "a[href*='/product/']"],
                "expected": 330
            },
            "original": {
                "name": "Original Seeds Store",
                "base_urls": [
                    "https://www.originalseedsstore.com/feminized-cannabis-seeds",
                    "https://www.originalseedsstore.com/regular-seeds"
                ],
                "pagination": None,
                "pages_per_category": [1, 1],
                "selectors": ["a.product-item-link", "a[href*='/product/']"],
                "expected": 56
            },
            "tiki": {
                "name": "Tiki Madman",
                "base_urls": ["https://tikimadman.com/strains/"],
                "pagination": None,
                "pages_per_category": [1],
                "selectors": ["a[href*='/strain/']", ".strain-card a"],
                "expected": 41
            },
            "compound": {
                "name": "Compound Genetics",
                "base_urls": [
                    "https://seeds.compound-genetics.com/collections/grape-gasoline",
                    "https://seeds.compound-genetics.com/collections/eye-candy",
                    "https://seeds.compound-genetics.com/collections/jokerz-volume-2",
                    "https://seeds.compound-genetics.com/collections/jokerz-vol-1"
                ],
                "pagination": None,
                "pages_per_category": [1, 1, 1, 1],
                "selectors": ["a[href*='/products/']", ".product-item a"],
                "expected": 29
            }
        }
    
    def create_database(self):
        """Create database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elite_urls (
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
                        
                        if self.is_product_url(full_url):
                            urls.add(full_url.split('?')[0])
        
        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
        
        return urls
    
    def is_product_url(self, url: str) -> bool:
        """Check if URL is a product page"""
        url_lower = url.lower()
        
        product_indicators = [
            '/product/', '/products/', '/seeds/', '/strain/', '/strains/',
            '-seeds', '.html'
        ]
        
        exclude_indicators = [
            '/category/', '/categories/', '/collection/', '/page/',
            '?page=', '/cart', '/account', '/login'
        ]
        
        has_product = any(indicator in url_lower for indicator in product_indicators)
        has_exclude = any(indicator in url_lower for indicator in exclude_indicators)
        
        return has_product and not has_exclude
    
    async def crawl_seedbank(self, session: aiohttp.ClientSession, bank_key: str):
        """Crawl a specific seedbank"""
        config = self.seedbanks[bank_key]
        logger.info(f"Crawling {config['name']} - Expected: {config['expected']}")
        
        all_urls = set()
        
        for i, base_url in enumerate(config["base_urls"]):
            max_pages = config["pages_per_category"][i]
            category = base_url.split('/')[-2] if '/' in base_url else "main"
            
            logger.info(f"{config['name']} {category}: {max_pages} pages")
            
            for page in range(1, max_pages + 1):
                if config["pagination"] and page > 1:
                    if '?' in config["pagination"]:
                        page_url = f"{base_url}{config['pagination'].format(page=page)}"
                    else:
                        page_url = f"{base_url.rstrip('/')}/{config['pagination'].format(page=page)}"
                else:
                    page_url = base_url
                
                logger.info(f"Fetching: {page_url}")
                html = await self.fetch_page(session, page_url)
                
                if html:
                    page_urls = self.extract_strain_urls(html, page_url, config["selectors"])
                    all_urls.update(page_urls)
                    logger.info(f"Found {len(page_urls)} URLs on page {page}")
                
                await asyncio.sleep(2)
                
                if not config["pagination"]:
                    break
        
        logger.info(f"{config['name']} total: {len(all_urls)} URLs")
        return all_urls
    
    def save_urls(self, seedbank: str, urls: set, category: str = ""):
        """Save URLs to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        added = 0
        for url in urls:
            url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
            
            cursor.execute('''
                INSERT OR IGNORE INTO elite_urls 
                (url_hash, original_url, seedbank, category)
                VALUES (?, ?, ?, ?)
            ''', (url_hash, url, seedbank, category))
            
            if cursor.rowcount > 0:
                added += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {added} new URLs for {seedbank}")
        return added
    
    async def crawl_all(self):
        """Crawl all elite seedbanks"""
        
        connector = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            results = {}
            
            for bank_key in self.seedbanks.keys():
                results[bank_key] = await self.crawl_seedbank(session, bank_key)
                await asyncio.sleep(5)
            
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
        
        cursor.execute('SELECT seedbank, COUNT(*) FROM elite_urls GROUP BY seedbank ORDER BY COUNT(*) DESC')
        stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM elite_urls')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        report = f"""
# Pipeline 06: Elite Seedbanks Discovery Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## THE 20K BREAKTHROUGH!
- **Total URLs Discovered**: {total:,}
- **Current Database**: 17,243 strains
- **NEW TOTAL**: {17243 + total:,} strains

## Detailed Breakdown
"""
        
        for seedbank_key, config in self.seedbanks.items():
            found = len(results.get(seedbank_key, set()))
            expected = config["expected"]
            percentage = (found / expected * 100) if expected > 0 else 0
            
            report += f"- **{config['name']}**: {found:,} URLs (expected: {expected:,}, {percentage:.1f}%)\n"
        
        total_expected = sum(config['expected'] for config in self.seedbanks.values())
        
        report += f"""
## Success Analysis
- **Total Expected**: {total_expected:,}
- **Total Found**: {total:,}
- **Overall Success**: {(total / total_expected * 100):.1f}%

## Next Steps
1. Run bulletproof HTML collection on ALL {total:,} URLs
2. Add to existing S3 archive: 17,243 + {total:,} = {17243 + total:,} total pages
3. Extract maximum value using Dutch Passion methodology
4. **BREAK 20,000 STRAINS!**

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'elite_discovery_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved: {report_path}")
        
        # Also save flat URL list
        cursor = conn.cursor()
        cursor.execute('SELECT original_url FROM elite_urls')
        urls = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        urls_file = Path(self.db_path).parent / 'elite_urls_flat.txt'
        with open(urls_file, 'w') as f:
            for url in urls:
                f.write(url + '\n')
        
        logger.info(f"URL list saved: {urls_file}")

async def main():
    """Main execution"""
    
    db_path = "../data/elite_strain_urls.db"
    Path(db_path).parent.mkdir(exist_ok=True)
    
    crawler = EliteSeedbankCrawler(db_path)
    crawler.create_database()
    
    total_added, results = await crawler.crawl_all()
    crawler.generate_report(results)
    
    print(f"\n{'='*60}")
    print("PIPELINE 06: ELITE SEEDBANKS URL DISCOVERY COMPLETE!")
    print(f"{'='*60}")
    print(f"Total URLs discovered: {total_added:,}")
    print(f"Ready for bulletproof HTML collection!")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())
