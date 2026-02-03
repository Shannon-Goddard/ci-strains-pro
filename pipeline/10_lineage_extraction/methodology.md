# Phase 10: Lineage Extraction Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Objective
Extract parent genetics, breeding methods, and generational data to enable lineage-based duplicate detection and genetic knowledge graph construction.

## Column Structure

### Direct Parents
- `parent_1_display` / `parent_1_slug` - First parent (display + research format)
- `parent_2_display` / `parent_2_slug` - Second parent
- `parent_1_is_hybrid` / `parent_2_is_hybrid` - Boolean flags for nested crosses

### Grandparents (Nested Crosses)
- `grandparent_1_display` / `grandparent_1_slug` - Extracted from hybrid parents
- `grandparent_2_display` / `grandparent_2_slug`
- `grandparent_3_display` / `grandparent_3_slug`

### Breeding Intelligence
- `generation_clean` - Primary generation marker (F1, S1, BX1, etc.)
- `filial_generation` - F-series (F1, F2, F3...)
- `selfed_generation` - S-series (S1, S2...)
- `backcross_generation` - BX-series (BX1, BX2...)

### Matching & Research
- `lineage_formula` - Normalized formula for duplicate detection (e.g., "big-bud x purple-haze")
- `lineage_depth` - Levels of crossing (1 = simple cross, 2 = nested cross)
- `has_nested_cross` - Boolean flag for complex genetics

## Extraction Patterns
- Cross patterns: "X x Y", "cross of X and Y", "X crossed with Y"
- Generation markers: F1-F9, S1-S9, BX1-BX9
- Nested detection: Identifies hybrid parents containing " x "

## Results (Phase 10 Initial)
- **3,084** strains with parent data (14.4%)
- **832** strains with generation markers (3.9%)
- **300** nested crosses identified (1.4%)
- **300** grandparents extracted

## Next Steps
- Manual review of high-value strains to improve coverage
- AI enrichment to fill missing lineage data
- Lineage-based deduplication after AI completion
