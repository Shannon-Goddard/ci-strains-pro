"""Debug Attitude HTML structure"""
import pandas as pd
import boto3
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
BUCKET = 'ci-strains-html-archive'

# Load inventories
inv_html = pd.read_csv('../../pipeline/03_s3_inventory/s3_html_inventory.csv')
url_to_key = dict(zip(inv_html['url'], inv_html['s3_html_key']))

# Get one Attitude URL
df = pd.read_csv('../../cleaning_csv/10g_missing_url_removed.csv', encoding='latin-1', low_memory=False)
attitude_row = df[df['seed_bank'] == 'attitude'].iloc[0]
url = attitude_row['source_url_raw']

print(f"URL: {url}\n")

s3_key = url_to_key.get(url)
response = s3.get_object(Bucket=BUCKET, Key=s3_key)
html = response['Body'].read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

# Check for breadcrumbs
print("=== Breadcrumb Search ===")
breadcrumb1 = soup.find('nav', {'aria-label': 'breadcrumbs'})
print(f"nav[aria-label=breadcrumbs]: {breadcrumb1 is not None}")

breadcrumb2 = soup.find('ol', class_='breadcrumb')
print(f"ol.breadcrumb: {breadcrumb2 is not None}")

breadcrumb3 = soup.find('div', class_='breadcrumb')
print(f"div.breadcrumb: {breadcrumb3 is not None}")

# Find all elements with 'bread' in class
bread_elements = soup.find_all(class_=lambda x: x and 'bread' in x.lower())
print(f"\nElements with 'bread' in class: {len(bread_elements)}")
for elem in bread_elements[:3]:
    print(f"  {elem.name}.{elem.get('class')}: {elem.get_text(strip=True)[:100]}")

# Check for product info
print("\n=== Product Info Search ===")
product_info = soup.find('div', class_=lambda x: x and 'product' in x.lower())
if product_info:
    print(f"Found product div: {product_info.get('class')}")
    print(f"Text: {product_info.get_text(strip=True)[:200]}")
