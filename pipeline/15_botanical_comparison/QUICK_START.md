# Pipeline 15 Quick Start

## TL;DR for Next Amazon Q

**Task:** Consolidate duplicate botanical columns in pipeline_14_final.csv

**Why:** Pipeline 14 contains BOTH old botanical data (from Pipeline 11) and new botanical data (from Pipeline 13). We need to compare them and create single clean columns.

**Input:** 
- `pipeline/15_botanical_comparison/input/pipeline_14_final.csv` (21,210 strains, 95 columns)

**Output:**
- `comparison_report.txt` - Coverage stats (old vs new)
- `conflicts_flagged.csv` - Strains with significant differences
- `pipeline_15_consolidated.csv` - Final dataset with single clean columns (~60-70 columns)

---

## Column Pairs to Consolidate

### OLD (from Pipeline 11) → NEW (from Pipeline 13)

**THC:**
- `thc_content_raw` → `thc_avg`
- `thc_min_raw` → `thc_min`
- `thc_max_raw` → `thc_max`

**CBD:**
- `cbd_content_raw` → `cbd_avg`
- `cbd_min_raw` → `cbd_min`
- `cbd_max_raw` → `cbd_max`

**Flowering:**
- `flowering_time_days_clean` → `flowering_days_avg`

**Height:**
- `height_indoor_cm_clean` → `height_indoor_cm_min`
- `height_outdoor_cm_clean` → `height_outdoor_cm_min`

**Yield:**
- `yield_indoor_g_m2_clean` → `yield_indoor_g_m2_min`
- `yield_outdoor_g_plant_clean` → `yield_outdoor_g_plant_min`

---

## Consolidation Logic

For each column pair:

1. **Only NEW has data** → Use NEW
2. **Only OLD has data** → Use OLD (fill gaps)
3. **Both have data, agree** → Use NEW (trust Pipeline 13 normalization)
4. **Both have data, conflict** → Use NEW, flag for review
5. **Neither has data** → NULL

**Conflict thresholds:**
- THC/CBD: >10% difference
- Flowering: >7 days difference
- Height: >20cm difference
- Yield: >100g difference

---

## Steps to Execute

1. Load `pipeline_14_final.csv`
2. Calculate coverage for old vs new columns
3. Compare values where both exist
4. Flag conflicts
5. Create `*_final` columns with consolidated data
6. Delete old and new columns (keep only `*_final`)
7. Save `pipeline_15_consolidated.csv`

---

## Expected Results

**Coverage improvement:**
- OLD THC: ~70% coverage (estimate)
- NEW THC: 35.6% coverage
- FINAL THC: ~75-80% coverage (best of both)

**Column reduction:**
- Pipeline 14: 95 columns
- Pipeline 15: ~60-70 columns (removed ~25-30 duplicate columns)

**Conflicts:**
- Estimate: 50-500 strains flagged for manual review

---

## Read the Full README

For complete context, read: `pipeline/15_botanical_comparison/README.md`

**Logic designed by Amazon Q, verified by Shannon Goddard.**
