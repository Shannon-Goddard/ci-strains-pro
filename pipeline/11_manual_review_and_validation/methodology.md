# Methodology: Strain Name Extraction from Source URLs

## Purpose
Extract clean, human-readable strain names from source URLs to create a new column `strain_name_from_source_url` for cross-validation and data quality purposes.

## Logic Designed By
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Process Overview

### Input
- Source file: `pipeline/11_manual_review_and_validation/output/pipeline_11_clean.csv`
- Source column: `source_url_raw`

### Transformation Logic
1. **URL Parsing**: Extract the last path segment from each URL (before query parameters)
2. **Suffix Removal**: Strip common seed bank suffixes:
   - `-weed-strain`
   - `-marijuana-seeds`
   - `-feminized-seeds`
   - `-autoflower-strain`
   - `-strain`
   - `-seeds`
   - `-feminized`
   - `-autoflowering`
   - `-auto`
3. **Formatting**: Convert URL slug to title case with spaces replacing hyphens

### Example Transformations
- `https://www.northatlanticseed.com/product/new-luxors-a5-silver-haze-f/` → `New Luxors A5 Silver Haze F`
- `https://amsterdammarijuanaseeds.com/420-carat-feminized/` → `420 Carat`
- `https://amsterdammarijuanaseeds.com/ak47-xtrm-autoflower/` → `Ak47 Xtrm`

### Output
- New file: `pipeline/11_manual_review_and_validation/output/strain_name_from_source_url.csv`
- Columns: `strain_id`, `source_url_raw`, `strain_name_from_source_url`
- Encoding: `latin-1` (to handle special cannabis breeder characters)
- Total rows processed: 21,237

## Data Integrity
- **No raw data overwritten**: Original `pipeline_11_clean.csv` remains unchanged
- **New column created**: `strain_name_from_source_url` is a derived field
- **Null handling**: Empty URLs return empty strings (no errors)

## Use Cases
1. Cross-validation with existing `strain_name_display` column
2. Identifying discrepancies between URL slugs and stored strain names
3. Quality assurance for strain identity verification
4. Backup strain name source when other fields are missing

## Script Location
`pipeline/11_manual_review_and_validation/extract_strain_names_from_urls.py`

## Execution Date
January 2026

---
*This methodology follows CI-Strains-Pro data processing rules: preserving raw data, using latin-1 encoding, and maintaining full transparency.*
