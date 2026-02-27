# Pipeline 16 Quick Start

## TL;DR

**Task:** Final cleanup - audit columns, delete low-coverage fields, validate data, create production-ready dataset

**Input:** `pipeline_15_final.csv` (21,210 strains, 74 columns, conflict-resolved)

**Output:** `pipeline_16_production_ready.csv` (21,210 strains, ~60-65 columns, FINAL PRODUCT)

---

## Execute in Order

1. **Column coverage audit** → `column_coverage_report.csv`
2. **Botanical validation** → `botanical_outliers.csv`
3. **Identity validation** → `identity_validation_report.txt`
4. **Delete low-coverage columns** (<5%) → `pipeline_16_cleaned.csv`
5. **Create data dictionary** → `data_dictionary.csv`
6. **Final validation** → `final_validation_report.txt`
7. **Save final dataset** → `pipeline_16_production_ready.csv`

---

## Key Rules

- Delete columns with <5% coverage
- Flag outliers (THC >40%, flowering <20 or >150 days, etc.)
- Validate no null strain_ids or strain names
- Preserve 21,210 rows (no strain deletions)
- Use `latin-1` encoding

---

## Read Full README

For complete context: `pipeline/16_final_cleanup/README.md`

**Logic designed by Amazon Q, verified by Shannon Goddard.**
