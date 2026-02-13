# Phase 12: Botanical Data Extraction - Setup Guide

**Date:** February 12, 2026  
**Status:** Ready to start  
**Input:** `pipeline/11_manual_review_and_validation/output/pipeline_11_clean.csv` (21,223 strains)  
**Goal:** 80%+ botanical data coverage using seed bank-specific extraction

---

## Current State (Phase 11 Complete)

**Identity Columns: GOLD Tier (100% verified)**
- `seed_bank_display_manual` - ✅ 100% verified
- `breeder_display_manual` - ✅ 100% verified  
- `strain_name_display_manual` - ✅ 100% verified
- `strain_name_raw` - ✅ 100% coverage
- `strain_name_slug` - ✅ 100% coverage

**Lineage Columns: SILVER Tier (76.1% coverage)**
- Parent genetics, grandparents, generation markers
- High value, Phase 10 extraction complete

**Botanical Columns: BRONZE Tier (15-53% coverage - NEEDS WORK)**
- THC: 52.9% coverage (thc_min_raw, thc_max_raw)
- CBD: 16.4% coverage (cbd_min_raw, cbd_max_raw)
- Flowering: 18.7% coverage (flowering_time_days_clean)
- Height: 15-19% coverage (height_indoor/outdoor_cm_clean)
- Yield: 15-17% coverage (yield_indoor/outdoor_g_clean)
- Effects: 10.1% coverage (effects_all_raw)
- Flavors: 21.6% coverage (flavors_all_raw)
- Terpenes: 5.3% coverage (terpenes_raw)

---

## Phase 12 Strategy: The Phase 10 Lineage Playbook

### Why Seed Bank-Specific Extraction Works

**Phase 10 Results (Lineage):**
- Generic extraction: ~20% coverage
- Seed bank-specific: **76.1% coverage**
- **3.8x improvement**

**Apply same approach to botanical data:**
- 19 custom extraction scripts (one per seed bank)
- Each script knows that seed bank's HTML structure
- Clean and validate per seed bank
- Merge into unified dataset

---

## Phase 12 Workflow

### 12a: Seed Bank-Specific Extraction (19 scripts)

**For each seed bank, extract:**
- **THC/CBD:** Min, max, average, content (handle ranges vs single values)
- **Flowering time:** Days, weeks (convert to days)
- **Height:** Indoor/outdoor in cm (convert from inches/feet)
- **Yield:** Indoor (g/m²), outdoor (g/plant)
- **Effects:** Energetic, relaxed, uplifting, etc.
- **Flavors:** Sweet, earthy, citrus, etc.
- **Terpenes:** Myrcene, limonene, caryophyllene, etc.
- **Climate:** Indoor, outdoor, greenhouse
- **Difficulty:** Easy, moderate, expert

**Script naming:** `extract_[seed_bank]_botanical.py`

**Example seed banks (19 total):**
1. Amsterdam Marijuana Seeds
2. Attitude Seed Bank
3. Barney's Farm
4. Crop King Seeds
5. Dutch Passion
6. Exotic Seeds
7. Gorilla Seeds
8. Herbies Seeds
9. ILGM
10. Mephisto Genetics
11. Multiverse Beans
12. Neptune Seed Bank
13. North Atlantic Seed Co
14. Royal Queen Seeds
15. Seed City
16. Seedsman
17. Seeds Here Now
18. Seed Supreme
19. Sensi Seeds

### 12b: Per-Seed-Bank Cleaning (19 scripts)

**For each seed bank, clean:**
- **Normalize units:**
  - Height: inches/feet → cm
  - Flowering: weeks → days
  - Yield: oz → grams
- **Fix encoding:** Handle special characters (Ã, â, etc.)
- **Standardize formats:**
  - THC: "20-25%" → thc_min=20, thc_max=25
  - Flowering: "8-10 weeks" → 56-70 days
- **Validate ranges:** Ensure min < max
- **Handle missing data:** Mark as null, don't infer

**Script naming:** `clean_[seed_bank]_botanical.py`

### 12c: Merge Clean Data

**Combine all 19 cleaned datasets:**
- Merge on `strain_id`
- Keep Phase 11 identity columns
- Add botanical columns with `_extracted` suffix
- Create coverage report

**Output:** `all_strains_botanical_extracted.csv`

### 12d: Gemini Flash Gap-Fill + Validation

**For strains with missing botanical data:**
- Read S3 HTML archive
- Extract missing fields with Gemini 2.0 Flash
- Add `_ai` suffix columns (thc_min_ai, thc_max_ai, etc.)
- Add `_confidence` and `_reasoning` for each AI field
- **Cost estimate:** ~$0.10 for 21,223 strains

**Output:** `all_strains_botanical_complete.csv`

---

## Technical Details

### Input File Location
```
pipeline/11_manual_review_and_validation/output/pipeline_11_clean.csv
```

### S3 HTML Archive Access
```python
import boto3
s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'
key = df['s3_html_key_raw']  # e.g., 'html/22135a34219dd5f1.html'
```

### Vertex AI Configuration
```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="gen-lang-client-0100184589", location="us-central1")
model = GenerativeModel("gemini-2.0-flash-exp")
```

### Encoding Rules
- **Read CSVs:** `encoding='latin-1'` (handles special breeder characters)
- **Write CSVs:** `encoding='utf-8'` (standard output)

### Column Naming Convention
- **Raw extraction:** `[field]_raw` (original from Phase 8)
- **Cleaned extraction:** `[field]_extracted` (Phase 12a-12b)
- **AI gap-fill:** `[field]_ai` (Phase 12d)
- **Confidence:** `[field]_confidence_ai` (0-100 score)
- **Reasoning:** `[field]_reasoning_ai` (why AI made this choice)

---

## Expected Coverage After Phase 12

| Field | Current | Target | Method |
|-------|---------|--------|--------|
| THC min/max | 52.9% | 80%+ | Seed bank extraction + AI |
| CBD min/max | 16.4% | 60%+ | Seed bank extraction + AI |
| Flowering time | 18.7% | 70%+ | Seed bank extraction + AI |
| Height indoor/outdoor | 15-19% | 65%+ | Seed bank extraction + AI |
| Yield indoor/outdoor | 15-17% | 65%+ | Seed bank extraction + AI |
| Effects | 10.1% | 50%+ | Seed bank extraction + AI |
| Flavors | 21.6% | 50%+ | Seed bank extraction + AI |
| Terpenes | 5.3% | 40%+ | Seed bank extraction + AI |

---

## Seed Bank Priority Order

**Start with highest-volume seed banks:**
1. **Attitude** (7,673 strains) - Largest inventory
2. **North Atlantic** (2,727 strains) - Good data quality
3. **Gorilla** (2,000 strains) - Clean HTML structure
4. **Neptune** (1,995 strains) - Consistent format
5. **Herbies** (753 strains) - High lineage coverage (83.9%)

**Then medium-volume:**
6. Seedsman (866 strains)
7. Barney's Farm (88 strains)
8. Royal Queen Seeds
9. ILGM (133 strains)
10. Mephisto Genetics

**Finally low-volume/difficult:**
11-19. Remaining seed banks

---

## Key Decisions from Phase 11

**Deduplication Strategy (for Phase 13.5):**
- **Ranges:** THC/CBD/flowering/height/yield → merge min/max across sources
- **Most filled:** Effects/flavors/terpenes → union of all values
- **First verified:** Lineage → flag conflicts for review

**Data Quality Tiers:**
- **GOLD:** Identity columns (100% verified by Shannon)
- **SILVER:** Lineage columns (76.1% coverage, Phase 10)
- **BRONZE:** Botanical columns (Phase 12 extraction + AI)

---

## Files to Create

### Phase 12a: Extraction Scripts (19 files)
```
scripts/extract_attitude_botanical.py
scripts/extract_north_atlantic_botanical.py
scripts/extract_gorilla_botanical.py
... (16 more)
```

### Phase 12b: Cleaning Scripts (19 files)
```
scripts/clean_attitude_botanical.py
scripts/clean_north_atlantic_botanical.py
scripts/clean_gorilla_botanical.py
... (16 more)
```

### Phase 12c: Merge Script (1 file)
```
scripts/merge_botanical_data.py
```

### Phase 12d: AI Gap-Fill Script (1 file)
```
scripts/gemini_gap_fill_botanical.py
```

### Documentation (3 files)
```
docs/EXTRACTION_PATTERNS.md (HTML patterns per seed bank)
docs/COVERAGE_REPORT.md (before/after statistics)
methodology.md (Phase 12 approach)
```

---

## Success Criteria

- [ ] 19 seed bank extraction scripts complete
- [ ] 19 seed bank cleaning scripts complete
- [ ] Merged dataset with 80%+ THC coverage
- [ ] Merged dataset with 60%+ CBD coverage
- [ ] Merged dataset with 70%+ flowering time coverage
- [ ] AI gap-fill complete (100% coverage with confidence scores)
- [ ] Coverage report generated
- [ ] Methodology documented

---

## Cost Estimate

**Gemini 2.0 Flash (gap-fill):**
- 21,223 strains × ~500 tokens/strain = ~10.6M tokens
- Input: $0.075 per 1M tokens = $0.80
- Output: $0.30 per 1M tokens = $3.18
- **Total: ~$4.00** (well under $1,200 Vertex budget)

---

## Next Steps

1. Copy `pipeline_11_clean.csv` to `pipeline/12_botanical_extraction/input/`
2. Start with Attitude seed bank (largest inventory)
3. Build extraction script for Attitude
4. Build cleaning script for Attitude
5. Validate output, then replicate for remaining 18 seed banks
6. Merge all cleaned data
7. Run Gemini gap-fill for missing fields
8. Generate coverage report

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
