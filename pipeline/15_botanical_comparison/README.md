# Pipeline 15: Botanical Data Comparison (New vs Old)

Compare new botanical data (Pipeline 14) with old scrape botanical data, flag conflicts, and merge best-of-both.

## Status
🔄 **READY TO START** - Setup complete, awaiting execution

---

## CRITICAL CONTEXT FOR NEW CHAT

### What Happened Before This Pipeline

**Pipeline 11** = Main dataset with 21,210 verified strains (identity columns: strain_name, breeder, seed_bank)

**Pipeline 12** = Extracted raw botanical data from HTML (THC, flowering, height, yield) into 19 separate CSVs by seed bank

**Pipeline 13** = Normalized raw botanical text into clean numeric columns:
- Processed 9 seed banks (18,792 strains)
- Added `_min`, `_max`, `_avg` columns for ranges
- Converted units (weeks→days, feet→cm)
- Preserved all `*_raw` columns
- **Shannon reviewed and approved**

**Pipeline 14** = Merged all botanical data with main dataset:
- Step 1: Merged 9 botanical CSVs → botanical_master.csv (18,792 strains)
- Step 2: Merged with Pipeline 11 → pipeline_14_final.csv (21,210 strains, 95 columns)
- Coverage: THC 35.6%, CBD 17.2%, Flowering 57.3%, Height 23.7%, Yield 28.7%

### What This Pipeline Does

**IMPORTANT DISCOVERY:** The "old scrape botanical data" is already in Pipeline 11 (columns 36-52 in pipeline_11_final.csv). Pipeline 14 merged NEW botanical data from Pipeline 13 with Pipeline 11, so pipeline_14_final.csv contains BOTH old and new botanical data.

**Actual Goal:** Compare old botanical columns (from Pipeline 11) vs new botanical columns (from Pipeline 13) within the same dataset (pipeline_14_final.csv), identify which is better, and consolidate into single clean columns.

**Process:**
1. Load pipeline_14_final.csv (contains both old and new botanical data)
2. Identify old botanical columns (from Pipeline 11, e.g., `thc_content_raw`, `flowering_time_days_clean`)
3. Identify new botanical columns (from Pipeline 13, e.g., `thc_min`, `thc_max`, `thc_avg`)
4. Compare coverage: Which has more non-NULL values?
5. Compare quality: Which has better data format (normalized vs raw)?
6. Flag conflicts: Where both exist but differ significantly
7. Consolidate: Create final clean columns, delete redundant columns

**Result:** 
- `comparison_report.txt` - Coverage and quality comparison
- `conflicts_flagged.csv` - Strains with significant differences (for manual review)
- `pipeline_15_consolidated.csv` - Final dataset with single clean botanical columns (no duplicates)

---

## Input Files

### Pipeline 14 Final Dataset (Contains BOTH Old and New Data)
**Location:** `pipeline/15_botanical_comparison/input/`
- **File:** `pipeline_14_final.csv`
- **Rows:** 21,210 strains
- **Columns:** 95

**OLD Botanical Columns (from Pipeline 11, columns 36-52):**
- `thc_min_raw`, `thc_max_raw`, `thc_content_raw` (old THC data)
- `cbd_min_raw`, `cbd_max_raw`, `cbd_content_raw` (old CBD data)
- `flowering_time_days_clean` (old flowering data, already in days)
- `height_indoor_cm_clean`, `height_outdoor_cm_clean` (old height data, already in cm)
- `yield_indoor_g_m2_clean`, `yield_outdoor_g_plant_clean` (old yield data, already in g)
- Coverage: Unknown (need to calculate)

**NEW Botanical Columns (from Pipeline 13, columns 61-95):**
- `thc_min`, `thc_max`, `thc_avg` (7,550 strains, 35.6%)
- `cbd_min`, `cbd_max`, `cbd_avg` (3,640 strains, 17.2%)
- `flowering_days_min`, `flowering_days_max`, `flowering_days_avg` (12,157 strains, 57.3%)
- `height_indoor_cm_min`, `height_indoor_cm_max` (5,027 strains, 23.7%)
- `height_outdoor_cm_min`, `height_outdoor_cm_max`
- `yield_indoor_g_m2_min`, `yield_indoor_g_m2_max` (6,081 strains, 28.7%)
- `yield_outdoor_g_plant_min`, `yield_outdoor_g_plant_max`

**IMPORTANT:** Both old and new data are in the same file. No need to load separate files or merge on strain_id.

---

## Comparison Strategy

### Step 1: Load Data and Identify Columns
1. Load pipeline_14_final.csv
2. Identify OLD columns (from Pipeline 11):
   - `thc_min_raw`, `thc_max_raw`, `thc_content_raw`
   - `cbd_min_raw`, `cbd_max_raw`, `cbd_content_raw`
   - `flowering_time_days_clean`
   - `height_indoor_cm_clean`, `height_outdoor_cm_clean`
   - `yield_indoor_g_m2_clean`, `yield_outdoor_g_plant_clean`
3. Identify NEW columns (from Pipeline 13):
   - `thc_min`, `thc_max`, `thc_avg`
   - `cbd_min`, `cbd_max`, `cbd_avg`
   - `flowering_days_min`, `flowering_days_max`, `flowering_days_avg`
   - `height_indoor_cm_min`, `height_indoor_cm_max`
   - `height_outdoor_cm_min`, `height_outdoor_cm_max`
   - `yield_indoor_g_m2_min`, `yield_indoor_g_m2_max`
   - `yield_outdoor_g_plant_min`, `yield_outdoor_g_plant_max`

### Step 2: Calculate Coverage
For each field (THC, CBD, flowering, height, yield):
```python
old_thc_coverage = df['thc_content_raw'].notna().sum()
new_thc_coverage = df['thc_avg'].notna().sum()
```

### Step 3: Compare Values
For strains where BOTH old and new have data:
```python
both_have_data = df['thc_content_raw'].notna() & df['thc_avg'].notna()
comparison_subset = df[both_have_data]
comparison_subset['thc_diff'] = abs(comparison_subset['thc_avg'] - comparison_subset['thc_content_raw'])
```

### Step 4: Flag Conflicts
**Conflict criteria:**
- Both old and new have values (not NULL)
- Difference is >10% for THC/CBD
- Difference is >7 days for flowering time
- Difference is >20cm for height
- Difference is >100g for yield

### Step 5: Consolidate Columns
**Decision logic:**
1. **If only NEW has data:** Use new value
2. **If only OLD has data:** Use old value
3. **If both have data and agree:** Use new value (trust Pipeline 13 normalization)
4. **If both have data and conflict:** Flag for review, default to new value
5. **If neither has data:** NULL

**Create final columns:**
- `thc_min_final`, `thc_max_final`, `thc_avg_final`
- `cbd_min_final`, `cbd_max_final`, `cbd_avg_final`
- `flowering_days_min_final`, `flowering_days_max_final`, `flowering_days_avg_final`
- `height_indoor_cm_min_final`, `height_indoor_cm_max_final`
- `yield_indoor_g_m2_min_final`, `yield_indoor_g_m2_max_final`

**Delete redundant columns:**
- Drop all old columns (`*_raw`, `*_clean` from Pipeline 11)
- Drop all new columns (`thc_min`, `thc_max`, etc. from Pipeline 13)
- Keep only `*_final` columns

---

## Expected Output Files

### 1. comparison_report.txt
- **Content:** Coverage comparison (old vs new for each field)
- **Purpose:** Understand which data source is better
- **Example:**
  ```
  THC Coverage:
    Old (thc_content_raw): 15,000 strains (70.8%)
    New (thc_avg): 7,550 strains (35.6%)
    Both have data: 5,000 strains
    Only old: 10,000 strains
    Only new: 2,550 strains
    Conflicts (>10% diff): 150 strains
  ```

### 2. conflicts_flagged.csv
- **Rows:** Estimated 50-500 strains (depends on conflict threshold)
- **Columns:** strain_id, strain_name, seed_bank, field, old_value, new_value, difference
- **Purpose:** Manual review by Shannon

### 3. pipeline_15_consolidated.csv
- **Rows:** 21,210 strains
- **Columns:** ~60-70 (reduced from 95 by consolidating duplicate columns)
- **Purpose:** Final dataset with single clean botanical columns
- **Changes:**
  - Deleted: All old columns (`*_raw`, `*_clean` from Pipeline 11)
  - Deleted: All new columns (`thc_min`, `thc_max`, etc. from Pipeline 13)
  - Added: Final consolidated columns (`*_final`)
  - Result: ~25-30 columns removed

---

## Merge Logic (Best-of-Both)

### For Each Botanical Field:

**Scenario 1: Only new has data**
```python
if pd.notna(new_value) and pd.isna(old_value):
    merged_value = new_value
    source = 'new'
```

**Scenario 2: Only old has data**
```python
if pd.isna(new_value) and pd.notna(old_value):
    merged_value = old_value
    source = 'old'
```

**Scenario 3: Both have data, no conflict**
```python
if pd.notna(new_value) and pd.notna(old_value):
    if abs(new_value - old_value) <= threshold:
        merged_value = new_value  # Trust Pipeline 13 normalization
        source = 'new'
```

**Scenario 4: Both have data, conflict detected**
```python
if pd.notna(new_value) and pd.notna(old_value):
    if abs(new_value - old_value) > threshold:
        merged_value = new_value  # Default to new, flag for review
        source = 'new_conflict'
        flag_for_review = True
```

**Scenario 5: Neither has data**
```python
if pd.isna(new_value) and pd.isna(old_value):
    merged_value = None
    source = 'none'
```

---

## Conflict Thresholds

### THC/CBD
- **Threshold:** 10% difference
- **Example:** Old=20%, New=25% → Difference=5% (25% of 20%) → Flag for review

### Flowering Time
- **Threshold:** 7 days difference
- **Example:** Old=56 days, New=70 days → Difference=14 days → Flag for review

### Height
- **Threshold:** 20cm difference
- **Example:** Old=100cm, New=130cm → Difference=30cm → Flag for review

### Yield
- **Threshold:** 100g difference
- **Example:** Old=400g, New=550g → Difference=150g → Flag for review

---

## Data Integrity Rules

### Must Preserve
- **All 21,210 strains** from Pipeline 14 (never drop strains)
- **All identity columns** (strain_id, strain_name, breeder, seed_bank)
- **All Pipeline 14 columns** (even if replaced with old data)
- **strain_id** as the primary key

### Must Validate
- No duplicate strain_ids in final dataset
- Row count: Pipeline 15 = 21,210 (same as Pipeline 14)
- Coverage improvement: New coverage >= Pipeline 14 coverage (should increase by filling gaps with old data)

### Encoding
- Use `latin-1` encoding for all CSV operations (handles special breeder characters)

---

## Expected Coverage Improvement

Based on typical old scrape data:

**Before (Pipeline 14):**
- THC: 7,550 strains (35.6%)
- CBD: 3,640 strains (17.2%)
- Flowering: 12,157 strains (57.3%)
- Height: 5,027 strains (23.7%)
- Yield: 6,081 strains (28.7%)

**After (Pipeline 15 - estimated):**
- THC: 15,000-18,000 strains (70-85%) ← Significant improvement expected
- CBD: 5,000-8,000 strains (24-38%) ← Moderate improvement
- Flowering: 15,000-18,000 strains (70-85%) ← Moderate improvement
- Height: 8,000-12,000 strains (38-57%) ← Significant improvement
- Yield: 10,000-14,000 strains (47-66%) ← Significant improvement

**Goal:** Fill gaps in Pipeline 14 data with old scrape data while preserving high-quality Pipeline 13 normalized data.

---

## Validation Checklist

After merge, validate:

1. **Row count:**
   - pipeline_15_merged.csv = 21,210 rows (same as Pipeline 14)

2. **No duplicates:**
   - `strain_id` is unique

3. **Coverage improvement:**
   - THC coverage >= 35.6% (Pipeline 14 baseline)
   - Flowering coverage >= 57.3% (Pipeline 14 baseline)
   - Height coverage >= 23.7% (Pipeline 14 baseline)
   - Yield coverage >= 28.7% (Pipeline 14 baseline)

4. **Conflict report:**
   - Generate list of strains with significant differences
   - Estimate: 50-500 strains flagged for manual review

5. **Data quality:**
   - No negative values for THC, CBD, flowering, height, yield
   - THC/CBD values between 0-100%
   - Flowering time between 30-120 days (reasonable range)
   - Height between 30-300cm (reasonable range)

---

## Files Structure

```
15_botanical_comparison/
├── input/
│   └── pipeline_14_final.csv      # Contains both old and new data
├── output/
│   ├── comparison_report.txt      # Coverage comparison
│   ├── conflicts_flagged.csv      # Strains needing manual review
│   └── pipeline_15_consolidated.csv # Final consolidated dataset
├── scripts/
│   ├── compare_coverage.py        # Step 1: Calculate coverage
│   ├── flag_conflicts.py          # Step 2: Identify conflicts
│   ├── consolidate_columns.py     # Step 3: Merge and consolidate
│   └── validate_consolidation.py  # Step 4: Validation
├── methodology.md                  # Consolidation logic and results
└── README.md                       # This file
```

---

## Key Questions for Shannon

Before starting, confirm:

1. **Column mapping:**
   - OLD: `thc_content_raw` → NEW: `thc_avg` (correct?)
   - OLD: `flowering_time_days_clean` → NEW: `flowering_days_avg` (correct?)
   - OLD: `height_indoor_cm_clean` → NEW: `height_indoor_cm_min` (correct?)
   - OLD: `yield_indoor_g_m2_clean` → NEW: `yield_indoor_g_m2_min` (correct?)

2. **Merge preference:**
   - Default to new data (trust Pipeline 13 normalization)?
   - Or best-of-both (fill gaps with old data)?

3. **Conflict handling:**
   - How many conflicts are acceptable for manual review?
   - Should conflicts default to new or old?

4. **Column naming:**
   - Keep `*_final` suffix for consolidated columns?
   - Or rename to simpler names (e.g., `thc_avg_final` → `thc_avg`)?

5. **Old column format:**
   - Are old columns single values or ranges?
   - If single values, map to `*_avg` columns?
   - If ranges, map to `*_min` and `*_max` columns?

---

## Implementation Notes

### Column Mapping (Old → New)
Map old Pipeline 11 columns to new Pipeline 13 columns:
```python
column_pairs = [
    ('thc_content_raw', 'thc_avg'),  # Old single value → New average
    ('cbd_content_raw', 'cbd_avg'),  # Old single value → New average
    ('flowering_time_days_clean', 'flowering_days_avg'),  # Already in days
    ('height_indoor_cm_clean', 'height_indoor_cm_min'),  # Old single → New min
    ('height_outdoor_cm_clean', 'height_outdoor_cm_min'),  # Old single → New min
    ('yield_indoor_g_m2_clean', 'yield_indoor_g_m2_min'),  # Old single → New min
    ('yield_outdoor_g_plant_clean', 'yield_outdoor_g_plant_min'),  # Old single → New min
]
```

### Consolidation Logic
For each column pair:
```python
def consolidate_column(old_col, new_col):
    # Scenario 1: Only new has data
    mask1 = df[new_col].notna() & df[old_col].isna()
    df.loc[mask1, 'final_col'] = df.loc[mask1, new_col]
    
    # Scenario 2: Only old has data
    mask2 = df[new_col].isna() & df[old_col].notna()
    df.loc[mask2, 'final_col'] = df.loc[mask2, old_col]
    
    # Scenario 3: Both have data, no conflict
    mask3 = df[new_col].notna() & df[old_col].notna() & (abs(df[new_col] - df[old_col]) <= threshold)
    df.loc[mask3, 'final_col'] = df.loc[mask3, new_col]  # Trust new
    
    # Scenario 4: Both have data, conflict
    mask4 = df[new_col].notna() & df[old_col].notna() & (abs(df[new_col] - df[old_col]) > threshold)
    df.loc[mask4, 'final_col'] = df.loc[mask4, new_col]  # Default to new, flag for review
    
    # Scenario 5: Neither has data
    mask5 = df[new_col].isna() & df[old_col].isna()
    df.loc[mask5, 'final_col'] = None
```

### No Unit Conversions Needed
Both old and new data are already in the same units:
- Flowering: days (both)
- Height: cm (both)
- Yield: g/m² or g/plant (both)
- THC/CBD: percentage (both)

---

## Next Steps After Pipeline 15

### Pipeline 16: Column Audit
- Calculate coverage % for each column
- Delete columns with <5% coverage (not worth keeping)
- Keep columns with >20% coverage
- Review columns with 5-20% coverage (case-by-case)
- Consolidate duplicate columns (e.g., `seed_type_raw_x` vs `seed_type_raw_y`)

### Pipeline 17: Final Cleanup
- Delete all `*_raw` columns (archive separately)
- Rename columns for consistency
- Add column descriptions/metadata
- Final dataset: `pipeline_17_production_ready.csv`
- Ready for Gumroad launch

---

## Critical Notes

- **Shannon's approval required** before finalizing merge strategy
- **Manual review expected** for 50-500 conflicting strains
- **Coverage should improve** by filling gaps with old data
- **Trust Pipeline 13 normalization** for high-quality seed banks (Crop King, ILGM, Amsterdam, Herbies)
- **Preserve all strains** - never drop rows
- **latin-1 encoding required** - special characters from breeders

---

## Success Criteria

✅ All 21,210 strains preserved  
✅ Coverage improved (more non-NULL values)  
✅ Conflicts identified and flagged for review  
✅ Coverage report generated  
✅ Final merged dataset validated  
✅ No duplicate strain_ids  
✅ No data loss from Pipeline 14  

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
