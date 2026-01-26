"""
Step 11: Breeder Name Extraction from S3 HTML
Extracts breeder names using seed-bank-specific patterns.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd
import boto3
import re
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
BUCKET = 'ci-strains-html-archive'

print("Loading S3 inventories...")
inv_html = pd.read_csv('../../pipeline/03_s3_inventory/s3_html_inventory.csv')
inv_js = pd.read_csv('../../pipeline/03_s3_inventory/s3_js_html_inventory.csv')
url_to_key = dict(zip(inv_html['url'], inv_html['s3_html_key']))
url_to_key.update(dict(zip(inv_js['url'], inv_js['html_key'])))
print(f"Loaded {len(url_to_key)} URL mappings")

def get_s3_html(url):
    try:
        s3_key = url_to_key.get(url)
        if not s3_key:
            return None
        response = s3.get_object(Bucket=BUCKET, Key=s3_key)
        return response['Body'].read().decode('utf-8', errors='ignore')
    except:
        return None

def extract_breeder(html, seed_bank):
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    
    # Self-branded (bank = breeder)
    if seed_bank == 'amsterdam':
        return 'Amsterdam Marijuana Seeds'
    elif seed_bank == 'dutch_passion':
        return 'Dutch Passion'
    elif seed_bank == 'barneys_farm':
        return "Barney's Farm"
    elif seed_bank == 'royal_queen_seeds':
        return 'Royal Queen Seeds'
    
    # Breadcrumb extraction
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
    
    # Seeds Here Now - breadcrumb with dash separator
    elif seed_bank == 'seeds_here_now':
        last_span = soup.find('span', class_='last')
        if last_span:
            text = last_span.get_text(strip=True)
            if '–' in text:
                return text.split('–')[-1].strip()
    
    # Great Lakes - h3 with dash separator
    elif seed_bank == 'great_lakes_genetics':
        h3 = soup.find('h3')
        if h3:
            text = h3.get_text(strip=True)
            if ' - ' in text:
                return text.split(' - ')[0].strip()
    
    # Multiverse - Brand tag
    elif seed_bank == 'multiverse_beans':
        brand_spans = soup.find_all('span', class_='posted_in')
        for span in brand_spans:
            if 'Brand:' in span.get_text():
                link = span.find('a')
                if link:
                    return link.get_text(strip=True)
    
    # Seed Supreme - Seedbank table value
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
    
    # ILGM - JS-rendered span
    elif seed_bank == 'ilgm':
        span = soup.find('span', class_=re.compile('font-display.*font-black', re.I))
        if span:
            text = span.get_text(strip=True)
            text = re.sub(r'<!--.*?-->', '', text)
            return text if text else None
    
    # Seedsman - breeder link (skip for now, low success rate)
    elif seed_bank == 'seedsman_js':
        breeder_link = soup.find('a', href=re.compile('/breeder/', re.I))
        if breeder_link:
            return breeder_link.get_text(strip=True)
    
    return None

# Load dataset
print("\nLoading dataset...")
df = pd.read_csv('../../cleaning_csv/10g_missing_url_removed.csv', encoding='latin-1', low_memory=False)
print(f"Total rows: {len(df)}")

# Create new column
df['breeder_name_extracted'] = None

# Extract for all rows
extracted = 0
failed = 0
skipped = 0

print("\nExtracting breeders...")
for idx in df.index:
    url = df.at[idx, 'source_url_raw']
    seed_bank = df.at[idx, 'seed_bank']
    
    html = get_s3_html(url)
    if not html:
        skipped += 1
        continue
    
    breeder = extract_breeder(html, seed_bank)
    
    if breeder:
        df.at[idx, 'breeder_name_extracted'] = breeder
        extracted += 1
    else:
        failed += 1
    
    if (extracted + failed + skipped) % 500 == 0:
        print(f"Processed: {extracted + failed + skipped}, Extracted: {extracted}, Failed: {failed}, Skipped: {skipped}")

print(f"\nExtraction complete:")
print(f"  Extracted: {extracted}")
print(f"  Failed: {failed}")
print(f"  Skipped: {skipped}")
print(f"  Success rate: {extracted/(extracted+failed)*100:.1f}%")

# Save
df.to_csv('../../cleaning_csv/11_breeder_extracted.csv', index=False, encoding='utf-8')
df.head(100).to_csv('output/11_breeder_extracted_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: {len(df)} rows -> ../../cleaning_csv/11_breeder_extracted.csv")
