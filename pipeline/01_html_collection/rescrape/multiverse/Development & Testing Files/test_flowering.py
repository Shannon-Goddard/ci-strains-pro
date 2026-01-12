#!/usr/bin/env python3
"""
Test flowering-type pages
"""

import requests
from bs4 import BeautifulSoup

def test_flowering_pages():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    urls = [
        'https://multiversebeans.com/flowering-type/autoflower/',
        'https://multiversebeans.com/flowering-type/photoperiod/'
    ]
    
    for url in urls:
        print(f"\nTesting: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for popup indicators
                if 'Want' in response.text and '10% OFF' in response.text:
                    print("  POPUP DETECTED - not product page")
                else:
                    # Look for product links
                    product_links = []
                    for link in soup.find_all('a', href=True):
                        href = link.get('href')
                        if href and '/product/' in href:
                            product_links.append(href)
                    
                    print(f"  Found {len(product_links)} product links")
                    if product_links:
                        print("  Sample links:")
                        for link in product_links[:3]:
                            print(f"    {link}")
                
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_flowering_pages()