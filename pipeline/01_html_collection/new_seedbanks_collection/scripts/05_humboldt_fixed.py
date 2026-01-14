#!/usr/bin/env python3
"""
Fixed Humboldt Crawler - Get URLs from fusion-image-switch-link elements
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

class FixedHumboldtCrawler:
    """Fixed crawler for Humboldt with correct selectors"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        # Fixed Humboldt configuration
        self.humboldt_urls = [
            "https://humboldtseedcompany.com/feminized-seeds/",
            "https://humboldtseedcompany.com/regularseeds/", 
            "https://humboldtseedcompany.com/autoflower-seeds/",
            "https://humboldtseedcompany.com/triploid-cannabis-seeds/"
        ]
        
        # Correct selectors based on chat.txt HTML
        self.selectors = [
            "a.fusion-image-switch-link",  # Main selector from chat.txt
            "a[href*='humboldtseedcompany.com']",  # Backup
            ".fusion-image-switch-link"  # Alternative
        ]
    
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
    
    def extract_humboldt_urls(self, html: str, base_url: str) -> set:
        """Extract Humboldt strain URLs using correct selectors"""
        urls = set()
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Try each selector
            for selector in self.selectors:
                links = soup.select(selector)
                logger.info(f"Selector '{selector}' found {len(links)} links")
                
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        
                        # Only Humboldt product pages
                        if 'humboldtseedcompany.com/' in full_url and self.is_product_url(full_url):
                            urls.add(full_url.split('?')[0])
            
            # Also try all <a> tags as fallback
            all_links = soup.find_all('a', href=True)
            logger.info(f"Total <a> tags found: {len(all_links)}")
            
            for link in all_links:
                href = link.get('href')
                if href and 'humboldtseedcompany.com/' in href:
                    full_url = urljoin(base_url, href)
                    if self.is_product_url(full_url):
                        urls.add(full_url.split('?')[0])
        
        except Exception as e:
            logger.error(f"Error extracting URLs: {e}")
        
        return urls
    
    def is_product_url(self, url: str) -> bool:
        """Check if URL is a Humboldt product page"""
        url_lower = url.lower()
        
        # Product indicators for Humboldt
        if 'humboldtseedcompany.com/' not in url_lower:
            return False
        
        # Exclude category pages
        exclude_terms = [
            '/feminized-seeds/',
            '/regularseeds/',
            '/autoflower-seeds/',
            '/triploid-cannabis-seeds/',
            '/category/',
            '/shop-all/',
            '/page/',
            '?page='
        ]
        
        # Must not be a category page
        if any(term in url_lower for term in exclude_terms):
            return False
        
        # Must have product indicators
        product_indicators = [
            '-feminized-',
            '-seeds/',
            '-strain',
            'cannabis-seeds'
        ]
        
        return any(indicator in url_lower for indicator in product_indicators)
    
    async def crawl_humboldt_fixed(self):
        """Crawl Humboldt with fixed selectors"""
        
        connector = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=connector) as session:
            
            all_urls = set()
            
            for url in self.humboldt_urls:
                logger.info(f"Crawling Humboldt category: {url}")
                
                html = await self.fetch_page(session, url)
                if html:
                    logger.info(f"HTML length: {len(html)} characters")
                    
                    page_urls = self.extract_humboldt_urls(html, url)
                    all_urls.update(page_urls)
                    
                    logger.info(f"Found {len(page_urls)} URLs from {url}")
                    
                    # Print first few URLs for debugging
                    for i, found_url in enumerate(list(page_urls)[:3]):
                        logger.info(f"  Example URL {i+1}: {found_url}")
                
                await asyncio.sleep(2)
            
            logger.info(f"Humboldt FIXED total: {len(all_urls)} URLs")
            return all_urls
    
    def save_urls(self, urls: set):
        """Save URLs to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS humboldt_fixed_urls (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        added = 0
        for url in urls:
            url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
            
            cursor.execute('''
                INSERT OR IGNORE INTO humboldt_fixed_urls 
                (url_hash, original_url)
                VALUES (?, ?)
            ''', (url_hash, url))
            
            if cursor.rowcount > 0:
                added += 1
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {added} new Humboldt URLs")
        return added

async def main():
    """Main execution"""
    
    db_path = "../data/humboldt_fixed.db"
    Path(db_path).parent.mkdir(exist_ok=True)
    
    crawler = FixedHumboldtCrawler(db_path)
    
    urls = await crawler.crawl_humboldt_fixed()
    added = crawler.save_urls(urls)
    
    print(f"\nHUMBOLDT FIXED CRAWLING COMPLETE!")
    print(f"Total URLs discovered: {added}")
    print(f"Expected: 97, Found: {added}")

if __name__ == "__main__":
    asyncio.run(main())