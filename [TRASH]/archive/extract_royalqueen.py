"""Royal Queen - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
import re
from extraction_helpers import *

def extract_royalqueen_strain_name(url):
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    slug = slug.replace('.html', '')
    slug = re.sub(r'^\d{3}-', '', slug)
    slug = re.sub(r'-automatic$', '', slug)
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    royal = df[df['seed_bank'] == 'royal_queen_seeds'].copy()
    royal['strain_name_extracted'] = royal['source_url_raw'].apply(extract_royalqueen_strain_name)
    royal.to_csv("../output/royalqueen_extracted.csv", index=False, encoding='utf-8')
    print(f"Royal Queen: {len(royal)} strains extracted")
