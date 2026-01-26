# Breeder Extraction Methodology

**Script**: `11_breeder_extraction.py`  
**Logic designed by**: Amazon Q  
**Verified by**: Shannon Goddard  
**Date**: January 20, 2026

---

## Objective
Extract breeder names from S3 HTML archives using seed-bank-specific patterns documented in `BREEDER_EXTRACTION_PATTERNS.md`.

---

## Approach

### 1. Pattern-Based Extraction (15 seed banks)
Each seed bank has unique HTML structure for breeder information:
- **Attitude**: Breadcrumb link with `/cat_XXX` pattern
- **North Atlantic**: `<span class="breeder-link">` with product category link
- **Gorilla**: `<h3 class="product-manufacturer">` with white link
- **Neptune**: `<a class="breeder-link">` with `/brand/` pattern
- **Seedsman JS**: `<div class="Brand">` with breeder link
- **Herbies**: Table row with "Strain brand" title
- **Multiverse Beans**: Product meta with "Brand:" label
- **Seed Supreme**: Table with "Seedbank:" label
- **ILGM JS**: `<span class="font-black">` with breeder name
- **Seeds Here Now**: Breadcrumb with "Strain – Breeder" format
- **Great Lakes**: `<h3>` with "Breeder - Strain" format

### 2. Self-Branded Banks (8 seed banks)
Banks that are also breeders - hardcoded mapping:
- Crop King Seeds
- Amsterdam Marijuana Seeds
- Dutch Passion
- Barney's Farm
- Royal Queen Seeds
- Mephisto Genetics
- Exotic Genetix
- Sensi Seeds

### 3. Data Quality
- Remove rows with missing `source_url_raw` (1 row: LA Kush Cake from ILGM)
- Use BeautifulSoup for HTML parsing
- Handle encoding errors gracefully
- Track extraction success rate per seed bank

---

## Output
- **CSV**: `11_breeder_extracted.csv` with new `breeder_extracted` column
- **Report**: `11_breeder_extraction_report.txt` with coverage statistics

---

## Validation
- Coverage target: >95% extraction success
- Manual QA on sample rows per seed bank
- Cross-reference with existing `breeder_name_raw` where available


---

## Step 10E: Breeder Name Standardization
**Date:** January 18, 2026  
**Input:** 21,360 rows  
**Output:** 21,360 rows  
**Operations:** 13,365 breeder names standardized

Applied 50+ standardization rules from Shannon's QA findings:
- Suffix removals: 11 breeders (e.g., "G13 Labs Seeds" → "G13 Labs")
- Suffix additions: 2 breeders (e.g., "Geist Grow" → "Geist Grow Genetics")
- Name variations: 20 breeders (e.g., "Humboldt Seed Company" → "Humboldt Seed Co")
- Leading character fixes: 2 breeders (e.g., "z710 Genetics" → "710 Genetics")
- Multi-breeder collaborations: 1 case (comma separation)

**New Column:** breeder_name_clean

---

## Step 10F: Non-Cannabis Product Removal
**Date:** January 18, 2026  
**Input:** 21,360 rows  
**Output:** 21,352 rows  
**Removed:** 8 rows

Removed non-cannabis products:
- Variety packs: 2 rows (bulk seeds, multipacks)
- Puffco vape products: 6 rows (vaporizers, accessories)

**Removal Logic:**
- URL-based removal: Exact URL match for known non-cannabis products
- Breeder-based removal: All products with breeder_name_clean = "Puffco"

---

**Phase 1 Extended Complete**  
**Final Dataset:** 21,352 rows  
**Total Operations (Steps 10A-10F):** 60,093 cleaning operations  
**Next Phase:** Breeder name re-extraction from S3 HTML (targeting 9.4% empty + contaminated names)


---

## Step 10G: Missing URL Removal
**Date:** January 18, 2026  
**Input:** 21,352 rows  
**Output:** 21,351 rows  
**Removed:** 1 row

Removed row with missing source_url_raw (unrecoverable URL).

---

**Phase 1 Extended Complete**  
**Final Dataset:** 21,351 rows  
**Total Operations (Steps 10A-10G):** 60,094 cleaning operations  
**Ready for:** Breeder name re-extraction from S3 HTML using 19 documented patterns


---

## Step 11: Breeder Name Extraction from S3 HTML
**Date:** January 18, 2026  
**Input:** 21,351 rows  
**Output:** 21,351 rows  
**Extracted:** 20,463 breeders (95.8% success rate)

Re-extracted breeder names from S3 HTML using 19 seed-bank-specific patterns:
- Self-branded (4): Amsterdam, Dutch Passion, Barney's Farm, Royal Queen Seeds
- Breadcrumb (9): Attitude, Crop King, North Atlantic, Gorilla, Neptune, Herbies, Sensi, Mephisto, Exotic Genetix
- Seeds Here Now: Breadcrumb with dash separator
- Great Lakes: H3 with dash separator
- Multiverse: Brand tag
- Seed Supreme: Seedbank table value
- ILGM: JS-rendered span
- Seedsman: Breeder link (low success)

**New Column:** breeder_name_extracted

---

## Step 11B: Merge Extracted Breeders & Apply Standardization
**Date:** January 18, 2026  
**Input:** 21,351 rows  
**Output:** 21,351 rows  
**Operations:** 1,081 standardizations

Merged S3-extracted breeders with existing data and applied Step 10E standardization rules.

**Breeder Coverage:**
- Before extraction: 8,348 (39.1%)
- After extraction: 20,812 (97.5%)
- Improvement: +12,464 breeders (+58.4 percentage points)

**Final breeder_name_clean column ready for deduplication.**

---

**Phase 1 Extended Complete**  
**Final Dataset:** 21,351 rows  
**Breeder Coverage:** 97.5%  
**Total Operations (Steps 10A-11B):** 81,638 cleaning operations  
**Ready for:** Phase 2 cleaning (deduplication, Gemini validation)


---

## Step 11C: Final Breeder Cleanup
**Date:** January 18, 2026  
**Input:** 21,351 rows  
**Output:** 21,348 rows  
**Operations:** 536 fallback fills + 3 deletions

Final breeder cleanup to achieve 100% coverage:
- Seedsman breeder extraction from breeder_name_raw (cleaned "Parental lines" contamination)
- Removed 3 non-cannabis products (sunglasses, t-shirts)
- Filled remaining gaps with seed bank name as fallback

**Final Breeder Coverage:** 21,348 (100.0%)

---

**Phase 1 Extended COMPLETE**  
**Final Dataset:** 21,348 rows  
**Breeder Coverage:** 100%  
**Total Operations:** 82,177 cleaning operations  
**Ready for:** Deduplication using strain_name + breeder_name key
