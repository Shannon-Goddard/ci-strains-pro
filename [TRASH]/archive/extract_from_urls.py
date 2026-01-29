"""
Phase 8: Extract Strain Names from URLs
Uses URL slugs + Phase 6 breeder list to extract clean strain names

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import re
from pathlib import Path

# Paths
INPUT_CSV = Path("../../07_data_cleaning/output/09_autoflower_classified.csv")
BREEDER_VARIATIONS = Path("../docs/ALL_BREEDER_VARIATIONS.txt")
OUTPUT_CSV = Path("../output/06_strain_names_auto_preserved.csv")

# Load data
print("Loading data...")
df = pd.read_csv(INPUT_CSV, low_memory=False)

# Load all breeder variations
print("Loading breeder variations...")
breeder_names = set()
with open(BREEDER_VARIATIONS, 'r', encoding='utf-8') as f:
    for line in f:
        breeder = line.strip()
        if breeder:
            breeder_names.add(breeder)

print(f"Loaded {len(breeder_names)} breeder variations")

# Convert to lowercase for matching
breeder_names_lower = {b.lower() for b in breeder_names if isinstance(b, str)}

# Common seed type keywords to remove
# Note: Removed 'auto' - it's part of strain names (Auto 1, Auto Blueberry)
# North Atlantic handles '-auto' suffix separately
SEED_TYPE_KEYWORDS = [
    'feminized', 'feminised', 'fem', 'autoflower', 'autoflowering',
    'regular', 'photoperiod', 'photo', 'fast-version', 'fast', 'seeds',
    'seed', 'cannabis', 'marijuana', 'strain', 'pack', 'bulk'
]

# Generation patterns to preserve
GENERATION_PATTERN = r'\b(F[1-9]|BX[1-9]?|S[1-9]|IX|IBL|P1)\b'

# Phenotype patterns to preserve
PHENOTYPE_PATTERN = r'(#\d+|cut-[a-z]|selection-[a-z]|pheno-\d+)'

def extract_url_slug(url):  
    """Extract the product slug from URL"""
    if pd.isna(url):
        return None
    
    # Remove domain and get path segments
    parts = url.rstrip('/').split('/')
    
    # Check if last segment is a product ID (prod_123, .html, etc.)
    if len(parts) >= 2:
        last_part = parts[-1]
        # If last part is product ID, use second-to-last
        if re.match(r'(prod_\d+|\.html?)$', last_part):
            slug = parts[-2] if len(parts) >= 2 else None
        else:
            slug = last_part
    else:
        slug = parts[-1] if parts else None
    
    # Remove common suffixes
    if slug:
        slug = re.sub(r'(prod_\d+|\.html?)$', '', slug)
    
    return slug

def clean_slug_to_name(slug, breeder_names_lower, seed_bank=None):
    """Convert URL slug to clean strain name"""
    if not slug:
        return None, None, None, None
    
    # Special handling for North Atlantic Seed
    # URL pattern: /product/{strain-name}-auto/ or /product/{strain-name}-fem/
    # Only remove seed type suffix at END of slug
    if seed_bank == 'north_atlantic':
        # Remove seed type suffixes only at the end
        seed_suffixes = ['-auto', '-fem', '-feminized', '-regular', '-photoperiod']
        for suffix in seed_suffixes:
            if slug.endswith(suffix):
                slug = slug[:-len(suffix)]
                break
    
    # Special handling for Attitude Seed Bank
    # URL patterns: 
    #   {breeder}-seeds-{strain-name}
    #   {breeder}-genetics-{strain-name}
    #   {breeder}-seedbank-{strain-name}
    if seed_bank == 'attitude':
        # Find breeder separator patterns
        separators = ['-seeds-', '-genetics-', '-seedbank-', '-seed-', '-farm-']
        for sep in separators:
            if sep in slug:
                # Everything after separator is the strain name
                parts = slug.split(sep, 1)
                if len(parts) == 2:
                    slug = parts[1]  # Use only the strain name part
                    break
        # If slug ends with breeder suffix, it's just the breeder name, skip
        if any(slug.endswith(suffix) for suffix in ['-seeds', '-genetics', '-seedbank', '-seed', '-farm']):
            return None, None, None, None
    
    # Replace hyphens/underscores with spaces
    name = slug.replace('-', ' ').replace('_', ' ')
    
    # Extract generation (F1, BX, S1, etc.)
    generation_match = re.search(GENERATION_PATTERN, name, re.IGNORECASE)
    generation = generation_match.group(1).upper() if generation_match else None
    
    # Extract phenotype marker (#4, Cut A, etc.)
    phenotype_match = re.search(PHENOTYPE_PATTERN, name, re.IGNORECASE)
    phenotype = phenotype_match.group(1) if phenotype_match else None
    
    # Remove breeder names (check each word)
    words = name.split()
    filtered_words = []
    skip_next = False
    
    for i, word in enumerate(words):
        if skip_next:
            skip_next = False
            continue
            
        word_lower = word.lower()
        
        # Special case: Preserve "Auto" if it's at the start and followed by a number/name
        # (e.g., "Auto 1", "Auto Blueberry")
        if i == 0 and word_lower == 'auto' and len(words) > 1:
            filtered_words.append(word)
            continue
        
        # Check if word is a breeder name
        if word_lower in breeder_names_lower:
            continue
        
        # Check if word + next word is a breeder name
        if i < len(words) - 1:
            two_word = f"{word_lower} {words[i+1].lower()}"
            if two_word in breeder_names_lower:
                skip_next = True
                continue
        
        # Check if word is a seed type keyword
        if word_lower in SEED_TYPE_KEYWORDS:
            continue
        
        filtered_words.append(word)
    
    # Reconstruct name
    clean_name = ' '.join(filtered_words).strip()
    
    # Title case (but preserve acronyms like OG, THC, CBD)
    clean_name = ' '.join([
        w.upper() if len(w) <= 3 and w.isupper() else w.title()
        for w in clean_name.split()
    ])
    
    # Create base name (remove generation, phenotype for deduplication)
    base_name = clean_name
    if generation:
        base_name = re.sub(rf'\b{generation}\b', '', base_name, flags=re.IGNORECASE)
    if phenotype:
        base_name = re.sub(re.escape(phenotype), '', base_name, flags=re.IGNORECASE)
    base_name = ' '.join(base_name.split()).strip()
    
    return clean_name, base_name, generation, phenotype

# Extract strain names
print("Extracting strain names from URLs...")
df['url_slug'] = df['source_url_raw'].apply(extract_url_slug)

results = df.apply(
    lambda row: clean_slug_to_name(row['url_slug'], breeder_names_lower, row['seed_bank']),
    axis=1
)

df['strain_name_extracted'] = results.apply(lambda x: x[0])
df['strain_name_base'] = results.apply(lambda x: x[1])
df['generation_extracted'] = results.apply(lambda x: x[2])
df['phenotype_marker_extracted'] = results.apply(lambda x: x[3])

# Stats
total = len(df)
extracted = df['strain_name_extracted'].notna().sum()
success_rate = (extracted / total) * 100

print("\nExtraction complete!")
print(f"Total strains: {total:,}")
print(f"Extracted: {extracted:,}")
print(f"Success rate: {success_rate:.2f}%")
print(f"Failed: {total - extracted:,}")

# Show failures
failures = df[df['strain_name_extracted'].isna()]
if len(failures) > 0:
    print(f"\nFailed extractions:")
    print(failures[['seed_bank', 'source_url_raw']].head(10))

# Show samples
print(f"\nSample extractions:")
samples = df[df['strain_name_extracted'].notna()].head(10)
for _, row in samples.iterrows():
    print(f"  URL: {row['source_url_raw']}")
    print(f"  Extracted: {row['strain_name_extracted']}")
    print(f"  Base: {row['strain_name_base']}")
    if row['generation_extracted']:
        print(f"  Generation: {row['generation_extracted']}")
    if row['phenotype_marker_extracted']:
        print(f"  Phenotype: {row['phenotype_marker_extracted']}")
    print()

# Save
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
print(f"\nSaved to: {OUTPUT_CSV}")
