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

**Date:** February 3, 2026  
**Phase:** 11 - Manual Review & Validation  
**Approach:** Manual correction → S3-to-Vertex audit → Final review  
**Columns:** seed_bank_display_manual, breeder_display_manual, strain_name_display_manual  
**Model:** Gemini 1.5 Pro (gemini-1.5-pro)  
**Cost:** <$0.50 estimated  

**Logic designed by Amazon Q, verified by Shannon Goddard.**
