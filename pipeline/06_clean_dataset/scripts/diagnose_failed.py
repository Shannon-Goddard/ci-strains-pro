import pandas as pd
import boto3
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
bucket = 'ci-strains-html'

# Load master
master = pd.read_csv('../input/master_strains_raw.csv', encoding='latin-1')

# Sample 2 URLs from each failed bank
banks = [
    ('ilgm', 'html_js/', '../../03_s3_inventory/s3_js_html_inventory.csv'),
    ('seeds_here_now', 'html/', '../../03_s3_inventory/s3_html_inventory.csv'),
    ('great_lakes_genetics', 'html/', '../../03_s3_inventory/s3_html_inventory.csv')
]

for bank_name, folder, inv_path in banks:
    print(f"\n{'='*80}")
    print(f"SEED BANK: {bank_name}")
    print(f"{'='*80}")
    
    inventory = pd.read_csv(inv_path, encoding='latin-1')
    bank_data = master[master['seed_bank'] == bank_name].head(2)
    
    for idx, row in bank_data.iterrows():
        url = row['source_url_raw']
        strain = row['strain_name_raw']
        
        print(f"\nSTRAIN: {strain}")
        print(f"URL: {url}")
        
        # Get S3 key
        key_col = 'html_key' if 'js' in folder else 's3_html_key'
        s3_key = inventory[inventory['url'] == url][key_col].values
        
        if len(s3_key) == 0:
            print("ERROR: No S3 key found")
            continue
        
        try:
            obj = s3.get_object(Bucket=bucket, Key=s3_key[0])
            html = obj['Body'].read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Search for common breeder indicators
            print("\n--- SEARCHING FOR BREEDER PATTERNS ---")
            
            # Pattern 1: Any link with "brand", "breeder", "producer"
            for keyword in ['brand', 'breeder', 'producer', 'manufacturer']:
                links = soup.find_all('a', href=lambda x: x and keyword in x.lower())
                if links:
                    print(f"\n{keyword.upper()} LINKS:")
                    for link in links[:3]:
                        print(f"  {link.get_text().strip()} -> {link.get('href')}")
            
            # Pattern 2: Meta tags
            meta = soup.find_all('meta', attrs={'property': lambda x: x and 'brand' in x.lower()})
            if meta:
                print("\nMETA TAGS:")
                for m in meta:
                    print(f"  {m.get('property')}: {m.get('content')}")
            
            # Pattern 3: Structured data (JSON-LD)
            scripts = soup.find_all('script', type='application/ld+json')
            if scripts:
                print("\nJSON-LD FOUND:")
                import json
                for script in scripts[:2]:
                    try:
                        data = json.loads(script.string)
                        if 'brand' in str(data).lower():
                            print(f"  Contains 'brand': {str(data)[:200]}...")
                    except:
                        pass
            
            # Pattern 4: Breadcrumbs
            breadcrumbs = soup.find_all(['nav', 'ol', 'ul'], class_=lambda x: x and 'breadcrumb' in x.lower())
            if breadcrumbs:
                print("\nBREADCRUMBS:")
                for bc in breadcrumbs[:2]:
                    print(f"  {bc.get_text().strip()[:200]}")
            
            # Pattern 5: Product info tables/divs
            for tag in ['table', 'div', 'dl']:
                elements = soup.find_all(tag, class_=lambda x: x and any(k in x.lower() for k in ['product', 'info', 'detail', 'spec']))
                if elements:
                    print(f"\n{tag.upper()} WITH PRODUCT INFO:")
                    for el in elements[:2]:
                        text = el.get_text().strip()[:300]
                        if any(k in text.lower() for k in ['brand', 'breeder', 'genetics', 'by ']):
                            print(f"  {text}")
                    break
            
        except Exception as e:
            print(f"ERROR: {e}")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
