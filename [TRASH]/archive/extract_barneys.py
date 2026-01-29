"""Barneys - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
import re
from extraction_helpers import *

def extract_barneys_strain_name(url):
    slug = get_url_slug(url, 'second_to_last')
    if not slug:
        return None
    slug = re.sub(r'-(weed-strain|auto-autoflower-strain).*$', '', slug)
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    barneys = df[df['seed_bank'] == 'barneys_farm'].copy()
    barneys['strain_name_extracted'] = barneys['source_url_raw'].apply(extract_barneys_strain_name)
    barneys.to_csv("../output/barneys_extracted.csv", index=False, encoding='utf-8')
    print(f"Barneys: {len(barneys)} strains extracted")
