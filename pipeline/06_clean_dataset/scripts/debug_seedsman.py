import pandas as pd
import boto3
from bs4 import BeautifulSoup
import re

s3 = boto3.client('s3')
BUCKET = 'ci-strains-html-archive'

inv_js = pd.read_csv('../../pipeline/03_s3_inventory/s3_js_html_inventory.csv')
url_to_key = dict(zip(inv_js['url'], inv_js['html_key']))

url = 'https://www.seedsman.com/us-en/platinum-green-apple-candy-feminized-seeds-atl-pgac-fem'
s3_key = url_to_key.get(url)

response = s3.get_object(Bucket=BUCKET, Key=s3_key)
html = response['Body'].read().decode('utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

print("=== Searching for breeder patterns ===\n")

# Try breeder link
breeder_link = soup.find('a', href=re.compile('/breeder/', re.I))
print(f"Breeder link: {breeder_link}")

# Try all links with 'breeder' in href
all_breeder_links = soup.find_all('a', href=re.compile('breeder', re.I))
print(f"\nAll breeder links: {len(all_breeder_links)}")
for link in all_breeder_links[:3]:
    print(f"  {link.get('href')}: {link.get_text(strip=True)}")

# Try product attributes
attrs = soup.find_all('div', class_=re.compile('attribute', re.I))
print(f"\nAttribute divs: {len(attrs)}")
for attr in attrs[:5]:
    print(f"  {attr.get('class')}: {attr.get_text(strip=True)[:100]}")

# Search for "Breeder" text
breeder_text = soup.find_all(string=re.compile('Breeder', re.I))
print(f"\n'Breeder' text occurrences: {len(breeder_text)}")
for text in breeder_text[:3]:
    parent = text.parent
    print(f"  Parent: {parent.name}.{parent.get('class')}")
    print(f"  Text: {text.strip()[:100]}")
