"""
Step 11E: Merge Fixed Breeders & Apply Standardization
Merges corrected breeders with existing data and applies standardization.
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd

df = pd.read_csv('../../cleaning_csv/11d_breeder_fixed.csv', encoding='latin-1', low_memory=False)
print(f"Input: {len(df)} rows")

# Merge: Use breeder_name_extracted if available, else keep breeder_name_raw
df['breeder_name_merged'] = df['breeder_name_extracted'].fillna(df['breeder_name_raw'])

print(f"Breeder coverage:")
print(f"  Before: {df['breeder_name_raw'].notna().sum()} ({df['breeder_name_raw'].notna().sum()/len(df)*100:.1f}%)")
print(f"  After: {df['breeder_name_merged'].notna().sum()} ({df['breeder_name_merged'].notna().sum()/len(df)*100:.1f}%)")

# Apply standardization
BREEDER_STANDARDIZATION = {
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
    'Geist Grow': 'Geist Grow Genetics',
    'Grandiflora': 'Grandiflora Genetics',
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
    'z710 Genetics': '710 Genetics',
    'zAce Seeds': 'Ace Seeds',
    "Brother's Grimm Seeds - Trailer Park Boys / Hemptown Collab": 'Brothers Grimm Seeds, Trailer Park Boys, Hemptown Collab',
}

df['breeder_name_clean'] = df['breeder_name_merged'].replace(BREEDER_STANDARDIZATION)
standardized = (df['breeder_name_merged'] != df['breeder_name_clean']).sum()
print(f"\nStandardized: {standardized} breeder names")

# Drop intermediate columns
df = df.drop(columns=['breeder_name_extracted', 'breeder_name_merged'])

df.to_csv('../../cleaning_csv/11e_breeder_merged.csv', index=False, encoding='utf-8')
df.head(100).to_csv('output/11e_breeder_merged_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: {len(df)} rows -> ../../cleaning_csv/11e_breeder_merged.csv")
