import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))
from extraction_helpers import get_url_slug, smart_title_case

def extract_sensi_name(url):
    if pd.isna(url):
        return None
    
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    # Convert to name
    name = slug.replace('-', ' ')
    name = smart_title_case(name)
    
    return name.strip()

def main():
    input_file = '../input/09_autoflower_classified.csv'
    output_file = '../output/sensi_seeds_extracted.csv'
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, encoding='latin-1')
    
    sensi_df = df[df['seed_bank'] == 'sensi_seeds'].copy()
    print(f"Found {len(sensi_df)} Sensi Seeds strains")
    
    sensi_df['strain_name_extracted'] = sensi_df['source_url_raw'].apply(extract_sensi_name)
    
    os.makedirs('../output', exist_ok=True)
    sensi_df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"Saved {len(sensi_df)} strains to {output_file}")
    
    print("\nSample extractions:")
    samples = sensi_df[['source_url_raw', 'strain_name_extracted']].head(20)
    for _, row in samples.iterrows():
        print(f"  {row['source_url_raw']} -> {row['strain_name_extracted']}")

if __name__ == '__main__':
    main()
