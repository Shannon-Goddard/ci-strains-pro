import pandas as pd
import sys
import os
import re
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_barneys_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Split on keywords
    keywords = ['weed-strain', 'auto-autoflower', 'autoflower-strain', 'strain']
    for keyword in keywords:
        if keyword in slug:
            slug = slug.split(keyword)[0].rstrip('-')
            break
    
    # Remove trailing numbers
    slug = re.sub(r'-\d+$', '', slug)
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/barneys_farm_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    bf_df = df[df['seed_bank'] == 'barneys_farm'].copy()
    print(f"Found {len(bf_df)} Barney's Farm strains")
    
    bf_df['strain_name_extracted'] = bf_df['source_url_raw'].apply(extract_barneys_name)
    
    os.makedirs('../output', exist_ok=True)
    bf_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(bf_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = bf_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
