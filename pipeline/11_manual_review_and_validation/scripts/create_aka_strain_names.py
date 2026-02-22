import pandas as pd
import re

df = pd.read_csv('output/strain_name_from_source_url_v2.csv', encoding='latin-1')

def extract_aka(name):
    if pd.isna(name):
        return ''
    match = re.search(r'\baka\b\s+(.+)', name, re.IGNORECASE)
    return match.group(1).strip() if match else ''

df['aka_strain_names'] = df['strain_name_from_source_url'].apply(extract_aka)

df[['strain_id', 'strain_name_from_source_url', 'aka_strain_names']].to_csv(
    'output/aka_strain_names.csv', 
    index=False, 
    encoding='latin-1'
)

print(f"Created aka_strain_names.csv")
print(f"Found AKA names: {(df['aka_strain_names'] != '').sum()}")
print(f"No AKA names: {(df['aka_strain_names'] == '').sum()}")
