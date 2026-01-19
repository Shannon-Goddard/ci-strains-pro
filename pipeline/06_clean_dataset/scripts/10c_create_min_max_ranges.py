import pandas as pd
import re
from pathlib import Path

# Paths
input_file = Path('../output/10b_thc_cbd_cleaned.csv')
output_file = Path('../output/10c_min_max_ranges_created.csv')
report_file = Path('../output/10c_min_max_ranges_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

stats = {
    'flowering_time_split': 0,
    'height_indoor_split': 0,
    'height_outdoor_split': 0,
    'yield_indoor_split': 0,
    'yield_outdoor_split': 0
}

# Parse range from raw field
def parse_range(val):
    if pd.isna(val): return None, None
    
    val_str = str(val).strip()
    
    # Look for range pattern (e.g., "8-10", "8 - 10", "8 to 10")
    match = re.search(r'(\d+(?:\.\d+)?)\s*[-to]+\s*(\d+(?:\.\d+)?)', val_str)
    if match:
        return float(match.group(1)), float(match.group(2))
    
    # Single value
    match = re.search(r'(\d+(?:\.\d+)?)', val_str)
    if match:
        val = float(match.group(1))
        return val, val
    
    return None, None

# Flowering time min/max
if 'flowering_time_raw' in df.columns:
    ranges = df['flowering_time_raw'].apply(parse_range)
    df['flowering_time_min_days_clean'] = ranges.apply(lambda x: x[0] * 7 if x[0] else None)
    df['flowering_time_max_days_clean'] = ranges.apply(lambda x: x[1] * 7 if x[1] else None)
    stats['flowering_time_split'] = df['flowering_time_min_days_clean'].notna().sum()
    
    # Delete old column
    if 'flowering_time_days_clean' in df.columns:
        df = df.drop(columns=['flowering_time_days_clean'])

# Height indoor min/max
if 'height_indoor_raw' in df.columns:
    ranges = df['height_indoor_raw'].apply(parse_range)
    df['height_indoor_min_cm_clean'] = ranges.apply(lambda x: x[0])
    df['height_indoor_max_cm_clean'] = ranges.apply(lambda x: x[1])
    stats['height_indoor_split'] = df['height_indoor_min_cm_clean'].notna().sum()
    
    # Delete old column
    if 'height_indoor_cm_clean' in df.columns:
        df = df.drop(columns=['height_indoor_cm_clean'])

# Height outdoor min/max
if 'height_outdoor_raw' in df.columns:
    ranges = df['height_outdoor_raw'].apply(parse_range)
    df['height_outdoor_min_cm_clean'] = ranges.apply(lambda x: x[0])
    df['height_outdoor_max_cm_clean'] = ranges.apply(lambda x: x[1])
    stats['height_outdoor_split'] = df['height_outdoor_min_cm_clean'].notna().sum()
    
    # Delete old column
    if 'height_outdoor_cm_clean' in df.columns:
        df = df.drop(columns=['height_outdoor_cm_clean'])

# Yield indoor min/max
if 'yield_indoor_raw' in df.columns:
    ranges = df['yield_indoor_raw'].apply(parse_range)
    df['yield_indoor_min_g_m2_clean'] = ranges.apply(lambda x: x[0])
    df['yield_indoor_max_g_m2_clean'] = ranges.apply(lambda x: x[1])
    stats['yield_indoor_split'] = df['yield_indoor_min_g_m2_clean'].notna().sum()
    
    # Delete old column
    if 'yield_indoor_g_m2_clean' in df.columns:
        df = df.drop(columns=['yield_indoor_g_m2_clean'])

# Yield outdoor min/max
if 'yield_outdoor_raw' in df.columns:
    ranges = df['yield_outdoor_raw'].apply(parse_range)
    df['yield_outdoor_min_g_plant_clean'] = ranges.apply(lambda x: x[0])
    df['yield_outdoor_max_g_plant_clean'] = ranges.apply(lambda x: x[1])
    stats['yield_outdoor_split'] = df['yield_outdoor_min_g_plant_clean'].notna().sum()
    
    # Delete old column
    if 'yield_outdoor_g_plant_clean' in df.columns:
        df = df.drop(columns=['yield_outdoor_g_plant_clean'])

# Delete total_grow_time_days_clean (unnecessary)
if 'total_grow_time_days_clean' in df.columns:
    df = df.drop(columns=['total_grow_time_days_clean'])

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 10C: Min/Max Range Creation Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n\n")
    f.write("Ranges created:\n")
    f.write(f"  Flowering time min/max: {stats['flowering_time_split']}\n")
    f.write(f"  Height indoor min/max: {stats['height_indoor_split']}\n")
    f.write(f"  Height outdoor min/max: {stats['height_outdoor_split']}\n")
    f.write(f"  Yield indoor min/max: {stats['yield_indoor_split']}\n")
    f.write(f"  Yield outdoor min/max: {stats['yield_outdoor_split']}\n")
    f.write(f"\nColumns deleted: flowering_time_days_clean, height_indoor_cm_clean, height_outdoor_cm_clean, yield_indoor_g_m2_clean, yield_outdoor_g_plant_clean, total_grow_time_days_clean\n")

print(f"\n[SUCCESS] Step 10C complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Total ranges created: {sum(stats.values())}")
