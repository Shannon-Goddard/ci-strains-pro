# Pipeline 14: Botanical Data Merge

Merge all normalized botanical CSVs from Pipeline 13, then merge with the main dataset from Pipeline 11.

## Status
🔄 **READY TO START** - Setup complete, awaiting execution

---

## CRITICAL CONTEXT FOR NEW CHAT

### What Happened Before This Pipeline

**Pipeline 11** = Main dataset with 21,220 verified strains (identity columns: strain_name, breeder, seed_bank)

**Pipeline 12** = Extracted raw botanical data from HTML (THC, flowering, height, yield) into 19 separate CSVs by seed bank

**Pipeline 13** = Normalized raw botanical text into clean numeric columns:
- Processed 9 seed banks (18,792 strains)
- Added `_min`, `_max`, `_avg` columns for ranges
- Converted units (weeks→days, feet→cm)
- Preserved all `*_raw` columns
- **Shannon reviewed and approved** - only a couple of fixes needed

### What This Pipeline Does

**Step 1:** Merge 9 normalized botanical CSVs into one master botanical file
**Step 2:** Merge master botanical file with Pipeline 11 main dataset by `strain_id`
**Result:** Single dataset with identity + botanical data (21,220 strains)

---

## Input Files

### From Pipeline 13 (9 normalized CSVs)
Location: `pipeline/13_botanical_normalization/output/`

1. **botanical_attitude_normalized.csv** (7,661 strains)
   - THC: 27.2%, Flowering: 61.4%, Height: 3-4%, Yield: 8%
   
2. **botanical_crop_king_normalized.csv** (3,332 strains)
   - THC: 99.4%, Flowering: 99.9%, Height: 99.5%, Yield: 95%+
   - **BEST DATA QUALITY**
   
3. **botanical_north_atlantic_normalized.csv** (2,717 strains)
   - No THC/CBD, Flowering: 77.4%, Height: 22%, Yield: 33%
   
4. **botanical_gorilla_normalized.csv** (1,967 strains)
   - THC: 58.6%, Flowering: 57.6%, Yield: 69.2%
   
5. **botanical_neptune_normalized.csv** (1,982 strains)
   - **NO BOTANICAL DATA** (lineage only)
   
6. **botanical_herbies_normalized.csv** (753 strains)
   - THC: 94.4%, Flowering: 97.6%, Height: 8.9%
   
7. **botanical_amsterdam_normalized.csv** (159 strains)
   - THC: 98.7%, Flowering: 97.5%
   
8. **botanical_ilgm_normalized.csv** (133 strains)
   - THC: 98.5% only
   
9. **botanical_barneys_farm_normalized.csv** (88 strains)
   - **0% COVERAGE** (empty values)

**Total: 18,792 strains with normalized botanical columns**

### From Pipeline 11 (Main Dataset)
Location: `pipeline/11_manual_review_and_validation/output/`

- **pipeline_11_final.csv** (21,220 strains)
  - Identity columns: strain_id, strain_name, breeder, seed_bank
  - 100% verified identity data
  - This is the master dataset

---

## Normalized Columns to Merge

Each normalized CSV has these columns (some may be NULL depending on seed bank):

### Cannabinoid Columns
- `thc_min`, `thc_max`, `thc_avg` (numeric, percentage)
- `cbd_min`, `cbd_max`, `cbd_avg` (numeric, percentage)

### Flowering Time Columns
- `flowering_days_min`, `flowering_days_max`, `flowering_days_avg` (numeric, days)

### Height Columns
- `height_indoor_cm_min`, `height_indoor_cm_max` (numeric, centimeters)
- `height_outdoor_cm_min`, `height_outdoor_cm_max` (numeric, centimeters)

### Yield Columns
- `yield_indoor_g_m2_min`, `yield_indoor_g_m2_max` (numeric, grams per square meter)
- `yield_outdoor_g_plant_min`, `yield_outdoor_g_plant_max` (numeric, grams per plant)

### Raw Columns (varies by seed bank)
- `thc_raw`, `cbd_raw`, `flowering_time_raw`, `flowering_raw`
- `height_raw`, `height_indoor_raw`, `height_outdoor_raw`
- `yield_raw`, `yield_indoor_raw`, `yield_outdoor_raw`
- Plus: `genetics_raw`, `lineage_raw`, `terpene_profile_raw`, `flavor_profile_raw`, etc.

**IMPORTANT:** Column names vary by seed bank. Some have `flowering_time_raw`, others have `flowering_raw`. Handle this carefully.

---

## Merge Strategy

### Step 1: Merge 9 Botanical CSVs

**Goal:** Create `botanical_master.csv` with all 18,792 strains

**Approach:**
1. Read all 9 normalized CSVs
2. Identify all unique columns across all files
3. Concatenate with `pd.concat()`, filling missing columns with NULL
4. Keep `strain_id` as the key
5. Validate: 18,792 rows, no duplicates

**Output:** `output/botanical_master.csv`

### Step 2: Merge with Pipeline 11

**Goal:** Create `pipeline_14_final.csv` with all 21,220 strains

**Approach:**
1. Read `pipeline_11_final.csv` (21,220 strains)
2. Read `botanical_master.csv` (18,792 strains)
3. Left join: Pipeline 11 LEFT JOIN botanical_master ON strain_id
4. Result: 21,220 rows (all strains keep identity data, 18,792 get botanical data)
5. Strains without botanical data will have NULL in botanical columns

**Output:** `output/pipeline_14_final.csv`

---

## Data Integrity Rules

### Must Preserve
- **All 21,220 strains** from Pipeline 11 (never drop strains)
- **All identity columns** from Pipeline 11 (strain_name, breeder, seed_bank)
- **All raw botanical columns** (never delete source data)
- **strain_id** as the primary key

### Must Validate
- No duplicate strain_ids in botanical_master.csv
- All strain_ids in botanical_master exist in Pipeline 11
- Row count: Pipeline 14 = 21,220 (same as Pipeline 11)
- Column count: Pipeline 11 columns + botanical columns

### Encoding
- Use `latin-1` encoding for all CSV operations (handles special breeder characters)

---

## Expected Output Structure

### botanical_master.csv
- **Rows:** 18,792 strains
- **Columns:** strain_id + all normalized columns + all raw columns from 9 seed banks
- **Key:** strain_id (unique)

### pipeline_14_final.csv
- **Rows:** 21,220 strains
- **Columns:** All Pipeline 11 columns + all botanical columns
- **Key:** strain_id (unique)
- **Coverage:** 18,792 strains with botanical data, 2,428 strains with NULL botanical data

---

## Validation Checklist

After merge, validate:

1. **Row counts:**
   - botanical_master.csv = 18,792 rows
   - pipeline_14_final.csv = 21,220 rows

2. **No duplicates:**
   - `strain_id` is unique in both files

3. **No data loss:**
   - All Pipeline 11 strains present in Pipeline 14
   - All botanical data from Pipeline 13 present in botanical_master

4. **NULL handling:**
   - 2,428 strains have NULL botanical data (expected)
   - Neptune (1,982) and Barneys Farm (88) mostly NULL (expected)

5. **Column integrity:**
   - All identity columns from Pipeline 11 preserved
   - All normalized columns present (even if mostly NULL)

---

## Files Structure

```
14_botanical_merge/
├── input/                     # (empty - references other pipelines)
├── output/
│   ├── botanical_master.csv  # Step 1 output (18,792 strains)
│   └── pipeline_14_final.csv # Step 2 output (21,220 strains)
├── scripts/
│   ├── merge_botanical.py    # Step 1: Merge 9 CSVs
│   ├── merge_with_main.py    # Step 2: Merge with Pipeline 11
│   └── validate_merge.py     # Validation checks
├── methodology.md             # Merge logic and results
└── README.md                  # This file
```

---

## Key Insights for Implementation

### Column Name Variations
Different seed banks use different column names:
- `flowering_time_raw` vs `flowering_raw`
- `height_raw` vs `height_indoor_raw` + `height_outdoor_raw`
- `yield_raw` vs `yield_indoor_raw` + `yield_outdoor_raw`

**Solution:** When merging, collect ALL unique column names and let pandas fill missing columns with NULL.

### Seed Banks with No Data
- **Neptune:** Only has `lineage_raw`, all botanical columns are NULL
- **Barneys Farm:** Has columns but all values are NULL (0% coverage)

**Solution:** Include them in merge anyway (preserves strain_id mapping).

### Best Data Quality
**Crop King** has 99% coverage across all fields. Use it as the quality benchmark.

### Coverage Expectations
After merge, expect:
- **THC data:** ~40-50% of 21,220 strains
- **Flowering data:** ~60-70% of 21,220 strains
- **Height data:** ~20-30% of 21,220 strains
- **Yield data:** ~30-40% of 21,220 strains

---

## Next Steps After Pipeline 14

1. **Vertex Audit** (optional) - AI validation of botanical columns
2. **Column Review** - Ensure all fields are correct
3. **Statistical Analysis** - Analyze THC ranges, flowering times, etc.
4. **Gumroad Launch Prep** - Clean dataset ready for marketplace

---

## Critical Notes

- **Shannon approved Pipeline 13** - only a couple of fixes needed
- **latin-1 encoding required** - special characters from breeders
- **Never drop strains** - all 21,220 must remain
- **Preserve raw columns** - source data traceability
- **Left join only** - Pipeline 11 is the master

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
