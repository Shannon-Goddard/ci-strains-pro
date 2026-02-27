# Pipeline 16: Final Cleanup & Production Ready

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Context: Where We Are

### Pipeline 15 Completed
✅ Consolidated old (Pipeline 11) and new (Pipeline 13) botanical data  
✅ Shannon manually reviewed **12,899 conflicts** (73% kept OLD, 27% kept NEW)  
✅ Applied all conflict resolutions  
✅ Added missing min/max columns (flowering, height, yield)  

**Current dataset:** `pipeline_15_final.csv` - 21,210 strains, 74 columns

---

## Pipeline 16 Objective

**Create the final production-ready dataset** by:
1. Auditing all columns for coverage and value
2. Deleting low-value columns (<5% coverage or no user demand)
3. Validating data quality (outliers, nulls, data types)
4. Creating data dictionary and metadata
5. Exporting final production CSV

**This is the FINAL dataset before discussing more/less data.**

---

## Input

**File:** `pipeline/16_final_cleanup/input/pipeline_15_final.csv`
- **Strains:** 21,210
- **Columns:** 74
- **Status:** Conflict-resolved, all botanical columns present

---

## Tasks

### Task 1: Column Coverage Audit

**Generate coverage report for ALL 74 columns:**
- Column name
- Non-null count
- Coverage percentage
- Data type
- Sample values (first 5 non-null)

**Output:** `column_coverage_report.csv`

**Decision criteria:**
- **<5% coverage** → DELETE (not worth keeping)
- **5-20% coverage** → FLAG as "incomplete" in metadata, keep for now
- **>20% coverage** → KEEP

### Task 2: Botanical Column Validation

**Check for outliers in botanical data:**

**THC:**
- Flag if thc_min > thc_max
- Flag if thc_avg not between min/max
- Flag if any value >40% (outlier)
- Flag if min/max/avg all present but inconsistent

**CBD:**
- Same checks as THC
- Flag if >30% (outlier)

**Flowering:**
- Flag if <20 days or >150 days (outlier)
- Flag if min > max

**Height:**
- Flag if <10cm or >400cm (outlier)
- Flag if min > max

**Yield:**
- Flag if <50g or >2000g (outlier for indoor)
- Flag if <100g or >5000g (outlier for outdoor)
- Flag if min > max

**Output:** `botanical_outliers.csv` - strains with suspicious values

### Task 3: Identity Column Validation

**Check critical identity columns:**
- `strain_id` - no nulls, all unique
- `strain_name_display` - no nulls
- `seed_bank_display` - no nulls
- `breeder_name_clean` - check coverage

**Output:** `identity_validation_report.txt`

### Task 4: Column Deletion

**Delete columns based on audit:**

**Definitely delete (<5% coverage):**
- TBD based on coverage audit

**Consider deleting (low user value):**
- `is_fast_flowering` - 100% coverage but low demand
- `is_regular_flowering` - 100% coverage but low demand
- Any `_raw` columns still present
- Any duplicate/redundant columns

**Output:** `pipeline_16_cleaned.csv`

### Task 5: Data Dictionary

**Create comprehensive data dictionary:**

For each column in final dataset:
- Column name
- Data type
- Description (what it means)
- Coverage percentage
- Example values
- Notes (e.g., "incomplete data", "outliers flagged")

**Output:** `data_dictionary.csv`

### Task 6: Final Validation

**Run final checks:**
- Row count: 21,210 (no loss)
- No duplicate strain_ids
- All botanical values are numeric (or null)
- No negative values in botanical fields
- Coverage summary for key fields (THC, CBD, flowering)

**Output:** `final_validation_report.txt`

---

## Expected Results

### Final Dataset
- **File:** `pipeline_16_production_ready.csv`
- **Strains:** 21,210
- **Columns:** ~60-65 (deleted ~10-15 low-value columns)

### Key Coverage (Expected)
- THC min/max: 62%+
- THC avg: 48%+
- CBD: 20-35%
- Flowering: 58%+
- Height indoor: 27%+
- Yield indoor: 30%+

### Quality Improvements
- All outliers flagged for review
- All low-coverage columns removed or flagged
- Data dictionary for every column
- Full validation report

---

## Pipeline 15 Summary (For Context)

### What Happened in Pipeline 15

**Step 1: Consolidation**
- Merged old (Pipeline 11) and new (Pipeline 13) botanical columns
- Created single clean columns, preferring NEW data
- Flagged 12,899 conflicts where old/new differed significantly

**Step 2: Manual Review**
- Shannon reviewed all 12,899 conflicts
- Marked each as "old_value" or "new_value"
- Results: 73% kept OLD, 27% kept NEW

**Step 3: Apply Overrides**
- Applied all 12,899 decisions
- Created `pipeline_15_consolidated_reviewed.csv`

**Step 4: Add Missing Columns**
- Added 6 missing min/max columns from botanical_master.csv
- Final: `pipeline_15_final.csv` (21,210 strains, 74 columns)

### Column Naming Pattern (Important!)

**OLD columns (from Pipeline 11):** End with `_raw` or `_clean`
- Example: `thc_content_raw`, `flowering_time_days_clean`

**NEW columns (from Pipeline 13):** Clean names with `_min`, `_max`, `_avg`
- Example: `thc_avg`, `flowering_days_min`

**After consolidation:** Only clean names remain (no `_raw` or `_clean` suffixes)

---

## Key Columns in Dataset

### Identity (100% coverage)
- `strain_id` - Unique identifier
- `strain_name_display` - Clean strain name
- `seed_bank_display` - Seed bank name
- `breeder_name_clean` - Breeder name (some nulls)

### Genetics (~76% coverage)
- `lineage_parent1`, `lineage_parent2` - Parent strains
- `sativa_percentage`, `indica_percentage` - Genetics breakdown

### Cannabinoids (20-62% coverage)
- `thc_min`, `thc_max`, `thc_avg`
- `cbd_min`, `cbd_max`, `cbd_avg`

### Growing Specs (16-58% coverage)
- `flowering_days_min`, `flowering_days_max`, `flowering_days_avg`
- `height_indoor_cm_min`, `height_indoor_cm_max`
- `height_outdoor_cm_min`, `height_outdoor_cm_max`
- `yield_indoor_g_m2_min`, `yield_indoor_g_m2_max`
- `yield_outdoor_g_plant_min`, `yield_outdoor_g_plant_max`

### Flowering Type (100% coverage)
- `is_auto_flowering`
- `is_feminized_flowering`
- `is_fast_flowering`
- `is_regular_flowering`

---

## Execution Steps

1. **Load** `pipeline_15_final.csv`
2. **Generate** column coverage audit
3. **Validate** botanical data (outliers, min/max consistency)
4. **Validate** identity columns (nulls, uniqueness)
5. **Delete** low-coverage columns (<5%)
6. **Create** data dictionary
7. **Run** final validation
8. **Save** `pipeline_16_production_ready.csv`

---

## Success Criteria

✅ All columns have >5% coverage (or are flagged/deleted)  
✅ No outliers in botanical data (or flagged for review)  
✅ No null strain_ids or strain names  
✅ Data dictionary covers every column  
✅ Final validation report shows no errors  
✅ Dataset is ready for Shannon to review and approve  

---

## After Pipeline 16

**Shannon will decide:**
- Is this dataset good enough to launch?
- Do we need more data (re-scrape, new seed banks)?
- Do we need less data (delete more columns)?

**This is the FINAL PRODUCT for review.**

---

## Files You'll Create

1. `column_coverage_report.csv` - Coverage audit for all 74 columns
2. `botanical_outliers.csv` - Strains with suspicious botanical values
3. `identity_validation_report.txt` - Identity column checks
4. `pipeline_16_cleaned.csv` - After deleting low-coverage columns
5. `data_dictionary.csv` - Comprehensive column documentation
6. `final_validation_report.txt` - Final quality checks
7. `pipeline_16_production_ready.csv` - FINAL DATASET
8. `methodology.md` - Documentation of what you did

---

## Notes

- Use `latin-1` encoding for all CSV operations
- Preserve row count: 21,210 strains (no deletions)
- Be aggressive with column deletion (<5% coverage = delete)
- Flag outliers but don't auto-delete (Shannon will review)
- This is the FINAL dataset - make it perfect

**Logic designed by Amazon Q, verified by Shannon Goddard.**
