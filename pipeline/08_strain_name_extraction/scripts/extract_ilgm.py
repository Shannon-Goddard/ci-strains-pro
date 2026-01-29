import pandas as pd
import sys
import os
import re
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_ilgm_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Remove seed suffixes
    suffixes = ['-feminized-seeds', '-autoflower-seeds', '-seeds']
    for suffix in suffixes:
        if slug.endswith(suffix):
            slug = slug[:-len(suffix)]
            break
    
    # Remove generation markers like f5
    slug = re.sub(r'-f\d+$', '', slug)
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/ilgm_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    ilgm_df = df[df['seed_bank'] == 'ilgm'].copy()
    print(f"Found {len(ilgm_df)} ILGM strains")
    
    ilgm_df['strain_name_extracted'] = ilgm_df['source_url_raw'].apply(extract_ilgm_name)
    
    os.makedirs('../output', exist_ok=True)
    ilgm_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(ilgm_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = ilgm_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
