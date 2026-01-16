# JavaScript Extraction Quick Start

Run enhanced extractors on JS-rendered HTML to capture full product data.

## ILGM Extraction
```bash
cd pipeline/02_s3_scraping/ilgm
python ilgm_js_extractor.py
```

**Expected Output:**
- `ilgm_js_extracted.csv` - Full dataset (133 strains, 50+ columns)
- `ILGM_JS_EXTRACTION_REPORT.md` - Coverage analysis

**Target:** 50+ columns, 80%+ THC coverage (vs 6.8% from static HTML)

## Seedsman Extraction
```bash
cd pipeline/02_s3_scraping/seedsman
python seedsman_js_extractor.py
```

**Expected Output:**
- `seedsman_js_extracted.csv` - Full dataset (878 strains, 60+ columns)
- `SEEDSMAN_JS_EXTRACTION_REPORT.md` - Coverage analysis

**Target:** 60+ columns, 70%+ THC coverage (vs 0% from static HTML)

## What Changed?
- **Source:** `html_js/{hash}_js.html` (JavaScript-rendered)
- **Previous:** `html/{hash}.html` (static, missing data)
- **Result:** Full product tables, specifications, and attributes

## Time Estimate
- ILGM: ~2 minutes (133 strains)
- Seedsman: ~10 minutes (878 strains)

## Success Criteria
✅ THC coverage > 70%
✅ Flowering time data present
✅ Yield and height data captured
✅ Effects and flavors extracted
✅ Genetics/lineage identified

---
**Logic designed by Amazon Q, verified by Shannon Goddard.**
