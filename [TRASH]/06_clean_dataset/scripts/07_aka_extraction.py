import pandas as pd
import re
from pathlib import Path

# Paths
input_file = Path('../output/06_strain_names_normalized.csv')
output_file = Path('../output/07_aka_extracted.csv')
report_file = Path('../output/07_aka_extraction_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

aka_count = 0

# Extract AKA names
def extract_aka(name):
    if pd.isna(name): return None, name
    
    name_str = str(name)
    
    # Patterns for AKA
    patterns = [
        r'\s*\(?\s*(?:aka|a\.k\.a\.|also known as)\s*[:\-]?\s*([^)]+)\)?',
        r'\s*\[?\s*(?:aka|a\.k\.a\.|also known as)\s*[:\-]?\s*([^\]]+)\]?'
    ]
    
    aka_names = []
    cleaned_name = name_str
    
    for pattern in patterns:
        matches = re.finditer(pattern, name_str, re.IGNORECASE)
        for match in matches:
            aka = match.group(1).strip()
            if aka:
                aka_names.append(aka)
                cleaned_name = cleaned_name.replace(match.group(0), '')
    
    # Clean up the name
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    
    return ', '.join(aka_names) if aka_names else None, cleaned_name

# Apply extraction
results = df['strain_name_raw'].apply(extract_aka)
df['aka_names_clean'] = results.apply(lambda x: x[0])
df['strain_name_no_aka'] = results.apply(lambda x: x[1])

# Update normalized name without AKA
df['strain_name_normalized'] = df['strain_name_no_aka'].apply(
    lambda x: str(x).lower().strip() if pd.notna(x) else None
)

aka_count = df['aka_names_clean'].notna().sum()

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 07: AKA Extraction Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n")
    f.write(f"AKA names extracted: {aka_count}\n")
    f.write(f"Extraction rate: {(aka_count / len(df) * 100):.2f}%\n\n")
    f.write("Sample AKA extractions:\n")
    samples = df[df['aka_names_clean'].notna()][['strain_name_raw', 'aka_names_clean']].head(10)
    for _, row in samples.iterrows():
        f.write(f"  {row['strain_name_raw']}\n")
        f.write(f"    AKA: {row['aka_names_clean']}\n")

print(f"\n[SUCCESS] Step 07 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"AKA names extracted: {aka_count}")
