import pandas as pd
import html

input_file = "output/pipeline_11_clean.csv"
output_file = "output/pipeline_11_clean.csv"

print("Reading dataset...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)

def clean_encoding(text):
    """Fix common encoding issues"""
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # Fix HTML entities
    text = html.unescape(text)
    
    # Fix common encoding issues
    replacements = {
        'â€"': '-',  # em dash
        'â€"': '-',  # en dash
        'â€™': "'",  # apostrophe
        'â€œ': '"',  # left quote
        'â€': '"',   # right quote
        'Ã—': 'x',   # multiplication sign
        'Ã¢': '',    # garbage
        'â€': '',    # garbage
        'Â': '',     # non-breaking space
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text.strip()

print("Cleaning strain_name_raw_2...")
df['strain_name_raw_2'] = df['strain_name_raw_2'].apply(clean_encoding)

# Save
df.to_csv(output_file, index=False, encoding='utf-8')
print(f"Saved to: {output_file}")

# Show samples
print("\nSample cleaned names:")
print(df[['strain_name_raw_2', 'strain_name_display']].head(20).to_string(index=False))
