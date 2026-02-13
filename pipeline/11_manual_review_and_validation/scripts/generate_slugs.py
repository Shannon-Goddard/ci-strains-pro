import pandas as pd
import re

def create_slug(name):
    """Convert strain name to URL-safe slug"""
    if pd.isna(name):
        return ''
    
    # Convert to lowercase
    slug = str(name).lower()
    
    # Remove periods
    slug = slug.replace('.', '')
    
    # Replace spaces and underscores with hyphens
    slug = slug.replace(' ', '-').replace('_', '-')
    
    # Remove any character that's not alphanumeric or hyphen
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    
    # Replace multiple hyphens with single hyphen
    slug = re.sub(r'-+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print(f"Reading {input_file}...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)

print(f"Total strains: {len(df):,}")

# Generate slug from strain_name_display_manual
print("\nGenerating slugs...")
df['strain_name_slug'] = df['strain_name_display_manual'].apply(create_slug)

# Show samples
print("\nSample slugs:")
samples = df[['strain_name_display_manual', 'strain_name_slug']].head(10)
print(samples.to_string(index=False))

# Check for empty slugs
empty_slugs = df['strain_name_slug'].isna() | (df['strain_name_slug'] == '')
if empty_slugs.any():
    print(f"\nWarning: {empty_slugs.sum()} strains have empty slugs")
    print(df[empty_slugs][['strain_id', 'strain_name_display_manual']].head())

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")
print(f"Added column: strain_name_slug")
