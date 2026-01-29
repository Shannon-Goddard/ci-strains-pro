import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_exotic_name(url):
    if pd.isna(url):
        return None
    
    # Filter out box-sets (mixed strains)
    if '/box-sets/' in url:
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    # Remove common suffixes
    import re
    name = re.sub(r'\s+Regs$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+Player Packs$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+Ltd Edition.*$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+Gen$', '', name)
    name = re.sub(r'\s+\d+$', '', name)  # Remove trailing numbers
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/exotic_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    exotic_df = df[df['seed_bank'] == 'exotic'].copy()
    print(f"Found {len(exotic_df)} Exotic Genetix strains")
    
    exotic_df['strain_name_extracted'] = exotic_df['source_url_raw'].apply(extract_exotic_name)
    
    # Filter out box-sets
    before_count = len(exotic_df)
    exotic_df = exotic_df[exotic_df['strain_name_extracted'].notna()].copy()
    after_count = len(exotic_df)
    print(f"Filtered out {before_count - after_count} box-set entries")
    
    os.makedirs('../output', exist_ok=True)
    exotic_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(exotic_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = exotic_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
