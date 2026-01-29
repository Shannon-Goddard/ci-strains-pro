import pandas as pd
import sys
import os
import re
from collections import Counter
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_neptune_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Remove "-strain" suffix
    if slug.endswith('-strain'):
        slug = slug[:-7]
    
    # Remove generation markers at end: f, f-2, f2, etc.
    slug = re.sub(r'-f-?\d+$', '', slug)
    slug = re.sub(r'-f$', '', slug)
    slug = re.sub(r'-s\d+$', '', slug)
    slug = re.sub(r'-bx\d+$', '', slug, flags=re.IGNORECASE)
    
    # Remove pack sizes
    slug = re.sub(r'-\d+pack$', '', slug)
    slug = re.sub(r'-\d+-pack$', '', slug)
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    # Remove pack sizes from name
    name = re.sub(r'\s+\d+\s*Pack$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+\d+Pk$', '', name, flags=re.IGNORECASE)
    
    # Remove "Strain Seeds" and similar
    name = re.sub(r'\s+Strain\s+Seeds$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+Seeds$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+Genetics$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+Pre\s+Sale$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+Freebie$', '', name, flags=re.IGNORECASE)
    
    # Remove "Auto" unless at start
    if not name.startswith('Auto '):
        name = name.replace(' Auto', '')
    
    return name.strip()

def find_breeder_prefixes(df):
    """Find common breeder prefixes in URLs"""
    prefixes = []
    for url in df['source_url_raw']:
        if pd.isna(url):
            continue
        slug = get_url_slug(url, 'last')
        if slug and not slug.endswith('-strain'):
            # Get first 2-4 words as potential breeder
            parts = slug.split('-')
            if len(parts) >= 3:
                prefixes.append('-'.join(parts[:2]) + '-')
                prefixes.append('-'.join(parts[:3]) + '-')
    
    # Find most common prefixes (appearing 5+ times)
    counter = Counter(prefixes)
    common = [p for p, count in counter.items() if count >= 5]
    return sorted(common, key=len, reverse=True)

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/neptune_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    neptune_df = df[df['seed_bank'] == 'neptune'].copy()
    print(f"Found {len(neptune_df)} Neptune strains")
    
    # Find breeder prefixes
    print("\nFinding breeder prefixes...")
    breeders = find_breeder_prefixes(neptune_df)
    print(f"Found {len(breeders)} common breeder prefixes")
    print("Top 20:", breeders[:20])
    
    # Extract strain names
    neptune_df['strain_name_extracted'] = neptune_df['source_url_raw'].apply(extract_neptune_name)
    
    # Remove breeder prefixes
    for breeder in breeders:
        breeder_pattern = breeder.rstrip('-').replace('-', ' ')
        neptune_df['strain_name_extracted'] = neptune_df['strain_name_extracted'].apply(
            lambda x: x.replace(breeder_pattern.title() + ' ', '') if isinstance(x, str) and x.startswith(breeder_pattern.title()) else x
        )
    
    # Save output
    os.makedirs('../output', exist_ok=True)
    neptune_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"\nSaved {len(neptune_df)} strains to {output_file}")
    
    # Show samples
    print("\nSample extractions:")
    samples = neptune_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
