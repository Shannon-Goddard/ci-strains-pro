# Amsterdam Marijuana Seeds Extraction Report

**Date:** January 14, 2026  
**Processor:** Amsterdam 9-Method Extractor  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Extraction Summary

### Success Metrics
- **Total Strains Extracted:** 163
- **Total Columns Captured:** 66
- **Data Source:** S3 unified inventory (html/html/ path)
- **Extraction Success Rate:** 100%

### Data Quality Scores
- **THC Data:** 159/163 strains (97.5%)
- **Effects Profile:** 163/163 strains (100%)
- **Flavor Profile:** 156/163 strains (95.7%)
- **Indica/Sativa Ratio:** Captured in ams_indica_/_sativa field
- **Flowering Time:** Captured in ams_flowering_time field

### Key Fields Extracted

#### AMS-Specific Table Data
- `ams_thc` - THC content indicator
- `ams_thc_level` - Specific THC percentage
- `ams_effects` - Psychoactive effects
- `ams_flavor` - Terpene/taste profile
- `ams_yield` - Production data
- `ams_seed_type` - Strain classification
- `ams_indica_/_sativa` - Genetic ratio
- `ams_plant_size` - Growth characteristics
- `ams_grow_difficulty` - Cultivation complexity
- `ams_flowering_time` - Time to harvest
- `ams_climate` - Growing environment

#### Meta & Description Data
- Meta tags (viewport, description, robots, og tags)
- Product descriptions
- Strain names from URLs

### Amsterdam-Specific Structure
Amsterdam uses a unique `ams-attr-table` structure with:
- `ams-attr-row` divs containing label/value pairs
- Clean, structured data presentation
- High data completeness across all fields

## Output Files
- **Main Dataset:** `amsterdam_extracted.csv`
- **Methodology:** `methodology.md`
- **Extractor:** `amsterdam_extractor.py`

## Next Steps
Continue with remaining elite seed banks:
1. ✅ Amsterdam Marijuana Seeds (163 strains)
2. Gorilla Seed Bank
3. Herbies Seeds
4. Exotic Genetix
5. Compound Genetics

---
**Processing completed with 9-method extraction pipeline.**
