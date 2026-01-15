# Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Amsterdam Marijuana Seeds Extraction

### Data Source
- **S3 Inventory**: `pipeline/03_s3_inventory/s3_html_inventory.csv` (21,706 strains)
- **HTML Location**: `s3://ci-strains-html-archive/html/{url_hash}.html`
- **Seed Bank**: Amsterdam Marijuana Seeds (amsterdammarijuanaseeds.com)

### 9-Method Extraction Pipeline

1. **AMS Table Extraction** - Parse `ams-attr-table` structure with label/value pairs
2. **Meta Tags** - Extract SEO and social metadata
3. **Description** - Product description from woocommerce div
4. **THC/CBD** - Cannabinoid content and ranges
5. **Genetics** - Indica/Sativa ratio and lineage
6. **Flowering Time** - Weeks to harvest
7. **Yield** - Indoor/outdoor production data
8. **Effects** - Psychoactive and physical effects
9. **Flavors** - Terpene and taste profile

### Amsterdam-Specific Structure
- Uses `ams-attr-table` with `ams-attr-row` divs
- Each row contains `ams-attr-label` and `ams-attr-value`
- Fields prefixed with `ams_` for clarity

### Output
- **File**: `amsterdam_extracted.csv`
- **Encoding**: UTF-8
- **Target**: 150+ columns for maximum data capture
