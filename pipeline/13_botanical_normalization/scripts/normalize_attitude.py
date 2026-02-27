import pandas as pd
import re

def parse_thc_cbd(value):
    if pd.isna(value) or value == '': return None, None, None
    value = str(value).strip()
    nums = re.findall(r'(\d+(?:\.\d+)?)', value.replace(',', '.'))
    if not nums: return None, None, None
    nums = [float(n) for n in nums]
    if len(nums) == 1: return nums[0], nums[0], nums[0]
    return min(nums), max(nums), sum(nums)/len(nums)

def parse_flowering(value):
    if pd.isna(value) or value == '': return None, None, None
    value = str(value).lower().strip()
    nums = re.findall(r'(\d+(?:\.\d+)?)', value)
    if not nums: return None, None, None
    nums = [float(n) for n in nums]
    mult = 7 if 'week' in value else 1
    nums = [n * mult for n in nums]
    if len(nums) == 1: return nums[0], nums[0], nums[0]
    return min(nums), max(nums), sum(nums)/len(nums)

def parse_height(value):
    if pd.isna(value) or value == '': return None, None
    value = str(value).strip()
    nums = re.findall(r'(\d+(?:\.\d+)?)', value)
    if not nums: return None, None
    nums = [float(n) for n in nums]
    if 'ft' in value.lower() or "'" in value:
        nums = [n * 30.48 for n in nums]
    if len(nums) == 1: return nums[0], nums[0]
    return min(nums), max(nums)

def parse_yield(value):
    if pd.isna(value) or value == '': return None, None
    value = str(value).strip()
    nums = re.findall(r'(\d+(?:\.\d+)?)', value)
    if not nums: return None, None
    nums = [float(n) for n in nums]
    if len(nums) == 1: return nums[0], nums[0]
    return min(nums), max(nums)

# Read Attitude data
df = pd.read_csv('../input/remove/botanical_attitude.csv', encoding='latin-1')
print(f"Loaded {len(df)} Attitude strains")

# THC
df[['thc_min','thc_max','thc_avg']] = df['thc_raw'].apply(lambda x: pd.Series(parse_thc_cbd(x)))

# CBD
df[['cbd_min','cbd_max','cbd_avg']] = df['cbd_raw'].apply(lambda x: pd.Series(parse_thc_cbd(x)))

# Flowering
df[['flowering_days_min','flowering_days_max','flowering_days_avg']] = df['flowering_time_raw'].apply(lambda x: pd.Series(parse_flowering(x)))

# Height Indoor
df[['height_indoor_cm_min','height_indoor_cm_max']] = df['height_indoor_raw'].apply(lambda x: pd.Series(parse_height(x)))

# Height Outdoor
df[['height_outdoor_cm_min','height_outdoor_cm_max']] = df['height_outdoor_raw'].apply(lambda x: pd.Series(parse_height(x)))

# Yield Indoor
df[['yield_indoor_g_m2_min','yield_indoor_g_m2_max']] = df['yield_indoor_raw'].apply(lambda x: pd.Series(parse_yield(x)))

# Yield Outdoor
df[['yield_outdoor_g_plant_min','yield_outdoor_g_plant_max']] = df['yield_outdoor_raw'].apply(lambda x: pd.Series(parse_yield(x)))

# Save
df.to_csv('../output/botanical_attitude_normalized.csv', index=False, encoding='latin-1')

# Coverage report
print("\n=== COVERAGE REPORT ===")
print(f"THC: {df['thc_min'].notna().sum()} / {len(df)} ({df['thc_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"CBD: {df['cbd_min'].notna().sum()} / {len(df)} ({df['cbd_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Flowering: {df['flowering_days_min'].notna().sum()} / {len(df)} ({df['flowering_days_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Height Indoor: {df['height_indoor_cm_min'].notna().sum()} / {len(df)} ({df['height_indoor_cm_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Height Outdoor: {df['height_outdoor_cm_min'].notna().sum()} / {len(df)} ({df['height_outdoor_cm_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Yield Indoor: {df['yield_indoor_g_m2_min'].notna().sum()} / {len(df)} ({df['yield_indoor_g_m2_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Yield Outdoor: {df['yield_outdoor_g_plant_min'].notna().sum()} / {len(df)} ({df['yield_outdoor_g_plant_min'].notna().sum()/len(df)*100:.1f}%)")
print("\nAttitude normalized successfully")
