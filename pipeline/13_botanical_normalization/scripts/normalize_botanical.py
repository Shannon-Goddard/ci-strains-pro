import pandas as pd
import re
import numpy as np

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

def normalize_botanical(input_path, output_path):
    df = pd.read_csv(input_path, encoding='latin-1')
    
    # THC
    if 'thc_raw' in df.columns:
        df[['thc_min','thc_max','thc_avg']] = df['thc_raw'].apply(lambda x: pd.Series(parse_thc_cbd(x)))
    
    # CBD
    if 'cbd_raw' in df.columns:
        df[['cbd_min','cbd_max','cbd_avg']] = df['cbd_raw'].apply(lambda x: pd.Series(parse_thc_cbd(x)))
    
    # Flowering
    if 'flowering_time_raw' in df.columns:
        df[['flowering_days_min','flowering_days_max','flowering_days_avg']] = df['flowering_time_raw'].apply(lambda x: pd.Series(parse_flowering(x)))
    
    # Height Indoor
    if 'height_indoor_raw' in df.columns:
        df[['height_indoor_cm_min','height_indoor_cm_max']] = df['height_indoor_raw'].apply(lambda x: pd.Series(parse_height(x)))
    
    # Height Outdoor
    if 'height_outdoor_raw' in df.columns:
        df[['height_outdoor_cm_min','height_outdoor_cm_max']] = df['height_outdoor_raw'].apply(lambda x: pd.Series(parse_height(x)))
    
    # Yield Indoor
    if 'yield_indoor_raw' in df.columns:
        df[['yield_indoor_g_m2_min','yield_indoor_g_m2_max']] = df['yield_indoor_raw'].apply(lambda x: pd.Series(parse_yield(x)))
    
    # Yield Outdoor
    if 'yield_outdoor_raw' in df.columns:
        df[['yield_outdoor_g_plant_min','yield_outdoor_g_plant_max']] = df['yield_outdoor_raw'].apply(lambda x: pd.Series(parse_yield(x)))
    
    df.to_csv(output_path, index=False, encoding='latin-1')
    print(f"✓ {output_path.split('/')[-1]}: {len(df)} strains")

if __name__ == '__main__':
    banks = ['attitude','crop_king','north_atlantic','gorilla','neptune','herbies','amsterdam','ilgm',
             'barneys_farm','dutch_passion','exotic','great_lakes_genetics','mephisto_genetics',
             'multiverse_beans_seed_bank','royal_queen_seeds','seed_supreme','seeds_here_now','seedsman','sensi_seeds']
    
    for bank in banks:
        inp = f'../input/remove/botanical_{bank}.csv'
        out = f'../output/botanical_{bank}_normalized.csv'
        try:
            normalize_botanical(inp, out)
        except Exception as e:
            print(f"✗ {bank}: {e}")
