# 2026 Build Log – Cannabis Intelligence Empire  
**Solo grind to the world's most rigorous, traceable cannabis strain dataset**  
**Transparent chronicle: real costs · real setbacks · real breakthroughs**

**Current Snapshot (as of March 5, 2026)**  
- Final working strain count: **~21,210–21,223**  
- Identity fields (seed bank + breeder + strain name): **100% human-verified**  
- Lineage coverage: **76.1%** (16,246 strains)  
- Botanical data extracted: **88.3%** of strains (18,744)  
- Latest validation (S3 HTML + Gemini 2.0 Flash): **91.8%** success (19,475 strains)  
- Corrections from validation: **1,303 total** (691 high-confidence)  
- Total spend to date: **≈ $117** (Bright Data $41.27 + ScrapingBee $49.99 + AWS $25.62 + Vertex ~$0.55)  

**Live Source of Truth Viewer:** https://strains.loyal9.app  
( paste any strain URL → see exact timestamped HTML archive, signed + watermarked + 5-min expiry )

## January 2026 – Foundation & Bulk Extraction

- **Phase 6** – Breeder extraction + standardization  
  → 21,943 strains kept | 519 unique breeders (from 580, merged 61 duplicates) | **95.4%** success

- **Phase 7** – S3 unified archive  
  → **21,706 HTML files** | 19 seed banks | **100%** coverage | metadata JSON mapping

- **Phase 8** – Full botanical + metadata extraction  
  → **21,361 strains** | 38 fields per strain (genetics, grow specs, effects, etc.) | **98.4%** success

- **Phase 9** – Vertex AI validation  
  → 21,400 strains processed | **39,681 corrections** (~1.85 per strain) | **1,089 flagged** (5.1%) | **$0.04** total cost | 95% confidence threshold

## February 2026 – Manual Quality Lockdown & Identity

- **Phase 9.5** – Manual deep dive on 1,089 flagged strains  
  → **20 hours** URL-by-URL verification | added `strain_name_aka_manual`, `strain_name_manual`, `breeder_manual`, notes

- **Phase 10** – Lineage (parent genetics) extraction  
  → **76.1%** coverage (16,246 / 21,361 strains) | 21 lineage columns | 12 seed banks parsed | exceeded 70% target

- **Phase 11** – Identity standardization & massive cleanup  
  - Seed banks: **100%** cleaned & verified  
  - Breeders: **100%** verified (AI rescued ~4,000 "Unknown" via S3 HTML) → final 489 edge cases manual  
  - Strain names: **21,361 reviewed** → **21,223 final** (removed 138 non-cannabis items)  
  - Column reduction: **110 → 48** (later 54–58 after extensions)  
  - Automated extractions from names/URLs: version markers, autoflower, feminized, CBD flags, AKA names, fast-flowering, etc.  
  - Major lesson: **Always backup before merges** (one failed merge → full rebuild of names & breeders)

## Late February 2026 – Botanical Extraction & Consolidation

- **Phase 12** – Seed-bank-specific botanical extraction  
  → **88.3%** strains with data (18,744 / 21,220)  
  → Strong coverage: Crop King (~100%), Attitude (93.5% after fix), North Atlantic (97% genetics), Herbies (95%+), etc.  
  → No/minimal data: Seedsman, Multiverse, Mephisto, Sensi, Barney’s, RQS, etc. (JS-rendered or unstructured)  
  → 19 separate CSVs + full HTML pattern documentation

- **Phases 13–16** – Normalization · merge · audit · cleanup  
  → Unified file: **21,210 strains × 53 columns**  
  → Early Gemini THC validation attempt → **95% error rate** (hallucinations) → abandoned

## March 2026 – Validation Breakthrough

- **Phases 17–18** – S3 HTML + Gemini 2.0 Flash validation (Mar 5)  
  - **Success:** **91.8%** (19,475 / 21,210 strains)  
  - Failed attempts: URL-grounding JSON → massive 400s & parsing errors → scrapped  
  - Winning approach: archived S3 HTML + controlled JSON + 5-strain batches (~3 hours, ~$0.50)  
  - Corrections: **1,303 total**  
    - 691 high-confidence (auto-apply candidates)  
    - 225 medium  
    - 387 low-confidence (manual review)  
  - Top corrected fields: genetics_type, flowering days, indica/sativa %, THC/CBD min-max

### Immediate Next Actions (Mar 5+)
1. Review `high_confidence_corrections.csv` (691 rows)  
2. Review `manual_review_needed.csv` (387 rows)  
3. Apply approved corrections  
4. Re-run full data quality audit  
5. (Optional) 2nd iterative Gemini pass on remaining issues  
6. Build **CLEAN** / **FILTERED** / **FILLED** dataset versions  
7. Prep raw-tier Gumroad launch

## Philosophy & Transparency
- **Gold tier** = 100% human-verified identity (seed bank, breeder, strain name)  
- **Silver tier** = high-coverage lineage  
- **Bronze tier** = extracted botanical (being cleaned/normalized)  
→ **"Ship what's clean. Mark what's not."**

From raw HTML graveyard to production-grade traceable dataset in ~6 weeks.  
All archives immutable. All corrections auditable. No trust-me-bro.

**Momentum strong. Keep grinding.** 🌿