"""Crop King - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
import re
from extraction_helpers import *

def extract_cropking_strain_name(url):
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    slug = re.sub(r'-(strain|feminized|autoflowering|marijuana|seeds?|fast-version)(?=-|$)', '', slug)
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    cropking = df[df['seed_bank'] == 'crop_king'].copy()
    cropking['strain_name_extracted'] = cropking['source_url_raw'].apply(extract_cropking_strain_name)
    cropking.to_csv("../output/cropking_extracted.csv", index=False, encoding='utf-8')
    print(f"Crop King: {len(cropking)} strains extracted")
