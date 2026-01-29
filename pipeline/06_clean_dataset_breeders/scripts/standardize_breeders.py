import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"

print("Loading merged breeder data...")
df = pd.read_csv(OUTPUT_DIR / "all_breeders_extracted.csv", encoding='utf-8', low_memory=False)

print(f"Before standardization: {df['breeder_extracted'].nunique()} unique breeders")

# Standardization mapping based on MANUAL_BREEDER_REVIEW.md
standardization = {
    # 00 Seeds
    '00 Seeds Bank': '00 Seeds',
    '00seeds': '00 Seeds',
    
    # 710 Genetics
    '710 Genetics Seeds': '710 Genetics',
    'z710 Genetics': '710 Genetics',
    
    # Ace Seeds
    'Ace Seeds': 'Ace Seeds',
    'Aceseeds': 'Ace Seeds',
    
    # Advanced Seeds
    'Advanced Seeds': 'Advanced Seeds',
    'Advanced Female Seeds': 'Advanced Seeds',
    
    # Anesia Seeds
    'Anesia Seeds': 'Anesia Seeds',
    'Anesiaseeds': 'Anesia Seeds',
    
    # Apothecary Genetics
    'Apothecary Genetics Seeds': 'Apothecary Genetics',
    
    # Archive Seeds
    'Archive Seeds': 'Archive Seeds',
    'Archive Seed Co': 'Archive Seeds',
    
    # Barney's Farm
    "Barney's Farm": "Barney's Farm",
    'Barneys Farm Seeds': "Barney's Farm",
    'Barneysfarm': "Barney's Farm",
    
    # BC Bud Depot
    'BC Bud Depot Seeds': 'BC Bud Depot',
    
    # Big Buddha
    'Big Buddha Seeds': 'Big Buddha',
    
    # Blimburn Seeds
    'Blimburn Seeds': 'Blimburn Seeds',
    'BlimBurn Seeds': 'Blimburn Seeds',
    'Blimburnseeds': 'Blimburn Seeds',
    
    # Bodhi Seeds
    'Bodhi Seeds': 'Bodhi Seeds',
    'Bodhiseeds': 'Bodhi Seeds',
    
    # Brothers Grimm
    'Brothers Grimm Seeds': 'Brothers Grimm',
    
    # Buddha Seeds
    'Buddha Seeds': 'Buddha Seeds',
    'Buddhaseeds': 'Buddha Seeds',
    
    # Cali Connection
    'Cali Connection': 'Cali Connection',
    'Cali Connection Seeds': 'Cali Connection',
    'The Cali Connection': 'Cali Connection',
    'Caliconnection': 'Cali Connection',
    
    # Cannarado Genetics
    'Cannarado Genetics': 'Cannarado Genetics',
    'Cannarado Genetics Seeds': 'Cannarado Genetics',
    
    # Compound Genetics
    'Compound Genetics': 'Compound Genetics',
    'Compoundgenetics': 'Compound Genetics',
    
    # Critical Mass Collective
    'Critical Mass Collective': 'Critical Mass Collective',
    'Critical Mass Collective Seeds': 'Critical Mass Collective',
    
    # Crop King Seeds
    'Crop King Seeds': 'Crop King Seeds',
    'Cropkingseeds': 'Crop King Seeds',
    
    # Dark Horse Genetics
    'Dark Horse Genetics': 'Dark Horse Genetics',
    'DarkHorse Genetics Seeds': 'Dark Horse Genetics',
    
    # Delicious Seeds
    'Delicious Seeds': 'Delicious Seeds',
    'Deliciousseeds': 'Delicious Seeds',
    
    # Dinafem Seeds
    'Dinafem Seeds': 'Dinafem Seeds',
    'DinaFem Seeds': 'Dinafem Seeds',
    'Dinafemseeds': 'Dinafem Seeds',
    
    # DNA Genetics
    'DNA Genetics': 'DNA Genetics',
    'DNA Genetics Seeds': 'DNA Genetics',
    'DNA Genetics Seeds Limited Collection': 'DNA Genetics',
    'Dnagenetics': 'DNA Genetics',
    
    # Dr. Krippling
    'Dr. Krippling Seeds': 'Dr. Krippling',
    'Dr Krippling Seeds': 'Dr. Krippling',
    
    # Dungeons Vault Genetics
    'Dungeons Vault Genetics': 'Dungeons Vault Genetics',
    'Dungeon Vault Genetics Seeds': 'Dungeons Vault Genetics',
    
    # Dutch Passion
    'Dutch Passion': 'Dutch Passion',
    'Dutch Passion Seeds': 'Dutch Passion',
    'Dutchpassion': 'Dutch Passion',
    
    # Elev8 Seeds
    'Elev8 Seeds': 'Elev8 Seeds',
    'Elev8': 'Elev8 Seeds',
    
    # Emerald Triangle
    'Emerald Triangle Seeds': 'Emerald Triangle',
    
    # Ethos Genetics
    'Ethos Genetics': 'Ethos Genetics',
    'Ethos': 'Ethos Genetics',
    
    # Exotic Genetix
    'Exotic Genetix': 'Exotic Genetix',
    'Exotic Genetix Seeds': 'Exotic Genetix',
    
    # Fast Buds
    'Fast Buds': 'Fast Buds',
    'Fast Buds Seeds': 'Fast Buds',
    'Fast buds': 'Fast Buds',
    'FastBuds Seeds': 'Fast Buds',
    
    # Feminised Seeds
    'Feminised Seeds': 'Feminised Seeds',
    'Feminised Seeds Company': 'Feminised Seeds',
    
    # Flying Dutchmen
    'Flyingdutchmen': 'Flying Dutchmen',
    
    # G13 Labs
    'G13 Labs Seeds': 'G13 Labs',
    
    # Geist Grow
    'Geist Grow Genetics': 'Geist Grow',
    
    # Green Bodhi
    'Green Bodhi Seeds': 'Green Bodhi',
    
    # Greenhouse Seed Co.
    'Greenhouse Seed Co.': 'Greenhouse Seed Co.',
    'Green House Seeds': 'Greenhouse Seed Co.',
    
    # Growers Choice
    'Growers Choice': 'Growers Choice',
    'Growers Choice Seeds': 'Growers Choice',
    'GrowersChoice': 'Growers Choice',
    
    # Happy Valley Genetics
    'Happy Valley Genetics (Powered by ETHOS)': 'Happy Valley Genetics',
    
    # Humboldt Seed Organization
    'Humboldt Seed Organization': 'Humboldt Seed Organization',
    'Humboldt Seeds': 'Humboldt Seed Organization',
    
    # Humboldt Seed Company
    'Humboldt Seed Company': 'Humboldt Seed Company',
    'Humboldt Seed Co': 'Humboldt Seed Company',
    'Humboldt Seed Co.': 'Humboldt Seed Company',
    
    # In House Genetics
    'In House Genetics': 'In House Genetics',
    'Inhousegenetics': 'In House Genetics',
    
    # Karma Genetics
    'Karma Genetics Seeds': 'Karma Genetics',
    'Karma Genetics Limited Seeds': 'Karma Genetics',
    
    # Katsu Bluebird
    'Katsu Seeds': 'Katsu Bluebird',
    
    # LIT Farms
    'LIT Farms': 'LIT Farms',
    'LIT Farms Seeds': 'LIT Farms',
    'Lit Farms': 'LIT Farms',
    
    # James Loud Genetics
    'Loud Seeds': 'James Loud Genetics',
    
    # Lovin\' In Her Eyes
    "Lovin' In Her Eyes": "Lovin' In Her Eyes",
    
    # Massive Creations
    'Massive Creations Seeds': 'Massive Creations',
    'Massive Seeds': 'Massive Creations',
    
    # Mephisto Genetics
    'Mephisto Genetics': 'Mephisto Genetics',
    'Mephisto Genetics Autos': 'Mephisto Genetics',
    
    # Mosca
    'Mosca Seeds': 'Mosca',
    
    # Neptune Pharms
    'Neptune Pharms': 'Neptune Pharms',
    
    # Night Owl
    'Night Owl Seeds': 'Night Owl',
    
    # Offensive Selections
    'Offensive Selections Seeds': 'Offensive Selections',
    
    # Oni Seed Co.
    'Oni Seed Co': 'Oni Seed Co.',
    
    # Perfect Tree
    'Perfect Tree Seeds': 'Perfect Tree',
    
    # Rare Dankness
    'Rare Dankness Seeds': 'Rare Dankness',
    
    # Royal Queen Seeds
    'Royal Queen Seeds': 'Royal Queen Seeds',
    'Royalqueenseeds': 'Royal Queen Seeds',
    
    # Seed Stockers
    'SeedStockers': 'Seed Stockers',
    
    # Seedsman
    'Seedsman Seeds': 'Seedsman',
    
    # Sin City Seeds
    'SinCity Seeds': 'Sin City Seeds',
    
    # Subcool
    'SubCools The Dank Seeds': 'Subcool',
    'Subcool Seeds': 'Subcool',
    
    # SuperCBDx
    'SuperCBDx Seeds': 'SuperCBDx',
    
    # TH Seeds
    'TH Seeds Seeds': 'TH Seeds',
    
    # Taste Budz
    'Taste-Budz Seeds': 'Taste Budz',
    'Tastebudz': 'Taste Budz',
    
    # Terp Hogz
    'Terp Hogz Genetics (Plantinum Seeds)': 'Terp Hogz',
    
    # Thug Pug
    'Thug Pug Genetics': 'Thug Pug',
    
    # Tonygreen\'s Tortured Beans
    'Tonygreens Tortured Beans': "Tonygreen's Tortured Beans",
    
    # Twenty20
    'Twenty 20 Genetics': 'Twenty20',
    'Twenty20 Mendocino': 'Twenty20',
    
    # World Breeders
    'World Breeders Seeds': 'World Breeders',
}

# Apply standardization
df['breeder_cleaned'] = df['breeder_extracted'].replace(standardization)

print(f"After standardization: {df['breeder_cleaned'].nunique()} unique breeders")
print(f"Reduced by: {df['breeder_extracted'].nunique() - df['breeder_cleaned'].nunique()} duplicates")

# Save
output_path = OUTPUT_DIR / "all_breeders_cleaned.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"\nOutput: {output_path}")
