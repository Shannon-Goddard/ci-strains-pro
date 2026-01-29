"""
Great Lakes Genetics - Strain Name Extraction
16 strains

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import re
from extraction_helpers import *

def extract_greatlakes_strain_name(url):
    """Extract strain name from Great Lakes URL - manual review needed"""
    slug = get_url_slug(url, 'second_to_last')
    if not slug:
        return None
    
    slug = re.sub(r'-(seeds?|f\d+|reg)(?=-|$)', '', slug)
    slug = re.sub(r'^\d+-', '', slug)
    
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    greatlakes = df[df['seed_bank'] == 'great_lakes_genetics'].copy()
    
    greatlakes['strain_name_extracted'] = greatlakes['source_url_raw'].apply(extract_greatlakes_strain_name)
    
    greatlakes.to_csv("../output/greatlakes_extracted.csv", index=False, encoding='utf-8')
    print(f"Great Lakes: {len(greatlakes)} strains extracted (manual review recommended)")
