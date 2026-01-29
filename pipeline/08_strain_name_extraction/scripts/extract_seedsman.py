import pandas as pd
import sys
import os
import re
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_seedsman_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Split on keywords and take first part
    keywords = ['regular-seeds', 'auto-feminised', 'feminised-seeds', 'autoflowering-seeds', 'regular', 'auto', 'feminised', 'feminized']
    for keyword in keywords:
        if keyword in slug:
            slug = slug.split(keyword)[0].rstrip('-')
            break
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/seedsman_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    seedsman_df = df[df['seed_bank'] == 'seedsman_js'].copy()
    print(f"Found {len(seedsman_df)} Seedsman strains")
    
    seedsman_df['strain_name_extracted'] = seedsman_df['source_url_raw'].apply(extract_seedsman_name)
    
    os.makedirs('../output', exist_ok=True)
    seedsman_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(seedsman_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = seedsman_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
