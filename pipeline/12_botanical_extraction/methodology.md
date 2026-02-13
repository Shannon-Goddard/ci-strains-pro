# Phase 12: Botanical Data Extraction - Methodology

**Date:** February 12, 2026  
**Approach:** Seed bank-specific extraction (Phase 10 lineage playbook)  
**Goal:** 80%+ botanical coverage with confidence scores

---

## Data Processing Rules

### File Integrity
- NEVER overwrite Phase 11 clean data
- Always create `_extracted` or `_ai` versions of columns
- Use `latin-1` encoding for CSV reads (special cannabis breeder characters)
- Use `utf-8` encoding for CSV writes (standard output)

### Transparency Log Requirement
- Every extraction script must document HTML patterns used
- Every cleaning script must document transformations applied
- Coverage reports must show before/after statistics
- AI gap-fill must include confidence scores and reasoning

### Naming Conventions
- Extraction scripts: `extract_[seed_bank]_botanical.py`
- Cleaning scripts: `clean_[seed_bank]_botanical.py`
- Output columns: `[field]_extracted`, `[field]_ai`, `[field]_confidence_ai`

---

## Extraction Patterns

### THC/CBD Extraction
- **Pattern:** `(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%` (range)
- **Pattern:** `(\d+(?:\.\d+)?)%` (single value)
- **Output:** `thc_min_extracted`, `thc_max_extracted`, `thc_avg_extracted`
- **Handle:** Ranges vs single values (if single, min=max=value)

### Flowering Time Extraction
- **Pattern:** `(\d+)\s*-\s*(\d+)\s*weeks?` (range in weeks)
- **Pattern:** `(\d+)\s*-\s*(\d+)\s*days?` (range in days)
- **Convert:** Weeks → days (multiply by 7)
- **Output:** `flowering_time_min_extracted`, `flowering_time_max_extracted`

### Height Extraction
- **Pattern:** `(\d+)\s*-\s*(\d+)\s*cm` (range in cm)
- **Pattern:** `(\d+)\s*-\s*(\d+)\s*inches?` (range in inches)
- **Convert:** Inches → cm (multiply by 2.54)
- **Output:** `height_indoor_min_extracted`, `height_indoor_max_extracted`

### Yield Extraction
- **Pattern:** `(\d+)\s*-\s*(\d+)\s*g/m²` (indoor)
- **Pattern:** `(\d+)\s*-\s*(\d+)\s*g/plant` (outdoor)
- **Convert:** oz → grams (multiply by 28.35)
- **Output:** `yield_indoor_min_extracted`, `yield_indoor_max_extracted`

### Effects/Flavors/Terpenes Extraction
- **Pattern:** Comma-separated lists or bullet points
- **Clean:** Lowercase, strip whitespace, remove duplicates
- **Output:** `effects_extracted`, `flavors_extracted`, `terpenes_extracted`

---

## Cleaning Rules

### Unit Normalization
- **Height:** All values in cm
- **Flowering:** All values in days
- **Yield:** Indoor in g/m², outdoor in g/plant
- **THC/CBD:** All values as percentages (0-100)

### Range Validation
- **Rule:** min ≤ max (if violated, flag for review)
- **Rule:** THC/CBD ≤ 40% (if exceeded, flag for review)
- **Rule:** Flowering time 30-120 days (if outside, flag for review)

### Missing Data Handling
- **Rule:** Mark as null/NaN, don't infer
- **Rule:** Don't copy from other seed banks (wait for AI gap-fill)
- **Rule:** Don't use default values

---

## AI Gap-Fill Rules (Phase 12d)

### When to Use AI
- Field is null/missing after seed bank extraction
- S3 HTML archive exists for that strain
- Confidence threshold: 70%+ (below = flag for review)

### AI Prompt Structure
```
Extract botanical data from this cannabis strain HTML:
- THC min/max (%)
- CBD min/max (%)
- Flowering time (days)
- Height indoor/outdoor (cm)
- Yield indoor/outdoor (g)
- Effects (comma-separated)
- Flavors (comma-separated)
- Terpenes (comma-separated)

Return JSON with confidence scores (0-100) and reasoning.
```

### AI Output Columns
- `[field]_ai` - AI-extracted value
- `[field]_confidence_ai` - Confidence score (0-100)
- `[field]_reasoning_ai` - Why AI made this choice

---

## Quality Assurance

### Coverage Targets
- THC: 80%+ (critical for users)
- CBD: 60%+ (medical users)
- Flowering: 70%+ (growers)
- Height/Yield: 65%+ (growers)
- Effects/Flavors: 50%+ (recreational users)

### Validation Checks
- [ ] No negative values
- [ ] Min ≤ max for all ranges
- [ ] THC/CBD ≤ 40%
- [ ] Flowering time 30-120 days
- [ ] Height 30-300 cm
- [ ] Yield 100-2000 g/m² (indoor), 50-5000 g/plant (outdoor)

### Error Handling
- Log all extraction failures
- Flag outliers for manual review
- Track coverage by seed bank
- Generate error report

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
