import boto3, pandas as pd

s3 = boto3.client('s3')
inv = pd.read_csv('c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/03_s3_inventory/s3_html_inventory.csv', encoding='latin-1')
seedsman = inv[inv['url'].str.contains('seedsman.com', na=False)].iloc[0]

obj = s3.get_object(Bucket='ci-strains-html-archive', Key=f'html/{seedsman["url_hash"]}.html')
html = obj['Body'].read().decode('utf-8')

print(f'URL: {seedsman["url"]}')
print(f'HTML length: {len(html)}')
print(f'Has table: {"<table" in html}')
print(f'Has ScandiPWA: {"ScandiPWA" in html}')
print(f'Has product schema: {"@type" in html and "Product" in html}')
print(f'\nFirst 1000 chars:')
print(html[:1000])
