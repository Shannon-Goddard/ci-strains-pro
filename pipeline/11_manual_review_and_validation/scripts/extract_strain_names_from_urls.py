import pandas as pd
import re

# Read the CSV
df = pd.read_csv('output/pipeline_11_clean.csv', encoding='latin-1')

# Function to extract strain name from URL
def extract_strain_name_from_url(url):
    if pd.isna(url):
        return ''
    
    # Extract the last part of the URL path (before query params)
    match = re.search(r'/([^/]+?)/?(?:\?|$)', url)
    if match:
        slug = match.group(1)
        # Replace hyphens with spaces and title case
        name = slug.replace('-', ' ').title()
        return name
    return ''

# Apply the function
df['strain_name_from_source_url'] = df['source_url_raw'].apply(extract_strain_name_from_url)

# Save to new CSV
df[['strain_id', 'source_url_raw', 'strain_name_from_source_url']].to_csv(
    'output/strain_name_from_source_url.csv', 
    index=False, 
    encoding='latin-1'
)

print(f"Processed {len(df)} rows")
print(f"Output saved to: output/strain_name_from_source_url.csv")
