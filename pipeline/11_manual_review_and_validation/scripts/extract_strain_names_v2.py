import pandas as pd
import re
from urllib.parse import urlparse

df = pd.read_csv('output/pipeline_11_clean.csv', encoding='latin-1')

def extract_strain_name(url):
    if pd.isna(url):
        return ''
    
    domain = urlparse(url).netloc
    path = urlparse(url).path
    
    # Amsterdam Marijuana Seeds
    if 'amsterdammarijuanaseeds.com' in domain:
        match = re.search(r'/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Barney's Farm
    elif 'barneysfarm.com' in domain:
        match = re.search(r'/([^/]+?)-\d+/?$', path)
        if match:
            return match.group(1).replace('-', ' ').title()
        match = re.search(r'/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Crop King Seeds
    elif 'cropkingseeds.com' in domain:
        match = re.search(r'/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Dutch Passion
    elif 'dutch-passion.us' in domain:
        match = re.search(r'/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Exotic Genetix
    elif 'exoticgenetix.com' in domain:
        match = re.search(r'/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Gorilla Cannabis Seeds
    elif 'gorilla-cannabis-seeds.co.uk' in domain:
        match = re.search(r'/([^/]+?)\.html', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Great Lakes Genetics
    elif 'greatlakesgenetics.com' in domain:
        match = re.search(r'/product/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Herbies Head Shop
    elif 'herbiesheadshop.com' in domain:
        match = re.search(r'/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # ILGM
    elif 'ilgm.com' in domain:
        match = re.search(r'/products/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Mephisto Genetics
    elif 'mephistogenetics.com' in domain:
        match = re.search(r'/products/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Multiverse Beans
    elif 'multiversebeans.com' in domain:
        match = re.search(r'/product/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Neptune Seed Bank
    elif 'neptuneseedbank.com' in domain:
        match = re.search(r'/product/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # North Atlantic Seed
    elif 'northatlanticseed.com' in domain:
        match = re.search(r'/product/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Royal Queen Seeds
    elif 'royalqueenseeds.com' in domain:
        match = re.search(r'/\d+-([^/]+?)\.html', path)
        if match:
            return match.group(1).replace('-', ' ').title()
        match = re.search(r'/([^/]+?)\.html', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Seed Supreme
    elif 'seedsupreme.com' in domain:
        match = re.search(r'/([^/]+?)\.html', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Seeds Here Now
    elif 'seedsherenow.com' in domain:
        match = re.search(r'/shop/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Seedsman
    elif 'seedsman.com' in domain:
        match = re.search(r'/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Sensi Seeds
    elif 'sensiseeds.us' in domain:
        match = re.search(r'/([^/]+?)/?$', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Cannabis Seeds Bank
    elif 'cannabis-seeds-bank.co.uk' in domain:
        match = re.search(r'/([^/]+?)/prod_\d+', path)
        return match.group(1).replace('-', ' ').title() if match else ''
    
    # Fallback
    match = re.search(r'/([^/]+?)/?$', path)
    return match.group(1).replace('-', ' ').title() if match else ''

df['strain_name_from_source_url'] = df['source_url_raw'].apply(extract_strain_name)

df[['strain_id', 'source_url_raw', 'strain_name_from_source_url']].to_csv(
    'output/strain_name_from_source_url_v2.csv', 
    index=False, 
    encoding='latin-1'
)

print(f"Processed {len(df)} rows")
print(f"Output saved to: output/strain_name_from_source_url_v2.csv")
