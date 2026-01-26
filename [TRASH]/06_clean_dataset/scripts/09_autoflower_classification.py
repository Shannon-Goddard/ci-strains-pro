import pandas as pd
import re
from pathlib import Path

# Paths
input_file = Path('../output/08_similar_spelling_normalized.csv')
output_file = Path('../output/09_autoflower_classified.csv')
report_file = Path('../output/09_autoflower_classification_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

# Detect autoflower
def is_autoflower(row):
    # Check seed_type_raw
    seed_type = str(row.get('seed_type_raw', '')).lower()
    if 'auto' in seed_type:
        return True
    
    # Check strain name
    strain_name = str(row.get('strain_name_raw', '')).lower()
    if re.search(r'\bauto\b', strain_name):
        return True
    
    # Check URL
    url = str(row.get('source_url_raw', '')).lower()
    if 'auto' in url or 'autoflower' in url:
        return True
    
    return False

df['is_autoflower_clean'] = df.apply(is_autoflower, axis=1)

autoflower_count = df['is_autoflower_clean'].sum()

# For autoflowers: move flowering time to seed-to-harvest
df['autoflower_seed_to_harvest_days_min_clean'] = None
df['autoflower_seed_to_harvest_days_max_clean'] = None

# Process autoflowers
for idx, row in df[df['is_autoflower_clean']].iterrows():
    # Get flowering time
    flowering_time = row.get('flowering_time_days_clean')
    
    if pd.notna(flowering_time):
        # Autoflowers: seed-to-harvest = flowering time (they don't have separate veg period)
        df.at[idx, 'autoflower_seed_to_harvest_days_min_clean'] = flowering_time
        df.at[idx, 'autoflower_seed_to_harvest_days_max_clean'] = flowering_time
        
        # Clear flowering time for autoflowers
        df.at[idx, 'flowering_time_days_clean'] = None

moved_count = df[df['is_autoflower_clean']]['autoflower_seed_to_harvest_days_min_clean'].notna().sum()

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 09: Autoflower Classification Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n")
    f.write(f"Autoflowers identified: {autoflower_count}\n")
    f.write(f"Autoflower rate: {(autoflower_count / len(df) * 100):.2f}%\n\n")
    f.write("Time separation:\n")
    f.write(f"  Flowering times moved to seed-to-harvest: {moved_count}\n")
    f.write(f"  Regular strains (kept flowering time): {len(df) - autoflower_count}\n")

print(f"\n[SUCCESS] Step 09 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Autoflowers identified: {autoflower_count}")
