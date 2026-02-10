# Phase 11: Column Cleanup Methodology

**Date:** February 9, 2026  
**Input:** `pipeline_11_breeder_extracted.csv` (21,361 strains, 110 columns)  
**Output:** `pipeline_11_clean.csv` (21,361 strains, 47 columns)  
**Removed:** 63 columns (57% reduction)

---

## Cleanup Strategy

### What We Kept (47 columns)

**Identity Columns (9) - GOLD TIER**
- `strain_id` - Unique identifier
- `seed_bank_display_manual` - ✅ 100% verified
- `breeder_display_manual` - ✅ 100% verified  
- `strain_name_display_manual` - ✅ 100% verified
- `source_url_raw` - Source of truth link
- `s3_html_key_raw` - Archive proof
- `scraped_at_raw` - Timestamp
- `notes_manual` - Manual review notes
- `manual_notes` - Additional notes

**Lineage Columns (16) - SILVER TIER**
- `parent_1_display`, `parent_2_display` (76.1% coverage)
- `parent_1_slug`, `parent_2_slug`
- `grandparent_1_display`, `grandparent_2_display`, `grandparent_3_display`
- `grandparent_1_slug`, `grandparent_2_slug`, `grandparent_3_slug`
- `lineage_formula` (61.8% coverage)
- `lineage_depth`
- `generation_clean`, `filial_generation`, `selfed_generation`, `backcross_generation`

**Genetics Metadata (5)**
- `genetics_type_clean` (Sativa/Indica/Hybrid)
- `indica_percentage_clean`, `sativa_percentage_clean`
- `is_autoflower_clean`
- `seed_type_raw`

**Botanical Data (18) - BRONZE TIER (Phase 12+ cleaning)**
- THC: `thc_min_raw`, `thc_max_raw`, `thc_content_raw`
- CBD: `cbd_min_raw`, `cbd_max_raw`, `cbd_content_raw`
- CBN: `cbn_content_raw`
- Grow specs: `flowering_time_days_clean`, `height_indoor_cm_clean`, `height_outdoor_cm_clean`
- Yield: `yield_indoor_g_m2_clean`, `yield_outdoor_g_plant_clean`
- Experience: `effects_all_raw`, `flavors_all_raw`, `terpenes_raw`
- Cultivation: `climate_raw`, `difficulty_raw`

---

## What We Deleted (63 columns)

**Phase 9 Validation Columns (10)**
- `validation_confidence`, `validation_reasoning`, `validation_changes`
- `flagged_for_review`, `validation_attempted`
- `breeder_validated`, `strain_name_validated`
- `breeder_confidence`, `breeder_reasoning`
- `genetics_confidence`
- **Reason:** Superseded by manual review (Phase 11)

**Duplicate/Redundant Columns (53)**
- All `*_raw` columns that have `*_manual` equivalents
- All `*_extracted` columns (Phase 8 - superseded)
- All `*_normalized` columns (not needed until strain name review complete)
- All intermediate `*_slug` columns (will regenerate after strain name review)
- Duplicate `source_url_raw.1`
- Low-value fields: `awards_raw`, `description_raw`, `similar_spelling_clean`, etc.

---

## Data Quality Tiers

**GOLD (100% verified)**
- Identity columns: seed bank, breeder, strain name
- Manually reviewed and corrected by Shannon

**SILVER (76.1% coverage)**
- Lineage data: parents, grandparents, generation markers
- High value, good coverage, Phase 10 extraction

**BRONZE (15-53% coverage)**
- Botanical data: THC, CBD, flowering, yield, effects
- Raw extraction, needs Phase 12+ cleaning
- Kept for future work, marked as unverified

---

## Next Steps

1. ✅ Column cleanup complete
2. 🔄 **Strain name manual review** (Shannon)
3. 📋 **Regenerate slugs** after strain name review
4. 📋 **Phase 12: Botanical data cleaning** (min/max expansion, validation)
5. 📋 **Phase 13: Master merge** (deduplication strategy)

---

## Philosophy

**"Ship what's clean. Mark what's not."**

- Don't ship 110 columns of confusion
- Don't pretend raw extraction is verified
- Keep botanical data for Phase 12+, but mark as BRONZE tier
- Transparency = value

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
