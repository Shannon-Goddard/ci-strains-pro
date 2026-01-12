#!/usr/bin/env python3
"""
Quick test to check Multiverse website structure
"""

import requests
from bs4 import BeautifulSoup

def test_multiverse():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Test main page first
    print("Testing main page...")
    try:
        response = requests.get('https://multiversebeans.com/', headers=headers, timeout=10)
        print(f"Main page status: {response.status_code}")
        if response.status_code == 200:
            print(f"Content length: {len(response.text)}")
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            print(f"Title: {title.get_text() if title else 'No title'}")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Main page error: {e}")
    
    # Test category pages
    test_urls = [
        'https://multiversebeans.com/flowering-type/autoflower/',
        'https://multiversebeans.com/flowering-type/photoperiod/',
        'https://multiversebeans.com/shop/',
        'https://multiversebeans.com/products/'
    ]
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for product links
                product_links = []
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    if href and '/product/' in href:
                        product_links.append(href)
                
                print(f"Found {len(product_links)} product links")
                if product_links:
                    print("Sample links:")
                    for link in product_links[:3]:
                        print(f"  {link}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_multiverse()