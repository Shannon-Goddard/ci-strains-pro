import pandas as pd
import re
from pathlib import Path

# Paths
input_file = Path('../output/09_autoflower_classified.csv')
output_file = Path('../output/10a_strain_names_deep_cleaned.csv')
report_file = Path('../output/10a_strain_name_deep_cleaning_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

stats = {
    'seed_types_removed': 0,
    'breeder_prefixes_removed': 0,
    'encoding_fixed': 0,
    'generic_terms_removed': 0,
    'promotional_removed': 0,
    'pack_sizes_removed': 0,
    'filial_extracted': 0,
    'rows_deleted': 0
}

# Patterns to remove
seed_type_patterns = [
    r'\b(feminized|feminised|fem|feminised seeds|strain fem)\b',
    r'\b(autoflowering cannabis seeds|autoflower|auto|automatic)\b',
    r'\b(regular|regular marijuana|regular cannabis seeds)\b',
    r'\(f\)', r'\(r\)'
]

generic_terms = [
    r'\bcannabis seeds\b', r'\bstrain\b', r'\bbulk cannabis seeds\b',
    r'\bcom abpa\b', r'\bafga\b', r'\bseeds sman\b', r'\balso know\b',
    r'&#8211;', r'\bseeds\b'
]

promotional_terms = [
    r'\[exclusive\]', r'\[.*?drop\]', r'\[limited edition.*?\]',
    r'\d+\s*pack', r'-\s*\d+', r'seeds\s*\d+'
]

# Known breeder prefixes
breeder_prefixes = [
    '3rd shift genetics', '3rd coast genetics', 'growers choice', 'aeque genetics',
    'herbies seeds usa', 'seeds ace', 'always be flowering genetics', 'barneys farm',
    'royal queen seeds', 'happy valley genetics', 'elev8 seeds', 'rqs', 'fast buds',
    'atlas', '710 genetics', '710 genetics seed bank', 'advanced', 
    'advanced feminized cannabis seeds', 'advanced seeds', 'afghan selection',
    'aficionado french connection', 'alpine', 'anesia', 'apothecary genetics',
    'archive seeds', 'archive'
]

# Encoding issues
encoding_patterns = [
    (r'Ã£Â¢Ã¢Â€Ã¢Â["\']', ''),
    (r'Ã£Â¢Ã¢Â€Ã¢Â‹', ''),
    (r'Ã£ÂƒÃ¢Â€', ''),
    (r'Ã£Â¢Ã¢Â€Ã¢Â¯', ''),
    (r'Ã£Â‚Ã¢Â©', ''),
    (r'bgs ag13s1', ''),
    (r'gh alz', '')
]

# Delete non-product rows
non_product_patterns = [
    '1 free seed from qr code',
    'assorted mix auto feminised seeds',
    'age verification',
    '6 cc 037 f6'
]

# Clean strain names
def deep_clean_strain_name(name):
    if pd.isna(name): return None
    
    name = str(name).lower().strip()
    
    # Check for non-product rows
    for pattern in non_product_patterns:
        if pattern in name:
            stats['rows_deleted'] += 1
            return 'DELETE_ROW'
    
    # Fix encoding issues
    for pattern, replacement in encoding_patterns:
        if re.search(pattern, name):
            stats['encoding_fixed'] += 1
            name = re.sub(pattern, replacement, name)
    
    # Remove breeder prefixes
    for breeder in breeder_prefixes:
        if name.startswith(breeder):
            stats['breeder_prefixes_removed'] += 1
            name = name.replace(breeder, '', 1).strip()
    
    # Remove seed types
    for pattern in seed_type_patterns:
        if re.search(pattern, name):
            stats['seed_types_removed'] += 1
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # Remove generic terms
    for pattern in generic_terms:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # Remove promotional terms
    for pattern in promotional_terms:
        if re.search(pattern, name):
            stats['promotional_removed'] += 1
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # Clean up whitespace
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name if name else None

# Apply cleaning
df['strain_name_normalized'] = df['strain_name_normalized'].apply(deep_clean_strain_name)

# Delete rows marked for deletion
rows_before = len(df)
df = df[df['strain_name_normalized'] != 'DELETE_ROW']
rows_after = len(df)
stats['rows_deleted'] = rows_before - rows_after

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 10A: Strain Name Deep Cleaning Report ===\n\n")
    f.write(f"Initial rows: {rows_before}\n")
    f.write(f"Final rows: {rows_after}\n")
    f.write(f"Rows deleted (non-products): {stats['rows_deleted']}\n\n")
    f.write("Cleaning operations:\n")
    f.write(f"  Seed types removed: {stats['seed_types_removed']}\n")
    f.write(f"  Breeder prefixes removed: {stats['breeder_prefixes_removed']}\n")
    f.write(f"  Encoding issues fixed: {stats['encoding_fixed']}\n")
    f.write(f"  Promotional terms removed: {stats['promotional_removed']}\n")
    f.write(f"\nTotal cleaning operations: {sum(stats.values())}\n")

print(f"\n[SUCCESS] Step 10A complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Rows deleted: {stats['rows_deleted']}")
print(f"Total operations: {sum(stats.values())}")
