# Complete S3 Bucket Inventory

**Bucket:** `ci-strains-html-archive`  
**Generated:** January 14, 2026  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Summary

**Total HTML Files:** 21,907  
**Total Storage:** ~10 GB

## Folder Structure

### 1. `html/` - Original 15 Seed Banks
- **Files:** 18,553 HTML files
- **Metadata:** 18,553 JSON files in `metadata/` folder
- **Content:** Original seed bank collection (Attitude, North Atlantic, Neptune, Crop King, etc.)
- **Mapping:** Each HTML has corresponding metadata JSON with source URL

### 2. `metadata/` - URL Mappings for html/ folder
- **Files:** 18,553 JSON files
- **Purpose:** Maps each HTML file hash to source URL
- **Structure:** `{"url": "...", "url_hash": "...", "seedbank": "...", ...}`

### 3. `pipeline06/` - Elite 5 Seed Banks
- **Files:** 3,354 HTML files
- **Content:** Elite seed banks collected separately
  - Amsterdam Marijuana Seeds
  - Gorilla Seeds Bank
  - Herbies Seeds
  - Exotic Genetix
  - Compound Genetics
- **Mapping:** Requires `elite_merged_urls.db` database for URL mappings

### 4. `processed_data/` - Processed outputs
- **Files:** 1 file
- **Purpose:** Processed/extracted data outputs

## Total Strain Coverage

- **Original 15 seed banks:** 18,553 strains (in `html/`)
- **Elite 5 seed banks:** 3,354 strains (in `pipeline06/`)
- **TOTAL:** 21,907 strains

## Extraction Status

### Already Extracted (15 seed banks in `html/`):
✅ Attitude Seed Bank  
✅ North Atlantic  
✅ Neptune  
✅ Crop King  
✅ Multiverse Beans  
✅ Seedsman  
✅ Sensi Seeds  
✅ Barney's Farm  
✅ Royal Queen Seeds  
✅ Dutch Passion  
✅ Seeds Here Now  
✅ ILGM  
✅ Mephisto Genetics  
✅ Great Lakes Genetics  
✅ Seed Supreme  

### Need Re-extraction (5 elite banks in `pipeline06/`):
🔄 Amsterdam Marijuana Seeds  
🔄 Gorilla Seeds Bank  
🔄 Herbies Seeds  
🔄 Exotic Genetix  
🔄 Compound Genetics  

## Next Steps

1. Use `s3_html_inventory.csv` for the 15 original seed banks
2. Create separate inventory for `pipeline06/` elite seed banks
3. Apply 9-method extraction pipeline to all 21,907 strains

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
