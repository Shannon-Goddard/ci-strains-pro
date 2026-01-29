"""Seed Supreme - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
import re
from extraction_helpers import *

def extract_seedsupreme_strain_name(url):
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    slug = slug.replace('.html', '')
    slug = re.sub(r'-(feminized|autoflower|regular).*$', '', slug)
    slug = re.sub(r'-cannabis-seeds$', '', slug)
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    seedsupreme = df[df['seed_bank'] == 'seed_supreme'].copy()
    seedsupreme['strain_name_extracted'] = seedsupreme['source_url_raw'].apply(extract_seedsupreme_strain_name)
    seedsupreme.to_csv("../output/seedsupreme_extracted.csv", index=False, encoding='utf-8')
    print(f"Seed Supreme: {len(seedsupreme)} strains extracted")
