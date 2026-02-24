# Pipeline 12: Botanical Data Extraction Methodology

**Date:** February 23, 2026  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Purpose
Extract botanical cultivation data (THC, CBD, flowering time, yield, height, etc.) from 21,220 cannabis strain HTML files stored in S3 bucket `ci-strains-html-archive`.

## Approach
One seed bank at a time. Each seed bank has unique HTML structure requiring custom extraction patterns.

## Data Integrity Rules
- Never overwrite raw data
- Extract raw measurements with mixed units (no conversion during extraction)
- Missing data = NULL
- Create separate CSV per seed bank
- Use `latin-1` encoding for all CSV operations

## Extraction Results

### Banks with Botanical Data (18,744 strains - 88.3%)
- **Attitude Seedbank** (7,661): 93.5% flowering, 33.7% THC, 18.1% CBD
- **Crop King Seeds** (3,332): 99.9% coverage on all fields
- **North Atlantic** (2,717): 97.1% genetics, 77.5% flowering, 65.1% yield
- **Gorilla Cannabis Seeds** (1,967): 79.5% THC, 85.0% yield, 88.5% flowering
- **Neptune Seed Bank** (1,982): 76.3% lineage (meta description only)
- **Herbies Seeds** (753): 95.5% THC, 97.6% flowering
- **Amsterdam Marijuana Seeds** (159): 98.7% THC, 97.5% flowering
- **ILGM** (133): 98.5% THC

### Banks with Minimal/No Data (2,476 strains - 11.7%)
- Seedsman (842): JS-rendered, no static HTML data
- Multiverse Beans (527): No structured botanical data
- Seed Supreme (353): No structured botanical data
- Mephisto Genetics (244): No structured botanical data
- Exotic Genetix (173): No structured botanical data
- Sensi Seeds (109): No structured botanical data
- Barney's Farm (88): No structured botanical data
- Royal Queen Seeds (67): No structured botanical data
- Dutch Passion (44): No structured botanical data
- Seeds Here Now (43): No structured botanical data
- Great Lakes Genetics (16): No structured botanical data

## HTML Patterns Used

### Attitude Seedbank
Pattern: Plain text with `<br/>` separators
```
Flowering Time: 45-50 days<br/>
THC: 18-22%<br/>
```

### Crop King Seeds
Pattern: `<table class="tablesorter eael-data-table">` with `<div class="td-content">` pairs

### North Atlantic
Pattern: `<div class="specs-grid">` with `<dt class="spec-label">` and `<dd class="spec-value">`

### Gorilla Cannabis Seeds
Pattern: `<table class="product-topattributes">` with `<th class="col label">` and `<td class="col data">`

### Neptune Seed Bank
Pattern: Meta description tags with "Lineage: X x Y" format

### Herbies Seeds
Pattern: `<table class="properties-list">` with `<tr class="properties-list__item">`

### Amsterdam Marijuana Seeds
Pattern: `<div class="ams-attr-row">` with label/value divs

### ILGM
Pattern: Plain text "THC - 30%" format

## Output Files
- 19 CSV files in `output/` directory
- Format: `botanical_{seed_bank_name}.csv`
- Columns: `strain_id` + botanical fields (varies by bank)
- Encoding: latin-1

## Total Coverage
- **21,220 / 21,220 strains processed (100%)**
- **18,744 strains with botanical data (88.3%)**
- **2,476 strains with no extractable data (11.7%)**

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
