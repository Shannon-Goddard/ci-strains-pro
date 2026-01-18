# Raw Data Decisions

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## What We DID Include in Raw Data

### 1. All Botanical & Cultivation Data (38 fields)
- Genetics, cannabinoids, terpenes, effects, flavors
- Flowering time, yield, height, difficulty, climate
- Seed type, breeder, awards, descriptions

**Rationale**: Educational/research data. No commercial value, publicly available information.

### 2. Source Attribution (3 fields)
- `source_url_raw` - Original URL for verification
- `s3_html_key_raw` - Archive reference (when available)
- `scraped_at_raw` - Collection timestamp

**Rationale**: Transparency and traceability. Enables "View Source" feature like strains.loyal9.app.

### 3. Multiple Extraction Versions (Intentional Duplicates)
- **Seedsman**: 878 (regular HTML) + 866 (JS) = 1,744 total
- **ILGM**: 133 (JS) + 133 (regular) + 36 (regular v2) = 302 total

**Rationale**: 
- Different extraction methods capture different data
- JS rendering often yields better results (ILGM: 97.7% THC coverage vs 6.8%)
- Preserves ability to compare extraction quality
- Deduplication happens in cleaned data, not raw

### 4. Original Data Formatting
- **No lowercase conversion** - Preserves "OG Kush" vs "og kush"
- **No standardization** - "8-10 weeks" stays as-is, not converted to days
- **No parsing** - THC ranges like "20-25%" kept as text

**Rationale**: Raw data rule - never modify original values. Cleaning happens in separate step.

---

## What We DID NOT Include in Raw Data

### 1. Commercial/Transactional Data (236 columns excluded)
- Prices (USD, GBP, EUR)
- Package sizes (1 seed, 3 pack, 10 pack)
- SKUs, product IDs
- Availability, stock status
- Discounts, promotions
- Shipping, payment methods

**Rationale**: 
- **Legal compliance** - Avoids commercial/competitive data scraping issues
- Positions dataset as educational/research only
- Same legal territory as Leafly, AllBud (strain info sites)

### 2. HTML Metadata (1,691 columns unmapped)
- Meta tags (og:title, twitter:card, etc.)
- JSON-LD structured data
- Image URLs, gallery counts
- Breadcrumb paths
- Page titles, descriptions

**Rationale**: Not botanical data. Useful for web scraping validation but not strain intelligence.

### 3. Cross-Seed-Bank Deduplication
- "Blue Dream" appears in 15+ seed banks - **all kept**
- Same strain name ≠ same genetics/breeder

**Rationale**:
- Different seed banks = different sources = different data points
- Genetics can vary (Blue Dream from Humboldt vs Dutch Passion)
- Deduplication requires domain expertise (happens in cleaned data)

### 4. Within-Seed-Bank Deduplication
- Same URL appearing twice in same seed bank - **both kept**

**Rationale**:
- May be legitimate (product updated, re-scraped)
- May be extraction error (worth investigating)
- Raw data preserves everything for analysis

---

## Data Quality Summary

**Total Records**: 23,009 strains  
**Total Columns**: 40 (38 botanical + strain_id + seed_bank)  
**Commercial Data**: 0 columns  
**Duplicate URLs**: Intentionally preserved  

**Coverage Highlights**:
- 89.4% have descriptions
- 67.3% have genetics/lineage
- 57.5% have THC data
- 36.8% have CBD data
- 76.8% flagged as hybrid

---

## Next Steps (Cleaned Data)

1. **Lowercase standardization** - "OG Kush" → "og kush"
2. **Parse ranges** - "20-25%" → thc_min=20, thc_max=25
3. **Convert units** - "8-10 weeks" → flowering_days_min=56, flowering_days_max=70
4. **Deduplicate within seed banks** - Pick best extraction version (JS > regular)
5. **Cross-reference genetics** - Identify true duplicates across seed banks
6. **Validate cannabinoid ranges** - Flag impossible values (THC > 40%)

---

**Date**: January 2026  
**Dataset Version**: master_strains_raw.csv v1.0  
**Total Investment**: $101.41 (AWS + Bright Data + ScrapingBee)  
**Legal Position**: Educational/research data extraction, no commercial data
