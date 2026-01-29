import pandas as pd
import sys
import os
import re
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_royal_queen_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Remove .html extension
    slug = slug.replace('.html', '')
    
    # Remove 3-digit number prefix
    slug = re.sub(r'^\d{3}-', '', slug)
    
    # Remove automatic suffix
    slug = re.sub(r'-automatic$', '', slug)
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/royal_queen_seeds_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    rqs_df = df[df['seed_bank'] == 'royal_queen_seeds'].copy()
    print(f"Found {len(rqs_df)} Royal Queen Seeds strains")
    
    rqs_df['strain_name_extracted'] = rqs_df['source_url_raw'].apply(extract_royal_queen_name)
    
    os.makedirs('../output', exist_ok=True)
    rqs_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(rqs_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = rqs_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
