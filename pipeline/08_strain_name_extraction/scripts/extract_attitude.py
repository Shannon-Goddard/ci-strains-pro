"""
Extract strain names from Attitude Seed Bank URLs

URL Pattern: {breeder}-{seeds|genetics|seedbank|farm}-{strain-name}/prod_####
Example: auto-seeds-auto-1/prod_1705 → "Auto 1"

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import re
from pathlib import Path
from extraction_helpers import *

# Paths
INPUT_CSV = Path("../../07_data_cleaning/output/09_autoflower_classified.csv")
OUTPUT_CSV = Path("../output/attitude_strain_names_v2.csv")

# Load data
print("Loading data...")
df = pd.read_csv(INPUT_CSV, low_memory=False)
df_bank = df[df['seed_bank'] == 'attitude'].copy()
print(f"Found {len(df_bank)} Attitude strains")

# Load breeder variations
print("Loading breeder variations...")
breeder_names_lower = load_breeder_variations()
print(f"Loaded {len(breeder_names_lower)} breeder variations")

# Build list of breeder prefixes from Attitude URLs
print("Building breeder prefix list from URLs...")
breeder_prefixes = set()
for url in df_bank['source_url_raw'].dropna():
    slug = get_url_slug(url, 'second_to_last')
    if slug and '-' in slug:
        # Try each breeder name
        for breeder in breeder_names_lower:
            breeder_slug = breeder.replace(' ', '-')
            # Only add if breeder is followed by a hyphen and more content
            # This prevents "serious" from matching when only "serious-seeds" should
            if slug.startswith(breeder_slug + '-'):
                # Verify there's content after the breeder name
                remainder = slug[len(breeder_slug + '-'):]
                if remainder and not remainder.startswith('-'):  # Has content and not just hyphens
                    breeder_prefixes.add(breeder_slug + '-')

print(f"Found {len(breeder_prefixes)} unique breeder prefixes")

def extract_attitude_strain(url, breeder_prefixes):
    """Extract strain name from Attitude URL by removing breeder prefix"""
    # Get slug (second-to-last segment before prod_####)
    slug = get_url_slug(url, 'second_to_last')
    if not slug:
        return None, None, None, None
    
    # Try to match and remove breeder prefix
    # Sort by length (longest first) to match "jinxproof-genetics" before "jinxproof"
    for prefix in sorted(breeder_prefixes, key=len, reverse=True):
        if slug.startswith(prefix):
            # Remove the prefix
            slug = slug[len(prefix):]
            break
    
    # Convert slug to name
    name = slug_to_name(slug)
    if not name:
        return None, None, None, None
    
    # Extract metadata
    generation = extract_generation(name)
    phenotype = extract_phenotype(name)
    
    # Title case
    name = smart_title_case(name)
    
    # Create base name
    base_name = create_base_name(name, generation, phenotype)
    
    return name, base_name, generation, phenotype

# Extract strain names
print("Extracting strain names...")
results = df_bank['source_url_raw'].apply(lambda url: extract_attitude_strain(url, breeder_prefixes))

df_bank['strain_name_extracted'] = results.apply(lambda x: x[0])
df_bank['strain_name_base'] = results.apply(lambda x: x[1])
df_bank['generation_extracted'] = results.apply(lambda x: x[2])
df_bank['phenotype_marker_extracted'] = results.apply(lambda x: x[3])

# Stats
total = len(df_bank)
extracted = df_bank['strain_name_extracted'].notna().sum()
success_rate = (extracted / total) * 100

print(f"\nExtraction complete!")
print(f"Total: {total:,}")
print(f"Extracted: {extracted:,}")
print(f"Success rate: {success_rate:.2f}%")
print(f"Failed: {total - extracted:,}")

# Show failures
failures = df_bank[df_bank['strain_name_extracted'].isna()]
if len(failures) > 0:
    print(f"\nFailed extractions:")
    print(failures[['source_url_raw']].head(10))

# Show samples
print(f"\nSample extractions:")
samples = df_bank[df_bank['strain_name_extracted'].notna()].head(10)
for _, row in samples.iterrows():
    print(f"  URL: {row['source_url_raw']}")
    print(f"  Extracted: {row['strain_name_extracted']}")
    if row['generation_extracted']:
        print(f"  Generation: {row['generation_extracted']}")
    print()

# Save
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df_bank.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
print(f"Saved to: {OUTPUT_CSV}")
