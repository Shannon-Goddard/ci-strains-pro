# Pipeline 13 - Botanical Data Normalization Methodology

## Overview
Pipeline 13 converts raw botanical data from Pipeline 12 into clean numeric columns with standardized units. All raw data is preserved, and normalized columns are added alongside.

## Data Source
- Input: `pipeline/13_botanical_normalization/input/remove/botanical_*.csv` (19 seed banks)
- Output: `pipeline/13_botanical_normalization/output/botanical_*_normalized.csv`

## Normalization Functions

### 1. THC/CBD Parsing (`parse_thc_cbd`)
**Input:** Raw text like "18-22%", "Up to 25%", "0.5%"
**Output:** `_min`, `_max`, `_avg` columns

**Logic:**
- Extract all numeric values using regex `(\d+(?:\.\d+)?)`
- Replace commas with periods for European decimals
- Single value: min=max=avg=value
- Multiple values: min=lowest, max=highest, avg=mean
- Non-numeric text: NULL

**Examples:**
- "18-22%" → min=18, max=22, avg=20
- "25%" → min=25, max=25, avg=25
- "High THC" → NULL

### 2. Flowering Time Parsing (`parse_flowering`)
**Input:** Raw text like "7-8 weeks", "45-50 days", "9 weeks"
**Output:** `flowering_days_min`, `flowering_days_max`, `flowering_days_avg`

**Logic:**
- Extract numeric values
- Multiply by 7 if "week" detected in text
- Single value: min=max=avg=value
- Multiple values: min=lowest, max=highest, avg=mean
- Non-numeric text: NULL

**Examples:**
- "7-8 weeks" → min=49, max=56, avg=52.5
- "60 days" → min=60, max=60, avg=60
- "Fast" → NULL

### 3. Height Parsing (`parse_height`)
**Input:** Raw text like "80-100 cm", "3'-5'", "90 - 150 cm"
**Output:** `height_indoor_cm_min`, `height_indoor_cm_max` (and outdoor variants)

**Logic:**
- Extract numeric values
- Convert feet to cm if "ft" or "'" detected (multiply by 30.48)
- Single value: min=max=value
- Multiple values: min=lowest, max=highest
- Non-numeric text: NULL

**Examples:**
- "80-100 cm" → min=80, max=100
- "3'-5'" → min=91.44, max=152.4
- "Compact" → NULL

### 4. Yield Parsing (`parse_yield`)
**Input:** Raw text like "450-550 gr/m2", "1200-1400 g/plant"
**Output:** `yield_indoor_g_m2_min`, `yield_indoor_g_m2_max` (and outdoor g/plant variants)

**Logic:**
- Extract numeric values
- Single value: min=max=value
- Multiple values: min=lowest, max=highest
- Non-numeric text: NULL
- Note: Does not distinguish units (assumes correct column placement)

**Examples:**
- "450-550 gr/m2" → min=450, max=550
- "500 g/m2" → min=500, max=500
- "High" → NULL

## Data Integrity Rules
1. **Never delete raw columns** - All `*_raw` columns preserved
2. **NULL for unparseable** - No guessing or imputation
3. **latin-1 encoding** - Handles special characters from breeders
4. **Preserve strain_id** - Maintains traceability to main dataset

## Attitude Seedbank Results (7,661 strains)
- THC: 2,086 strains (27.2%)
- CBD: 853 strains (11.1%)
- Flowering: 4,702 strains (61.4%)
- Height Indoor: 242 strains (3.2%)
- Height Outdoor: 339 strains (4.4%)
- Yield Indoor: 629 strains (8.2%)
- Yield Outdoor: 0 strains (0.0%)

## Crop King Seedbank Results (3,332 strains)
- THC: 3,313 strains (99.4%)
- CBD: 2,787 strains (83.6%)
- Flowering: 3,328 strains (99.9%)
- Height Indoor: 3,317 strains (99.5%)
- Height Outdoor: 3,316 strains (99.5%)
- Yield Indoor: 3,190 strains (95.7%)
- Yield Outdoor: 3,183 strains (95.5%)

## Next Steps
Process remaining 18 seed banks one at a time:
- Crop King (3,332 strains)
- North Atlantic (2,717 strains)
- Gorilla (1,967 strains)
- Neptune (1,982 strains)
- Herbies (753 strains)
- Amsterdam (159 strains)
- ILGM (133 strains)
- Plus 11 others

Each seed bank may have different data formats requiring custom handling.

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
