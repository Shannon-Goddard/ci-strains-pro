import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_seed_supreme_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Remove .html extension
    slug = slug.replace('.html', '')
    
    # Split on keywords and take first part
    keywords = ['feminized-cannabis-seeds', 'autoflower-cannabis-seeds', 'regular-cannabis-seeds',
                'feminized', 'autoflower', 'regular']
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
    output_file = '../output/seed_supreme_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    ss_df = df[df['seed_bank'] == 'seed_supreme'].copy()
    print(f"Found {len(ss_df)} Seed Supreme strains")
    
    ss_df['strain_name_extracted'] = ss_df['source_url_raw'].apply(extract_seed_supreme_name)
    
    os.makedirs('../output', exist_ok=True)
    ss_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(ss_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = ss_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
