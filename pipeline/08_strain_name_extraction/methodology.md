# Phase 8: Strain Name Extraction - Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Overview

Extract clean strain names from 21,361 strains across 19 seed banks using URL pattern analysis, breeder detection, and keyword removal.

---

## Approach

### 1. URL Pattern Analysis
- Documented URL structure for each seed bank
- Identified breeder name placement (prefix, suffix, or embedded)
- Cataloged seed type markers (auto, feminized, regular)
- Noted generation markers (F1, BX, S1)

### 2. Extraction Strategies

**Simple Pattern Removal** (9 seed banks):
- Amsterdam, ILGM, Sensi Seeds, Seed Supreme, Gorilla
- Dutch Passion, Seedsman, Barney's Farm, Mephisto
- Remove keywords: autoflower, feminized, seeds, strain
- Clean slug → title case

**Breeder Prefix Matching** (5 seed banks):
- Attitude, North Atlantic, Neptune, Multiverse, Crop King
- Build prefix list from actual URLs (3+ occurrences)
- Match longest prefix first
- Remove once to preserve strain numbers

**Breeder Suffix Matching** (2 seed banks):
- Herbies, Seeds Here Now
- Build suffix list from URL endings
- Remove breeder names at end

**Special Cases** (3 seed banks):
- Royal Queen: Remove 3-digit product codes
- Exotic Genetix: Filter out box-set URLs
- Great Lakes: Manual review recommended (no clear pattern)

### 3. Helper Functions

**extraction_helpers.py** provides:
- `get_url_slug()`: Extract path segments
- `slug_to_name()`: Convert hyphens to spaces
- `smart_title_case()`: Preserve acronyms (OG, CBD, THC)
- `build_breeder_prefixes()`: Dynamic prefix detection
- `build_breeder_suffixes()`: Dynamic suffix detection

---

## Execution

### Individual Scripts
Each seed bank has dedicated extraction script:
- `extract_attitude.py` (7,673 strains)
- `extract_cropking.py` (3,336 strains)
- `extract_north_atlantic.py` (2,727 strains)
- `extract_gorilla.py` (2,000 strains)
- `extract_neptune.py` (1,995 strains)
- `extract_seedsman.py` (866 strains)
- `extract_herbies.py` (753 strains)
- `extract_multiverse_beans.py` (518 strains)
- `extract_seed_supreme.py` (353 strains)
- `extract_mephisto_genetics.py` (245 strains)
- `extract_exotic.py` (216 strains)
- `extract_amsterdam.py` (163 strains)
- `extract_ilgm.py` (133 strains)
- `extract_sensi_seeds.py` (115 strains)
- `extract_barneys_farm.py` (88 strains)
- `extract_royal_queen_seeds.py` (67 strains)
- `extract_dutch_passion.py` (54 strains)
- `extract_seeds_here_now.py` (43 strains)
- `extract_great_lakes_genetics.py` (16 strains)

### Merge
`merge_all_banks.py` combines all 19 outputs into single master CSV

---

## Output Format

**File**: `all_strains_extracted.csv`

**Columns**:
- All original columns from input
- `strain_name_extracted`: Clean strain name

---

## Quality Checks

1. **Completeness**: All 21,361 strains processed (100% success)
2. **Accuracy**: Manual review performed on each seed bank
3. **Consistency**: Title case, no breeder names in strain field
4. **Edge Cases**: Numbers preserved (Project 4516, Haze 13, Auto 1)
5. **Auto Handling**: "Auto" removed from end unless at start of name

---

## Results

**Total Strains**: 21,361  
**Seed Banks**: 19  
**Scripts Created**: 20 (19 extractors + 1 merge)  
**Success Rate**: 100%  
**Output File**: `output/all_strains_extracted.csv`

## Next Steps

Phase 9: Cross-bank strain matching and deduplication
