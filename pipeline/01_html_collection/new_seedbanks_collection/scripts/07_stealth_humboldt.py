#!/usr/bin/env python3
"""
Stealth Humboldt Crawler - Bypass 403 blocking
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def stealth_humboldt():
    """Try to bypass Humboldt's 403 blocking"""
    
    # More realistic headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }
    
    # Try different URLs
    urls_to_try = [
        "https://humboldtseedcompany.com/",  # Homepage first
        "https://humboldtseedcompany.com/feminized-seeds/",
        "https://humboldtseedcompany.com/regularseeds/",
        "https://humboldtseedcompany.com/autoflower-seeds/",
        "https://californiahempseeds.com/shop-all/"  # Alternative domain
    ]
    
    connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        
        for url in urls_to_try:
            logger.info(f"Trying: {url}")
            
            try:
                async with session.get(url, headers=headers) as response:
                    logger.info(f"Status: {response.status}")
                    
                    if response.status == 200:
                        html = await response.text()
                        logger.info(f"✅ SUCCESS! HTML length: {len(html)} characters")
                        
                        # Quick check for product links
                        soup = BeautifulSoup(html, 'html.parser')
                        all_links = soup.find_all('a', href=True)
                        
                        product_links = []
                        for link in all_links:
                            href = link.get('href', '')
                            if ('humboldtseedcompany.com' in href or 'californiahempseeds.com' in href) and any(term in href.lower() for term in ['seed', 'strain', 'cannabis', 'feminized']):
                                product_links.append(href)
                        
                        logger.info(f"Found {len(product_links)} potential product links")
                        
                        # Show first few
                        for i, link in enumerate(product_links[:5]):
                            logger.info(f"  Product {i+1}: {link}")
                        
                        return product_links
                    
                    elif response.status == 403:
                        logger.warning(f"❌ Still blocked (403): {url}")
                    else:
                        logger.warning(f"❌ HTTP {response.status}: {url}")
                
            except Exception as e:
                logger.error(f"Error with {url}: {e}")
            
            # Random delay between requests
            await asyncio.sleep(random.uniform(3, 7))
    
    logger.error("All attempts failed - Humboldt has strong anti-bot protection")
    return []

if __name__ == "__main__":
    asyncio.run(stealth_humboldt())