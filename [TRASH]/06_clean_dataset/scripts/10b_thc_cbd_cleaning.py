import pandas as pd
import re
from pathlib import Path

# Paths
input_file = Path('../output/10a_strain_names_deep_cleaned.csv')
output_file = Path('../output/10b_thc_cbd_cleaned.csv')
report_file = Path('../output/10b_thc_cbd_cleaning_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

stats = {
    'thc_outliers_removed': 0,
    'cbd_outliers_removed': 0,
    'encoding_fixed': 0,
    'percentages_removed': 0
}

# Clean THC/CBD values
def clean_cannabinoid_value(val):
    if pd.isna(val): return None
    
    val_str = str(val).strip()
    
    # Remove encoding issues
    if 'Ã' in val_str:
        stats['encoding_fixed'] += 1
        val_str = re.sub(r'[ÃƒÂ¢Ã‚Â€Ã‚Â"]+', '-', val_str)
    
    # Standardize separators
    val_str = val_str.replace(' to ', '-')
    val_str = val_str.replace('(up to)', '-')
    val_str = val_str.replace(' and ', '-')
    
    # Remove descriptive words
    val_str = re.sub(r'average\s+thc', '', val_str, flags=re.IGNORECASE)
    
    # Remove % symbol
    if '%' in val_str:
        stats['percentages_removed'] += 1
        val_str = val_str.replace('%', '')
    
    # Try to convert to float
    try:
        return float(val_str)
    except:
        return None

# Clean THC columns
for col in ['thc_min_raw', 'thc_max_raw', 'thc_average_raw', 'thc_content_raw']:
    if col in df.columns:
        df[col] = df[col].apply(clean_cannabinoid_value)
        
        # Remove outliers
        outliers = df[col].isin([0, 0.03, 40, 50])
        stats['thc_outliers_removed'] += outliers.sum()
        df.loc[outliers, col] = None

# Clean CBD columns
for col in ['cbd_min_raw', 'cbd_max_raw', 'cbd_content_raw']:
    if col in df.columns:
        df[col] = df[col].apply(clean_cannabinoid_value)
        
        # Remove outliers
        outliers = df[col].isin([0, 0.03])
        stats['cbd_outliers_removed'] += outliers.sum()
        df.loc[outliers, col] = None

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 10B: THC/CBD Data Cleaning Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n\n")
    f.write("Cleaning operations:\n")
    f.write(f"  THC outliers removed (0, 0.03, 40, 50): {stats['thc_outliers_removed']}\n")
    f.write(f"  CBD outliers removed (0, 0.03): {stats['cbd_outliers_removed']}\n")
    f.write(f"  Encoding issues fixed: {stats['encoding_fixed']}\n")
    f.write(f"  Percentage symbols removed: {stats['percentages_removed']}\n")
    f.write(f"\nTotal operations: {sum(stats.values())}\n")

print(f"\n[SUCCESS] Step 10B complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Total operations: {sum(stats.values())}")
