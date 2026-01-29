"""Multiverse - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
import re
from extraction_helpers import *

def build_breeder_prefixes(urls):
    prefixes = {}
    for url in urls:
        slug = get_url_slug(url, 'last')
        if slug and '-' in slug:
            parts = slug.split('-')
            for i in range(1, len(parts)):
                prefix = '-'.join(parts[:i]) + '-'
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
    return [p for p, count in prefixes.items() if count >= 3]

def extract_multiverse_strain_name(url, breeder_prefixes):
    slug = get_url_slug(url, 'last')
    if not slug:
        return None
    for prefix in sorted(breeder_prefixes, key=len, reverse=True):
        if slug.startswith(prefix):
            slug = slug[len(prefix):]
            break
    slug = re.sub(r'-(strain|fem|photo|reg|pack).*$', '', slug)
    slug = re.sub(r'-(r[1-3]|s[1-3])(?=-|$)', '', slug)
    slug = re.sub(r'-ff-', '-', slug)
    name = slug_to_name(slug)
    return smart_title_case(name) if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    multiverse = df[df['seed_bank'] == 'multiverse_beans'].copy()
    breeder_prefixes = build_breeder_prefixes(multiverse['source_url_raw'])
    multiverse['strain_name_extracted'] = multiverse['source_url_raw'].apply(lambda x: extract_multiverse_strain_name(x, breeder_prefixes))
    multiverse.to_csv("../output/multiverse_extracted.csv", index=False, encoding='utf-8')
    print(f"Multiverse: {len(multiverse)} strains extracted")
