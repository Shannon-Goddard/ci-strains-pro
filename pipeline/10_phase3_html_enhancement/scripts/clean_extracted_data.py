#!/usr/bin/env python3
"""
Phase 3 Data Cleaning Script
Removes HTML artifacts and cleans extracted medical/terpene data

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import re
import json
from typing import List, Dict

def clean_medical_applications(medical_text: str) -> str:
    """Clean medical applications text of HTML artifacts"""
    if not medical_text or pd.isna(medical_text):
        return ""
    
    # Remove HTML tags and entities
    cleaned = re.sub(r'<[^>]+>', '', medical_text)
    cleaned = re.sub(r'&[a-zA-Z0-9#]+;', '', cleaned)
    
    # Remove partial HTML artifacts
    cleaned = re.sub(r'[<>&]', '', cleaned)
    
    # Split and clean individual applications
    applications = []
    for app in cleaned.split(','):
        app = app.strip()
        # Skip if too short, contains numbers/symbols, or common HTML words
        if (len(app) > 3 and 
            not re.search(r'\d{2,}|[{}[\]()"]', app) and
            app.lower() not in ['div', 'span', 'class', 'style', 'href', 'src', 'alt', 'title']):
            applications.append(app.title())
    
    return ', '.join(applications[:6])  # Limit to 6 clean applications

def clean_terpene_profile(terpene_json: str) -> str:
    """Clean terpene profile JSON"""
    if not terpene_json or pd.isna(terpene_json):
        return ""
    
    try:
        terpenes = json.loads(terpene_json)
        cleaned_terpenes = {}
        
        for terpene, value in terpenes.items():
            # Clean terpene name
            clean_name = re.sub(r'[<>&]', '', terpene).strip().lower()
            if clean_name in ['myrcene', 'limonene', 'pinene', 'linalool', 'caryophyllene', 'humulene', 'terpinolene', 'ocimene']:
                cleaned_terpenes[clean_name] = value
        
        return json.dumps(cleaned_terpenes) if cleaned_terpenes else ""
    except:
        return ""

def clean_harvest_window(harvest_text: str) -> str:
    """Clean harvest window text"""
    if not harvest_text or pd.isna(harvest_text):
        return ""
    
    # Remove HTML artifacts
    cleaned = re.sub(r'<[^>]+>', '', harvest_text)
    cleaned = re.sub(r'&[a-zA-Z0-9#]+;', '', cleaned)
    cleaned = re.sub(r'[<>&]', '', cleaned)
    
    # Keep only if contains month names
    if re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december|early|mid|late)', cleaned, re.IGNORECASE):
        return cleaned.strip()
    
    return ""

def main():
    """Clean the Phase 3 enhanced dataset"""
    
    # Load enhanced dataset
    input_file = '../../../cannabis_database_fixed_phase3_enhanced.csv'
    df = pd.read_csv(input_file, encoding='utf-8')
    
    print(f"Loaded {len(df)} strains for cleaning")
    
    # Clean medical applications
    print("Cleaning medical applications...")
    df['medical_applications_cleaned'] = df['medical_applications'].apply(clean_medical_applications)
    
    # Clean terpene profiles
    print("Cleaning terpene profiles...")
    df['terpene_profile_cleaned'] = df['terpene_profile_structured'].apply(clean_terpene_profile)
    
    # Clean harvest windows
    print("Cleaning harvest windows...")
    df['harvest_window_cleaned'] = df['harvest_window_outdoor'].apply(clean_harvest_window)
    
    # Calculate cleaning statistics
    stats = {
        'medical_before': (df['medical_applications'] != '').sum(),
        'medical_after': (df['medical_applications_cleaned'] != '').sum(),
        'terpene_before': (df['terpene_profile_structured'] != '').sum(),
        'terpene_after': (df['terpene_profile_cleaned'] != '').sum(),
        'harvest_before': (df['harvest_window_outdoor'] != '').sum(),
        'harvest_after': (df['harvest_window_cleaned'] != '').sum(),
    }
    
    # Save cleaned dataset
    output_file = '../../../cannabis_database_phase3_cleaned.csv'
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\nCleaning Statistics:")
    print(f"Medical Applications: {stats['medical_before']} → {stats['medical_after']} ({stats['medical_after']/stats['medical_before']*100:.1f}% retained)")
    print(f"Terpene Profiles: {stats['terpene_before']} → {stats['terpene_after']} ({stats['terpene_after']/stats['terpene_before']*100:.1f}% retained)")
    print(f"Harvest Windows: {stats['harvest_before']} → {stats['harvest_after']} ({stats['harvest_after']/stats['harvest_before']*100:.1f}% retained)")
    
    print(f"\nCleaned dataset saved: {output_file}")

if __name__ == "__main__":
    main()