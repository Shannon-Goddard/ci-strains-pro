import pandas as pd
import sys
import os
import re
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_great_lakes_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Remove seed count and type at end (e.g., -12-reg-seeds, -3-auto-fem-seeds)
    slug = re.sub(r'-\d+-.*-seeds$', '', slug)
    slug = re.sub(r'-\d+-seeds$', '', slug)
    
    # Remove common breeder prefixes
    breeders = ['green-wolfe-seed-co-', 'night-owl-seeds-', 'satori-seeds-', 'off-grid-seeds-',
                'northern-leaf-seeds-', 'matchmaker-genetics-', 'sunny-valley-seed-co-', 
                'subcool-seeds-', 'forests-fires-', 'jaws-genetics-', 'strayfox-gardenz-',
                'tonygreens-tortured-beans-', 'bodhi-seeds-', 'backyard-boogie-', 
                'anthos-seeds-', 'twenty20-']
    
    for breeder in breeders:
        if slug.startswith(breeder):
            slug = slug[len(breeder):]
            break
    
    # Remove generation markers
    slug = re.sub(r'-f\d+$', '', slug)
    slug = re.sub(r'-bc\d+-f\d+$', '', slug, flags=re.IGNORECASE)
    slug = re.sub(r'-bc\d+$', '', slug, flags=re.IGNORECASE)
    
    # Remove extra keywords
    slug = re.sub(r'-seeds$', '', slug)
    slug = re.sub(r'-fast-auto', '', slug, flags=re.IGNORECASE)
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/great_lakes_genetics_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    gl_df = df[df['seed_bank'] == 'great_lakes_genetics'].copy()
    print(f"Found {len(gl_df)} Great Lakes Genetics strains")
    
    gl_df['strain_name_extracted'] = gl_df['source_url_raw'].apply(extract_great_lakes_name)
    
    os.makedirs('../output', exist_ok=True)
    gl_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(gl_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = gl_df[['source_url_raw', 'strain_name_extracted']]
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
