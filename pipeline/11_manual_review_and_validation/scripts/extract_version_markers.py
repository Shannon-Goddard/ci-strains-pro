import pandas as pd
import re

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)
print(f"Total strains: {len(df):,}")

def extract_version(strain_name):
    """Extract version marker from strain name"""
    if pd.isna(strain_name):
        return None
    
    name = str(strain_name)
    
    # Check for version markers (case-insensitive)
    # Order matters - check specific patterns first
    
    # Fast version
    if re.search(r'\bfast\b', name, re.IGNORECASE):
        return 'Fast'
    
    # Version numbers (V1, V2, V3, etc.)
    v_match = re.search(r'\bv(\d+)\b', name, re.IGNORECASE)
    if v_match:
        return f'V{v_match.group(1)}'
    
    # Selfed generations (S1, S2, S3, etc.)
    s_match = re.search(r'\bs(\d+)\b', name, re.IGNORECASE)
    if s_match:
        return f'S{s_match.group(1)}'
    
    # Filial generations (F1, F2, F3, etc.)
    f_match = re.search(r'\bf(\d+)\b', name, re.IGNORECASE)
    if f_match:
        return f'F{f_match.group(1)}'
    
    # Backcross (BX1, BX2, etc.)
    bx_match = re.search(r'\bbx(\d+)\b', name, re.IGNORECASE)
    if bx_match:
        return f'BX{bx_match.group(1)}'
    
    # XL version
    if re.search(r'\bxl\b', name, re.IGNORECASE):
        return 'XL'
    
    # XXL version
    if re.search(r'\bxxl\b', name, re.IGNORECASE):
        return 'XXL'
    
    return None

print("\nExtracting version markers from strain_name_raw...")
df['version'] = df['strain_name_raw'].apply(extract_version)

# Show results
version_counts = df['version'].value_counts()
print(f"\nVersion markers found:")
print(version_counts)

total_with_version = df['version'].notna().sum()
print(f"\nTotal strains with version: {total_with_version:,} / {len(df):,} ({(total_with_version/len(df)*100):.1f}%)")

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")

# Show samples
print("\nSample strains with versions:")
print(df[df['version'].notna()][['strain_name_raw', 'version', 'strain_name_display']].head(20).to_string(index=False))
