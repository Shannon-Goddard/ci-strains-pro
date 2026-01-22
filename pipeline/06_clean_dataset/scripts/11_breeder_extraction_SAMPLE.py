"""
Breeder Name Extraction - SAMPLE TEST (100 rows)
Tests extraction patterns before running on full 21K dataset
"""

import pandas as pd
import boto3
import re
from bs4 import BeautifulSoup
from pathlib import Path

# S3 Configuration
S3_BUCKET = 'ci-strains-html-archive'
s3_client = boto3.client('s3')

def get_s3_html(s3_key):
    """Fetch HTML from S3 with timeout"""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        return response['Body'].read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def extract_breeder_attitude(html):
    soup = BeautifulSoup(html, 'html.parser')
    breadcrumb = soup.find('div', class_='breadCrumb')
    if breadcrumb:
        link = breadcrumb.find('a', href=re.compile(r'/cat_\d+'))
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_north_atlantic(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', href=re.compile(r'/product-category/seeds/'))
    if link and 'breeder-link' in link.get('class', []):
        return link.get_text(strip=True)
    span = soup.find('span', class_='breeder-link')
    if span:
        link = span.find('a')
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_gorilla(html):
    soup = BeautifulSoup(html, 'html.parser')
    h3 = soup.find('h3', class_='product-manufacturer')
    if h3:
        link = h3.find('a', class_='white')
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_neptune(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', class_='breeder-link', href=re.compile(r'/brand/'))
    if link:
        return link.get_text(strip=True)
    return None

def extract_breeder_seedsman(html):
    soup = BeautifulSoup(html, 'html.parser')
    brand_div = soup.find('div', class_='Brand')
    if brand_div:
        link = brand_div.find('a', href=re.compile(r'/cannabis-seed-breeders/'))
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_herbies(html):
    soup = BeautifulSoup(html, 'html.parser')
    tr = soup.find('tr', title='Strain brand')
    if tr:
        link = tr.find('a', href=re.compile(r'/producers/'))
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_multiverse(html):
    soup = BeautifulSoup(html, 'html.parser')
    meta = soup.find('div', class_='product_meta')
    if meta:
        brand_span = meta.find('span', class_='posted_in', string=re.compile(r'Brand:'))
        if brand_span:
            link = brand_span.find('a', href=re.compile(r'/brand/'))
            if link:
                return link.get_text(strip=True)
    return None

def extract_breeder_seed_supreme(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='product-attribute-specs-table')
    if table:
        for tr in table.find_all('tr'):
            label = tr.find('td', class_='label', string=re.compile(r'Seedbank:'))
            if label:
                data = tr.find('td', class_='data')
                if data:
                    return data.get_text(strip=True)
    return None

def extract_breeder_ilgm(html):
    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find('span', class_='font-black', string=re.compile(r'\w+'))
    if span and 'font-display' in span.get('class', []):
        text = span.get_text(strip=True)
        text = re.sub(r'<!--.*?-->', '', text)
        if text and len(text) > 2:
            return text
    return None

def extract_breeder_seeds_here_now(html):
    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find('span', class_='last')
    if span:
        text = span.get_text(strip=True)
        if '–' in text:
            return text.split('–')[-1].strip()
    return None

def extract_breeder_great_lakes(html):
    soup = BeautifulSoup(html, 'html.parser')
    h3 = soup.find('h3')
    if h3:
        text = h3.get_text(strip=True)
        if ' - ' in text:
            return text.split(' - ')[0].strip()
    return None

def extract_breeder(seed_bank, html):
    if not html:
        return None
    
    extractors = {
        'attitude': extract_breeder_attitude,
        'north_atlantic': extract_breeder_north_atlantic,
        'gorilla': extract_breeder_gorilla,
        'neptune': extract_breeder_neptune,
        'seedsman_js': extract_breeder_seedsman,
        'herbies': extract_breeder_herbies,
        'multiverse_beans': extract_breeder_multiverse,
        'seed_supreme': extract_breeder_seed_supreme,
        'ilgm_js': extract_breeder_ilgm,
        'ilgm': extract_breeder_ilgm,
        'seeds_here_now': extract_breeder_seeds_here_now,
        'great_lakes_genetics': extract_breeder_great_lakes,
    }
    
    self_branded = {
        'crop_king': 'Crop King Seeds',
        'amsterdam': 'Amsterdam Marijuana Seeds',
        'dutch_passion': 'Dutch Passion',
        'barneys_farm': "Barney's Farm",
        'royal_queen_seeds': 'Royal Queen Seeds',
        'mephisto_genetics': 'Mephisto Genetics',
        'exotic': 'Exotic Genetix',
        'sensi_seeds': 'Sensi Seeds'
    }
    
    if seed_bank in self_branded:
        return self_branded[seed_bank]
    
    if seed_bank in extractors:
        return extractors[seed_bank](html)
    
    return None

def main():
    print("=" * 80)
    print("BREEDER EXTRACTION - SAMPLE TEST (100 rows)")
    print("=" * 80)
    
    # Load sample
    input_path = Path('../input/diverse_sample_100.csv')
    print(f"\nLoading sample from: {input_path}")
    df = pd.read_csv(input_path, encoding='latin-1', low_memory=False)
    print(f"Sample size: {len(df)} rows")
    
    # Remove missing URLs
    missing_url = df['source_url_raw'].isna() | (df['source_url_raw'] == '')
    if missing_url.sum() > 0:
        print(f"Removing {missing_url.sum()} row(s) with missing URLs")
        df = df[~missing_url].copy()
    
    df['breeder_extracted'] = None
    
    # Extract
    seed_banks = df['seed_bank'].unique()
    print(f"\nProcessing {len(seed_banks)} seed banks in sample...\n")
    
    for bank in seed_banks:
        bank_df = df[df['seed_bank'] == bank]
        print(f"{bank}: {len(bank_df)} strains", end=' ', flush=True)
        
        extracted = 0
        for idx, row in bank_df.iterrows():
            s3_key = row['s3_html_key_raw']
            html = get_s3_html(s3_key)
            breeder = extract_breeder(bank, html)
            if breeder:
                df.at[idx, 'breeder_extracted'] = breeder
                extracted += 1
        
        print(f"-> {extracted} extracted ({extracted/len(bank_df)*100:.0f}%)")
    
    # Summary
    total_extracted = df['breeder_extracted'].notna().sum()
    print(f"\n{'='*80}")
    print(f"SAMPLE TEST COMPLETE")
    print(f"{'='*80}")
    print(f"Extracted: {total_extracted} / {len(df)} ({total_extracted/len(df)*100:.1f}%)")
    
    # Show sample results
    print(f"\nSample Results:")
    print(df[['seed_bank', 'strain_name_raw', 'breeder_extracted']].head(20).to_string(index=False))
    
    # Save sample
    output_path = Path('../output/11_breeder_extracted_SAMPLE.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nSaved: {output_path}")

if __name__ == '__main__':
    main()
