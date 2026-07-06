# CI-Strains-Pro — Build Log
**Development chronicle for the CI-Strains-Pro dataset**

**Current Snapshot (as of July 2026)**
- Final working strain count: **~21,210–21,223**
- Identity fields (seed bank + breeder + strain name): **100% human-verified**
- Lineage coverage: **76.1%** (16,246 strains)
- Botanical data extracted: **88.3%** of strains (18,744)
- Latest validation (S3 HTML + Gemini 2.0 Flash): **91.8%** success (19,475 strains)
- Corrections from validation: **1,303 total** (691 high-confidence)
- Total spend to date: **≈ $117** (Bright Data $41.27 + ScrapingBee $49.99 + AWS $25.62 + Vertex ~$0.55)
- License: **CC BY 4.0** (data) / **MIT** (code)

---

## January 2026 — Foundation & Bulk Extraction

- **Phase 6** – Breeder extraction + standardization
  → 21,943 strains kept | 519 unique breeders (from 580, merged 61 duplicates) | 95.4% success

- **Phase 7** – S3 unified archive
  → 21,706 HTML files | 19 seed banks | 100% coverage | metadata JSON mapping

- **Phase 8** – Full botanical + metadata extraction
  → 21,361 strains | 38 fields per strain (genetics, grow specs, effects, etc.) | 98.4% success

- **Phase 9** – Vertex AI validation
  → 21,400 strains processed | 39,681 corrections (~1.85 per strain) | 1,089 flagged (5.1%) | $0.04 total cost | 95% confidence threshold

---

## February 2026 — Manual Quality Lockdown & Identity

- **Phase 9.5** – Manual deep dive on 1,089 flagged strains
  → 20 hours URL-by-URL verification | added `strain_name_aka_manual`, `strain_name_manual`, `breeder_manual`, notes

- **Phase 10** – Lineage (parent genetics) extraction
  → 76.1% coverage (16,246 / 21,361 strains) | 21 lineage columns | 12 seed banks parsed | exceeded 70% target

- **Phase 11** – Identity standardization & cleanup
  - Seed banks: 100% cleaned & verified
  - Breeders: 100% verified (AI rescued ~4,000 "Unknown" via S3 HTML) → final 489 edge cases manual
  - Strain names: 21,361 reviewed → 21,223 final (removed 138 non-cannabis items)
  - Column reduction: 110 → 48 (later 54–58 after extensions)
  - Automated extractions from names/URLs: version markers, autoflower, feminized, CBD flags, AKA names, fast-flowering

---

## Late February 2026 — Botanical Extraction & Consolidation

- **Phase 12** – Seed-bank-specific botanical extraction
  → 88.3% strains with data (18,744 / 21,220)
  → Strong coverage: Crop King (~100%), Attitude (93.5%), North Atlantic (97% genetics), Herbies (95%+)
  → No/minimal data: Seedsman, Multiverse, Mephisto, Sensi, Barney's, RQS (JS-rendered or unstructured)
  → 19 separate CSVs + full HTML pattern documentation

- **Phases 13–16** – Normalization · merge · audit · cleanup
  → Unified file: 21,210 strains × 53 columns
  → Early Gemini THC validation attempt → 95% error rate (hallucinations) → abandoned

---

## March 2026 — Validation Breakthrough

- **Phases 17–18** – S3 HTML + Gemini 2.0 Flash validation
  - **Success:** 91.8% (19,475 / 21,210 strains)
  - Failed attempts: URL-grounding JSON → massive 400s & parsing errors → scrapped
  - Winning approach: archived S3 HTML + controlled JSON + 5-strain batches (~3 hours, ~$0.50)
  - Corrections: 1,303 total
    - 691 high-confidence (auto-apply candidates)
    - 225 medium
    - 387 low-confidence (manual review)
  - Top corrected fields: genetics_type (245), flowering times (407), genetics % (237), cannabinoids (414)

### Shannon's V1 Audit Notes
- Filtered `all_corrections.csv` by status → highlighted incorrect rows
- Removed average fields from review (thc_avg, cbd_avg, flowering_days_avg are calculated, not in HTML)
- Identified false positives: Gemini flagging flowering days that were correctly converted from weeks
  - Example: `early-misty-marijuana-seeds` — HTML says "10 weeks", we have 70 days. Gemini tried to "correct" to 10.
  - Example: `g13labs/purple-haze` — HTML has both "8-9 weeks" and "55-65 days". Converted weeks off by a couple days.

### V2 Validation Prepared (not yet run)
- Removed 3 avg columns (53 → 50 columns)
- Added standardization rules to Gemini prompt:
  - Flowering times must be in days (convert weeks × 7)
  - If HTML has both weeks AND days, prefer explicit days value
  - Genetics % must add to 100%
  - Genetics type must be Indica/Sativa Dominant or Balanced Hybrid
- Expanded validation to 17 fields (added heights, yields)
- Input: `pipeline/17_gemini_revalidation/input/pipeline_16_no_avg.csv`
- Script: `pipeline/17_gemini_revalidation/scripts/validate_s3_html_v2.py`

### Status at pause (March 5)
- V2 validation script ready but not executed
- 691 high-confidence corrections pending review/apply
- 387 low-confidence corrections pending manual review

---

## July 2026 — Project Revival & License Change

**Context**: Project paused March–July while working on other projects. Returning with fresh perspective.

### Decisions Made
- **Data is now free.** Licensed under CC BY 4.0 (attribution required, commercial use allowed)
- Removed commercial terms (Gumroad tiers, pricing, enterprise licensing)
- README overhauled — professional tone, clear usage instructions
- Original concept repo linked: [cannabis-intelligence-database](https://github.com/Shannon-Goddard/cannabis-intelligence-database)

### Cleanup
- Removed hardcoded GCP Project ID from 4 pipeline 17 scripts → now uses `GCP_PROJECT_ID` environment variable
- Scanned pipelines 16–18 for secrets — all clear

### Domain Planning (deferred)
- `strains.loyal9.app` → `strains.poweredbyci.live` (will update when ready)
- 51 domain references identified across project, mapped for future bulk update
- Separate repo (`ci-strains-pro-landing`) will serve the grower-facing strain tool

### What's Next
- V2 validation still pending execution
- High-confidence corrections still pending apply
- Domain migration when ready
- Strain explorer/search tool in `ci-strains-pro-landing`

---

## Philosophy
- Identity fields are gold standard (100% human-verified)
- Lineage is high-coverage (76.1%)
- Botanical data is being cleaned/validated iteratively
- Every data point traceable to archived HTML source
- Ship what's clean. Mark what's not.
