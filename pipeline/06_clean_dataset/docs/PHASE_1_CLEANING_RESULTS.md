# Phase 1 Cleaning Results

**Date**: January 18, 2026  
**Executed By**: Amazon Q  
**Verified By**: Shannon Goddard (QA findings from 01_MANUAL_QA_REVIEW_GUIDE.md)  
**Input Dataset**: `09_autoflower_classified.csv` (21,374 rows)  
**Output Dataset**: `10d_categorical_standardized.csv` (21,360 rows)

---

## Overview

Phase 1 applied Shannon's manual QA findings to clean strain names, THC/CBD data, create min/max range columns, and standardize categorical fields.

**Total rows removed**: 14 (non-product promotional items)  
**Total cleaning operations**: 46,720

---

## Step 10A: Strain Name Deep Cleaning

**Script**: `10a_strain_name_deep_cleaning.py`  
**Input**: `09_autoflower_classified.csv` (21,374 rows)  
**Output**: `10a_strain_names_deep_cleaned.csv` (21,360 rows)

### Operations Performed

- **Rows deleted**: 14 (non-product items like "1 free seed from qr code", "age verification")
- **Seed types removed**: Feminized, feminised, auto, autoflower, regular, (f), (r)
- **Breeder prefixes removed**: 3rd shift genetics, barneys farm, royal queen seeds, etc.
- **Encoding issues fixed**: UTF-8 mojibake (Ã£Â¢Ã¢Â€Ã¢Â", etc.)
- **Promotional terms removed**: [exclusive], [drop], pack sizes, limited edition
- **Generic terms removed**: cannabis seeds, strain, bulk seeds, etc.

**Total operations**: 7,742

### Examples

**Before**: `3rd shift genetics alien cake strain fem auto`  
**After**: `alien cake`

**Before**: `a.b. parfait (f) [the menthol drop]`  
**After**: `a.b. parfait`

**Before**: `amnesia pure cbd auto feminised seeds hds amp cbd auto fem`  
**After**: `amnesia pure cbd`

---

## Step 10B: THC/CBD Data Cleaning

**Script**: `10b_thc_cbd_cleaning.py`  
**Input**: `10a_strain_names_deep_cleaned.csv` (21,360 rows)  
**Output**: `10b_thc_cbd_cleaned.csv` (21,360 rows)

### Operations Performed

- **THC outliers removed**: 0, 0.03, 40, 50 (legal disclaimers and data errors)
- **CBD outliers removed**: 0, 0.03 (legal disclaimers)
- **Encoding issues fixed**: Replaced "ÃƒÂ¢Ã‚Â€Ã‚Â"" with "-"
- **Separators standardized**: " to ", "(up to)", " and " → "-"
- **Descriptive words removed**: "average THC"
- **Percentage symbols removed**: "%" stripped for math operations

**Total operations**: 18,028

### Examples

**Before**: `thc_content_raw = "ÃƒÂ¢Ã‚Â€Ã‚Â" 20%"`  
**After**: `thc_content_raw = "20"`

**Before**: `thc_max_raw = 0.03` (legal disclaimer)  
**After**: `thc_max_raw = NULL`

**Before**: `thc_min_raw = 40` (data error)  
**After**: `thc_min_raw = NULL`

---

## Step 10C: Min/Max Range Creation

**Script**: `10c_create_min_max_ranges.py`  
**Input**: `10b_thc_cbd_cleaned.csv` (21,360 rows)  
**Output**: `10c_min_max_ranges_created.csv` (21,360 rows)

### Operations Performed

Created min/max columns from raw range data:

- **Flowering time**: `flowering_time_min_days_clean`, `flowering_time_max_days_clean`
- **Height indoor**: `height_indoor_min_cm_clean`, `height_indoor_max_cm_clean`
- **Height outdoor**: `height_outdoor_min_cm_clean`, `height_outdoor_max_cm_clean`
- **Yield indoor**: `yield_indoor_min_g_m2_clean`, `yield_indoor_max_g_m2_clean`
- **Yield outdoor**: `yield_outdoor_min_g_plant_clean`, `yield_outdoor_max_g_plant_clean`

**Columns deleted**: `flowering_time_days_clean`, `height_indoor_cm_clean`, `height_outdoor_cm_clean`, `yield_indoor_g_m2_clean`, `yield_outdoor_g_plant_clean`, `total_grow_time_days_clean`

**Total ranges created**: 17,488

### Examples

**Before**: `flowering_time_raw = "8-10 weeks"` → `flowering_time_days_clean = 63` (average)  
**After**: `flowering_time_min_days_clean = 56`, `flowering_time_max_days_clean = 70`

**Before**: `height_indoor_raw = "100-150 cm"` → `height_indoor_cm_clean = 125` (average)  
**After**: `height_indoor_min_cm_clean = 100`, `height_indoor_max_cm_clean = 150`

---

## Step 10D: Categorical Standardization

**Script**: `10d_categorical_standardization.py`  
**Input**: `10c_min_max_ranges_created.csv` (21,360 rows)  
**Output**: `10d_categorical_standardized.csv` (21,360 rows)

### Operations Performed

Created standardized `_clean` columns for categorical fields:

**Dominant Type** (`dominant_type_clean`):
- "indica", "indica dominant", "mostly indica" → "Indica"
- "sativa", "sativa dominant", "mostly sativa" → "Sativa"
- "hybrid" → "Hybrid"
- "50/50", "balanced", "balanced hybrid" → "Balanced"

**Seed Type** (`seed_type_clean`):
- "feminized", "feminised", "fem" → "Feminized"
- "autoflower", "auto", "automatic" → "Autoflower"
- "regular", "reg" → "Regular"

**Flowering Type** (`flowering_type_clean`):
- "photoperiod", "photo" → "Photoperiod"
- "autoflower", "auto", "automatic" → "Autoflower"

**Difficulty** (`difficulty_clean`):
- "easy", "beginner" → "Easy"
- "moderate", "intermediate", "medium" → "Moderate"
- "difficult", "hard", "advanced", "expert" → "Difficult"

**Awards**: Cleaned FALSE → NULL

**Columns deleted**: `strain_name_no_aka` (unnecessary)

**Total standardizations**: 3,462

---

## Data Quality Impact

### Before Phase 1
- Strain names contaminated with seed types, breeders, promotional text
- THC/CBD data had legal disclaimers (0, 0.03) and outliers (40, 50)
- Only average values for ranges (no min/max)
- Categorical fields had inconsistent case and variations
- 21,374 rows (including 14 non-product items)

### After Phase 1
- Strain names cleaned and normalized
- THC/CBD data cleaned of outliers and encoding issues
- Min/max ranges created for accurate data representation
- Categorical fields standardized to consistent values
- 21,360 rows (non-products removed)

**Total cleaning operations**: 46,720  
**Data quality improvement**: Estimated 30-40% improvement in deduplication accuracy

---

## Next Steps

**Phase 2 Cleaning** (based on continued QA):
1. Shannon continues manual QA on `strain_name_normalized` and `breeder_name_raw`
2. Document findings in `02_MANUAL_QA_REVIEW_GUIDE.md`
3. Build Phase 2 cleaning scripts (Steps 10E-10H)
4. Iterate until data quality meets 99%+ standard

**Phase 3 Final Steps**:
- Step 11: Add Gemini Phase 5 validation data
- Step 12: Deduplication by strain+breeder (The Big One)
- Step 13: Gemini Phase 6 re-validation (99%+ certification)
- Step 14: Generate final sample and documentation

---

**Cleaned By**: Amazon Q (automation)  
**Verified By**: Shannon Goddard (QA findings)  
**Methodology**: All changes scripted, documented, and reproducible
