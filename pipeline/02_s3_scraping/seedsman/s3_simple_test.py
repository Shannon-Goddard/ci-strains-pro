#!/usr/bin/env python3

import boto3
import pandas as pd
from bs4 import BeautifulSoup
import re
import hashlib
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def url_to_hash(url):
    """Convert URL to hash like the S3 system does"""
    return hashlib.md5(url.encode()).hexdigest()[:16]

def extract_strain_data(html_content, url):
    """Extract strain data from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check for JavaScript dependency
    text_content = soup.get_text()
    if 'You need to enable Jav' in text_content:
        return None
        
    data = {'url': url, 'strain_name': '', 'thc_content': '', 'genetics': ''}
    
    # Extract strain name from title
    title = soup.find('title')
    if title:
        strain_name = re.sub(r'(Seedsman|Cannabis Seeds).*', '', title.get_text()).strip()
        data['strain_name'] = strain_name
    
    # Extract THC and genetics from text
    text = soup.get_text()
    thc_match = re.search(r'THC[:\s]*(\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?)%', text)
    if thc_match:
        data['thc_content'] = thc_match.group(1)
    
    sativa_match = re.search(r'(\d+)%\s*[Ss]ativa', text)
    indica_match = re.search(r'(\d+)%\s*[Ii]ndica', text)
    if sativa_match or indica_match:
        genetics = []
        if sativa_match:
            genetics.append(f"{sativa_match.group(1)}% Sativa")
        if indica_match:
            genetics.append(f"{indica_match.group(1)}% Indica")
        data['genetics'] = " / ".join(genetics)
    
    return data

def main():
    # Read existing Seedsman URLs
    df = pd.read_csv('seedsman_maximum_extraction.csv')
    urls = df['url'].tolist()[:50]  # Test with first 50
    
    s3_client = boto3.client('s3')
    bucket = 'ci-strains-html-archive'
    results = []
    
    logger.info(f"Processing {len(urls)} Seedsman URLs from S3...")
    
    for i, url in enumerate(urls, 1):
        try:
            url_hash = url_to_hash(url)
            html_key = f'html/{url_hash}.html'
            
            # Get HTML from S3
            response = s3_client.get_object(Bucket=bucket, Key=html_key)
            html_content = response['Body'].read().decode('utf-8', errors='ignore')
            
            # Extract data
            data = extract_strain_data(html_content, url)
            if data:
                results.append(data)
                logger.info(f"✓ {i}/{len(urls)}: {data['strain_name']}")
            else:
                logger.warning(f"✗ {i}/{len(urls)}: JavaScript dependency")
                
        except Exception as e:
            logger.error(f"✗ {i}/{len(urls)}: {e}")
    
    # Save results
    if results:
        result_df = pd.DataFrame(results)
        result_df.to_csv('seedsman_s3_sample.csv', index=False)
        logger.info(f"Saved {len(results)} strains to seedsman_s3_sample.csv")
    else:
        logger.error("No valid data extracted")

if __name__ == "__main__":
    main()