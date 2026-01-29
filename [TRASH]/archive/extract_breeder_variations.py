"""
Extract all breeder name variations from MANUAL_BREEDER_REVIEW.md
Includes both standardized names and all raw variations

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import re
from pathlib import Path

# Paths
MANUAL_REVIEW = Path("../../06_clean_dataset_breeders/docs/MANUAL_BREEDER_REVIEW.md")
BREEDER_LIST = Path("../../06_clean_dataset_breeders/BREEDER_LIST_CLEANED.md")
OUTPUT_FILE = Path("../docs/ALL_BREEDER_VARIATIONS.txt")

# Load all breeder variations
all_variations = set()

# 1. Load standardized names from BREEDER_LIST_CLEANED.md
print("Loading standardized breeder names...")
with open(BREEDER_LIST, 'r', encoding='utf-8') as f:
    in_table = False
    for line in f:
        line = line.strip()
        if line.startswith('| Breeder |'):
            in_table = True
            continue
        if line.startswith('|---'):
            continue
        if in_table and not line.startswith('|'):
            break
        if in_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                breeder = parts[1].strip()
                if breeder and breeder != 'Breeder':
                    all_variations.add(breeder)

print(f"  Loaded {len(all_variations)} standardized names")

# 2. Load all variations from MANUAL_BREEDER_REVIEW.md
print("Loading breeder variations from manual review...")
with open(MANUAL_REVIEW, 'r', encoding='utf-8') as f:
    content = f.read()
    
    # Extract all quoted variations (e.g., "Fast Buds", "Fast buds", "FastBuds Seeds")
    variations = re.findall(r'"([^"]+)"', content)
    for var in variations:
        # Skip non-breeder text
        if var in ['Current values found', 'Standardized value', 'what it should be']:
            continue
        all_variations.add(var)

print(f"  Total variations: {len(all_variations)}")

# 3. Generate additional common variations
print("Generating common variations...")
additional = set()
for breeder in list(all_variations):
    # Add lowercase version
    additional.add(breeder.lower())
    
    # Add version without "Seeds" suffix
    if breeder.endswith(' Seeds'):
        additional.add(breeder[:-6])
    
    # Add version without "Genetics" suffix
    if breeder.endswith(' Genetics'):
        additional.add(breeder[:-9])
    
    # Add version without spaces
    additional.add(breeder.replace(' ', ''))
    
    # Add version with hyphens instead of spaces
    additional.add(breeder.replace(' ', '-'))

all_variations.update(additional)
print(f"  Total with variations: {len(all_variations)}")

# Sort and save
sorted_variations = sorted(all_variations, key=str.lower)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for var in sorted_variations:
        f.write(f"{var}\n")

print(f"\nSaved {len(sorted_variations)} breeder variations to: {OUTPUT_FILE}")
print("\nSample variations:")
for var in sorted_variations[:20]:
    print(f"  - {var}")
