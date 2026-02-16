# Phase 11 Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Data Processing Approach

### File Integrity
- NEVER overwrite raw data
- Manual corrections stored in new `*_manual` columns
- Original columns preserved for audit trail
- Use `latin-1` encoding for CSV reads to handle special characters

### Workflow
1. **Manual Correction** - Shannon reviews and corrects data based on 19 years of domain expertise
2. **S3-to-Vertex Audit** - Gemini 1.5 Pro validates corrections against original HTML archives
3. **Final Review** - Shannon reviews flagged items and resolves discrepancies

### Why This Approach?
- **Human expertise first** - Domain knowledge > AI pattern matching
- **AI as auditor** - Validates human work at scale, catches errors
- **S3 archives** - Zero latency, 100% fidelity, cost efficient
- **Proven pattern** - Same approach as Phase 9 ($0.04 for 21,400 strains)

---

## Data Quality Rules

### Seed Bank Names
- Use official seed bank names
- Remove redundant suffixes ("Seed Bank", "Seeds")
- Consistent capitalization

### Breeder Names
**Critical Rule:** Distinguish breeders from seed banks
- Seed banks sell seeds from multiple breeders
- Breeders create the genetics
- If HTML mentions a specific breeder, use that (not the seed bank)

**Standardization:**
- Remove redundant words ("Seeds", "Genetics")
- Keep possessives ("Barney's Farm")
- Collaboration format: "Breeder1 x Breeder2"

### Strain Names
**Remove:**
- Suffixes: "Feminized", "Auto" (unless at start), "Regular", "Seeds"
- Pack sizes: "3 pack", "5pk", "[10]"
- Codes: "BFS", "DNA", strain IDs
- Breeder prefixes when redundant

**Preserve:**
- "Auto" at the START of the name
- Numbers and special characters (#, -)
- Phenotype markers (F1, F2, BX)

**Standardize:**
- Title Case capitalization
- Single spaces
- Preserve # and hyphens

---

## Automated Extraction from strain_name_raw

### Version Markers
**Pattern:** `\b(Fast|V\d+|S\d+|F\d+|BX\d+|XXL|XL)\b` (case-insensitive)
- Extracts: Fast, V1-V21, S1-S2, F1-F13, BX1-BX4, XL, XXL
- Stored in `version` column
- Keeps `strain_name_display` clean while preserving original markers
- Coverage: 1,056 strains (5.0%)

### Autoflower Detection
**Pattern:** `\b(auto|automatic)\b` (case-insensitive)
- Sets `is_autoflower` = TRUE if detected
- Sets `is_autoflower` = FALSE if not detected
- Coverage: 3,967 autoflowers (18.7%)

### CBD Dominant
**Pattern:** `\bCBD\b` (case-insensitive)
- Sets `cbd_dominant` = TRUE if "CBD" found in name
- Sets `cbd_dominant` = FALSE otherwise
- Coverage: 361 CBD strains (1.7%)

### CBD Level
**Pattern:** `\b(high cbd|cbd rich|cbd crew)\b` (case-insensitive)
- Sets `cbd_level` = "High" if detected
- Otherwise remains NULL (to be filled in Phase 12 from actual CBD data)
- Coverage: 17 high CBD strains (0.08%)

### CBD Ratio
**Pattern:** `(\d+:\d+)` (e.g., 1:1, 2:1, 1:20)
- Extracts THC:CBD ratios from strain names
- Stored in `cbd_ratio` column
- Most common: 1:1 (19 strains), 20:1 (4), 1:20 (3)
- Coverage: 38 strains (0.18%)

### Flowering Type
**Logic:** Derived from `is_autoflower`
- `flowering_type` = "Autoflower" if `is_autoflower` = TRUE
- `flowering_type` = "Photoperiod" if `is_autoflower` = FALSE
- `flowering_type` = "Unknown" if `is_autoflower` = NULL
- Replaces need for separate "is_regular" column

### Feminized Detection
**Pattern:** `\b(fem|feminized|feminised)\b` (case-insensitive)
- Sets `is_feminized` = TRUE if detected
- Sets `is_feminized` = FALSE otherwise
- Independent of flowering type (can be feminized photoperiod OR feminized autoflower)
- Coverage: 5,911 feminized strains (27.9%)

---

## S3-to-Vertex Audit Process

### Input
- CSV with manual corrections (`*_manual` columns)
- S3 HTML archives (original source of truth)

### Process
1. Load CSV with manual corrections
2. For each row:
   - Fetch original HTML from S3 using `s3_html_key_raw`
   - Send HTML + manual corrections to Gemini 1.5 Pro
   - Gemini audits: "Does the HTML support these corrections?"
3. Generate confidence scores (0-1)
4. Flag items below 0.90 confidence threshold

### Output
- `audit_results.csv` - All strains with audit columns
- `audit_flagged.csv` - Low confidence items for review

### Audit Columns
- `audit_seed_bank_correct` - Boolean
- `audit_breeder_correct` - Boolean
- `audit_strain_name_correct` - Boolean
- `audit_confidence` - Score (0-1)
- `audit_suggested_corrections` - JSON
- `audit_reasoning` - Gemini's explanation
- `audit_flagged` - Boolean (needs review)

---

## Cost & Performance

### Expected Metrics
- **Total strains:** 21,361
- **Processing time:** 30-60 minutes
- **Cost:** ~$0.10-0.50 (Gemini 1.5 Pro)
- **Flagged rate:** <5% expected

### Rate Limiting
- Batch size: 50 strains
- Sleep: 1 second between requests
- Progress saved after each batch

---

## Transparency Log

**Date:** February 12, 2026  
**Phase:** 11 - Manual Review & Validation  
**Approach:** Manual correction → Automated extraction from strain_name_raw → S3-to-Vertex audit → Final review  
**Manual Columns:** seed_bank_display, breeder_display, strain_name_display (20+ hours manual review)  
**Automated Columns:** version, is_autoflower, cbd_dominant, cbd_level, cbd_ratio, flowering_type, is_feminized  
**Model:** Gemini 1.5 Pro (gemini-1.5-pro) - audit only  
**Total Strains:** 21,220 (138 non-cannabis items removed)  
**Cost:** <$0.50 estimated  

**Logic designed by Amazon Q, verified by Shannon Goddard.**
