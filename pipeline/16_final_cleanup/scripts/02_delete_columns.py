import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load data
df = pd.read_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\input\pipeline_15_final.csv', encoding='latin-1', low_memory=False)

print(f"Starting with {len(df)} strains, {len(df.columns)} columns")

# Columns to delete
delete_cols = [
    'notes_manual', 'grandparent_3_slug', 'grandparent_3_display', 'cbn_content_raw',
    'climate_raw', 'outdoor_harvest_raw', 'grandparent_1_display', 'grandparent_1_slug',
    'grandparent_2_slug', 'grandparent_2_display', 'difficulty_raw', 'terpenes_raw_y',
    'seed_type_raw_x'
]

# Delete columns
df = df.drop(columns=delete_cols, errors='ignore')

print(f"✅ Deleted {len(delete_cols)} columns")
print(f"Final: {len(df)} strains, {len(df.columns)} columns")

# Save
df.to_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\output\pipeline_16_cleaned.csv', index=False, encoding='latin-1')
print(f"\n✅ Saved: pipeline_16_cleaned.csv")
