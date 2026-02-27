import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\output\pipeline_16_cleaned.csv', encoding='latin-1', low_memory=False)

print(f"Starting: {len(df.columns)} columns")

rename_map = {
    'source_url_raw': 'source_url',
    'strain_name_raw': 'strain_name_original',
    'version_og': 'version',
    'aka_strain_name_og': 'aka_strain_name',
    'seed_bank_display': 'seed_bank',
    'breeder_displayl': 'breeder',
    's3_html_key_raw': 's3_html_key',
    'scraped_at_raw': 'scraped_at',
    'genetics_type_clean': 'genetics_type',
    'indica_percentage_clean': 'indica_percentage',
    'sativa_percentage_clean': 'sativa_percentage',
    'effects_all_raw': 'effects',
    'flavors_all_raw': 'flavors',
    'terpenes_raw_x': 'terpenes',
    'genetics_raw': 'genetics_description',
    'category_type_raw': 'category_type',
    'harvest_time_raw': 'harvest_time',
    'lineage_raw': 'lineage_description',
    'generation_clean': 'generation'
}

df = df.rename(columns=rename_map)

print(f"✅ Renamed {len(rename_map)} columns")
print(f"Final: {len(df.columns)} columns")

df.to_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\output\pipeline_16_cleaned.csv', index=False, encoding='latin-1')
print("✅ Saved")
