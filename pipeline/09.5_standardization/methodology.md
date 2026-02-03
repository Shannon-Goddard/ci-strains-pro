# Phase 9.5: Name Standardization Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Objective
Create display-ready and research-ready versions of breeder and strain names across all 21,489 strains.

## Data Source Priority
1. `*_manual` (human-verified, 1,088 strains)
2. `*_validated` (AI-verified, 21,400 strains)
3. `*_raw` (extracted data)

## Standardization Rules

### Display Names (`*_display`)
- Proper title case capitalization
- Preserve special characters and punctuation
- Exception words: "and", "x", "the", "of", "by" (lowercase unless first word)
- Purpose: Customer-facing UI, reports, marketplace listings

### Slug Names (`*_slug`)
- All lowercase
- Remove special characters (keep alphanumeric, hyphens)
- Replace spaces with hyphens
- Purpose: Deduplication matching, database keys, research queries

## Output Columns
- `breeder_display` - Display-ready breeder name
- `breeder_slug` - Research-ready breeder slug
- `strain_name_display` - Display-ready strain name
- `strain_name_slug` - Research-ready strain slug

## Results
- **21,489** breeders standardized (100%)
- **21,432** strain names standardized (99.7%)
- Ready for Phase 10 deduplication
