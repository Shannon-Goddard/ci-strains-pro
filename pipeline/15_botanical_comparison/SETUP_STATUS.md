# Pipeline 15 Setup Status

## ✅ Directory Structure Created
- `pipeline/15_botanical_comparison/input/` (ready for files)
- `pipeline/15_botanical_comparison/output/` (empty, will be populated)
- `pipeline/15_botanical_comparison/scripts/` (empty, will be created during execution)

## 📋 README Complete
- Comprehensive context from Pipelines 11-14
- **IMPORTANT:** Old data is already in Pipeline 14 (from Pipeline 11)
- Consolidation strategy (compare old vs new columns within same file)
- Conflict detection thresholds
- Best-of-both merge logic
- Coverage improvement expectations
- Validation checklist

## 🔄 Next Steps for Shannon

1. **Copy Pipeline 14 output to Pipeline 15 input:**
   ```
   Copy: pipeline/14_botanical_merge/output/pipeline_14_final.csv
   To: pipeline/15_botanical_comparison/input/pipeline_14_final.csv
   ```
   ✅ **DONE** (Shannon confirmed)

2. **Start new chat and say:**
   ```
   "Execute Pipeline 15. The old botanical data is already in pipeline_14_final.csv 
   (columns from Pipeline 11). Compare old columns vs new columns (from Pipeline 13) 
   and consolidate into single clean columns."
   ```

## 📊 Expected Results

**Input:**
- Pipeline 14: 21,210 strains, 95 columns
- OLD columns (from Pipeline 11): `thc_content_raw`, `flowering_time_days_clean`, etc.
- NEW columns (from Pipeline 13): `thc_avg`, `flowering_days_avg`, etc.

**Output:**
- Pipeline 15: 21,210 strains, ~60-70 columns (reduced by consolidating duplicates)
- Coverage improved by filling gaps with old data
- Conflicts flagged: 50-500 strains for manual review
- Comparison report: Old vs new coverage stats

## 🎯 Goal
Consolidate duplicate botanical columns (old from Pipeline 11, new from Pipeline 13) into single clean columns, taking the best of both.

---

**Setup complete. Ready for execution.**
