import pandas as pd
import re

def standardize_genetics_type(row):
    """Determine genetics type from percentages or dominant_type"""
    indica = row['indica_percentage_raw']
    sativa = row['sativa_percentage_raw']
    dominant = row['dominant_type_raw']
    desc = row['description_raw']
    
    # From percentages
    if pd.notna(indica) and pd.notna(sativa):
        indica = float(indica)
        sativa = float(sativa)
        
        if indica >= 70:
            return 'Indica Dominant', int(indica), int(sativa), 'extracted'
        elif sativa >= 70:
            return 'Sativa Dominant', int(indica), int(sativa), 'extracted'
        elif abs(indica - sativa) <= 10:
            return 'Balanced Hybrid', int(indica), int(sativa), 'extracted'
        elif indica > sativa:
            return 'Indica Dominant', int(indica), int(sativa), 'extracted'
        else:
            return 'Sativa Dominant', int(indica), int(sativa), 'extracted'
    
    # From dominant_type field
    if pd.notna(dominant):
        dominant_lower = str(dominant).lower()
        if 'indica' in dominant_lower:
            return 'Indica Dominant', 60, 40, 'inferred'
        elif 'sativa' in dominant_lower:
            return 'Sativa Dominant', 40, 60, 'inferred'
        elif 'hybrid' in dominant_lower or 'balanced' in dominant_lower:
            return 'Balanced Hybrid', 50, 50, 'inferred'
    
    # From description
    if pd.notna(desc):
        desc_lower = str(desc).lower()
        if 'indica-dominant' in desc_lower or 'indica dominant' in desc_lower:
            return 'Indica Dominant', 60, 40, 'inferred'
        elif 'sativa-dominant' in desc_lower or 'sativa dominant' in desc_lower:
            return 'Sativa Dominant', 40, 60, 'inferred'
        elif '100% indica' in desc_lower or 'pure indica' in desc_lower:
            return 'Indica Dominant', 100, 0, 'inferred'
        elif '100% sativa' in desc_lower or 'pure sativa' in desc_lower:
            return 'Sativa Dominant', 0, 100, 'inferred'
    
    return None, None, None, 'unknown'

# Load data
print("Loading dataset...")
df = pd.read_csv('output/all_strains_lineage_extracted.csv', encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df)}")

# Standardize genetics type
print("\nStandardizing genetics types...")
genetics_data = df.apply(standardize_genetics_type, axis=1)

df['genetics_type_clean'] = [x[0] for x in genetics_data]
df['indica_percentage_clean'] = [x[1] for x in genetics_data]
df['sativa_percentage_clean'] = [x[2] for x in genetics_data]
df['genetics_confidence'] = [x[3] for x in genetics_data]

# Add ruderalis for autos (from existing is_autoflower_clean)
df['ruderalis_percentage_clean'] = 0

# Save
output_path = 'output/all_strains_genetics_standardized.csv'
df.to_csv(output_path, index=False, encoding='latin-1')

print(f"\nGenetics standardization complete: {output_path}")
print(f"Genetics type extracted: {df['genetics_type_clean'].notna().sum()} ({df['genetics_type_clean'].notna().sum()/len(df)*100:.1f}%)")
print(f"  Indica Dominant: {(df['genetics_type_clean'] == 'Indica Dominant').sum()}")
print(f"  Sativa Dominant: {(df['genetics_type_clean'] == 'Sativa Dominant').sum()}")
print(f"  Balanced Hybrid: {(df['genetics_type_clean'] == 'Balanced Hybrid').sum()}")
print(f"Confidence breakdown:")
print(f"  Extracted: {(df['genetics_confidence'] == 'extracted').sum()}")
print(f"  Inferred: {(df['genetics_confidence'] == 'inferred').sum()}")
