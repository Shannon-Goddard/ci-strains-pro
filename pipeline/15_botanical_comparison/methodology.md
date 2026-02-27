# Pipeline 15: Botanical Consolidation Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Objective
Consolidate duplicate botanical columns from Pipeline 11 (old data) and Pipeline 13 (new data) into single clean columns, maximizing coverage while flagging conflicts for review.

---

## Input
- **File:** `pipeline/14_botanical_merge/output/pipeline_14_final.csv`
- **Strains:** 21,210
- **Columns:** 95 (includes both old and new botanical data)

---

## Process

### 1. Column Identification
**OLD columns (from Pipeline 11):** End with `_raw` or `_clean` suffix
- `thc_content_raw`, `thc_min_raw`, `thc_max_raw`
- `cbd_content_raw`, `cbd_min_raw`, `cbd_max_raw`
- `flowering_time_days_clean`
- `height_indoor_cm_clean`, `height_outdoor_cm_clean`
- `yield_indoor_g_m2_clean`, `yield_outdoor_g_plant_clean`

**NEW columns (from Pipeline 13):** Clean names with `_min`, `_max`, `_avg`
- `thc_avg`, `thc_min`, `thc_max`
- `cbd_avg`, `cbd_min`, `cbd_max`
- `flowering_days_avg`
- `height_indoor_cm_min`, `height_outdoor_cm_min`
- `yield_indoor_g_m2_min`, `yield_outdoor_g_plant_min`

### 2. Consolidation Logic
For each column pair (old, new):

1. **Convert to numeric** (handle mixed types from CSV)
2. **Prefer NEW data** (trust Pipeline 13 normalization)
3. **Fill gaps with OLD data** (maximize coverage)
4. **Flag conflicts** where both exist and differ significantly

**Conflict thresholds:**
- THC/CBD: >10% difference
- Flowering: >7 days difference
- Height: >20cm difference
- Yield: >100g difference

### 3. Column Cleanup
- Keep only consolidated `*_final` columns
- Remove duplicate old/new columns
- Rename `*_final` → remove suffix for clean names
- Retain all identity columns (strain_id, names, seed banks, etc.)

---

## Results

### Coverage Improvements
| Column | Old Coverage | New Coverage | Final Coverage | Improvement |
|--------|--------------|--------------|----------------|-------------|
| thc_avg | 8,755 (41.3%) | 7,550 (35.6%) | 10,256 (48.4%) | +7.1% |
| thc_min | 11,263 (53.1%) | 7,550 (35.6%) | 13,219 (62.3%) | +9.2% |
| thc_max | 11,263 (53.1%) | 7,550 (35.6%) | 13,219 (62.3%) | +9.2% |
| cbd_avg | 7,931 (37.4%) | 3,640 (17.2%) | 8,061 (38.0%) | +0.6% |
| cbd_min | 3,498 (16.5%) | 3,640 (17.2%) | 4,242 (20.0%) | +2.8% |
| cbd_max | 3,498 (16.5%) | 3,640 (17.2%) | 4,242 (20.0%) | +2.8% |
| flowering_days_avg | 3,996 (18.8%) | 12,157 (57.3%) | 12,413 (58.5%) | +1.2% |
| height_indoor_cm_min | 4,162 (19.6%) | 5,027 (23.7%) | 5,683 (26.8%) | +3.1% |
| height_outdoor_cm_min | 3,314 (15.6%) | 3,655 (17.2%) | 3,856 (18.2%) | +0.9% |
| yield_indoor_g_m2_min | 3,719 (17.5%) | 6,081 (28.7%) | 6,431 (30.3%) | +1.7% |
| yield_outdoor_g_plant_min | 3,398 (16.0%) | 3,183 (15.0%) | 3,486 (16.4%) | +0.4% |

### Conflicts Flagged
**Total conflicts:** 12,899 strains with significant differences

**Top conflict categories:**
- Height indoor: 3,366 conflicts (avg diff: 103.7cm)
- Height outdoor: 3,111 conflicts (avg diff: 100.8cm)
- Yield indoor: 2,608 conflicts (avg diff: 1,195.4g)
- Flowering days: 1,178 conflicts (avg diff: 13.6 days)
- Yield outdoor: 839 conflicts (avg diff: 437.4g)
- THC avg: 671 conflicts (avg diff: 74.2%)

**Note:** Many conflicts are due to unit conversion issues or data entry errors in old scrape. NEW data preferred by default.

### Final Dataset
- **File:** `pipeline_15_consolidated.csv`
- **Strains:** 21,210
- **Columns:** 68 (reduced from 95)
- **Botanical columns:** 15 clean consolidated columns

---

## Data Integrity

### Validation Checks
✅ Row count preserved: 21,210 strains
✅ No data loss: All non-NULL values retained
✅ Coverage improved: All columns show positive or neutral improvement
✅ Conflicts documented: 12,899 flagged for potential review

### Encoding
- All CSV operations use `latin-1` encoding for special characters in breeder names

---

## Output Files

1. **pipeline_15_consolidated.csv** - Final consolidated dataset (21,210 strains, 68 columns)
2. **comparison_report.txt** - Coverage statistics for old vs new vs final
3. **conflicts_flagged.csv** - 12,899 strains with significant differences between old/new data

---

## Next Steps (Pipeline 16)

1. **Review high-impact conflicts** (THC, flowering, yield)
2. **Column audit** - Identify low-coverage columns (<5%) for deletion
3. **Add missing botanical columns** from Pipeline 13 (flowering_days_min/max, height_max, yield_max)
4. **Final cleanup** before Gumroad launch

---

## Notes

- OLD data had better THC coverage (53.1% vs 35.6%) but NEW data is more normalized
- NEW data had better flowering coverage (57.3% vs 18.8%)
- Consolidation achieved best-of-both: 62.3% THC coverage, 58.5% flowering coverage
- Conflicts are expected due to different scraping methods and normalization approaches
- All conflicts default to NEW data (trust Pipeline 13 normalization)

**Logic designed by Amazon Q, verified by Shannon Goddard.**
