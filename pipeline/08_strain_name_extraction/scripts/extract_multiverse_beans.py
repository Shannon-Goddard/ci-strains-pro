import pandas as pd
import sys
import os
import re
from collections import Counter
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_multiverse_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Remove suffixes
    keywords = ['-strain', '-fem', '-photo', '-reg', '-pack', '-auto']
    for keyword in keywords:
        if keyword in slug:
            slug = slug.split(keyword)[0]
            break
    
    # Remove generation markers (as separate words, not within names)
    slug = re.sub(r'-r\d+$', '', slug)
    slug = re.sub(r'-s\d+$', '', slug)
    slug = re.sub(r'-ff-', '-', slug)  # Remove -ff- but not ff in names
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def find_breeder_prefixes(df):
    """Find common breeder prefixes"""
    prefixes = []
    for url in df['source_url_raw']:
        if pd.isna(url):
            continue
        slug = get_url_slug(url, 'last')
        if slug:
            parts = slug.split('-')
            if len(parts) >= 3:
                prefixes.append('-'.join(parts[:2]) + '-')
                prefixes.append('-'.join(parts[:3]) + '-')
    
    counter = Counter(prefixes)
    common = [p for p, count in counter.items() if count >= 5]
    return sorted(common, key=len, reverse=True)

def find_breeder_suffixes(df):
    """Find common breeder suffixes"""
    suffixes = []
    for url in df['source_url_raw']:
        if pd.isna(url):
            continue
        slug = get_url_slug(url, 'last')
        if slug:
            parts = slug.split('-')
            if len(parts) >= 2:
                suffixes.append('-'.join(parts[-2:]))
    
    counter = Counter(suffixes)
    common = [s for s, count in counter.items() if count >= 5]
    return sorted(common, key=len, reverse=True)

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/multiverse_beans_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    mv_df = df[df['seed_bank'] == 'multiverse_beans'].copy()
    print(f"Found {len(mv_df)} Multiverse Beans strains")
    
    # Find breeders
    print("\nFinding breeder prefixes...")
    prefixes = find_breeder_prefixes(mv_df)
    print(f"Found {len(prefixes)} common prefixes")
    print("Top 15:", prefixes[:15])
    
    print("\nFinding breeder suffixes...")
    suffixes = find_breeder_suffixes(mv_df)
    print(f"Found {len(suffixes)} common suffixes")
    print("Top 15:", suffixes[:15])
    
    # Extract strain names
    mv_df['strain_name_extracted'] = mv_df['source_url_raw'].apply(extract_multiverse_name)
    
    # Remove breeder prefixes
    for breeder in prefixes:
        breeder_pattern = breeder.rstrip('-').replace('-', ' ').title()
        mv_df['strain_name_extracted'] = mv_df['strain_name_extracted'].apply(
            lambda x: x[len(breeder_pattern):].strip() if isinstance(x, str) and x.startswith(breeder_pattern) else x
        )
    
    # Remove breeder suffixes
    for breeder in suffixes:
        breeder_pattern = breeder.replace('-', ' ').title()
        mv_df['strain_name_extracted'] = mv_df['strain_name_extracted'].apply(
            lambda x: x[:-len(breeder_pattern)].strip() if isinstance(x, str) and x.endswith(breeder_pattern) else x
        )
    
    # Additional cleanup
    def clean_name(name):
        if not isinstance(name, str):
            return name
        # Remove extra keywords
        keywords = [' Autoflower Cannabis Seeds Female', ' Photoperiod Cannabis Seeds Female', 
                    ' Cannabis Seeds Female', ' Autoflower', ' Photoperiod', ' Female', ' Seeds']
        for keyword in keywords:
            name = name.replace(keyword, '')
        # Remove Auto unless at start
        if not name.startswith('Auto '):
            name = name.replace(' Auto', '')
        return name.strip()
    
    mv_df['strain_name_extracted'] = mv_df['strain_name_extracted'].apply(clean_name)
    
    # Save output
    os.makedirs('../output', exist_ok=True)
    mv_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"\nSaved {len(mv_df)} strains to {output_file}")
    
    # Show samples
    print("\nSample extractions:")
    samples = mv_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
