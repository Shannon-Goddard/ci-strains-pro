"""
Step 10E: Breeder Name Standardization
Standardizes breeder names based on Shannon's QA findings.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd

# Read input
df = pd.read_csv('../../cleaning_csv/10d_categorical_standardized.csv', encoding='latin-1', low_memory=False)
print(f"Input: {len(df)} rows")

# Standardization mapping (from BREEDER_EXTRACTION_FAILURES.md)
BREEDER_STANDARDIZATION = {
    # Suffix removals
    'Feminised Seeds Company': 'Feminised Seeds',
    'G13 Labs Seeds': 'G13 Labs',
    'Green Bodhi Seeds': 'Green Bodhi',
    'LIT Farms Seeds': 'LIT Farms',
    "Lovin' In Her Eyes Seeds": "Lovin' In Her Eyes",
    'Massive Creations Seeds': 'Massive Creations',
    'Offensive Selections Seeds': 'Offensive Selections',
    'Rare Dankness Seeds': 'Rare Dankness',
    'Seedsman Seeds': 'Seedsman',
    'SuperCBDx Seeds': 'SuperCBDx',
    'TH Seeds Seeds': 'TH Seeds',
    
    # Suffix additions
    'Geist Grow': 'Geist Grow Genetics',
    'Grandiflora': 'Grandiflora Genetics',
    
    # Name variations
    'Greenhouse - Strain Hunters': 'Greenhouse Seed Co.',
    'GrowersChoice': 'Growers Choice Seeds',
    'Haute Genetics': 'Haute Genetique',
    'Humboldt': 'Humboldt Seed Organization',
    'Humboldt Seed Co.': 'Humboldt Seed Co',
    'Humboldt Seed Company': 'Humboldt Seed Co',
    'Humboldt Seeds REGULAR': 'Humboldt Seeds',
    'Jaws Gear': 'Jaws Genetics',
    'Katsu Seeds': 'Katsu Bluebird Seeds',
    'Lit Farms': 'LIT Farms',
    'Lovin In Her Eyes': "Lovin' In Her Eyes",
    'Mephisto Genetics Autos': 'Mephisto Genetics',
    'Mosca Negra': 'Mosca Seeds',
    'Oni Seed Co.': 'Oni Seed Co',
    'SinCity Seeds': 'Sin City Seeds',
    'Strain Hunters Seedbank': 'Strain Hunters Seeds',
    'Strayfox Gardenz': 'Stray Fox Gardenz',
    'SubCools The Dank Seeds': 'Subcool Seeds',
    'Taste Budz Seeds': 'Tastebudz',
    'Taste-Budz Seeds': 'Tastebudz',
    'Thug Pug Genetics': 'Thug Pug',
    "Tony Green's": 'Tonygreens Tortured Beans',
    'Twenty 20 Genetics': 'Twenty20 Mendocino',
    
    # Leading character fixes
    'z710 Genetics': '710 Genetics',
    'zAce Seeds': 'Ace Seeds',
    
    # Multi-breeder collaborations
    "Brother's Grimm Seeds - Trailer Park Boys / Hemptown Collab": 'Brothers Grimm Seeds, Trailer Park Boys, Hemptown Collab',
}

# Apply standardization
df['breeder_name_clean'] = df['breeder_name_raw'].replace(BREEDER_STANDARDIZATION)

operations = sum(df['breeder_name_raw'] != df['breeder_name_clean'])
print(f"Standardized: {operations} breeder names")

# Output
df.to_csv('../../cleaning_csv/10e_breeder_standardized.csv', index=False, encoding='utf-8')
df.head(100).to_csv('output/10e_breeder_standardized_sample.csv', index=False, encoding='utf-8')
print(f"Output: {len(df)} rows -> ../../cleaning_csv/10e_breeder_standardized.csv")
