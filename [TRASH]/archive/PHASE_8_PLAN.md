# Phase 8: Strain Name Extraction & Standardization - Detailed Plan

**Status**: 📋 PLANNED  
**Goal**: Extract clean strain names from 21,374 strains, similar to Phase 6 breeder extraction  
**Estimated Time**: 4-6 hours  
**Complexity**: High (multiple seed banks, varied naming patterns)

---

## Overview

Extract and standardize strain names from cleaned dataset (Phase 7 output). Each seed bank has unique naming patterns that need custom extraction logic.

---

## Input

**File**: `../07_data_cleaning/output/09_autoflower_classified.csv`  
**Rows**: 21,374 strains  
**Current State**: `strain_name_raw` column contains mixed data (breeder names, seed types, pack sizes, promo text)

---

## Extraction Strategy

### Approach (Same as Phase 6 Breeders)

1. **Pattern Documentation** (Shannon): Analyze strain name patterns for each seed bank
2. **Script Development** (Amazon Q): Build seed-bank-specific extraction scripts
3. **Iterative Testing** (Both): Run scripts, identify edge cases, improve patterns
4. **Merge & Standardize**: Combine all extractions, apply standardization rules
5. **Generate Lists**: Create A-Z lists for manual review

---

## Seed Bank Breakdown (21,374 strains)

| Seed Bank | Strains | Extraction Complexity | Notes |
|-----------|---------|----------------------|-------|
| Attitude | 7,673 | Medium | Remove breeder prefix, seed type suffix |
| Crop King | 3,336 | Low | Clean format, minimal noise |
| North Atlantic | 2,726 | Medium | Remove pack sizes, freebies |
| Gorilla | 2,000 | Medium | Remove breeder, feminized/auto tags |
| Neptune | 1,995 | Medium | Remove breeder prefix, strain codes |
| Seedsman (JS) | 866 | High | Mixed formats, promo text |
| Herbies | 753 | Medium | Remove breeder, seed counts |
| Sensi Seeds | 620 | Low | Clean format |
| Multiverse Beans | 528 | Medium | Remove breeder, product codes |
| Seed Supreme | 350 | Medium | Remove breeder, feminized tags |
| Mephisto Genetics | 245 | Low | Clean autoflower names |
| Exotic Genetix | 227 | Low | Clean format |
| Amsterdam | 163 | Low | Clean format |
| ILGM (JS) | 133 | Medium | Remove breeder, autoflower tags |
| Dutch Passion | 119 | Low | Clean format |
| Barney's Farm | 88 | Low | Clean format |
| Royal Queen Seeds | 67 | Low | Clean format |
| Seeds Here Now | 39 | Medium | Remove breeder suffix |
| Great Lakes | 16 | Medium | Remove breeder prefix |

---

## Extraction Patterns to Handle

### Common Noise to Remove:
- **Breeder names**: "Barney's Farm - Blue Gelato" → "Blue Gelato"
- **Seed types**: "OG Kush Feminized" → "OG Kush"
- **Pack sizes**: "Gorilla Glue (3 seeds)" → "Gorilla Glue"
- **Autoflower tags**: "Northern Lights Auto" → "Northern Lights" (keep auto flag separate)
- **Promo text**: "FREE SEED - Zkittlez" → "Zkittlez"
- **Product codes**: "GG4-FEM-5PK" → "GG4"
- **Encoding issues**: "Gelato 33 â€" Feminized" → "Gelato 33"

### Patterns to Preserve:
- **Strain numbers**: "Gelato 33", "AK-47", "G13"
- **Phenotypes**: "Purple Punch #2", "Wedding Cake S1"
- **Crosses**: "Blue Dream x Cookies"
- **Generations**: "F1", "F2", "BX1"

---

## Scripts to Create

### 1. Pattern Documentation
**File**: `docs/STRAIN_NAME_PATTERNS.md`  
**Owner**: Shannon  
**Content**: Sample URLs, HTML snippets, extraction patterns for each seed bank

### 2. Extraction Scripts (per seed bank)
**Files**: `scripts/extract_[seedbank].py` (19 scripts)  
**Owner**: Amazon Q  
**Logic**: Seed-bank-specific regex/parsing to extract clean strain names

### 3. Merge Script
**File**: `scripts/merge_all_strains.py`  
**Owner**: Amazon Q  
**Logic**: Combine all extractions into single CSV

### 4. Standardization Script
**File**: `scripts/standardize_strain_names.py`  
**Owner**: Amazon Q  
**Logic**: Apply manual review rules (capitalization, spacing, abbreviations)

### 5. List Generation
**File**: `scripts/generate_strain_list.py`  
**Owner**: Amazon Q  
**Output**: `STRAIN_LIST.md` (A-Z), `STRAIN_LIST_CLEANED.md` (A-Z)

---

## Expected Challenges

1. **Breeder Prefix Removal**: "Barney's Farm Blue Gelato" vs "Blue Gelato Barney's Farm"
2. **Autoflower Handling**: Keep "Auto" flag in separate column, remove from name
3. **Feminized/Regular Tags**: Remove from name, preserve in seed_type column
4. **Pack Sizes**: "(3 seeds)", "(5-pack)", "10pk" - all need removal
5. **Promo Text**: "FREE", "SALE", "NEW" - remove but log for review
6. **Encoding Issues**: Fix mojibake (â€", Ã©, etc.)
7. **Abbreviations**: "OG" vs "O.G.", "AK47" vs "AK-47" - standardize

---

## Success Criteria

- ✅ 100% extraction rate (all 21,374 strains have `strain_name_extracted`)
- ✅ Clean names (no breeder prefixes, seed types, pack sizes)
- ✅ Standardized format (consistent capitalization, spacing, punctuation)
- ✅ Autoflower flag preserved in separate column
- ✅ Manual review list generated (A-Z) for final QA
- ✅ Duplicate detection (identify similar names for deduplication)

---

## Output Files

### Extraction Results:
- `output/[seedbank]_strain_names.csv` (19 files)
- `output/all_strain_names_extracted.csv` (merged)

### Standardization:
- `output/all_strain_names_cleaned.csv` (standardized)

### Documentation:
- `STRAIN_LIST.md` (raw names, A-Z)
- `STRAIN_LIST_CLEANED.md` (standardized names, A-Z)
- `docs/STRAIN_NAME_PATTERNS.md` (extraction patterns)
- `docs/MANUAL_STRAIN_REVIEW.md` (standardization rules)

---

## Timeline

1. **Pattern Documentation** (Shannon): 1-2 hours
2. **Script Development** (Amazon Q): 2-3 hours (19 extraction scripts)
3. **Execution & Testing**: 30-60 minutes (run all scripts, fix edge cases)
4. **Manual Review** (Shannon): 1-2 hours (review A-Z list, create standardization rules)
5. **Standardization** (Amazon Q): 30 minutes (apply rules, generate cleaned list)

**Total**: 4-6 hours

---

## Next Steps After Phase 8

1. **Phase 9**: Final Deduplication (merge similar strains)
2. **Phase 10**: Master Dataset Assembly (combine all cleaned data)
3. **Phase 11**: Marketplace Launch (Gumroad, pricing tiers)

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
