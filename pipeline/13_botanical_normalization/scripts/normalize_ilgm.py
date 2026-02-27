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

df = pd.read_csv('../input/remove/botanical_ilgm.csv', encoding='latin-1')
print(f"Loaded {len(df)} ILGM strains")

df[['thc_min','thc_max','thc_avg']] = df['thc_raw'].apply(lambda x: pd.Series(parse_thc_cbd(x)))
df['cbd_min'] = None
df['cbd_max'] = None
df['cbd_avg'] = None
df['flowering_days_min'] = None
df['flowering_days_max'] = None
df['flowering_days_avg'] = None
df['height_indoor_cm_min'] = None
df['height_indoor_cm_max'] = None
df['height_outdoor_cm_min'] = None
df['height_outdoor_cm_max'] = None
df['yield_indoor_g_m2_min'] = None
df['yield_indoor_g_m2_max'] = None
df['yield_outdoor_g_plant_min'] = None
df['yield_outdoor_g_plant_max'] = None

df.to_csv('../output/botanical_ilgm_normalized.csv', index=False, encoding='latin-1')

print("\n=== COVERAGE REPORT ===")
print(f"THC: {df['thc_min'].notna().sum()} / {len(df)} ({df['thc_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"CBD: {df['cbd_min'].notna().sum()} / {len(df)} ({df['cbd_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Flowering: {df['flowering_days_min'].notna().sum()} / {len(df)} ({df['flowering_days_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Height Indoor: {df['height_indoor_cm_min'].notna().sum()} / {len(df)} ({df['height_indoor_cm_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Height Outdoor: {df['height_outdoor_cm_min'].notna().sum()} / {len(df)} ({df['height_outdoor_cm_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Yield Indoor: {df['yield_indoor_g_m2_min'].notna().sum()} / {len(df)} ({df['yield_indoor_g_m2_min'].notna().sum()/len(df)*100:.1f}%)")
print(f"Yield Outdoor: {df['yield_outdoor_g_plant_min'].notna().sum()} / {len(df)} ({df['yield_outdoor_g_plant_min'].notna().sum()/len(df)*100:.1f}%)")
print("\nILGM normalized successfully")
