#!/usr/bin/env python3
"""
Bulletproof Elite Seedbank Crawler - For 5 failing seedbanks
Uses Bright Data/ScrapingBee to bypass bot protection

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import sys
import sqlite3
import hashlib
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import logging

sys.path.append(str(Path(__file__).parent.parent / 'config'))
from aws_secrets import get_aws_credentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BulletproofCrawler:
    """Bulletproof crawler using Bright Data/ScrapingBee"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        creds = get_aws_credentials()
        self.scrapingbee_key = creds.get('SCRAPINGBEE_API_KEY')
        
        # 5 failing seedbanks
        self.seedbanks = {
            "herbies": {
                "name": "Herbies Seeds",
                "urls": [f"https://herbiesheadshop.com/collections/feminized-seeds/page/{i}" for i in range(1, 23)],
                "selectors": ["a.category-item__image-wrap", "a[href*='/cannabis-seeds/']"]  
            },
            "zamnesia": {
                "name": "Zamnesia",
                "urls": [f"https://www.zamnesia.com/cannabis-seeds?p={i}" for i in range(1, 8)] +
                        [f"https://www.zamnesia.com/autoflowering-seeds?p={i}" for i in range(1, 6)],
                "selectors": ["a[href*='/cannabis-seeds/']", "a[href*='/autoflowering-seeds/']"]
            },
            "exotic": {
                "name": "Exotic Genetix",
                "urls": [f"https://exoticgenetix.com/product-category/seeds/page/{i}/" for i in range(1, 23)],
                "selectors": ["a[href*='/product/']", ".product a"]
            },
            "original": {
                "name": "Original Seeds Store",
                "urls": ["https://www.originalseeds.org/cannabis-seeds", 
                        "https://www.originalseeds.org/cannabis-seeds?p=2"],
                "selectors": ["a[href*='/cannabis-seeds/']", ".product-item a"]
            },
            "tiki": {
                "name": "Tiki Madman",
                "urls": ["https://tikimadman.com/product-category/seeds/"],
                "selectors": ["a[href*='/product/']", ".product a"]
            }
        }
    

    def fetch_with_scrapingbee(self, url: str) -> str:
        """Fetch using ScrapingBee"""
        try:
            api_url = "https://app.scrapingbee.com/api/v1/"
            params = {
                'api_key': self.scrapingbee_key,
                'url': url,
                'render_js': 'true',
                'premium_proxy': 'true'
            }
            response = requests.get(api_url, params=params, timeout=60)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logger.warning(f"ScrapingBee failed for {url}: {e}")
        return ""
    
    def fetch_bulletproof(self, url: str) -> str:
        """Fetch using ScrapingBee with premium proxy"""
        html = self.fetch_with_scrapingbee(url)
        if html:
            return html
        
        time.sleep(2)
        
        # Retry once more
        html = self.fetch_with_scrapingbee(url)
        return html if html else ""
    
    def extract_product_urls(self, html: str, base_url: str, selectors: list) -> set:
        """Extract product URLs"""
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
        
        product_patterns = [
            '/seeds/', '/product/', '/cannabis-seeds/', '/autoflowering-seeds/'
        ]
        
        exclude_patterns = [
            '/category/', '/page/', '?page=', '?p=', '/cart', '/checkout',
            '/account', '/shop', 'cannabis-seeds?', 'autoflowering-seeds?'
        ]
        
        has_product = any(p in url_lower for p in product_patterns)
        has_exclude = any(p in url_lower for p in exclude_patterns)
        
        return has_product and not has_exclude
    
    def crawl_seedbank(self, key: str) -> set:
        """Crawl one seedbank"""
        config = self.seedbanks[key]
        logger.info(f"Crawling {config['name']} - {len(config['urls'])} pages")
        
        all_urls = set()
        
        for i, url in enumerate(config['urls'], 1):
            logger.info(f"{config['name']} page {i}/{len(config['urls'])}: {url}")
            
            html = self.fetch_bulletproof(url)
            
            if html:
                urls = self.extract_product_urls(html, url, config['selectors'])
                all_urls.update(urls)
                logger.info(f"Found {len(urls)} products on page {i}")
            else:
                logger.warning(f"Failed to fetch page {i}")
            
            time.sleep(3)  # Rate limiting
        
        logger.info(f"{config['name']}: {len(all_urls)} total URLs")
        return all_urls
    
    def save_urls(self, seedbank: str, urls: set):
        """Save URLs to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bulletproof_urls (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                seedbank TEXT NOT NULL,
                discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        added = 0
        for url in urls:
            url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
            
            cursor.execute('''
                INSERT OR IGNORE INTO bulletproof_urls 
                (url_hash, original_url, seedbank)
                VALUES (?, ?, ?)
            ''', (url_hash, url, seedbank))
            
            if cursor.rowcount > 0:
                added += 1
        
        conn.commit()
        conn.close()
        
        return added
    
    def crawl_all(self):
        """Crawl all 5 failing seedbanks"""
        results = {}
        
        for key in ["herbies", "zamnesia", "exotic", "original", "tiki"]:
            urls = self.crawl_seedbank(key)
            config = self.seedbanks[key]
            added = self.save_urls(config["name"], urls)
            results[key] = len(urls)
            logger.info(f"Saved {added} new URLs for {config['name']}")
            time.sleep(5)
        
        return results
    
    def generate_report(self, results: dict):
        """Generate report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT seedbank, COUNT(*) FROM bulletproof_urls GROUP BY seedbank')
        stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM bulletproof_urls')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        report = f"""
# Bulletproof Crawler Report - 5 Failing Seedbanks
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Results Summary
- **Total URLs Discovered**: {total:,}

## Breakdown by Seedbank

"""
        
        for row in stats:
            report += f"- **{row[0]}**: {row[1]:,} URLs\n"
        
        report += f"""
## Combined Pipeline 06 Results
- **Simple Crawler (3 seedbanks)**: 2,174 URLs
- **Bulletproof Crawler (5 seedbanks)**: {total:,} URLs
- **TOTAL PIPELINE 06**: {2174 + total:,} URLs

## Next Steps
1. Merge both databases
2. Run bulletproof HTML collection on all {2174 + total:,} URLs
3. Expand archive: 16,623 + {2174 + total:,} = {16623 + 2174 + total:,} total pages

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'bulletproof_discovery_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved: {report_path}")

def main():
    """Main execution"""
    
    db_path = "../data/elite_bulletproof_urls.db"
    Path(db_path).parent.mkdir(exist_ok=True)
    
    crawler = BulletproofCrawler(db_path)
    
    results = crawler.crawl_all()
    crawler.generate_report(results)
    
    print(f"\nBULLETPROOF CRAWLING COMPLETE!")
    print(f"Check bulletproof_discovery_report.md for results")

if __name__ == "__main__":
    main()
