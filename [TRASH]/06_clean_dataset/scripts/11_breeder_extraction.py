"""
Breeder Name Extraction from S3 HTML Files
Extracts breeder names using seed-bank-specific patterns documented in BREEDER_EXTRACTION_PATTERNS.md
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
    """Attitude: <a href="/breeder-slug/cat_XXX">Breeder Name</a> in breadcrumb"""
    soup = BeautifulSoup(html, 'html.parser')
    breadcrumb = soup.find('div', class_='breadCrumb')
    if breadcrumb:
        link = breadcrumb.find('a', href=re.compile(r'/cat_\d+'))
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_north_atlantic(html):
    """North Atlantic: <a href=".../product-category/seeds/breeder/">Breeder</a>"""
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', href=re.compile(r'/product-category/seeds/'))
    if link and 'breeder-link' in link.get('class', []):
        return link.get_text(strip=True)
    # Fallback: look for span.breeder-link
    span = soup.find('span', class_='breeder-link')
    if span:
        link = span.find('a')
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_gorilla(html):
    """Gorilla: <a href="/breeder-slug" title="Breeder" class="white">Breeder</a>"""
    soup = BeautifulSoup(html, 'html.parser')
    h3 = soup.find('h3', class_='product-manufacturer')
    if h3:
        link = h3.find('a', class_='white')
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_neptune(html):
    """Neptune: <a href=".../brand/breeder/" class="breeder-link">Breeder</a>"""
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', class_='breeder-link', href=re.compile(r'/brand/'))
    if link:
        return link.get_text(strip=True)
    return None

def extract_breeder_seedsman(html):
    """Seedsman JS: <a href=".../cannabis-seed-breeders/breeder">Breeder</a> in div.Brand"""
    soup = BeautifulSoup(html, 'html.parser')
    brand_div = soup.find('div', class_='Brand')
    if brand_div:
        link = brand_div.find('a', href=re.compile(r'/cannabis-seed-breeders/'))
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_herbies(html):
    """Herbies: <a href=".../producers/breeder">Breeder</a> in properties-list"""
    soup = BeautifulSoup(html, 'html.parser')
    tr = soup.find('tr', title='Strain brand')
    if tr:
        link = tr.find('a', href=re.compile(r'/producers/'))
        if link:
            return link.get_text(strip=True)
    return None

def extract_breeder_multiverse(html):
    """Multiverse: <a href=".../brand/breeder/" rel="tag">Breeder</a>"""
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
    """Seed Supreme: <td class="col data">Seed Supreme</td> after Seedbank label"""
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
    """ILGM JS: <span class="group font-display text-display-xs font-black">Breeder</span>"""
    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find('span', class_='font-black', string=re.compile(r'\w+'))
    if span and 'font-display' in span.get('class', []):
        text = span.get_text(strip=True)
        # Remove HTML comments
        text = re.sub(r'<!--.*?-->', '', text)
        if text and len(text) > 2:
            return text
    return None

def extract_breeder_seeds_here_now(html):
    """Seeds Here Now: <span class="last">Strain – Breeder</span>"""
    soup = BeautifulSoup(html, 'html.parser')
    span = soup.find('span', class_='last')
    if span:
        text = span.get_text(strip=True)
        # Extract text after "–"
        if '–' in text:
            return text.split('–')[-1].strip()
    return None

def extract_breeder_great_lakes(html):
    """Great Lakes: <h3>Breeder - Strain</h3>"""
    soup = BeautifulSoup(html, 'html.parser')
    h3 = soup.find('h3')
    if h3:
        text = h3.get_text(strip=True)
        # Extract text before " - "
        if ' - ' in text:
            return text.split(' - ')[0].strip()
    return None

def extract_breeder(seed_bank, html):
    """Route to appropriate extraction function"""
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
    print("BREEDER NAME EXTRACTION")
    print("=" * 80)
    
    # Load dataset
    input_path = Path('../../../cleaning_csv/10d_categorical_standardized.csv')
    print(f"\nLoading: {input_path}")
    df = pd.read_csv(input_path, encoding='latin-1', low_memory=False)
    print(f"Total rows: {len(df):,}")
    
    # Remove missing URL row
    missing_url = df['source_url_raw'].isna() | (df['source_url_raw'] == '')
    if missing_url.sum() > 0:
        print(f"\nRemoving {missing_url.sum()} row(s) with missing URLs")
        df = df[~missing_url].copy()
    
    # Add breeder column
    df['breeder_extracted'] = None
    
    # Extract by seed bank
    seed_banks = df['seed_bank'].unique()
    print(f"\nProcessing {len(seed_banks)} seed banks...")
    print("NOTE: S3 fetching may take 10-15 minutes for 21K+ strains\n")
    
    total_processed = 0
    for bank in seed_banks:
        bank_df = df[df['seed_bank'] == bank]
        print(f"{bank}: {len(bank_df):,} strains", end=' ', flush=True)
        
        extracted = 0
        for i, (idx, row) in enumerate(bank_df.iterrows()):
            # Progress indicator every 500 rows
            if i > 0 and i % 500 == 0:
                print(f"[{i}/{len(bank_df)}]", end=' ', flush=True)
            
            s3_key = row['s3_html_key_raw']
            html = get_s3_html(s3_key)
            breeder = extract_breeder(bank, html)
            if breeder:
                df.at[idx, 'breeder_extracted'] = breeder
                extracted += 1
            
            total_processed += 1
        
        print(f"-> {extracted:,} extracted ({extracted/len(bank_df)*100:.1f}%)")
    
    # Summary
    total_extracted = df['breeder_extracted'].notna().sum()
    print(f"\n{'='*80}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*80}")
    print(f"Total extracted: {total_extracted:,} / {len(df):,} ({total_extracted/len(df)*100:.1f}%)")
    
    # Save
    output_path = Path('../output/11_breeder_extracted.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nSaved: {output_path}")
    
    # Report
    report_path = Path('../output/11_breeder_extraction_report.txt')
    with open(report_path, 'w') as f:
        f.write("BREEDER EXTRACTION REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total rows processed: {len(df):,}\n")
        f.write(f"Total extracted: {total_extracted:,} ({total_extracted/len(df)*100:.1f}%)\n\n")
        f.write("BY SEED BANK:\n")
        f.write("-" * 80 + "\n")
        for bank in sorted(seed_banks):
            bank_df = df[df['seed_bank'] == bank]
            extracted = bank_df['breeder_extracted'].notna().sum()
            f.write(f"{bank:25} {extracted:6,} / {len(bank_df):6,} ({extracted/len(bank_df)*100:5.1f}%)\n")
    
    print(f"Report: {report_path}")

if __name__ == '__main__':
    main()
