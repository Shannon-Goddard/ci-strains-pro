#!/usr/bin/env python3
"""
S3 HTML Analyzer for Dutch Passion
Examines random HTML files to identify all extractable data points
"""

import boto3
import pandas as pd
import random
from bs4 import BeautifulSoup
import re

def analyze_dutch_passion_html():
    s3 = boto3.client('s3')
    bucket = 'ci-strains-html-archive'
    
    # Get Dutch Passion URLs
    try:
        response = s3.get_object(Bucket=bucket, Key='index/url_mapping.csv')
        df = pd.read_csv(response['Body'])
    except:
        df = pd.read_csv('../../01_html_collection/data/unique_urls.csv', encoding='latin-1')
    
    dutch_passion_urls = df[df['url'].str.contains('dutch-passion', na=False)]
    
    # Get available HTML files
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix='html/')
    
    all_files = []
    for page in page_iterator:
        if 'Contents' in page:
            all_files.extend([obj['Key'] for obj in page['Contents']])
    
    available_hashes = {f.split('/')[-1].replace('.html', '') for f in all_files if f.endswith('.html')}
    
    # Find Dutch Passion files that exist
    existing_dutch_files = []
    for _, row in dutch_passion_urls.iterrows():
        if row['url_hash'] in available_hashes:
            existing_dutch_files.append((row['url_hash'], row['url']))
    
    # Select 3 random files
    random_files = random.sample(existing_dutch_files, min(3, len(existing_dutch_files)))
    
    print(f"Analyzing {len(random_files)} random Dutch Passion HTML files:\n")
    
    for i, (url_hash, url) in enumerate(random_files, 1):
        print(f"=== FILE {i}: {url} ===")
        
        try:
            # Get HTML from S3
            html_key = f'html/{url_hash}.html'
            response = s3.get_object(Bucket=bucket, Key=html_key)
            html_content = response['Body'].read().decode('utf-8')
            
            # Parse and analyze
            soup = BeautifulSoup(html_content, 'html.parser')
            analyze_single_file(soup, url)
            
        except Exception as e:
            print(f"Error processing {url}: {e}")
        
        print("\n" + "="*80 + "\n")

def analyze_single_file(soup, url):
    """Analyze a single HTML file for all possible data points"""
    
    print(f"URL: {url}")
    print(f"Title: {soup.find('title').get_text() if soup.find('title') else 'No title'}")
    
    # 1. Basic strain info
    print("\n--- BASIC STRAIN INFO ---")
    h1 = soup.find('h1')
    if h1:
        print(f"H1 Title: {h1.get_text().strip()}")
    
    # 2. Tables and structured data
    print("\n--- TABLES & STRUCTURED DATA ---")
    tables = soup.find_all('table')
    for i, table in enumerate(tables):
        print(f"Table {i+1}:")
        rows = table.find_all('tr')
        for row in rows[:5]:  # First 5 rows
            cells = [td.get_text().strip() for td in row.find_all(['td', 'th'])]
            if cells:
                print(f"  {' | '.join(cells)}")
    
    # 3. Specification divs/sections
    print("\n--- SPECIFICATION SECTIONS ---")
    spec_selectors = [
        'div[class*="spec"]', 'div[class*="detail"]', 'div[class*="info"]',
        'div[class*="product"]', 'section[class*="spec"]'
    ]
    for selector in spec_selectors:
        elements = soup.select(selector)
        for elem in elements[:3]:  # First 3 matches
            text = elem.get_text().strip()
            if len(text) > 20 and len(text) < 200:
                print(f"  {selector}: {text[:100]}...")
    
    # 4. Meta tags
    print("\n--- META TAGS ---")
    meta_tags = soup.find_all('meta')
    for meta in meta_tags:
        name = meta.get('name') or meta.get('property')
        content = meta.get('content')
        if name and content and len(content) > 10:
            print(f"  {name}: {content[:100]}...")
    
    # 5. JSON-LD structured data
    print("\n--- JSON-LD DATA ---")
    json_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_scripts:
        print(f"  JSON-LD found: {script.string[:100] if script.string else 'Empty'}...")
    
    # 6. Lists and bullet points
    print("\n--- LISTS & FEATURES ---")
    lists = soup.find_all(['ul', 'ol'])
    for i, ul in enumerate(lists[:3]):
        items = [li.get_text().strip() for li in ul.find_all('li')]
        if items:
            print(f"  List {i+1}: {items[:3]}...")
    
    # 7. Specific cannabis data patterns
    print("\n--- CANNABIS-SPECIFIC PATTERNS ---")
    html_text = soup.get_text()
    
    # THC patterns
    thc_matches = re.findall(r'THC[:\s]*(\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*%)', html_text, re.IGNORECASE)
    if thc_matches:
        print(f"  THC patterns: {thc_matches}")
    
    # CBD patterns
    cbd_matches = re.findall(r'CBD[:\s]*(\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*%)', html_text, re.IGNORECASE)
    if cbd_matches:
        print(f"  CBD patterns: {cbd_matches}")
    
    # Flowering time
    flowering_matches = re.findall(r'(\d+(?:\s*[-–]\s*\d+)?\s*weeks?\s*(?:flower|bloom))', html_text, re.IGNORECASE)
    if flowering_matches:
        print(f"  Flowering time: {flowering_matches}")
    
    # Yield patterns
    yield_matches = re.findall(r'yield[:\s]*(\d+(?:\s*[-–]\s*\d+)?\s*(?:g|grams?|oz|ounces?))', html_text, re.IGNORECASE)
    if yield_matches:
        print(f"  Yield patterns: {yield_matches}")
    
    # Height patterns
    height_matches = re.findall(r'height[:\s]*(\d+(?:\s*[-–]\s*\d+)?\s*(?:cm|m|ft|inches?))', html_text, re.IGNORECASE)
    if height_matches:
        print(f"  Height patterns: {height_matches}")
    
    # Genetics patterns
    genetics_matches = re.findall(r'(?:genetics|cross|lineage)[:\s]*([^.\n]{10,80})', html_text, re.IGNORECASE)
    if genetics_matches:
        print(f"  Genetics patterns: {genetics_matches[:2]}")
    
    # 8. Images and media
    print("\n--- IMAGES & MEDIA ---")
    images = soup.find_all('img')
    relevant_images = [img for img in images if img.get('src') and any(term in img.get('src', '').lower() for term in ['strain', 'seed', 'cannabis', 'bud'])]
    if relevant_images:
        print(f"  Strain images found: {len(relevant_images)}")
        for img in relevant_images[:2]:
            print(f"    {img.get('src')}")
    
    # 9. Price information
    print("\n--- PRICING DATA ---")
    price_patterns = [r'\$(\d+(?:\.\d{2})?)', r'€(\d+(?:\.\d{2})?)', r'£(\d+(?:\.\d{2})?)']
    for pattern in price_patterns:
        prices = re.findall(pattern, html_text)
        if prices:
            print(f"  Prices found: {prices[:3]}")
    
    # 10. Awards and certifications
    print("\n--- AWARDS & CERTIFICATIONS ---")
    award_keywords = ['cup', 'award', 'winner', 'champion', 'medal', 'prize', 'certified']
    for keyword in award_keywords:
        matches = re.findall(rf'{keyword}[^.\n]{{0,50}}', html_text, re.IGNORECASE)
        if matches:
            print(f"  {keyword.title()}: {matches[:2]}")

if __name__ == "__main__":
    analyze_dutch_passion_html()