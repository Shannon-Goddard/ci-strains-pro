# Phase 6 Cleaning Pipeline Methodology

## Step 01: URL Deduplication + Seedsman HTML Cleanup

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Remove Seedsman HTML extraction (bad data) and deduplicate URLs to ensure each strain entry represents a unique source page.

### Problem Identified
Seedsman had two extractions in the raw dataset:
- `seedsman` (878 strains) - HTML extraction with poor data quality
- `seedsman_js` (866 strains) - JavaScript extraction with proper URLs and complete data

The HTML extraction was useless and needed to be removed entirely before deduplication.

### Methodology
1. Read raw dataset (23,000 strains)
2. **Remove entire Seedsman HTML seed bank** (`seed_bank = 'seedsman'`)
3. Keep Seedsman JS extraction (`seed_bank = 'seedsman_js'`)
4. Identify duplicates based on `source_url_raw` column
5. Keep first occurrence of each URL
6. Remove subsequent duplicates

### Results
- **Initial rows**: 23,000
- **Seedsman HTML removed**: 878 strains (bad extraction)
- **After Seedsman cleanup**: 22,122
- **Duplicate URLs found**: 748
- **Final rows**: 21,374
- **Total removed**: 1,626 rows (878 Seedsman HTML + 748 URL duplicates = 7.1%)

### Key Findings
- **Seedsman cleanup**: Removed 878 useless HTML extraction records, kept 866 good JS extraction records
- **URL duplicates breakdown**:
  - Dutch Passion: 66 duplicate URLs (2 occurrences each)
  - ILGM: 36 URLs with 3 occurrences each
  - Crop King: 300 duplicate URLs (2 occurrences each)
  - Barney's Farm: 88 duplicate URLs (2 occurrences each)
  - Multiverse Beans: ~271 duplicate URLs
  - Other seed banks: ~87 duplicates

### Data Quality Impact
- Eliminated 878 low-quality Seedsman HTML records
- Preserved 866 high-quality Seedsman JS records with proper URLs
- Eliminated 748 redundant entries from same source URLs
- Reduced dataset size by 7.1% while improving overall data quality
- Final dataset: 21,374 unique, high-quality strain records

### Seed Bank Distribution (After Cleanup)
- Attitude: 7,673 strains
- Crop King: 3,336 strains
- North Atlantic: 2,727 strains
- Gorilla: 2,000 strains
- Neptune: 1,995 strains
- **Seedsman JS**: 866 strains (HTML removed)
- Herbies: 753 strains
- Sensi Seeds: 620 strains
- Multiverse Beans: ~528 strains
- Other seed banks: ~876 strains

### Output Files
- `01_deduped_urls.csv` - Cleaned dataset (21,374 rows)
- `01_url_dedup_report.txt` - Detailed deduplication report

---

## Step 02: Unit Normalization

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Standardize all measurement units to consistent formats for data analysis and API responses.

### Conversion Rules
1. **Flowering time**: weeks → days (multiply by 7)
2. **Height**: feet/inches → centimeters (ft × 30.48, in × 2.54)
3. **Yield indoor**: oz/ft² → g/m² (multiply by 305.15)
4. **Yield outdoor**: oz → g/plant (multiply by 28.35)
5. **Total grow time**: weeks → days (multiply by 7)

### Methodology
1. Read deduplicated dataset (21,374 strains)
2. Apply regex pattern matching to extract numeric values and units
3. Convert to standardized units using conversion factors
4. Create new `_clean` columns with normalized values
5. Preserve original `_raw` columns for reference

### Results
- **Rows processed**: 21,374
- **Total conversions**: 17,665

**Breakdown**:
- Flowering time (weeks → days): 3,810 conversions
- Height (ft/in → cm): 12,802 conversions
- Yield indoor (oz → g/m²): 527 conversions
- Yield outdoor (oz → g/plant): 526 conversions
- Total grow time (weeks → days): 0 conversions (field not present)

### New Columns Created
- `flowering_time_days_clean` - Flowering time in days
- `height_indoor_cm_clean` - Indoor height in centimeters
- `height_outdoor_cm_clean` - Outdoor height in centimeters
- `yield_indoor_g_m2_clean` - Indoor yield in grams per square meter
- `yield_outdoor_g_plant_clean` - Outdoor yield in grams per plant
- `total_grow_time_days_clean` - Total grow time in days

### Data Quality Impact
- 17,665 values converted to standardized units (82.6% of relevant fields)
- All measurements now use consistent metric units
- Original raw values preserved for transparency
- Ready for mathematical operations (averaging, filtering, sorting)

### Output Files
- `02_unit_normalized.csv` - Dataset with normalized units (21,374 rows)
- `02_unit_normalization_report.txt` - Conversion statistics

---

## Step 03: Placeholder Removal

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Replace placeholder text values with NULL to improve data quality and enable proper statistical analysis.

### Placeholder Patterns Detected
- `n/a`, `na`, `not available`, `not specified`, `unknown`
- `tbd`, `tba`, `coming soon`, `contact us`
- `varies`, `variable`, `depends`, `multiple`
- `see description`, `-`, `--`, `---`, `none`, `null`, `nil`

### Methodology
1. Read unit-normalized dataset (21,374 strains)
2. Scan all `_raw` and `_clean` columns
3. Convert placeholder text to NULL values
4. Track replacements by column

### Results
- **Rows processed**: 21,374
- **Total placeholders removed**: 67
- **Affected columns**: 6

**Breakdown by column**:
- `cbd_content_raw`: 33 placeholders
- `genetics_lineage_raw`: 26 placeholders
- `yield_outdoor_raw`: 3 placeholders
- `thc_content_raw`: 2 placeholders
- `yield_indoor_raw`: 2 placeholders
- `source_url_raw`: 1 placeholder

### Data Quality Impact
- Removed 67 non-informative placeholder values (0.3% of fields)
- Converted placeholder text to proper NULL values
- Enables accurate completeness calculations
- Prevents placeholder text from contaminating analysis
- Most placeholders found in CBD content and genetics lineage fields

### Output Files
- `03_placeholders_removed.csv` - Dataset with NULL values (21,374 rows)
- `03_placeholder_removal_report.txt` - Removal statistics

---

## Step 04: Data Type Standardization

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Ensure all columns have appropriate data types for analysis and database storage.

### Data Type Rules
1. **Numeric fields**: Convert to float64 (THC/CBD percentages, measurements)
2. **Boolean fields**: Convert to bool (is_hybrid, etc.)
3. **Text fields**: Ensure string type (strain names, descriptions)
4. **Clean columns**: All `_clean` columns must be numeric

### Methodology
1. Read placeholder-removed dataset (21,374 strains)
2. Identify columns by naming pattern and content
3. Apply appropriate type conversions with error handling
4. Track all type changes

### Results
- **Rows processed**: 21,374
- **Columns converted**: 4

**Type conversions**:
- `flowering_time_raw`: object → float64
- `flowering_type_raw`: object → float64
- `indica_percentage_raw`: object → float64
- `sativa_percentage_raw`: object → float64

### Data Quality Impact
- Standardized data types across all columns
- Enabled proper mathematical operations on numeric fields
- Converted invalid numeric values to NULL (via `errors='coerce'`)
- Prepared dataset for database import and API responses
- All percentage and measurement fields now properly typed

### Output Files
- `04_data_types_standardized.csv` - Dataset with proper types (21,374 rows)
- `04_data_type_report.txt` - Type conversion statistics

---

## Step 05: Genetics Normalization

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Enhance genetics data by calculating missing values and extracting breeding information.

### Genetics Rules
1. **Ruderalis calculation**: If indica + sativa < 100%, calculate ruderalis = 100 - (indica + sativa)
2. **Filial extraction**: Extract generation markers (F1, F2, S1, BX1, IBL, P1) from generation field
3. **Breeding status**: Identify Landrace, Heirloom, IBL, Polyhybrid, or Hybrid from lineage/name

### Methodology
1. Read type-standardized dataset (21,374 strains)
2. Calculate ruderalis percentage when indica + sativa < 100%
3. Extract filial generation using regex patterns
4. Identify breeding status from genetics lineage and strain name
5. Create new `_clean` columns for derived genetics data

### Results
- **Rows processed**: 21,374
- **Total genetics enhancements**: 3,919

**Breakdown**:
- Ruderalis percentage calculated: 229 strains
- Filial generation extracted: 398 strains (F1, F2, S1, BX1, IBL, etc.)
- Breeding status identified: 3,292 strains (Landrace, Heirloom, IBL, Polyhybrid, Hybrid)

### New Columns Created
- `ruderalis_percentage_clean` - Calculated ruderalis percentage (0-100)
- `filial_type_clean` - Filial generation (F1, F2, S1, BX1, IBL, P1, etc.)
- `breeding_status_clean` - Breeding classification (Landrace, Heirloom, IBL, Polyhybrid, Hybrid)

### Data Quality Impact
- Added 229 ruderalis percentages (auto-flowering genetics)
- Extracted 398 filial generation markers for breeding tracking
- Classified 3,292 strains by breeding status (15.4% of dataset)
- Completed genetics profile: indica + sativa + ruderalis = 100%
- Enhanced searchability by breeding type and generation

### Output Files
- `05_genetics_normalized.csv` - Dataset with genetics enhancements (21,374 rows)
- `05_genetics_normalization_report.txt` - Enhancement statistics

---

## Step 06: Strain Name Normalization

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Create normalized strain names for deduplication by removing seed type suffixes and formatting variations.

### Normalization Rules
1. Convert to lowercase
2. Remove parentheses and brackets content
3. Remove seed type suffixes (feminized, auto, autoflower, regular, fem)
4. Remove product terms (seeds, strain, cannabis, marijuana)
5. Remove pack sizes and quantities (3 pack, x5, etc.)
6. Remove extra whitespace
7. Remove special characters (except # and -)

### Methodology
1. Read genetics-normalized dataset (21,374 strains)
2. Apply normalization rules to `strain_name_raw`
3. Create `strain_name_normalized` column for matching
4. Preserve original `strain_name_raw` for display
5. Calculate deduplication potential

### Results
- **Rows processed**: 21,374
- **Strain names normalized**: 20,892 (97.7%)

**Normalization impact**:
- Unique raw names: 13,762
- Unique normalized names: 10,710
- **Potential duplicates identified**: 3,052
- **Deduplication rate**: 22.18%

### Examples
- "Blue Dream Feminized Seeds" → "blue dream"
- "OG Kush Auto (3 Pack)" → "og kush"
- "Girl Scout Cookies [Fem]" → "girl scout cookies"
- "Northern Lights #5" → "northern lights #5" (preserves #)

### New Column Created
- `strain_name_normalized` - Lowercase, cleaned name for deduplication matching

### Data Quality Impact
- Identified 3,052 potential duplicate strains (22.18% of unique names)
- Standardized naming for accurate strain+breeder deduplication in Step 07
- Preserved original names for display purposes
- Enabled cross-seed-bank strain matching

### Output Files
- `06_strain_names_normalized.csv` - Dataset with normalized names (21,374 rows)
- `06_strain_name_normalization_report.txt` - Normalization statistics

---

## Step 07: AKA (Also Known As) Extraction

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Extract alternative strain names (AKA) from strain names and store separately.

### Methodology
1. Read strain-name-normalized dataset (21,374 strains)
2. Detect AKA patterns: "(aka ...)", "[aka ...]", "also known as"
3. Extract AKA names to separate column
4. Remove AKA text from strain name
5. Update normalized name without AKA

### Results
- **Rows processed**: 21,374
- **AKA names extracted**: 27 (0.13%)

**Examples**:
- "GG Genetics Original Glue (GG4 S1) AKA Gorilla Glue 4" → AKA: "Gorilla Glue 4"
- "Seeds Of Africa Zimbabwe AKA Zim-Licious" → AKA: "Zim-Licious"
- "Auto-Flowering Lemon (AKA AUTO LemonBubble)" → AKA: "AUTO LemonBubble"

### New Columns Created
- `aka_names_clean` - Alternative names (comma-separated)
- `strain_name_no_aka` - Strain name with AKA removed

### Output Files
- `07_aka_extracted.csv` - Dataset with AKA names (21,374 rows)
- `07_aka_extraction_report.txt` - Extraction statistics

---

## Step 08: Similar Spelling Normalization

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Create ultra-normalized names to match spelling variations used by different breeders.

### Normalization Rules
1. Remove all spaces ("grand daddy" → "granddaddy")
2. Remove hyphens and underscores ("girl-scout" → "girlscout")
3. Remove special characters except numbers ("og #1" → "og1")

### Methodology
1. Read AKA-extracted dataset (21,374 strains)
2. Apply aggressive normalization to `strain_name_normalized`
3. Create `similar_spelling_clean` for fuzzy matching
4. Calculate additional match potential

### Results
- **Rows processed**: 21,374
- **Unique normalized names**: 10,710
- **Unique similar spelling forms**: 10,668
- **Additional matches identified**: 42 (0.39%)

**Examples**:
- "grand daddy purple" → "granddaddypurple"
- "girl-scout-cookies" → "girlscoutcookies"
- "og #1" → "og1"

### New Column Created
- `similar_spelling_clean` - Ultra-normalized name for fuzzy matching

### Output Files
- `08_similar_spelling_normalized.csv` - Dataset with fuzzy matching (21,374 rows)
- `08_similar_spelling_report.txt` - Normalization statistics

---

## Step 09: Autoflower Classification

**Date**: January 17, 2026  
**Logic Designed By**: Amazon Q  
**Verified By**: Shannon Goddard

### Objective
Identify autoflower strains and separate their seed-to-harvest time from photoperiod flowering time.

### Detection Rules
1. Check `seed_type_raw` for "auto"
2. Check strain name for "auto" keyword
3. Check URL for "auto" or "autoflower"

### Methodology
1. Read similar-spelling-normalized dataset (21,374 strains)
2. Apply autoflower detection logic
3. Create `is_autoflower_clean` boolean column
4. For autoflowers: move `flowering_time_days_clean` to `autoflower_seed_to_harvest_days_min/max_clean`
5. Clear flowering time for autoflowers (they don't have separate flowering period)

### Results
- **Rows processed**: 21,374
- **Autoflowers identified**: 3,944 (18.45%)
- **Flowering times moved**: 469
- **Regular strains**: 17,430 (81.55%)

### New Columns Created
- `is_autoflower_clean` - Boolean flag for autoflower strains
- `autoflower_seed_to_harvest_days_min_clean` - Seed-to-harvest minimum (days)
- `autoflower_seed_to_harvest_days_max_clean` - Seed-to-harvest maximum (days)

### Data Quality Impact
- Properly classified 18.45% of dataset as autoflowers
- Separated autoflower timing from photoperiod flowering
- Enables accurate filtering by grow type
- Moved 469 flowering times to correct autoflower columns

### Output Files
- `09_autoflower_classified.csv` - Dataset with autoflower classification (21,374 rows)
- `09_autoflower_classification_report.txt` - Classification statistics

---

*This methodology document will be updated as each cleaning step is completed.*
