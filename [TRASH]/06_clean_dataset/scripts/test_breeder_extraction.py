"""Test breeder extraction on small sample"""
import pandas as pd
import boto3
import re
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
BUCKET = 'ci-strains-html-archive'

# Load inventories
inv_html = pd.read_csv('../../pipeline/03_s3_inventory/s3_html_inventory.csv')
inv_js = pd.read_csv('../../pipeline/03_s3_inventory/s3_js_html_inventory.csv')
url_to_key = dict(zip(inv_html['url'], inv_html['s3_html_key']))
url_to_key.update(dict(zip(inv_js['url'], inv_js['html_key'])))

# Load dataset
df = pd.read_csv('../../cleaning_csv/10g_missing_url_removed.csv', encoding='latin-1', low_memory=False)

# Test on 5 rows per seed bank
test_banks = ['attitude', 'multiverse_beans', 'seed_supreme', 'amsterdam', 'seeds_here_now', 'ilgm', 'seedsman_js']
test_rows = []
for bank in test_banks:
    bank_rows = df[df['seed_bank'] == bank].head(5)
    test_rows.append(bank_rows)

test_df = pd.concat(test_rows)
print(f"Testing on {len(test_df)} rows across {len(test_banks)} seed banks\n")

def extract_breeder(html, seed_bank):
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    
    # Self-branded
    if seed_bank == 'amsterdam':
        return 'Amsterdam Marijuana Seeds'
    elif seed_bank == 'dutch_passion':
        return 'Dutch Passion'
    elif seed_bank == 'barneys_farm':
        return "Barney's Farm"
    elif seed_bank == 'royal_queen_seeds':
        return 'Royal Queen Seeds'
    
    # Breadcrumb
    elif seed_bank in ['attitude', 'crop_king', 'north_atlantic', 'gorilla', 'neptune', 
                       'herbies', 'sensi_seeds', 'mephisto_genetics', 'exotic']:
        breadcrumb = soup.find('nav', {'aria-label': 'breadcrumbs'}) or \
                    soup.find('ol', class_=re.compile('breadcrumb', re.I)) or \
                    soup.find('div', class_=re.compile('breadcrumb', re.I))
        if breadcrumb:
            text = breadcrumb.get_text(strip=True)
            parts = [p.strip() for p in text.split('>')]
            for part in parts:
                if part.lower() not in ['home', 'shop', 'products', 'seeds', 'strains', 'cannabis', '']:
                    return part
    
    # Seeds Here Now
    elif seed_bank == 'seeds_here_now':
        last_span = soup.find('span', class_='last')
        if last_span:
            text = last_span.get_text(strip=True)
            if '–' in text:
                return text.split('–')[-1].strip()
    
    # Great Lakes
    elif seed_bank == 'great_lakes_genetics':
        h3 = soup.find('h3')
        if h3:
            text = h3.get_text(strip=True)
            if ' - ' in text:
                return text.split(' - ')[0].strip()
    
    # Multiverse
    elif seed_bank == 'multiverse_beans':
        brand_spans = soup.find_all('span', class_='posted_in')
        for span in brand_spans:
            if 'Brand:' in span.get_text():
                link = span.find('a')
                if link:
                    return link.get_text(strip=True)
    
    # Seed Supreme
    elif seed_bank == 'seed_supreme':
        table = soup.find('table', id='product-attribute-specs-table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                for i, cell in enumerate(cells):
                    if 'Seedbank:' in cell.get_text():
                        if i + 1 < len(cells):
                            breeder = cells[i + 1].get_text(strip=True)
                            if breeder != 'Seed Supreme':
                                return breeder
        return 'Seed Supreme'
    
    # ILGM
    elif seed_bank == 'ilgm':
        span = soup.find('span', class_=re.compile('font-display.*font-black', re.I))
        if span:
            text = span.get_text(strip=True)
            text = re.sub(r'<!--.*?-->', '', text)
            return text if text else None
    
    # Seedsman
    elif seed_bank == 'seedsman_js':
        breeder_link = soup.find('a', href=re.compile('/breeder/', re.I))
        if breeder_link:
            return breeder_link.get_text(strip=True)
    
    return None

# Test extraction
for idx, row in test_df.iterrows():
    url = row['source_url_raw']
    seed_bank = row['seed_bank']
    
    s3_key = url_to_key.get(url)
    if not s3_key:
        print(f"ERROR {seed_bank}: No S3 key")
        continue
    
    try:
        response = s3.get_object(Bucket=BUCKET, Key=s3_key)
        html = response['Body'].read().decode('utf-8', errors='ignore')
        breeder = extract_breeder(html, seed_bank)
        
        if breeder:
            print(f"OK {seed_bank}: {breeder}")
        else:
            print(f"WARN {seed_bank}: No breeder found")
    except Exception as e:
        print(f"ERROR {seed_bank}: {str(e)[:50]}")
