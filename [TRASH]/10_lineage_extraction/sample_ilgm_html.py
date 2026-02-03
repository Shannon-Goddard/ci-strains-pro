import boto3
from bs4 import BeautifulSoup

s3 = boto3.client('s3')
obj = s3.get_object(Bucket='ci-strains-html-archive', Key='html/0017fbd840f2539f.html')
html = obj['Body'].read().decode('utf-8')

# Check if "Lineage" appears anywhere
if 'Lineage' in html or 'lineage' in html:
    print("'Lineage' found in HTML")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all text containing lineage
    for tag in soup.find_all(string=lambda text: text and 'lineage' in text.lower()):
        parent = tag.parent
        print(f"\nTag: {parent.name}, Class: {parent.get('class')}")
        print(f"Text: {tag[:100]}")
        print(f"Parent HTML: {str(parent)[:200]}")
else:
    print("'Lineage' NOT found in HTML - ILGM static HTML may not contain lineage data")
