"""
Seeds Here Now - Strain Name Extraction
39 strains

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import re
from extraction_helpers import *

def build_prefix_suffix_patterns(urls):
    """Build common 2-word prefixes and suffixes"""
    prefixes = {}
    suffixes = {}
    
    for url in urls:
        slug = get_url_slug(url, 'last')
        if slug and '-' in slug:
            parts = slug.split('-')
            if len(parts) >= 2:
                prefix = '-'.join(parts[:2]) + '-'
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                
                suffix = '-' + '-'.join(parts[-2:])
                suffixes[suffix] = suffixes.get(suffix, 0) + 1
    
    return ([p for p, c in prefixes.items() if c >= 2], 
            [s for s, c in suffixes.items() if c >= 2])

def extract_seedsherenow_strain_name(url, prefixes, suffixes):
    """Extract strain name from Seeds Here Now URL"""
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    
    for prefix in sorted(prefixes, key=len, reverse=True):
        if slug.startswith(prefix):
            slug = slug[len(prefix):]
            break
    
    for suffix in sorted(suffixes, key=len, reverse=True):
        if slug.endswith(suffix):
            slug = slug[:-len(suffix)]
            break
    
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    shn = df[df['seed_bank'] == 'seeds_here_now'].copy()
    
    prefixes, suffixes = build_prefix_suffix_patterns(shn['source_url_raw'])
    shn['strain_name_extracted'] = shn['source_url_raw'].apply(lambda x: extract_seedsherenow_strain_name(x, prefixes, suffixes))
    
    shn.to_csv("../output/seedsherenow_extracted.csv", index=False, encoding='utf-8')
    print(f"Seeds Here Now: {len(shn)} strains extracted")
