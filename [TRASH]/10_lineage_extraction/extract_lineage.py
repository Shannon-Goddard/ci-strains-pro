import pandas as pd
import re

def extract_generation(text):
    """Extract F1, S1, BX1, etc."""
    if pd.isna(text):
        return None, None, None, None
    text = str(text).upper()
    f_gen = re.search(r'\bF(\d+)\b', text)
    s_gen = re.search(r'\bS(\d+)\b', text)
    bx_gen = re.search(r'\bBX(\d+)\b', text)
    
    filial = f"F{f_gen.group(1)}" if f_gen else None
    selfed = f"S{s_gen.group(1)}" if s_gen else None
    backcross = f"BX{bx_gen.group(1)}" if bx_gen else None
    
    generation = filial or selfed or backcross
    return generation, filial, selfed, backcross

def parse_lineage(text):
    """Parse parent crosses from description"""
    if pd.isna(text):
        return {}
    
    text = str(text)
    
    # Look for cross patterns: "X x Y", "cross of X and Y", "X crossed with Y"
    patterns = [
        r'cross(?:ed)?\s+(?:of|between)\s+([^.]+?)\s+(?:and|with|x)\s+([^.]+?)(?:\.|,|$)',
        r'([^.]+?)\s+x\s+([^.]+?)(?:\s+[FS]\d+|\s+BX\d+|\.|\,|$)',
        r'blend(?:ing)?\s+(?:of\s+)?([^.]+?)\s+(?:and|with)\s+([^.]+?)(?:\.|,|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            p1 = match.group(1).strip()
            p2 = match.group(2).strip()
            
            # Check if parent 1 is nested (contains x)
            p1_nested = ' x ' in p1.lower()
            p2_nested = ' x ' in p2.lower()
            
            # Extract grandparents if nested
            grandparents = []
            if p1_nested:
                gp = re.split(r'\s+x\s+', p1, flags=re.IGNORECASE)
                grandparents.extend([g.strip() for g in gp])
            if p2_nested:
                gp = re.split(r'\s+x\s+', p2, flags=re.IGNORECASE)
                grandparents.extend([g.strip() for g in gp])
            
            return {
                'parent_1': p1,
                'parent_2': p2,
                'parent_1_is_hybrid': p1_nested,
                'parent_2_is_hybrid': p2_nested,
                'grandparents': grandparents if grandparents else None,
                'has_nested_cross': p1_nested or p2_nested
            }
    
    return {}

def create_slug(name):
    """Create slug for matching"""
    if pd.isna(name) or name == '':
        return None
    name = str(name).strip().lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')

# Load data
print("Loading dataset...")
df = pd.read_csv('../09.5_standardization/output/all_strains_standardized_clean.csv', encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df)}")

# Extract generations
print("\nExtracting generations...")
gen_results = df['description_raw'].apply(extract_generation)
df['generation_clean'] = [x[0] if x else None for x in gen_results]
df['filial_generation'] = [x[1] if x else None for x in gen_results]
df['selfed_generation'] = [x[2] if x else None for x in gen_results]
df['backcross_generation'] = [x[3] if x else None for x in gen_results]

# Parse lineage
print("Parsing lineage...")
lineage_data = df['description_raw'].apply(parse_lineage)

df['parent_1_display'] = lineage_data.apply(lambda x: x.get('parent_1'))
df['parent_2_display'] = lineage_data.apply(lambda x: x.get('parent_2'))
df['parent_1_is_hybrid'] = lineage_data.apply(lambda x: x.get('parent_1_is_hybrid', False))
df['parent_2_is_hybrid'] = lineage_data.apply(lambda x: x.get('parent_2_is_hybrid', False))
df['has_nested_cross'] = lineage_data.apply(lambda x: x.get('has_nested_cross', False))

# Create slugs
df['parent_1_slug'] = df['parent_1_display'].apply(create_slug)
df['parent_2_slug'] = df['parent_2_display'].apply(create_slug)

# Extract grandparents
def extract_grandparents(row):
    gp = []
    if row['parent_1_is_hybrid'] and pd.notna(row['parent_1_display']):
        gp.extend(re.split(r'\s+x\s+', row['parent_1_display'], flags=re.IGNORECASE))
    if row['parent_2_is_hybrid'] and pd.notna(row['parent_2_display']):
        gp.extend(re.split(r'\s+x\s+', row['parent_2_display'], flags=re.IGNORECASE))
    return [g.strip() for g in gp] if gp else None

grandparents = df.apply(extract_grandparents, axis=1)
df['grandparent_1_display'] = grandparents.apply(lambda x: x[0] if x and len(x) > 0 else None)
df['grandparent_2_display'] = grandparents.apply(lambda x: x[1] if x and len(x) > 1 else None)
df['grandparent_3_display'] = grandparents.apply(lambda x: x[2] if x and len(x) > 2 else None)

df['grandparent_1_slug'] = df['grandparent_1_display'].apply(create_slug)
df['grandparent_2_slug'] = df['grandparent_2_display'].apply(create_slug)
df['grandparent_3_slug'] = df['grandparent_3_display'].apply(create_slug)

# Create lineage formula
def create_formula(row):
    if pd.notna(row['parent_1_slug']) and pd.notna(row['parent_2_slug']):
        return f"{row['parent_1_slug']} x {row['parent_2_slug']}"
    return None

df['lineage_formula'] = df.apply(create_formula, axis=1)

# Calculate lineage depth
df['lineage_depth'] = df['has_nested_cross'].apply(lambda x: 2 if x else 1 if pd.notna(x) else 0)

# Save
output_path = 'output/all_strains_lineage_extracted.csv'
df.to_csv(output_path, index=False, encoding='latin-1')

print(f"\nLineage extraction complete: {output_path}")
print(f"Parents extracted: {df['parent_1_display'].notna().sum()}")
print(f"Generations extracted: {df['generation_clean'].notna().sum()}")
print(f"Nested crosses: {df['has_nested_cross'].sum()}")
print(f"Grandparents extracted: {df['grandparent_1_display'].notna().sum()}")
