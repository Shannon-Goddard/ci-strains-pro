"""Gorilla - Strain Name Extraction
Logic designed by Amazon Q, verified by Shannon Goddard."""
import pandas as pd
import re
from extraction_helpers import *

def extract_gorilla_strain_name(raw_name):
    if not raw_name or str(raw_name) == 'nan':
        return None
    
    name = str(raw_name)
    
    # Remove keywords
    name = re.sub(r'\s+(Feminized|Feminised|Autoflowering|Autoflower|Fast Flowering|Regular)\s+(Cannabis\s+)?Seeds?', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+(Feminized|Feminised|Autoflowering|Autoflower|Fast Flowering|Regular|Cannabis Seeds|Early Version|Automatic)$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+Auto(?!\s+CBD)$', '', name, flags=re.IGNORECASE)  # Remove Auto at end unless followed by CBD
    
    # Handle aka names - keep the aka
    # "Night Night (aka Kali's Lullaby)" stays as is
    # "818 Headband Aka Sour OG" stays as is
    
    name = ' '.join(name.split()).strip()
    return name if name else None

if __name__ == "__main__":
    df = pd.read_csv("../input/09_autoflower_classified.csv", encoding='latin-1', low_memory=False)
    gorilla = df[df['seed_bank'] == 'gorilla'].copy()
    gorilla['strain_name_extracted'] = gorilla['strain_name_raw'].apply(extract_gorilla_strain_name)
    gorilla.to_csv("../output/gorilla_extracted.csv", index=False, encoding='utf-8')
    print(f"Gorilla: {len(gorilla)} strains extracted")
