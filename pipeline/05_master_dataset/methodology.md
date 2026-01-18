# Methodology: Master Dataset Pipeline

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Purpose
Consolidate 21,706 strains from 20 seed banks into a unified master dataset with standardized schema and quality scoring.

## Data Integrity Rules
- **Never overwrite raw data** - All original columns preserved with `_raw` suffix
- **Always create cleaned versions** - Standardized data uses `_cleaned` suffix
- **Latin-1 encoding** - Handles special characters from cannabis breeder names

## Pipeline Steps

### 01: Column Analysis ✅
**Script**: `01_column_analysis.py`  
**Input**: 23 CSV files from seed bank extractions  
**Output**: 
- `column_analysis.json` - Full column inventory per seed bank
- `column_frequency.txt` - Column occurrence across all files

**Results**:
- 1,848 unique columns across all files
- 0 universal columns (none in all files)
- 58 common columns (in 10+ files)

### 02: Column Mapping ✅
**Script**: `02_column_mapping.py`  
**Input**: Column analysis results  
**Output**:
- `column_mapping.json` - 1,156 column mappings to 35 unified fields
- `excluded_columns.json` - 236 commercial columns excluded
- `unmapped_columns.json` - 1,773 metadata columns (not botanical)

**Logic**:
1. Map column variations to unified schema (e.g., `thc_content`, `spec_thc`, `thc_level` → `thc_content_raw`)
2. Exclude all commercial data (prices, SKUs, package sizes, availability)
3. Preserve only botanical and cultivation intelligence

**Legal Compliance**: All commercial/transactional data excluded to maintain educational/research use position

### 03: Merge Raw ✅
**Script**: `03_merge_raw.py`  
**Input**: 23 seed bank CSVs + column mappings  
**Output**: `master_strains_raw.csv`

**Results**:
- **23,009 strains** consolidated
- **37 columns**: 35 botanical fields + strain_id + seed_bank
- **Zero commercial data** included

**Logic**:
1. Load each CSV with latin-1 encoding
2. Apply column mappings to unified schema
3. Skip all excluded commercial columns
4. Generate UUID for each strain
5. Combine into single master dataset

### 04: Clean Data (Planned)
**Script**: `04_clean_data.py`  
**Purpose**: Apply extraction patterns to create `_cleaned` columns:
- **Genetics**: Extract Sativa/Indica percentages using `(\d+)%\s*Sativa` pattern
- **Cannabinoids**: Parse THC/CBD ranges into `_min`, `_max`, `_avg` columns
- **Lineage**: Detect "Cross:", "Genetics:", "Parents:" patterns

### 05: Quality Scoring (Planned)
**Script**: `05_quality_scoring.py`  
**Purpose**: Calculate completeness and quality metrics per strain

### 06: Validation (Planned)
**Script**: `06_validate_master.py`  
**Purpose**: Final validation and statistics report

## Master Dataset Schema (37 Columns)

**Core Identity (3)**:
- `strain_id` - UUID
- `seed_bank` - Source attribution
- `strain_name_raw` - Primary name

**Genetics (7)**:
- `genetics_lineage_raw` - Parent strains
- `sativa_percentage_raw` - Sativa %
- `indica_percentage_raw` - Indica %
- `dominant_type_raw` - Sativa/Indica/Hybrid
- `is_hybrid_raw` - Boolean flag
- `breeder_name_raw` - Original breeder
- `generation_raw` - F1, F2, etc.

**Cannabinoids (8)**:
- `thc_content_raw` - THC as scraped
- `thc_min_raw`, `thc_max_raw`, `thc_range_raw`, `thc_average_raw`
- `cbd_content_raw` - CBD as scraped
- `cbd_min_raw`, `cbd_max_raw`, `cbd_range_raw`
- `cbn_content_raw` - CBN content

**Effects & Flavors (3)**:
- `effects_all_raw` - All effects
- `flavors_all_raw` - All flavors/aromas
- `terpenes_raw` - Terpene profile

**Cultivation (11)**:
- `flowering_time_raw` - Flowering period
- `flowering_type_raw` - Photoperiod/Auto
- `seed_type_raw` - Feminized/Regular/Auto
- `yield_indoor_raw`, `yield_outdoor_raw`
- `height_indoor_raw`, `height_outdoor_raw`, `height_raw`
- `difficulty_raw` - Grow difficulty
- `climate_raw` - Suitable climates
- `suitable_environments_raw` - Indoor/outdoor/greenhouse
- `total_grow_time_raw` - Seed to harvest

**Other (5)**:
- `awards_raw` - Cannabis Cup wins
- `description_raw` - Strain overview

## Extraction Patterns (For Future Cleaning)

### Genetics
- **Sativa**: `(\d+)%\s*Sativa`
- **Indica**: `(\d+)%\s*Indica`
- **Lineage**: Detect "Cross:", "Genetics:", or "Parents:" followed by "X"

### Cannabinoids
- **THC Range**: `THC[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%`
- **Single Values**: Create `_min` = `_max` = value, `_avg` = value
- **Ranges**: Calculate `_avg` as mean of min/max

## Naming Conventions
- **Files**: `lowercase_with_underscores.csv`
- **Columns**: `field_name_raw` or `field_name_cleaned`
- **Output**: `master_strains.csv`, `master_strains_cleaned.csv`

## Data Quality Summary

**Coverage by Seed Bank**:
- Attitude: 7,673 strains, 25 fields
- Crop King: 3,336 strains, 26 fields
- North Atlantic: 2,727 strains, 25 fields
- Gorilla: 2,009 strains, 16 fields
- Neptune: 1,995 strains, 18 fields
- Seedsman: 1,744 strains (2 versions), 22 fields
- Multiverse Beans: 528 strains, 22 fields
- Herbies: 753 strains, 17 fields
- Sensi Seeds: 620 strains, 26 fields
- Seed Supreme: 353 strains, 26 fields
- ILGM: 302 strains (3 versions), 12 fields
- Mephisto: 245 strains, 13 fields
- Exotic: 227 strains, 2 fields
- Amsterdam: 163 strains, 16 fields
- Dutch Passion: 119 strains, 25 fields
- Barney's Farm: 88 strains, 21 fields
- Royal Queen: 67 strains, 21 fields
- Seeds Here Now: 43 strains, 12 fields
- Great Lakes: 16 strains, 7 fields
- Compound: 1 strain, 4 fields

**Total**: 23,009 strains across 20 seed banks

## Attribution
- **Architecture & Scripts**: Amazon Q
- **Domain Expertise & Verification**: Shannon Goddard (19 years cannabis industry)
- **Data Sources**: 20 seed banks, 23,009 strains
- **Extraction Period**: January 2026
- **Legal Compliance**: Commercial data excluded, botanical/educational data only
