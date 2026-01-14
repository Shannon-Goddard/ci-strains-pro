#!/usr/bin/env python3
"""
Debug Humboldt Crawler - See what HTML we're getting
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def debug_humboldt():
    """Debug what HTML we're getting from Humboldt"""
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    async with aiohttp.ClientSession() as session:
        
        url = "https://humboldtseedcompany.com/feminized-seeds/"
        logger.info(f"Fetching: {url}")
        
        try:
            headers = {'User-Agent': user_agent}
            async with session.get(url, headers=headers, timeout=30) as response:
                logger.info(f"Status: {response.status}")
                
                if response.status == 200:
                    html = await response.text()
                    logger.info(f"HTML length: {len(html)} characters")
                    
                    # Save HTML to file for inspection
                    with open("../data/humboldt_debug.html", "w", encoding="utf-8") as f:
                        f.write(html)
                    
                    # Parse and look for links
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Check different selectors
                    selectors_to_try = [
                        "a.fusion-image-switch-link",
                        "a[href*='humboldtseedcompany.com']",
                        ".fusion-image-switch-link",
                        "a[href*='cannabis-seeds']",
                        "a[href*='feminized']",
                        "a[href*='strain']"
                    ]
                    
                    for selector in selectors_to_try:
                        links = soup.select(selector)
                        logger.info(f"Selector '{selector}': {len(links)} matches")
                        
                        for i, link in enumerate(links[:3]):  # Show first 3
                            href = link.get('href', 'NO HREF')
                            text = link.get_text().strip()[:50]
                            logger.info(f"  {i+1}: {href} | Text: {text}")
                    
                    # Check all <a> tags
                    all_links = soup.find_all('a', href=True)
                    logger.info(f"Total <a> tags: {len(all_links)}")
                    
                    # Look for any humboldtseedcompany.com links
                    humboldt_links = [link for link in all_links if 'humboldtseedcompany.com' in link.get('href', '')]
                    logger.info(f"Humboldt links found: {len(humboldt_links)}")
                    
                    for i, link in enumerate(humboldt_links[:5]):
                        href = link.get('href')
                        text = link.get_text().strip()[:30]
                        logger.info(f"  Humboldt {i+1}: {href} | {text}")
                    
                    # Check if page has JavaScript loading
                    scripts = soup.find_all('script')
                    logger.info(f"Script tags found: {len(scripts)}")
                    
                    # Look for specific content
                    if 'fusion-image-switch-link' in html:
                        logger.info("✅ Found 'fusion-image-switch-link' in HTML")
                    else:
                        logger.info("❌ 'fusion-image-switch-link' NOT found in HTML")
                    
                    if 'banana-melt' in html.lower():
                        logger.info("✅ Found 'banana-melt' in HTML")
                    else:
                        logger.info("❌ 'banana-melt' NOT found in HTML")
                
                else:
                    logger.error(f"HTTP {response.status}")
                    
        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_humboldt())