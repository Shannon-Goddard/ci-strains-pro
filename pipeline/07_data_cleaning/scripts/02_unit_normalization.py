import pandas as pd
import re
from pathlib import Path

# Paths
input_file = Path('../output/01_deduped_urls.csv')
output_file = Path('../output/02_unit_normalized.csv')
report_file = Path('../output/02_unit_normalization_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8')
print(f"Initial rows: {len(df)}")

conversions = {
    'flowering_time': 0,
    'height_indoor': 0,
    'height_outdoor': 0,
    'yield_indoor': 0,
    'yield_outdoor': 0,
    'total_grow_time': 0
}

# Flowering time: weeks -> days
def normalize_flowering_time(val):
    if pd.isna(val): return None
    val = str(val).lower()
    # Extract weeks
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:week|wk|w)', val)
    if match:
        conversions['flowering_time'] += 1
        return float(match.group(1)) * 7
    # Already in days
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:day|d)', val)
    if match:
        return float(match.group(1))
    return None

# Height: ft/inches -> cm
def normalize_height(val):
    if pd.isna(val): return None
    val = str(val).lower()
    # Feet to cm
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:ft|feet|foot)', val)
    if match:
        conversions['height_indoor'] += 1
        return float(match.group(1)) * 30.48
    # Inches to cm
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:in|inch|inches|")', val)
    if match:
        conversions['height_indoor'] += 1
        return float(match.group(1)) * 2.54
    # Already in cm
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:cm)', val)
    if match:
        return float(match.group(1))
    return None

# Yield indoor: oz -> g/m²
def normalize_yield_indoor(val):
    if pd.isna(val): return None
    val = str(val).lower()
    # oz/ft² to g/m²
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:oz)', val)
    if match:
        conversions['yield_indoor'] += 1
        return float(match.group(1)) * 305.15  # 1 oz/ft² = 305.15 g/m²
    # Already in g/m²
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:g)', val)
    if match:
        return float(match.group(1))
    return None

# Yield outdoor: oz -> g/plant
def normalize_yield_outdoor(val):
    if pd.isna(val): return None
    val = str(val).lower()
    # oz to g
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:oz)', val)
    if match:
        conversions['yield_outdoor'] += 1
        return float(match.group(1)) * 28.35
    # Already in g
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:g)', val)
    if match:
        return float(match.group(1))
    return None

# Total grow time: weeks -> days
def normalize_total_grow_time(val):
    if pd.isna(val): return None
    val = str(val).lower()
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:week|wk|w)', val)
    if match:
        conversions['total_grow_time'] += 1
        return float(match.group(1)) * 7
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:day|d)', val)
    if match:
        return float(match.group(1))
    return None

# Apply conversions
if 'flowering_time_raw' in df.columns:
    df['flowering_time_days_clean'] = df['flowering_time_raw'].apply(normalize_flowering_time)

if 'height_indoor_raw' in df.columns:
    df['height_indoor_cm_clean'] = df['height_indoor_raw'].apply(normalize_height)

if 'height_outdoor_raw' in df.columns:
    df['height_outdoor_cm_clean'] = df['height_outdoor_raw'].apply(normalize_height)
    conversions['height_outdoor'] = conversions['height_indoor']

if 'yield_indoor_raw' in df.columns:
    df['yield_indoor_g_m2_clean'] = df['yield_indoor_raw'].apply(normalize_yield_indoor)

if 'yield_outdoor_raw' in df.columns:
    df['yield_outdoor_g_plant_clean'] = df['yield_outdoor_raw'].apply(normalize_yield_outdoor)

if 'total_grow_time_raw' in df.columns:
    df['total_grow_time_days_clean'] = df['total_grow_time_raw'].apply(normalize_total_grow_time)

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 02: Unit Normalization Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n\n")
    f.write("Conversions performed:\n")
    f.write(f"  Flowering time (weeks -> days): {conversions['flowering_time']}\n")
    f.write(f"  Height (ft/in -> cm): {conversions['height_indoor'] + conversions['height_outdoor']}\n")
    f.write(f"  Yield indoor (oz -> g/m²): {conversions['yield_indoor']}\n")
    f.write(f"  Yield outdoor (oz -> g/plant): {conversions['yield_outdoor']}\n")
    f.write(f"  Total grow time (weeks -> days): {conversions['total_grow_time']}\n")
    f.write(f"\nTotal conversions: {sum(conversions.values())}\n")

print(f"\n[SUCCESS] Step 02 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Total conversions: {sum(conversions.values())}")
