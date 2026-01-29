import pandas as pd
import sys
import os
import re
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_seeds_here_now_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Remove common breeder suffixes
    breeders = ['barneys-farm', 'exotic-genetix', 'omuerta-genetix', 'fast-buds', 'cali-connection', 
                'cali-kush-farms', 'swamp-boys-seeds', 'top-dawg-seeds', 'skunk-house-genetics',
                'strait-a-genetics']
    for breeder in breeders:
        if slug.endswith(breeder):
            slug = slug[:-(len(breeder)+1)]  # +1 for hyphen
            break
    
    # Remove common breeder prefixes
    prefixes = ['dominion-seed-company-', 'elite-clone-seed-company-', 'thug-pug-genetics-',
                'humboldt-seed-company-', 'fast-buds-', 'elev8-seeds-', 'aficionado-seeds-']
    for prefix in prefixes:
        if slug.startswith(prefix):
            slug = slug[len(prefix):]
            break
    
    # Remove pack sizes
    slug = re.sub(r'-\d+pk$', '', slug)
    slug = re.sub(r'-reg-\d+pk$', '', slug)
    slug = re.sub(r'-fem-\d+pk$', '', slug)
    
    # Remove keywords
    slug = re.sub(r'-feminized$', '', slug)
    slug = re.sub(r'-autoflower$', '', slug)
    slug = re.sub(r'-autofem$', '', slug)
    slug = re.sub(r'-regular$', '', slug)
    slug = re.sub(r'-fem$', '', slug)
    slug = re.sub(r'-reg$', '', slug)
    slug = re.sub(r'-auto$', '', slug)
    slug = re.sub(r'-f\d+$', '', slug)
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/seeds_here_now_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    shn_df = df[df['seed_bank'] == 'seeds_here_now'].copy()
    print(f"Found {len(shn_df)} Seeds Here Now strains")
    
    shn_df['strain_name_extracted'] = shn_df['source_url_raw'].apply(extract_seeds_here_now_name)
    
    os.makedirs('../output', exist_ok=True)
    shn_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(shn_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = shn_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
