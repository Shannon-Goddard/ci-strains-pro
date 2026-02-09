# Phase 11: Manual Review & Validation (Names, Breeders, Seed Banks)

**Status:** 🚧 IN PROGRESS  
**Focus:** Strain names, breeder names, and seed bank names (the foundation)  
**Date Started:** February 3, 2026

---

## Overview

This phase focuses on **manual correction → S3-to-Vertex audit → final review** for the three most critical identity columns:
1. **Seed Bank Names** - Standardize seed bank display names
2. **Breeder Names** - Correct breeder attributions, distinguish from seed banks
3. **Strain Names** - Clean strain display names, remove suffixes/prefixes

**Approach:** Shannon manually corrects data in new `*_manual` columns, then Gemini 1.5 Pro audits corrections against the original S3 HTML archives to catch errors and validate accuracy.

**Note:** This is NOT the final production-ready dataset. All other botanical columns (THC, CBD, effects, flowering time, lineage, etc.) will be cleaned in future phases. These three columns are the foundation for strain identity.

---

## Folder Structure

```
pipeline/11_manual_review_and_validation/
├── input/
│   └── all_strains_lineage_final.csv          # From Phase 10 (21,361 strains)
├── output/
│   └── pipeline_11_manual_review.csv          # Shannon's manual corrections (in progress)
├── audit/
│   ├── s3_to_vertex_auditor.py                # S3-to-Vertex audit script
│   ├── audit_results.csv                      # Gemini audit results with confidence scores
│   └── audit_flagged.csv                      # Low confidence items for Shannon's review
├── final/
│   └── all_strains_phase11_final.csv          # Final output after audit review
├── methodology.md                              # Data processing rules
└── README.md                                   # This file
```

---

## Workflow

### Step 1: Manual Corrections (Shannon) ✅ IN PROGRESS
**Goal:** Manually correct seed bank, breeder, and strain names based on domain expertise

**Process:**
1. Open `output/pipeline_11_manual_review.csv`
2. Fill in three new columns:
   - `seed_bank_display_manual` - Standardized seed bank name
   - `breeder_display_manual` - Correct breeder attribution
   - `strain_name_display_manual` - Clean strain display name
3. Use domain knowledge to:
   - Distinguish breeders from seed banks
   - Remove suffixes (Feminized, Auto, pack sizes)
   - Standardize capitalization and formatting
   - Correct misattributions

**Output:**
- `output/pipeline_11_manual_review.csv` (with `*_manual` columns filled)

---

### Step 2: S3-to-Vertex Audit (Amazon Q + Gemini 1.5 Pro) 📋 READY
**Goal:** Validate Shannon's manual corrections against original S3 HTML archives

**Process:**
1. Load `pipeline_11_manual_review.csv`
2. For each row:
   - Use `s3_html_key_raw` to fetch original HTML from S3
   - Send HTML + manual corrections to Gemini 1.5 Pro
   - Gemini audits: "Does the HTML support these corrections?"
3. Generate confidence scores (0-1) and suggested corrections
4. Flag items below 0.90 confidence for review

**Why S3 Archives:**
- Zero latency (no web scraping)
- 100% fidelity (exact HTML used for extraction)
- Cost efficient (no proxy services)
- Gemini 1.5 Pro's huge context window can read entire HTML files

**Script:**
- `audit/s3_to_vertex_auditor.py`

**Output:**
- `audit/audit_results.csv` (all strains with audit columns)
- `audit/audit_flagged.csv` (low confidence subset)

**Cost Estimate:** ~$0.10-0.50 (based on Phase 9: $0.04 for 21,400 strains)

---

### Step 3: Final Review (Shannon) 📋 PENDING
**Goal:** Review flagged items and finalize corrections

**Process:**
1. Review `audit/audit_flagged.csv` (expected <5% of total)
2. Compare Gemini's suggestions with manual corrections
3. Make final decisions on discrepancies
4. Merge finalized data

**Output:**
- `final/all_strains_phase11_final.csv`

---

## Key Columns

### Input Columns (from Phase 10)
- `strain_id` - Unique strain identifier
- `seed_bank` - Original seed bank from extraction
- `strain_name_raw` - Original strain name from extraction
- `breeder_name_raw` - Original breeder name from extraction
- `source_url_raw` - Original URL
- `s3_html_key_raw` - S3 path to archived HTML

### Manual Correction Columns (Step 1)
- `seed_bank_display_manual` - Shannon's corrected seed bank name
- `breeder_display_manual` - Shannon's corrected breeder name
- `strain_name_display_manual` - Shannon's corrected strain name

### Audit Columns (Step 2)
- `audit_seed_bank_correct` - Boolean: Is seed bank correction accurate?
- `audit_breeder_correct` - Boolean: Is breeder correction accurate?
- `audit_strain_name_correct` - Boolean: Is strain name correction accurate?
- `audit_confidence` - Overall confidence score (0-1)
- `audit_suggested_corrections` - JSON with Gemini's suggestions
- `audit_reasoning` - Gemini's explanation
- `audit_flagged` - Boolean: Needs human review?

---

## Data Quality Guidelines

### Seed Bank Names
**Standardize:**
- Use official seed bank names
- Remove "Seed Bank", "Seeds" suffixes when redundant
- Consistent capitalization

**Examples:**
- "The Attitude Seedbank" → "The Attitude Seedbank"
- "Neptune Seed Bank" → "Neptune Seed Bank"
- "Gorilla Cannabis Seeds" → "Gorilla Cannabis Seeds"

### Breeder Names
**Critical Rule:** Distinguish breeders from seed banks
- Seed banks sell seeds from multiple breeders
- Breeders create the genetics
- If HTML mentions a specific breeder, use that (not the seed bank)

**Remove:**
- "Seeds", "Seed Bank", "Genetics" when redundant
- Legal suffixes: "LLC", "Inc"

**Standardize:**
- Possessives: "Barney's Farm" (keep apostrophe)
- Spacing and capitalization
- Collaboration format: "Breeder1 x Breeder2"

**Examples:**
- "Barney's Farm Seeds" → "Barney's Farm"
- "DNA Genetics LLC" → "DNA Genetics"
- "00 Seeds" → "00 Seeds" (breeder, not seed bank)
- "Mephisto x Night Owl" → "Mephisto Genetics x Night Owl Seeds"

### Strain Names
**Remove:**
- Suffixes: "Feminized", "Auto", "Autoflower", "Regular", "Seeds"
- Pack sizes: "3 pack", "5pk", "[10]"
- Codes: "BFS", "DNA", strain IDs
- Breeder prefixes when redundant

**Preserve:**
- "Auto" at the START of the name (e.g., "Auto Blue Dream")
- Numbers and special characters (#, -)
- Phenotype markers (F1, F2, BX)

**Standardize:**
- Capitalization (Title Case)
- Special characters (preserve #, keep hyphens)
- Spacing (single spaces)

**Examples:**
- "Zkittlez Feminized Auto [5pk]" → "Zkittlez"
- "Auto Zkittlez Feminized" → "Auto Zkittlez" (preserve Auto at start)
- "DNA Lemon Skunk" → "Lemon Skunk" (if breeder is DNA Genetics)
- "gorilla glue #4" → "Gorilla Glue #4"

---

## Success Criteria

### Manual Correction Phase
- ✅ All 21,361 strains reviewed
- ✅ `*_manual` columns filled with corrections
- ✅ Domain expertise applied to distinguish breeders from seed banks

### S3-to-Vertex Audit Phase
- ✅ All 21,361 strains audited against S3 HTML archives
- ✅ Confidence scores generated (0-1)
- ✅ Low confidence items flagged (<5% expected)
- ✅ Cost under $0.50

### Final Review Phase
- ✅ Flagged items manually reviewed
- ✅ Discrepancies resolved
- ✅ Phase 11 output ready for Phase 12

---

## Next Steps After Phase 11

**Phase 12: Lineage Validation**
- Apply same manual correction → S3 audit → review process to lineage columns
- Clean parent names, validate crosses, handle nested genetics

**Phase 13+:** Remaining botanical columns:
- THC/CBD content
- Flowering time
- Yield data
- Height data
- Effects and flavors
- Medical uses
- Climate and difficulty
- Terpenes and aromas

**Each phase will follow the Phase 11 pattern:**
1. Shannon's manual corrections
2. S3-to-Vertex audit validation
3. Final human review of flagged items

---

## Cost & Time Estimates

**Manual Corrections:** 10-20 hours (Shannon)
- Seed banks: 2-3 hours
- Breeders: 5-8 hours (hardest part)
- Strain names: 3-5 hours

**S3-to-Vertex Audit:** 30-60 minutes runtime, ~$0.10-0.50 cost
- Gemini 1.5 Pro: ~$0.00002 per strain (21,361 strains)
- Based on Phase 9 experience: $0.04 for 21,400 strains

**Final Review:** 2-5 hours (Shannon reviewing flagged items)

**Total Phase 11:** 15-30 hours human time, <$0.50 AI cost

---

## Important Notes

⚠️ **This is NOT the final production dataset**
- Only 3 columns validated in Phase 11 (seed banks, breeders, strain names)
- 35+ botanical columns still need cleaning (lineage, THC, CBD, effects, etc.)
- Phase 11 establishes the pattern for future phases

✅ **Why these three columns first?**
- **Seed banks** = source attribution and credibility
- **Breeders** = critical for marketplace value and genetics tracking
- **Strain names** = primary key for deduplication and search

🎯 **Phase 11 Goal:**
Clean, validated foundation for strain identity. All other data columns will be cleaned in subsequent phases using the same proven workflow: manual correction → S3 audit → final review.

💡 **Why S3-to-Vertex Audit?**
- Shannon's domain expertise > AI pattern matching
- AI validates human work (not the other way around)
- S3 archives = zero latency, 100% fidelity, cost efficient
- Proven approach from Phase 9 ($0.04 for 21,400 strains)

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
