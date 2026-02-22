import pandas as pd
import re

# Read CSV
df = pd.read_csv('output/strain_name_from_source_url_v2.csv', encoding='latin-1')

def extract_version(strain_name):
    if pd.isna(strain_name):
        return ''
    
    # Common version patterns
    patterns = [
        r'\b(#\d+)\b',           # #1, #2, #420
        r'\b(V\d+)\b',           # V1, V2, V3
        r'\b(\d+\.\d+)\b',       # 2.0, 3.5
        r'\b(S\d+)\b',           # S1, S2
        r'\b(BX\d+)\b',          # BX1, BX2
        r'\b(F\d+)\b',           # F1, F2, F3
        r'\b(R\d+)\b',           # R1, R2
        r'\b(IX\d+)\b',          # IX1, IX2
        r'\b(Gen\s*\d+)\b',      # Gen 1, Gen2
        r'\b(Generation\s*\d+)\b' # Generation 1
    ]
    
    versions = []
    for pattern in patterns:
        matches = re.findall(pattern, strain_name, re.IGNORECASE)
        versions.extend(matches)
    
    return ' '.join(versions) if versions else ''

df['version'] = df['strain_name_from_source_url'].apply(extract_version)

df[['strain_id', 'strain_name_from_source_url', 'version']].to_csv(
    'output/version.csv', 
    index=False, 
    encoding='latin-1'
)

print(f"Created version.csv")
print(f"Found versions: {(df['version'] != '').sum()}")
print(f"No versions: {(df['version'] == '').sum()}")
