import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_north_atlantic_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Remove everything after '-drop'
    if '-drop' in slug:
        slug = slug.split('-drop')[0]
    
    # Remove suffixes (only at end)
    suffixes = ['-auto', '-fem', '-feminized', '-regular']
    for suffix in suffixes:
        if slug.endswith(suffix):
            slug = slug[:-len(suffix)]
            break
    
    # Remove single '-f' at end (but not if part of word)
    if slug.endswith('-f'):
        slug = slug[:-2]
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    # Remove generation markers at end
    import re
    name = re.sub(r'\s+[RSF]\d+$', '', name)
    name = re.sub(r'\s+[RSF]$', '', name)
    
    # Remove shipping/presale/tester info
    keywords = ['Ships Late', 'Ships Mid', 'Ships Early', 'Presale', 'Flimited', 'Limited', 'Tester', 'Edition', 'Coming Soon']
    for keyword in keywords:
        if keyword in name:
            name = name.split(keyword)[0]
    
    # Remove date/number patterns from drops
    name = re.sub(r'\s+\d+\s+\d+.*$', '', name)
    name = re.sub(r'\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}.*$', '', name, flags=re.IGNORECASE)
    
    # Remove "Auto" unless at start
    if not name.startswith('Auto '):
        name = name.replace(' Auto ', ' ').replace(' Auto', '')
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/north_atlantic_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    # Filter North Atlantic strains
    na_df = df[df['seed_bank'] == 'north_atlantic'].copy()
    print(f"Found {len(na_df)} North Atlantic strains")
    
    # Extract strain names
    na_df['strain_name_extracted'] = na_df['source_url_raw'].apply(extract_north_atlantic_name)
    
    # Save output
    os.makedirs('../output', exist_ok=True)
    na_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(na_df)} strains to {output_file}")
    
    # Show samples
    print("\nSample extractions:")
    samples = na_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
