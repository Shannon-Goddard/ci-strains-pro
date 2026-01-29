# Phase 7: Data Cleaning Pipeline

**Status**: ✅ COMPLETE  
**Started**: January 25, 2026  
**Completed**: January 25, 2026  
**Goal**: Clean and normalize master dataset before strain name extraction

---

## Overview

This phase applies 9 sequential cleaning steps to the master dataset, preparing it for strain name extraction and deduplication. Each step builds on the previous, progressively improving data quality.

---

## Input Files

- `input/master_strains_raw.csv` - 23,000 strains from Phase 5

---

## Cleaning Pipeline

### Step 1: Remove Duplicate URLs
**Script**: `01_remove_duplicate_urls.py`  
**Input**: 23,000 rows  
**Output**: 21,374 rows  
**Removed**: 1,626 rows (878 Seedsman HTML + 748 duplicate URLs)  
**Result**: `output/01_deduped_urls.csv`

### Step 2: Unit Normalization
**Script**: `02_unit_normalization.py`  
**Input**: 21,374 rows  
**Conversions**: 17,665 (THC%, CBD%, flowering time, height, yield)  
**Result**: `output/02_unit_normalized.csv`

### Step 3: Placeholder Removal
**Script**: `03_placeholder_removal.py`  
**Input**: 21,374 rows  
**Removed**: 67 placeholders ("N/A", "Unknown", "TBD", etc.)  
**Result**: `output/03_placeholders_removed.csv`

### Step 4: Data Type Standardization
**Script**: `04_data_type_standardization.py`  
**Input**: 21,374 rows  
**Converted**: 4 columns (numeric types, boolean flags)  
**Result**: `output/04_data_types_standardized.csv`

### Step 5: Genetics Normalization
**Script**: `05_genetics_normalization.py`  
**Input**: 21,374 rows  
**Enhancements**: 3,919 (parent extraction, cross detection, lineage parsing)  
**Result**: `output/05_genetics_normalized.csv`

### Step 6: Strain Name Normalization
**Script**: `06_strain_name_normalization.py`  
**Input**: 21,374 rows  
**Identified**: 3,052 potential duplicates (similar names, spelling variations)  
**Result**: `output/06_strain_names_normalized.csv`

### Step 7: AKA Extraction
**Script**: `07_aka_extraction.py`  
**Input**: 21,374 rows  
**Extracted**: 27 AKA names (alternate strain names)  
**Result**: `output/07_aka_extracted.csv`

### Step 8: Similar Spelling Normalization
**Script**: `08_similar_spelling_normalization.py`  
**Input**: 21,374 rows  
**Matched**: 42 additional similar spellings  
**Result**: `output/08_similar_spelling_normalized.csv`

### Step 9: Autoflower Classification
**Script**: `09_autoflower_classification.py`  
**Input**: 21,374 rows  
**Identified**: 3,944 autoflower strains  
**Result**: `output/09_autoflower_classified.csv`

---

## Final Output

**File**: `output/09_autoflower_classified.csv`  
**Rows**: 21,374 strains  
**Status**: Cleaned and ready for Phase 8 (Strain Name Extraction)

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Initial Rows | 23,000 |
| Final Rows | 21,374 |
| Rows Removed | 1,626 |
| Unit Conversions | 17,665 |
| Placeholders Removed | 67 |
| Genetics Enhancements | 3,919 |
| Potential Duplicates | 3,052 |
| AKA Names | 27 |
| Similar Spellings | 42 |
| Autoflowers | 3,944 |

---

## Reports Generated

All steps generate detailed reports in `output/`:
- `01_url_dedup_report.txt`
- `02_unit_normalization_report.txt`
- `03_placeholder_removal_report.txt`
- `04_data_type_report.txt`
- `05_genetics_normalization_report.txt`
- `06_strain_name_normalization_report.txt`
- `07_aka_extraction_report.txt`
- `08_similar_spelling_report.txt`
- `09_autoflower_classification_report.txt`

---

## Next Steps

1. ✅ Complete all 9 cleaning steps
2. ⏳ Phase 8: Strain Name Extraction (similar to Phase 6 breeder extraction)
3. ⏳ Phase 9: Final Deduplication & Master Dataset

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
