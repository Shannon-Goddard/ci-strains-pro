import pandas as pd
import sys
import os
import re
from collections import Counter
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_herbies_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Convert to name first
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def find_breeder_suffixes(df):
    """Find common breeder suffixes in URLs"""
    suffixes = []
    for url in df['source_url_raw']:
        if pd.isna(url):
            continue
        slug = get_url_slug(url, 'last')
        if slug:
            parts = slug.split('-')
            if len(parts) >= 3:
                # Get last 2-4 words as potential breeder
                suffixes.append('-'.join(parts[-2:]))
                suffixes.append('-'.join(parts[-3:]))
                if len(parts) >= 4:
                    suffixes.append('-'.join(parts[-4:]))
    
    # Find most common suffixes (appearing 5+ times)
    counter = Counter(suffixes)
    common = [s for s, count in counter.items() if count >= 5]
    return sorted(common, key=len, reverse=True)

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/herbies_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    herbies_df = df[df['seed_bank'] == 'herbies'].copy()
    print(f"Found {len(herbies_df)} Herbies strains")
    
    # Find breeder suffixes
    print("\nFinding breeder suffixes...")
    breeders = find_breeder_suffixes(herbies_df)
    print(f"Found {len(breeders)} common breeder suffixes")
    print("Top 20:", breeders[:20])
    
    # Extract strain names
    herbies_df['strain_name_extracted'] = herbies_df['source_url_raw'].apply(extract_herbies_name)
    
    # Remove breeder suffixes
    for breeder in breeders:
        breeder_pattern = breeder.replace('-', ' ').title()
        herbies_df['strain_name_extracted'] = herbies_df['strain_name_extracted'].apply(
            lambda x: x[:-len(breeder_pattern)].strip() if isinstance(x, str) and x.endswith(breeder_pattern) else x
        )
    
    # Additional cleanup
    def clean_name(name):
        if not isinstance(name, str):
            return name
        # Remove Auto/Autoflower unless at start
        if not name.startswith('Auto '):
            name = name.replace(' Autoflower', '').replace(' Auto', '')
        # Remove Fast Version
        name = name.replace(' Fast Version', '')
        # Remove common abbreviations at end
        abbrevs = [' Ghs', ' Gg', ' Fastbuds', ' Gc']
        for abbrev in abbrevs:
            if name.endswith(abbrev):
                name = name[:-len(abbrev)]
        return name.strip()
    
    herbies_df['strain_name_extracted'] = herbies_df['strain_name_extracted'].apply(clean_name)
    
    # Save output
    os.makedirs('../output', exist_ok=True)
    herbies_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"\nSaved {len(herbies_df)} strains to {output_file}")
    
    # Show samples
    print("\nSample extractions:")
    samples = herbies_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
