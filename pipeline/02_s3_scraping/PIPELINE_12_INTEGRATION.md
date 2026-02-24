# Pipeline 12 Botanical Extraction - Integration Notes

**Date:** February 23, 2026  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Overview

Pipeline 12 performed targeted botanical data extraction from S3 HTML archives for seed banks not covered by pipeline 02's comprehensive extractors.

## Seed Banks Processed

### Successfully Extracted (New)
These banks had no prior extractors in pipeline 02:

1. **Gorilla Cannabis Seeds** (1,967 strains)
   - Pattern: `<table class="product-topattributes">`
   - Coverage: 79.5% THC, 85.0% yield, 88.5% flowering

2. **Neptune Seed Bank** (1,982 strains)
   - Pattern: Meta description tags
   - Coverage: 76.3% lineage

3. **Amsterdam Marijuana Seeds** (159 strains)
   - Pattern: `<div class="ams-attr-row">`
   - Coverage: 98.7% THC, 97.5% flowering

4. **ILGM** (133 strains)
   - Pattern: Plain text "THC - X%"
   - Coverage: 98.5% THC

### Already Covered by Pipeline 02
These banks already had comprehensive extractors:
- Attitude Seedbank (7,661)
- Crop King Seeds (3,332)
- North Atlantic (2,717)
- Herbies Seeds (753)
- Barney's Farm (88)
- And others...

## Files Created

Location: `pipeline/12_botanical_extraction/output/`

- botanical_gorilla.csv
- botanical_neptune.csv
- botanical_amsterdam.csv
- botanical_ilgm.csv
- botanical_exotic.csv (placeholder - no data)
- botanical_multiverse_beans_seed_bank.csv (placeholder)
- botanical_seed_supreme.csv (placeholder)
- botanical_mephisto_genetics.csv (placeholder)
- botanical_seedsman.csv (placeholder)
- Plus others...

## Integration

Pipeline 12 outputs are separate from pipeline 02 extractions. Both contain botanical data but:
- Pipeline 02: Comprehensive 94-column extractions with quality scores
- Pipeline 12: Targeted botanical-only extractions for gaps

Use pipeline 02 results where available (higher quality). Use pipeline 12 for banks not in pipeline 02.

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
