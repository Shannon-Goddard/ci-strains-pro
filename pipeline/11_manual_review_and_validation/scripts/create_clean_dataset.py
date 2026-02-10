import pandas as pd

input_file = "output/pipeline_11_breeder_extracted.csv"
output_file = "output/pipeline_11_clean.csv"

print(f"Reading {input_file}...")
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)
print(f"Original: {len(df):,} rows, {len(df.columns)} columns")

# KEEP columns
keep_cols = [
    # Core Identity (GOLD - 100% verified)
    'strain_id',
    'seed_bank_display_manual',
    'breeder_display_manual',
    'strain_name_display_manual',
    'source_url_raw',
    's3_html_key_raw',
    'scraped_at_raw',
    
    # Manual notes
    'notes_manual',
    'manual_notes',
    
    # Lineage (76.1% coverage - HIGH VALUE)
    'parent_1_display',
    'parent_2_display',
    'parent_1_slug',
    'parent_2_slug',
    'grandparent_1_display',
    'grandparent_2_display',
    'grandparent_3_display',
    'grandparent_1_slug',
    'grandparent_2_slug',
    'grandparent_3_slug',
    'lineage_formula',
    'lineage_depth',
    'generation_clean',
    'filial_generation',
    'selfed_generation',
    'backcross_generation',
    
    # Genetics metadata
    'genetics_type_clean',
    'indica_percentage_clean',
    'sativa_percentage_clean',
    'is_autoflower_clean',
    'seed_type_raw',
    
    # Botanical data (RAW - for Phase 12+ cleaning)
    'thc_min_raw',
    'thc_max_raw',
    'thc_content_raw',
    'cbd_min_raw',
    'cbd_max_raw',
    'cbd_content_raw',
    'cbn_content_raw',
    'flowering_time_days_clean',
    'height_indoor_cm_clean',
    'height_outdoor_cm_clean',
    'yield_indoor_g_m2_clean',
    'yield_outdoor_g_plant_clean',
    'effects_all_raw',
    'flavors_all_raw',
    'terpenes_raw',
    'climate_raw',
    'difficulty_raw',
]

# Filter to existing columns only
keep_cols = [c for c in keep_cols if c in df.columns]
df_clean = df[keep_cols].copy()

print(f"Clean: {len(df_clean):,} rows, {len(df_clean.columns)} columns")
print(f"Removed: {len(df.columns) - len(df_clean.columns)} columns")

# Save
df_clean.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nSaved to: {output_file}")

# Show what we kept
print("\nColumns kept:")
print(f"  Identity: 9")
print(f"  Lineage: 16")
print(f"  Genetics: 5")
print(f"  Botanical (raw): 18")
print(f"  Total: {len(keep_cols)}")
