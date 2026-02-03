import pandas as pd
import re

def create_display_name(name):
    """Proper capitalization for display"""
    if pd.isna(name) or name == '':
        return None
    name = str(name).strip()
    # Title case with exceptions
    exceptions = ['and', 'x', 'the', 'of', 'by']
    words = name.split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in exceptions:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return ' '.join(result)

def create_slug(name):
    """Lowercase slug for research/matching"""
    if pd.isna(name) or name == '':
        return None
    name = str(name).strip().lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.strip('-')

# Load merged dataset
print("Loading dataset...")
df = pd.read_csv('../09_vertex_validation/output/all_strains_validated_merged.csv', encoding='latin-1', low_memory=False)
print(f"Total rows: {len(df)}")

# Prioritize manual > validated > raw for source data
df['breeder_source'] = df['breeder_manual'].fillna(df['breeder_validated']).fillna(df['breeder_name_raw'])
df['strain_source'] = df['strain_name_manual'].fillna(df['strain_name_validated']).fillna(df['strain_name_raw'])

# Create display and slug columns
print("\nStandardizing breeders...")
df['breeder_display'] = df['breeder_source'].apply(create_display_name)
df['breeder_slug'] = df['breeder_source'].apply(create_slug)

print("Standardizing strain names...")
df['strain_name_display'] = df['strain_source'].apply(create_display_name)
df['strain_name_slug'] = df['strain_source'].apply(create_slug)

# Save
output_path = 'output/all_strains_standardized.csv'
df.to_csv(output_path, index=False, encoding='latin-1')

print(f"\nStandardization complete: {output_path}")
print(f"Breeder display: {df['breeder_display'].notna().sum()}")
print(f"Breeder slug: {df['breeder_slug'].notna().sum()}")
print(f"Strain display: {df['strain_name_display'].notna().sum()}")
print(f"Strain slug: {df['strain_name_slug'].notna().sum()}")
