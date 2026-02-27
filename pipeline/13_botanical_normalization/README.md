# Pipeline 13: Botanical Data Normalization

Convert raw botanical data from Pipeline 12 into clean numeric columns with standardized units.

## Status
✅ **COMPLETE** - 9 seed banks normalized (18,792 strains)

## Overview

Pipeline 13 normalizes raw botanical text data into clean numeric columns with standardized units. All raw data is preserved, and normalized columns are added alongside for analysis.

**Input:** 19 CSVs from `pipeline/12_botanical_extraction/output/`  
**Output:** 9 normalized CSVs with `_min`, `_max`, `_avg` columns  
**Coverage:** 18,792 / 21,220 strains (88.6%)

## Results Summary

### Processed Seed Banks (9)
1. **Attitude** (7,661 strains) - THC: 27.2%, Flowering: 61.4%
2. **Crop King** (3,332 strains) - THC: 99.4%, Flowering: 99.9%, Height: 99.5%, Yield: 95%+
3. **North Atlantic** (2,717 strains) - Flowering: 77.4%, Height: 22.0%, Yield: 33.2%
4. **Gorilla** (1,967 strains) - THC: 58.6%, Flowering: 57.6%, Yield: 69.2%
5. **Neptune** (1,982 strains) - No botanical data (lineage only)
6. **Herbies** (753 strains) - THC: 94.4%, Flowering: 97.6%
7. **Amsterdam** (159 strains) - THC: 98.7%, Flowering: 97.5%
8. **ILGM** (133 strains) - THC: 98.5%
9. **Barneys Farm** (88 strains) - 0% coverage (empty values)

### Skipped Seed Banks (10)
No botanical data extracted in Pipeline 12:
- Dutch Passion (44 strains)
- Exotic (173 strains)
- Great Lakes Genetics (16 strains)
- Mephisto Genetics (244 strains)
- Multiverse Beans (527 strains)
- Royal Queen Seeds (67 strains)
- Seed Supreme (353 strains)
- Seeds Here Now (43 strains)
- Seedsman (842 strains)
- Sensi Seeds (109 strains)

## Structure
```
13_botanical_normalization/
├── input/remove/              # Full CSVs from Pipeline 12
├── output/                    # 9 normalized CSVs
├── scripts/                   # 9 normalization scripts
│   ├── normalize_attitude.py
│   ├── normalize_crop_king.py
│   ├── normalize_north_atlantic.py
│   ├── normalize_gorilla.py
│   ├── normalize_neptune.py
│   ├── normalize_herbies.py
│   ├── normalize_amsterdam.py
│   ├── normalize_ilgm.py
│   └── normalize_barneys_farm.py
├── SETUP_INSTRUCTIONS.md      # Detailed normalization rules
├── methodology.md             # Conversion logic & results
└── README.md                  # This file
```

## Key Conversions

### THC/CBD Parsing
- **"18-22%"** → min=18, max=22, avg=20
- **"25%"** → min=25, max=25, avg=25
- **"High THC"** → NULL (unparseable)

### Flowering Time
- **"7-8 weeks"** → min=49, max=56, avg=52.5 days
- **"60 days"** → min=60, max=60, avg=60 days
- **"Fast"** → NULL (unparseable)

### Height (converted to cm)
- **"80-100 cm"** → min=80, max=100
- **"3'-5'"** → min=91.44, max=152.4 (feet × 30.48)
- **"Compact"** → NULL (unparseable)

### Yield
- **"450-550 gr/m2"** → min=450, max=550 g/m²
- **"500 g/plant"** → min=500, max=500 g/plant
- **"High"** → NULL (unparseable)

## Normalized Columns Added

- `thc_min`, `thc_max`, `thc_avg` (percentage)
- `cbd_min`, `cbd_max`, `cbd_avg` (percentage)
- `flowering_days_min`, `flowering_days_max`, `flowering_days_avg` (days)
- `height_indoor_cm_min`, `height_indoor_cm_max` (centimeters)
- `height_outdoor_cm_min`, `height_outdoor_cm_max` (centimeters)
- `yield_indoor_g_m2_min`, `yield_indoor_g_m2_max` (grams per square meter)
- `yield_outdoor_g_plant_min`, `yield_outdoor_g_plant_max` (grams per plant)

## Data Integrity Rules

1. **Never delete raw columns** - All `*_raw` columns preserved
2. **NULL for unparseable** - No guessing or imputation
3. **latin-1 encoding** - Handles special characters from breeders
4. **Preserve strain_id** - Maintains traceability to main dataset
5. **Validate ranges** - Ensure min ≤ max

## Files Used

### Input Files (from Pipeline 12)
- `pipeline/12_botanical_extraction/output/botanical_attitude.csv`
- `pipeline/12_botanical_extraction/output/botanical_crop_king.csv`
- `pipeline/12_botanical_extraction/output/botanical_north_atlantic.csv`
- `pipeline/12_botanical_extraction/output/botanical_gorilla.csv`
- `pipeline/12_botanical_extraction/output/botanical_neptune.csv`
- `pipeline/12_botanical_extraction/output/botanical_herbies.csv`
- `pipeline/12_botanical_extraction/output/botanical_amsterdam.csv`
- `pipeline/12_botanical_extraction/output/botanical_ilgm.csv`
- `pipeline/12_botanical_extraction/output/botanical_barneys_farm.csv`

### Output Files (normalized)
- `output/botanical_attitude_normalized.csv`
- `output/botanical_crop_king_normalized.csv`
- `output/botanical_north_atlantic_normalized.csv`
- `output/botanical_gorilla_normalized.csv`
- `output/botanical_neptune_normalized.csv`
- `output/botanical_herbies_normalized.csv`
- `output/botanical_amsterdam_normalized.csv`
- `output/botanical_ilgm_normalized.csv`
- `output/botanical_barneys_farm_normalized.csv`

### Scripts
- `scripts/normalize_attitude.py` - Attitude Seedbank normalization
- `scripts/normalize_crop_king.py` - Crop King normalization
- `scripts/normalize_north_atlantic.py` - North Atlantic normalization
- `scripts/normalize_gorilla.py` - Gorilla normalization
- `scripts/normalize_neptune.py` - Neptune normalization
- `scripts/normalize_herbies.py` - Herbies normalization
- `scripts/normalize_amsterdam.py` - Amsterdam normalization
- `scripts/normalize_ilgm.py` - ILGM normalization
- `scripts/normalize_barneys_farm.py` - Barneys Farm normalization

### Documentation
- `SETUP_INSTRUCTIONS.md` - Detailed normalization rules and examples
- `methodology.md` - Parsing logic, conversion formulas, and coverage results
- `README.md` - This file

## Key Insights

- **Crop King** has the best data quality (95-99% coverage across all fields)
- **Attitude** has the most strains but lower coverage (3-61% varies by field)
- **Column structure varies** by seed bank - each required custom handling
- **10 seed banks** had no botanical data extracted in Pipeline 12
- **THC data** most common (when present, usually 90%+ coverage)
- **Height/Yield data** sparse for most banks except Crop King

## Next Steps

Pipeline 13 complete. Normalized botanical data ready for:
- Statistical analysis
- Strain comparison tools
- Filtering/search features
- Data visualization
- Merge with main dataset (pipeline_11_final.csv)

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
