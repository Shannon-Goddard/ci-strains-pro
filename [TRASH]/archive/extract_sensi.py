"""Sensi - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
from extraction_helpers import *

def extract_sensi_strain_name(url):
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    sensi = df[df['seed_bank'] == 'sensi_seeds'].copy()
    sensi['strain_name_extracted'] = sensi['source_url_raw'].apply(extract_sensi_strain_name)
    sensi.to_csv("../output/sensi_extracted.csv", index=False, encoding='utf-8')
    print(f"Sensi: {len(sensi)} strains extracted")
