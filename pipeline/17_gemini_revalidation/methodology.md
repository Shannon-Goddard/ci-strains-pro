# Pipeline 17 - Gemini Revalidation Methodology

## Purpose
Validate 20 botanical fields across 21,210 cannabis strains using archived S3 HTML sources with Gemini 2.0 Flash.

## Logic Designer
Logic designed by Amazon Q, verified by Shannon Goddard.

## Validation Approach

### Version 2 (Current) - With Standardization Rules
**Date**: March 5, 2026  
**Input**: `pipeline_16_no_avg.csv` (21,210 strains, 50 columns - removed avg columns)  
**Output**: `s3_validation_v2_results.json`

### Key Changes from V1
1. **Removed Average Columns**: Deleted `thc_avg`, `cbd_avg`, `flowering_days_avg` (calculated fields, not in HTML)
2. **Added Standardization Rules**: Gemini now converts weeks → days (1 week = 7 days)
3. **Explicit Unit Handling**: When both weeks and days present in HTML, prefer explicit days value
4. **Expanded Field Coverage**: Added height and yield validations (17 fields total)

### Standardization Rules
- **Flowering times**: MUST be in days. Convert weeks to days (1 week = 7 days)
- **Genetics percentages**: Must add to 100% (Indica + Sativa = 100%)
- **Genetics type**: Must be "Indica Dominant", "Sativa Dominant", or "Balanced Hybrid"
- **Heights**: All in centimeters (cm)
- **Yields**: Indoor in g/m², outdoor in g/plant

### Fields Validated (17 total)
**Cannabinoids (4)**:
- thc_min, thc_max
- cbd_min, cbd_max

**Genetics (3)**:
- indica_pct, sativa_pct
- genetics_type

**Flowering (2)**:
- flowering_min, flowering_max

**Heights (4)**:
- height_indoor_cm_min, height_indoor_cm_max
- height_outdoor_cm_min, height_outdoor_cm_max

**Yields (4)**:
- yield_indoor_g_m2_min, yield_indoor_g_m2_max
- yield_outdoor_g_plant_min, yield_outdoor_g_plant_max

### Technical Details
- **Model**: Gemini 2.0 Flash (gemini-2.0-flash)
- **Batch Size**: 5 strains per API call
- **HTML Source**: S3 bucket `ci-strains-html-archive` (first 50K chars)
- **Response Format**: JSON with structured validation results
- **Checkpoints**: Every 100 strains

### Expected Improvements
- Fewer false positives on flowering times (weeks vs days confusion eliminated)
- No corrections on average fields (removed from validation)
- Better alignment with pipeline's standardization approach
- More accurate corrections on height/yield fields

## Version History

### V1 - Initial S3 Validation
- **Date**: March 5, 2026
- **Results**: 91.8% success (19,475/21,210), 1,303 corrections
- **Issue**: Flagged weeks→days conversions as incorrect (didn't know about standardization)
- **Issue**: Tried to validate average columns (not in HTML)

### V2 - With Standardization
- **Date**: March 5, 2026
- **Status**: Ready to run
- **Changes**: Removed avg columns, added standardization rules, expanded field coverage
