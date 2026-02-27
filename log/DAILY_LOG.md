# 2026 Build Log – Solo Grind to Cannabis Intelligence Empire

**Current Status (as of Feb 1, 2026)**  
✅ Phase 9.5 Complete | **1,089 strains manually reviewed** | 20 hours | 100% human-verified  
✅ Phase 9 Complete | **21,400 strains validated** | 39,681 AI corrections | $0.04 cost  
✅ Phase 8 Complete | **21,361 strains extracted** | 19 seed banks | Full botanical data  
✅ Phase 7 Complete | **21,706 HTML files** | S3 unified inventory | 100% archive coverage  
✅ Phase 6 Complete | **21,943 breeders extracted** | 519 standardized | 95.4% success  

**Source of Truth Viewer:** https://strains.loyal9.app  
**Costs so far:** Bright Data $41.27 • ScrapingBee $49.99 • AWS $25.62 • Google Cloud $0 (credits)

**Transparent daily chronicle of building the world's most rigorous cannabis dataset ecosystem.**  
Solo dev | Real costs | Real setbacks | Real breakthroughs

### Quick Jump
- [January 2026](#january-2026)
- [February 2026](#february-2026)

## January 2026 – Key Milestones (late Jan highlights)

### Jan 25: Phase 6 – Breeder Extraction & Standardization
- **Phase 6 COMPLETE**
- **Extracted breeders** from 23,000 strains (12 seed banks)
- **Valid strains kept:** 21,943 (95.4% success)
- **Top banks covered (100%):**
  - Attitude: 7,673
  - Gorilla: 2,000
  - North Atlantic: 2,726
  - Neptune: 1,995
  - … (14 more banks)
- **Standardization results:**
  - Before: 580 unique breeders
  - After: **519 standardized** (61 duplicates merged)
- **Output files created:**
  - all_breeders_extracted.csv
  - all_breeders_cleaned.csv
  - BREEDER_LIST.md (raw + cleaned)

### Jan 26–27: Phase 7 – S3 Unified Inventory
- **Phase 7 COMPLETE**
- **Total HTML files:** 21,706 (19 seed banks)
- **Metadata:** 21,706 JSON files (URL → hash mapping)
- **S3 structure:** `/unified/[seed_bank]/[hash].html`
- **Archive coverage:** **100%** of extracted strains
- **Verification:** All files accessible, zero broken links

### Jan 28: Phase 8 – Full Botanical Extraction
- **Phase 8 COMPLETE**
- **Final strains:** **21,361** (98.4% success)
- **Removed:** 345 duplicate/invalid pages
- **Fields extracted per strain:** 38 botanical + metadata
  - Genetics (THC%, CBD%, lineage…)
  - Cultivation (flowering, height, yield…)
  - Effects, flavors, medical uses
  - Seed type, breeder, price…
- **Coverage:** All 19 seed banks processed
- **Main output:** `all_strains_extracted.csv` (ready for AI validation)

### Jan 29: Phase 9 – Vertex AI Validation
- **Phase 9 COMPLETE**
- **Strains processed:** **21,400**
- **AI corrections:** **39,681** (≈1.85 per strain)
- **Flagged for human review:** **1,089** (5.1%)
- **Confidence:** 95% (90%+ threshold)
- **Cost:** **$0.04** (96% under budget)
- **Key fixes applied:**
  - Breeder from URL when missing
  - Removed breeder from strain name
  - Cleaned suffixes ("Feminized Auto" etc.)
  - Normalized breeder names
- **Tech highlights:**
  - 428 batches × 50 strains
  - Exponential backoff retry
  - Checkpoint saves every 10 batches
- **Outputs:**
  - all_strains_validated.csv (+8 validation columns)
  - all_strains_validated_flagged.csv (1,089 items)
  - all_strains_validated_report.txt

## February 2026 – The Manual Grind

### Feb 1: Phase 9.5 – Manual Deep Dive (1,089 flagged strains)
- **Phase 9.5 COMPLETE**
- **Time spent:** **20 hours** (URL-by-URL verification)
- **Process:**
  - Visited every source page
  - Cross-checked strain name, breeder, genetics
  - Captured **AKA names**
  - Noted edge cases & broken links
- **Key findings & fixes:**
  - Broken URLs: **2** (Neptune removed pages)
  - Breeder corrections: removed "Seeds", collabs, standardized
  - Strain name fixes: removed prefixes, codes, pack sizes
- **New columns added:**
  - `strain_name_aka_manual`
  - `strain_name_manual` ← final authority
  - `breeder_manual` ← final authority
  - `manual_notes`
- **Output:** `all_strains_validated_flagged_manual_review.csv`
- **Quality impact:** 5.1% of dataset now triple-verified (extract → AI → human)
- **Next:** Merge manual corrections → main 21,400-strain dataset

### Feb 2: Phase 10 – Lineage Extraction (Parent Genetics)
- **Phase 10 COMPLETE**
- **Coverage:** **76.1%** (16,246/21,361 strains) ✅ **Exceeded 70% target**
- **Seed banks extracted:** **12** (Attitude, Barney's, Crop King, Exotic, Gorilla, Herbies, Mephisto, Neptune, North Atlantic, Royal Queen, Seedsman JS, Seeds Here Now)
- **Extraction method:** Seed bank-specific HTML parsing patterns
- **Top performers:**
  - Barney's Farm: 84.1% (74/88)
  - Herbies: 83.9% (632/753)
  - Attitude: 79.3% (6,082/7,673)
  - North Atlantic: 76.0% (2,074/2,727)
- **Lineage schema:** 21 columns
  - Parent fields (display + slug)
  - Grandparent fields (4 pairs)
  - Generation markers (F1/S1/BX1)
  - Metadata (formula, confidence, notes)
- **Key challenges:**
  - Each seed bank has unique HTML structure
  - Nested crosses handled (split on last "x")
  - UTF-8 encoding for special characters
  - Some banks have no lineage data (Multiverse, Seed Supreme, Amsterdam)
- **Output:** `all_strains_lineage_final.csv` (21,361 strains, 118 columns)
- **Next:** Phase 11 – Manual Identity Review

### Feb 3-8: Phase 11 – Manual Identity Review & Standardization
- **Phase 11 IN PROGRESS**
- **Focus:** Seed bank, breeder, and strain name identity columns
- **Approach:** Manual correction → S3-to-Vertex audit → Final review

**Seed Banks (✅ COMPLETE)**
- **Total strains:** 21,361
- **Standardized:** 100% seed bank names cleaned
- **Output column:** `seed_bank_display_manual`

**Breeders (✅ COMPLETE)**
- **Starting point:** 4,755 "Unknown" breeders
- **Manual review:** Few hundred done by Shannon
- **AI extraction:** 3,994 breeders extracted from S3 HTML (89.1% success)
  - Average confidence: 99.75%
  - Low confidence: 78 items (1.7%)
- **Remaining unknowns:** 489 (mostly Seed Supreme - white label operation)
- **Final manual review:** 489 unknowns completed
- **Output column:** `breeder_display_manual`
- **Result:** 100% breeder review complete

**Strain Names (🔄 NEXT)**
- **Status:** Ready for review/edit
- **Tasks:**
  1. Review `strain_name_display_manual` for display names
  2. Create standardized slug column
  3. Remove suffixes (Feminized, Auto unless at start, pack sizes)
  4. Standardize capitalization (Title Case)
  5. Preserve #, -, and phenotype markers (F1, F2, BX)
- **Expected output columns:**
  - `strain_name_display_manual` - Clean display name
  - `strain_name_slug` - URL-safe slug

**Key Achievement:**
- **AI-assisted extraction saved 4,000+ manual lookups** (Gemini read S3 HTML archives)
- **Cost:** ~$0.10-0.15 for 4,483 breeder extractions
- **Human expertise applied:** Edge cases, Seed Supreme review, final validation

**Next:** Strain name review/standardization, then Phase 11 complete

**[TBD – momentum building…]**

### Feb 9: Phase 11 – Column Cleanup & Strain Name Review Begins
- **Column Cleanup (✅ COMPLETE)**
  - **Before:** 110 columns (chaos)
  - **After:** 47 columns (clean foundation)
  - **Removed:** 63 columns (57% reduction)
  - **Deleted:**
    - 10 Phase 9 validation columns (superseded by manual review)
    - 53 duplicate/redundant columns (raw/extracted/normalized variants)
  - **Kept:**
    - 9 Identity columns (GOLD tier - 100% verified)
    - 16 Lineage columns (SILVER tier - 76.1% coverage)
    - 5 Genetics metadata columns
    - 18 Botanical columns (BRONZE tier - for Phase 12+ cleaning)
  - **Output:** `pipeline_11_clean.csv` (21,361 strains, 47 columns)
  - **Documentation:** Column audit report + cleanup methodology

**Strain Names (🔄 IN PROGRESS)**
- **Started:** Manual review of 21,361 strain names
- **Progress:** 500 strains reviewed (2 hours)
- **Approach:**
  - Remove seed type suffixes ("Feminized", "Auto", "Regular", "Seeds")
  - Standardize spelling ("Alaskan Thunderfuck" not "Thunder Fuck")
  - Fix typos ("Alley Oop" not "Alley Oooop")
  - Keep phenotype markers (#1, #33, S1, F1)
  - Preserve breeder intent (numbered variants stay separate)
- **Key decisions:**
  - Deduplication key: `breeder + strain_name + is_autoflower`
  - Autoflower vs photoperiod = separate strains (different genetics)
  - AKA names only added if explicitly on seed bank page (no inference)
- **Estimated time:** 2-3 more days of review
- **Next:** Complete strain name review → generate slugs + standardized names

**Roadmap Updated:**
- **Phase 13.5 added:** Dataset generation (Clean → Filtered → Filled)
- **3-Dataset strategy:**
  1. CLEAN: 21,361 strains (all variants, verified)
  2. FILTERED: ~4,000 strains (deduplicated master strains)
  3. FILLED: ~4,000 strains (100% complete with AI gap-fill)
- **Deduplication approach:**
  - Ranges: THC/CBD/flowering/height/yield (merge min/max)
  - Most filled: Effects/flavors/terpenes (union all values)
  - First verified: Lineage (flag conflicts)
- **Launch blocker:** No Gumroad until 100% data + API (Phase 14)
- **Revenue target:** $110K Q2 2026

**Philosophy:** "Ship what's clean. Mark what's not." GOLD/SILVER/BRONZE transparency.

### Feb 12: Phase 11 – Strain Name Review Complete
- **Strain Names (✅ COMPLETE)**
  - **Time spent:** ~20 hours of manual review
  - **Total reviewed:** 21,361 strains
  - **Removed:** 138 non-cannabis items (seed mixes, merchandise, growing supplies)
  - **Final count:** 21,223 verified strains
  - **Standardization applied:**
    - Removed seed type suffixes ("Feminized", "Auto", "Regular", "Seeds")
    - Fixed spelling ("Alaskan Thunderfuck" not "Thunder Fuck")
    - Corrected typos ("Alley Oop" not "Alley Oooop")
    - Kept phenotype markers (#1, #33, S1, F1)
    - Preserved breeder intent (numbered variants stay separate)
  - **Key decisions enforced:**
    - Deduplication key: `breeder + strain_name + is_autoflower`
    - Autoflower vs photoperiod = separate strains (different genetics)
    - AKA names only if explicitly on seed bank page (no inference)
    - "Auto" prefix removed (flag handles it)
  - **Columns finalized:**
    - `strain_name_raw` - Original from seed bank (100% coverage)
    - `strain_name_display_manual` - Shannon's cleaned version (100% verified)
    - `strain_name_slug` - URL-safe slug (auto-generated)
  - **Output:** `pipeline_11_clean.csv` (21,223 strains, 48 columns)

**Phase 11 Status: 100% COMPLETE**
- ✅ Seed banks: 100% verified
- ✅ Breeders: 100% verified
- ✅ Strain names: 100% verified
- ✅ Column cleanup: 110 → 48 columns
- ✅ Non-cannabis items removed: 138 deleted

**Next:** Phase 12 – Botanical Data Extraction (seed bank-specific approach)

**[TBD – momentum building…]**

**This log is living proof: setbacks happen, but the grind wins.**  
From skeleton to production-ready 21k+ strain dataset in ~18 days.  
Raw tier Gumroad launch coming soon.  
🌿 Built with blood, sweat, coffee, Vertex credits, and relentless human-AI teamwork.


### Feb 15: Phase 11 – Automated Extraction from strain_name_raw
- **Phase 11 EXTENDED (Automated Extraction)**
- **Approach:** Mine strain_name_raw for botanical metadata
- **Total strains:** 21,220

**Version Markers (✅ COMPLETE)**
- **Pattern:** Fast, V1-V21, S1-S2, F1-F13, BX1-BX4, XL, XXL
- **Coverage:** 1,056 strains (5.0%)
- **Most common:** Fast (336), S1 (143), F2 (124), XL (112)
- **Output column:** `version`
- **Purpose:** Preserve original markers while keeping strain_name_display clean

**Autoflower Detection (✅ COMPLETE)**
- **Pattern:** "Auto" or "Automatic" in strain_name_raw
- **Updates:** 36 strains corrected to is_autoflower=TRUE
- **Coverage:** 3,967 autoflowers (18.7%)
- **Output column:** `is_autoflower` (TRUE/FALSE)

**CBD Dominant (✅ COMPLETE)**
- **Pattern:** "CBD" keyword in strain_name_raw
- **Coverage:** 361 CBD strains (1.7%)
- **Output column:** `cbd_dominant` (TRUE/FALSE)
- **Result:** 100% coverage (no more NaN values)

**CBD Level (✅ COMPLETE)**
- **Pattern:** "High CBD", "CBD Rich", "CBD Crew" in strain_name_raw
- **Coverage:** 17 high CBD strains (0.08%)
- **Output column:** `cbd_level` (High/NULL)
- **Note:** NULL values to be filled in Phase 12 from actual CBD data

**CBD Ratio (✅ COMPLETE)**
- **Pattern:** THC:CBD ratios (1:1, 2:1, 1:20, etc.)
- **Coverage:** 38 strains (0.18%)
- **Most common:** 1:1 (19), 20:1 (4), 1:20 (3)
- **Output column:** `cbd_ratio`

**Flowering Type (✅ COMPLETE)**
- **Logic:** Derived from is_autoflower
  - Autoflower if is_autoflower=TRUE
  - Photoperiod if is_autoflower=FALSE
  - Unknown if is_autoflower=NULL
- **Coverage:** 3,967 Autoflower, 17,247 Photoperiod, 6 Unknown
- **Output column:** `flowering_type`
- **Purpose:** Replaces need for separate "is_regular" column

**Feminized Detection (✅ COMPLETE)**
- **Pattern:** "Fem", "Feminized", "Feminised" in strain_name_raw
- **Coverage:** 5,911 feminized strains (27.9%)
- **Output column:** `is_feminized` (TRUE/FALSE)
- **Note:** Independent of flowering_type (can be feminized photoperiod OR feminized autoflower)

**Results:**
- **New columns added:** 7 (version, cbd_level, cbd_ratio, flowering_type, is_feminized + updated is_autoflower, cbd_dominant)
- **Total columns:** 54 (was 50)
- **Methodology updated:** All extraction rules documented
- **Cost:** $0 (regex extraction from existing data)

**Next:** Shannon reviews new data → Audit script → Phase 12 botanical extraction

**[TBD – momentum building…]**


### Feb 22: Phase 11 – URL-Based Extraction Pipeline (Recovery & Rebuild)
- **Context:** Previous merge attempt failed (no backup copy made) → had to reclean strain names & breeders
- **Lesson learned:** Always make backups before major merges 🤦
- **Recovery complete:** Rebuilt from pipeline_11_clean.csv

**URL Parsing System (✅ COMPLETE)**
- **Challenge:** Each seed bank has different URL structures
- **Solution:** Seed bank-specific parsing logic for all 19 banks
- **Examples:**
  - Barney's Farm: Remove trailing numbers (`-700`)
  - Royal Queen: Remove leading numbers (`494-`)
  - Cannabis Seeds Bank: Extract from path before `/prod_####`
  - North Atlantic: Handle numeric-only product IDs
- **Output column:** `strain_name_from_source_url`
- **Coverage:** 21,210 strains parsed (99.97%)

**Flowering Type Extraction (✅ COMPLETE)**
- **Method:** Check both URL path AND extracted strain name
- **Patterns detected:**
  - Fast flowering: "fast", "ff", "quick", "rapid", "speed"
  - Regular: "regular", "reg" + `/regular-seeds/` in URL
  - Feminized: "feminized", "feminised", "fem" + `/feminized-seeds/` in URL
  - Autoflower: "auto", "autoflower", "autoflowering" + `/auto` in URL
- **Results:**
  - `is_fast_flowering`: 373 TRUE (1.8%)
  - `is_regular_flowering`: 150 TRUE (0.7%)
  - `is_feminized_flowering`: 6,315 TRUE (29.8%)
  - `is_auto_flowering`: 3,774 TRUE (17.8%)
- **Output:** 4 new boolean columns (TRUE/FALSE strings)

**AKA Names Extraction (✅ COMPLETE)**
- **Pattern:** Extract text after "AKA", "Aka", "aka" in strain names
- **Coverage:** 154 AKA names found (0.7%)
- **Examples:**
  - `00 Seeds 00 Hashchis Aka 00 Cheese` → AKA: `00 Cheese`
  - `00 Seeds Auto 00 Hashchis Aka Auto 00 Cheese` → AKA: `Auto 00 Cheese`
- **Output column:** `aka_strain_names`

**Version Markers Extraction (✅ COMPLETE)**
- **Patterns:** #1-#420, V1-V3, 2.0-3.5, S1-S2, BX1-BX2, F1-F3, R1-R2, IX1-IX2, Gen 1
- **Coverage:** 688 versions found (3.2%)
- **Examples:**
  - `10Th Planet R1 Feminized Seeds` → `R1`
  - `22 Feminised Seeds 6 Cc 037 F6` → `F6`
  - `303 Seeds Bio Diesel Bx2` → `Bx2`
  - `98 Aloha White Widow S1 Strain` → `S1`
- **Output column:** `version`

**Data Pipeline (✅ COMPLETE)**
- **Individual CSVs created:**
  1. `strain_name_from_source_url_v2.csv` (seed bank-specific parsing)
  2. `is_fast_flowering.csv`
  3. `is_regular_flowering.csv`
  4. `is_feminized_flowering.csv`
  5. `is_auto_flowering.csv`
  6. `aka_strain_names.csv`
  7. `version.csv`
- **Review file:** `url_extraction_review.csv` (all 7 columns merged)
- **Final merge:** `pipeline_11_final.csv` (21,216 strains, 58 columns)

**New Columns Added:** 7
- `strain_name_from_source_url` - Parsed from URL (seed bank-specific logic)
- `is_fast_flowering` - TRUE/FALSE
- `is_regular_flowering` - TRUE/FALSE
- `is_feminized_flowering` - TRUE/FALSE
- `is_auto_flowering` - TRUE/FALSE
- `aka_strain_names` - Alternative names from URLs
- `version` - Version markers (F1, S1, BX1, etc.)

**Key Achievements:**
- ✅ Recovered from failed merge (no data loss)
- ✅ Built robust seed bank-specific URL parser (19 banks)
- ✅ Extracted 5 flowering type indicators from URLs
- ✅ Captured 154 AKA names automatically
- ✅ Identified 688 version markers
- ✅ Created modular CSV pipeline for review
- ✅ Final dataset: 58 columns, 21,216 strains

**Cost:** $0 (pure regex extraction)
**Time saved:** ~10 hours of manual URL parsing
**Lesson learned:** ALWAYS BACKUP BEFORE MERGING 🔥

**Next:** Phase 12 – Botanical data extraction

**[TBD – momentum building…]**


### Feb 23: Phase 12 – Botanical Data Extraction (Seed Bank-Specific Patterns)
- **Phase 12 COMPLETE**
- **Total strains processed:** 21,220 (100%)
- **Strains with botanical data:** 18,744 (88.3%)
- **Approach:** One seed bank at a time, custom HTML patterns per bank

**Extraction Results by Seed Bank:**

**Major Banks (High Coverage):**
- **Attitude Seedbank** (7,661 strains)
  - Pattern: Plain text with `<br/>` separators
  - Coverage: 93.5% flowering, 33.7% THC, 18.1% CBD
  - Debugged: Initial 0.1-3.7% → fixed to dual pattern (structured + old format)
  
- **Crop King Seeds** (3,332 strains)
  - Pattern: `<table class="tablesorter eael-data-table">` with nested divs
  - Coverage: 99.9% on all fields (THC, CBD, flowering, heights, yields, terpenes)
  
- **North Atlantic** (2,717 strains)
  - Pattern: `<div class="specs-grid">` with `<dt>/<dd>` pairs
  - Coverage: 97.1% genetics, 77.5% flowering, 65.1% yield
  
- **Gorilla Cannabis Seeds** (1,967 strains)
  - Pattern: `<table class="product-topattributes">` with `<th>/<td>` pairs
  - Coverage: 79.5% THC, 85.0% yield, 88.5% flowering
  - Debugged: Documented pattern didn't match → downloaded samples → found correct table structure
  
- **Neptune Seed Bank** (1,982 strains)
  - Pattern: Meta description tags with "Lineage: X x Y" format
  - Coverage: 76.3% lineage (only field available)
  
- **Herbies Seeds** (753 strains)
  - Pattern: `<table class="properties-list">` with `<tr class="properties-list__item">`
  - Coverage: 95.5% THC, 97.6% flowering, 8.9% height
  
- **Amsterdam Marijuana Seeds** (159 strains)
  - Pattern: `<div class="ams-attr-row">` with label/value divs
  - Coverage: 98.7% THC, 92.5% yield, 97.5% flowering
  
- **ILGM** (133 strains)
  - Pattern: Plain text "THC - 30%" format
  - Coverage: 98.5% THC

**Small Banks (Minimal/No Data):**
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

**Key Debugging Moments:**
1. **Gorilla**: Documented pattern (`<div class="g-product-features">`) didn't exist → downloaded samples → found actual pattern was table-based
2. **Attitude**: Initial extraction got 0.1-3.7% coverage → discovered dual format (new structured + old plain text) → updated to handle both → 93.5% coverage

**Data Integrity Rules Applied:**
- No unit conversion (raw values preserved: "450-550 gr/m2", "5 to 8 FT")
- latin-1 encoding for all CSV operations
- Separate CSV per seed bank (19 output files)
- NULL for missing data
- Never overwrite raw data

**Output Files Created:**
- Location: `pipeline/12_botanical_extraction/output/`
- Format: `botanical_{seed_bank_name}.csv`
- Total: 19 CSV files
- Columns vary by bank (strain_id + available botanical fields)

**Documentation:**
- `methodology.md` - Full extraction methodology
- `README.md` - Quick start guide
- `docs/BOTANICAL_PATTERNS.md` - HTML patterns documented
- `pipeline/02_s3_scraping/PIPELINE_12_INTEGRATION.md` - Integration notes

**Key Achievement:**
- ✅ 88.3% of strains have extractable botanical data
- ✅ Seed bank-specific patterns documented for future use
- ✅ Raw measurements preserved (no premature normalization)
- ✅ All 21,220 strains processed with placeholder files for banks with no data

**Cost:** $0 (S3 reads only, no API calls)
**Time:** ~6 hours (debugging patterns, running extractions)

**Next:** Phase 13 – Botanical data normalization & unit conversion

**[TBD – momentum building…]**


### Feb 27: Pipelines 13-16 – Data Cleaning & Consolidation
- **Pipelines 13-16 COMPLETE**
- **Total strains:** 21,210 (final count after cleanup)
- **Approach:** Normalize botanical data, merge extractions, clean dataset

**Pipeline 13: Botanical Data Normalization**
- Normalized units (cm, grams, days)
- Fixed encoding issues
- Standardized formats
- Validated ranges (min < max)

**Pipeline 14: Data Merging**
- Merged botanical extractions from 19 seed banks
- Combined with identity columns (Phase 11)
- Combined with lineage data (Phase 10)
- Resolved conflicts across sources

**Pipeline 15: Data Quality Audit**
- Generated data quality report
- Identified inconsistencies and outliers
- Flagged suspicious values for review
- Created audit trail for all fields

**Pipeline 16: Final Cleanup**
- Removed duplicate columns
- Standardized column names
- Applied final data quality rules
- Output: `pipeline_16_cleaned.csv` (21,210 strains, 53 columns)

**Pipeline 17: Gemini Validation Attempt**
- Ran THC validation on all 21,210 strains (~30 hours)
- Results: 95% error rate (19/20 manual checks failed)
- Issue: Gemini hallucinating values not in HTML
- Decision: Scrapping Gemini validation approach
- Keeping original extractions (more accurate than AI validation)

**Next Steps:**
- Shannon to review Pipeline 15 audit notes
- Manual edits based on audit findings
- Move to product generation (skip further Gemini validation)

**[TBD – momentum building…]**
