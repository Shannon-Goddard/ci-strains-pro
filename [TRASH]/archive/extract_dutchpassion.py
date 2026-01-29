"""Dutch Passion - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
import re
from extraction_helpers import *

def extract_dutchpassion_strain_name(url):
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    slug = re.sub(r'^auto-', '', slug)
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    dutch = df[df['seed_bank'] == 'dutch_passion'].copy()
    dutch['strain_name_extracted'] = dutch['source_url_raw'].apply(extract_dutchpassion_strain_name)
    dutch.to_csv("../output/dutchpassion_extracted.csv", index=False, encoding='utf-8')
    print(f"Dutch Passion: {len(dutch)} strains extracted")
