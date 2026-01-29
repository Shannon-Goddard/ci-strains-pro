"""
Shared helper functions for strain name extraction
Used by all seed-bank-specific extraction scripts

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import re
from pathlib import Path

# Load breeder variations (2,575 variations)
def load_breeder_variations():
    """Load all breeder name variations from Phase 6"""
    breeder_file = Path("../docs/ALL_BREEDER_VARIATIONS.txt")
    
    breeder_names = set()
    with open(breeder_file, 'r', encoding='utf-8') as f:
        for line in f:
            breeder = line.strip()
            if breeder:
                breeder_names.add(breeder.lower())
    return breeder_names

# Extract generation markers (F1, BX, S1, etc.)
def extract_generation(name):
    """Extract generation marker from strain name"""
    pattern = r'\b(F[1-9]|BX[1-9]?|S[1-9]|IX|IBL|P1|R[1-9]?)\b'
    match = re.search(pattern, name, re.IGNORECASE)
    return match.group(1).upper() if match else None

# Extract phenotype markers (#4, Cut A, etc.)
def extract_phenotype(name):
    """Extract phenotype marker from strain name"""
    pattern = r'(#\d+|cut-[a-z]|selection-[a-z]|pheno-\d+)'
    match = re.search(pattern, name, re.IGNORECASE)
    return match.group(1) if match else None

# Create base name (remove generation/phenotype for deduplication)
def create_base_name(name, generation, phenotype):
    """Create base name by removing generation and phenotype markers"""
    base = name
    if generation:
        base = re.sub(rf'\b{generation}\b', '', base, flags=re.IGNORECASE)
    if phenotype:
        base = re.sub(re.escape(phenotype), '', base, flags=re.IGNORECASE)
    return ' '.join(base.split()).strip()

# Title case with acronym preservation
def smart_title_case(name):
    """Title case but preserve acronyms (OG, THC, CBD)"""
    words = name.split()
    result = []
    for word in words:
        # Preserve 2-3 letter uppercase acronyms
        if len(word) <= 3 and word.isupper():
            result.append(word)
        else:
            result.append(word.title())
    return ' '.join(result)

# Remove breeder names from strain name
def remove_breeder_names(name, breeder_names_lower):
    """Remove breeder names from strain name"""
    words = name.split()
    filtered = []
    skip_next = False
    
    for i, word in enumerate(words):
        if skip_next:
            skip_next = False
            continue
        
        word_lower = word.lower()
        
        # Check single word
        if word_lower in breeder_names_lower:
            continue
        
        # Check two-word breeder names
        if i < len(words) - 1:
            two_word = f"{word_lower} {words[i+1].lower()}"
            if two_word in breeder_names_lower:
                skip_next = True
                continue
        
        # Check three-word breeder names
        if i < len(words) - 2:
            three_word = f"{word_lower} {words[i+1].lower()} {words[i+2].lower()}"
            if three_word in breeder_names_lower:
                skip_next = True
                continue
        
        filtered.append(word)
    
    return ' '.join(filtered).strip()

# Get URL slug (last or second-to-last path segment)
def get_url_slug(url, position='last'):
    """Extract slug from URL
    
    Args:
        url: Full URL string
        position: 'last' or 'second_to_last'
    """
    if not url or str(url) == 'nan':
        return None
    
    parts = str(url).rstrip('/').split('/')
    
    if position == 'second_to_last' and len(parts) >= 2:
        return parts[-2]
    elif position == 'last' and len(parts) >= 1:
        return parts[-1]
    
    return None

# Clean slug to name
def slug_to_name(slug):
    """Convert URL slug to readable name"""
    if not slug:
        return None
    
    # Remove file extensions
    slug = re.sub(r'\.(html?|php)$', '', slug)
    
    # Replace hyphens/underscores with spaces
    name = slug.replace('-', ' ').replace('_', ' ')
    
    # Remove extra spaces
    name = ' '.join(name.split())
    
    return name
