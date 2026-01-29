"""Mephisto - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
from extraction_helpers import *

def extract_mephisto_strain_name(url):
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    mephisto = df[df['seed_bank'] == 'mephisto_genetics'].copy()
    mephisto['strain_name_extracted'] = mephisto['source_url_raw'].apply(extract_mephisto_strain_name)
    mephisto.to_csv("../output/mephisto_extracted.csv", index=False, encoding='utf-8')
    print(f"Mephisto: {len(mephisto)} strains extracted")
