# Pipeline 13 Setup Instructions - Botanical Data Normalization

## Context
Pipeline 12 extracted raw botanical data from 21,220 strains across 19 seed banks. Data is in mixed formats with text, ranges, and various units. Pipeline 13 will normalize this into clean numeric columns.

## Input Files
Location: `pipeline/12_botanical_extraction/output/`
- botanical_attitude.csv (7,661 strains)
- botanical_crop_king.csv (3,332 strains)
- botanical_north_atlantic.csv (2,717 strains)
- botanical_gorilla.csv (1,967 strains)
- botanical_neptune.csv (1,982 strains)
- botanical_herbies.csv (753 strains)
- botanical_amsterdam.csv (159 strains)
- botanical_ilgm.csv (133 strains)
- Plus 11 placeholder files (no botanical data)

## Raw Data Examples
- THC: "18-22%", "Up to 21%", "High THC", "Average", "17% THC"
- Flowering: "7-8 weeks", "45-50 days", "Fast (6-10 weeks)", "70 - 84 days"
- Height: "60 to 100 cm Inside, 200 to 270 cm Outside", "Medium (5 to 8 FT)", "Compact"
- Yield: "450-550 gr/m2", "500-600 g/plant", "Average", "400-500 g/m²"

## Normalization Tasks

### 1. THC/CBD Normalization
**Input columns:** `thc_raw`, `cbd_raw`, `thc_content_raw`, `cbd_content_raw`
**Output columns:**
- `thc_min` (numeric, percentage)
- `thc_max` (numeric, percentage)
- `thc_avg` (numeric, calculated from min/max)
- `cbd_min` (numeric, percentage)
- `cbd_max` (numeric, percentage)
- `cbd_avg` (numeric, calculated from min/max)

**Rules:**
- Extract numeric values only
- Handle ranges: "18-22%" → min=18, max=22, avg=20
- Handle single values: "21%" → min=21, max=21, avg=21
- Handle "Up to X": "Up to 21%" → min=NULL, max=21, avg=21
- Handle qualitative: "High THC", "Average" → NULL (can't convert)
- Remove % symbol, keep only numbers

### 2. Flowering Time Normalization
**Input columns:** `flowering_raw`, `flowering_time_raw`, `from_seed_to_harvest`
**Output columns:**
- `flowering_days_min` (numeric, days)
- `flowering_days_max` (numeric, days)
- `flowering_days_avg` (numeric, calculated)

**Rules:**
- Convert weeks to days (multiply by 7)
- Handle ranges: "7-8 weeks" → min=49, max=56, avg=52.5
- Handle "X to Y days": "45-50 days" → min=45, max=50, avg=47.5
- Handle text: "Fast (6-10 weeks)" → extract 6-10, convert to days
- Handle single values: "70 days" → min=70, max=70, avg=70

### 3. Height Normalization
**Input columns:** `height_raw`, `height_indoor_raw`, `height_outdoor_raw`, `height_indoor_cm_clean`, `height_outdoor_cm_clean`
**Output columns:**
- `height_indoor_cm_min` (numeric, centimeters)
- `height_indoor_cm_max` (numeric, centimeters)
- `height_outdoor_cm_min` (numeric, centimeters)
- `height_outdoor_cm_max` (numeric, centimeters)

**Rules:**
- Convert all to centimeters (1 ft = 30.48 cm, 1 inch = 2.54 cm)
- Handle ranges: "60 to 100 cm" → min=60, max=100
- Handle feet: "5 to 8 FT" → min=152.4, max=243.84
- Handle combined: "60 to 100 cm Inside, 200 to 270 cm Outside" → split and parse
- Handle qualitative: "Compact", "Medium" → NULL

### 4. Yield Normalization
**Input columns:** `yield_raw`, `yield_indoor_raw`, `yield_outdoor_raw`
**Output columns:**
- `yield_indoor_g_m2_min` (numeric, grams per square meter)
- `yield_indoor_g_m2_max` (numeric, grams per square meter)
- `yield_outdoor_g_plant_min` (numeric, grams per plant)
- `yield_outdoor_g_plant_max` (numeric, grams per plant)

**Rules:**
- Indoor yields: convert to g/m² (handle gr/m2, g/m², grams/m2)
- Outdoor yields: convert to g/plant (handle g/plant, grams/plant)
- Handle ranges: "450-550 gr/m2" → min=450, max=550
- Handle single values: "500 g/plant" → min=500, max=500
- Handle qualitative: "Average", "High" → NULL

### 5. Genetics/Lineage (Keep as-is)
**Input columns:** `genetics_raw`, `lineage_raw`
**Output:** No normalization needed, keep raw text

### 6. Terpenes/Flavors (Keep as-is)
**Input columns:** `terpenes_raw`, `flavor_profile_raw`
**Output:** No normalization needed, keep raw text

## Data Integrity Rules
- NEVER delete raw columns (keep `*_raw` columns)
- Add new normalized columns alongside raw
- NULL for unparseable values (don't guess)
- Use latin-1 encoding for all CSV operations
- Preserve strain_id for merging back to main dataset

## Output Structure
**Per seed bank CSV:**
- Keep all original columns from pipeline 12
- Add normalized columns (suffix: `_min`, `_max`, `_avg`, `_cm`, `_g_m2`, `_g_plant`)
- Example: botanical_attitude_normalized.csv

**Final merged output:**
- `pipeline_13_botanical_normalized.csv`
- Merge all seed bank CSVs by strain_id
- Join back to `pipeline/12_botanical_extraction/input/pipeline_11_final.csv`
- Result: 21,220 strains with both raw and normalized botanical columns

## Approach
1. Process one seed bank at a time
2. Create normalization functions (parse_thc, parse_flowering, parse_height, parse_yield)
3. Apply functions to each CSV
4. Validate: Check min <= max, reasonable ranges
5. Generate coverage report per field
6. Merge all normalized CSVs
7. Create methodology.md documenting all conversion rules

## Expected Coverage
Based on pipeline 12 results:
- THC: ~80-99% (varies by bank)
- Flowering: ~75-98% (varies by bank)
- Height: ~10-90% (varies by bank)
- Yield: ~65-85% (varies by bank)

## Questions to Clarify
None - instructions are clear. Pipeline 13 will normalize raw botanical data into clean numeric columns with proper unit conversions.

## Key Files to Reference
- `pipeline/12_botanical_extraction/methodology.md` - Extraction patterns
- `pipeline/12_botanical_extraction/output/*.csv` - Input files
- `pipeline/12_botanical_extraction/input/pipeline_11_final.csv` - Main dataset for final merge

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
