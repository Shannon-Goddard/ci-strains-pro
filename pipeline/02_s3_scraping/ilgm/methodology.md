# ILGM Methodology

## Current Extraction
- **Source**: S3 static HTML (no JavaScript)
- **Strains**: 133
- **THC Coverage**: 6.8%

## What's Available
- Meta descriptions with THC ranges
- Basic strain info
- URLs

## What's Missing (Requires JS)
- Plant Type, Genotype, Lineage
- Flowering times, Yield data
- Terpenes, Effects, Flavors
- Bud structure, Growing specs
- Temperature/humidity ranges

## Rescrape Requirements
**Tool**: ScrapingBee with JavaScript rendering  
**Target**: Table rows with class `flex justify-between`  
**Expected**: 25+ fields per strain

**Logic designed by Amazon Q, verified by Shannon Goddard.**
