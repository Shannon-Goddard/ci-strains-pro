# Seedsman Dual Extraction Issue

## Problem Discovery

During Step 01 (URL Deduplication), we discovered that Seedsman had two separate extractions in the raw dataset:

1. **`seedsman`** (878 strains) - HTML extraction
   - Poor data quality
   - Missing or incomplete URLs
   - Unreliable field extraction
   
2. **`seedsman_js`** (866 strains) - JavaScript extraction
   - High data quality
   - Complete URLs
   - Proper field extraction with 79 columns

## Root Cause

Seedsman's website uses JavaScript to render product data. The initial HTML extraction captured the page structure but missed the dynamically loaded content. A second extraction using JavaScript rendering (via ScrapingBee) successfully captured the complete data.

## Decision

**Remove entire `seedsman` seed bank, keep `seedsman_js`**

### Rationale
- HTML extraction provided no value (incomplete/missing data)
- JS extraction provided complete, high-quality data
- Keeping both would create confusion and data quality issues
- Better to have 866 high-quality records than 878 low-quality + 866 high-quality

## Implementation

Modified `01_remove_duplicate_urls.py` to:
1. Filter out all rows where `seed_bank = 'seedsman'` (878 strains removed)
2. Keep all rows where `seed_bank = 'seedsman_js'` (866 strains retained)
3. Proceed with normal URL deduplication on remaining dataset

## Impact

- **Removed**: 878 low-quality Seedsman HTML records
- **Retained**: 866 high-quality Seedsman JS records
- **Net loss**: 12 strains (likely duplicates or non-product pages)
- **Quality improvement**: 100% of remaining Seedsman data is high-quality

## Lessons Learned

For future JavaScript-heavy websites:
1. Always use JavaScript rendering (ScrapingBee, Playwright, Selenium)
2. Don't waste time on HTML-only extraction for JS-rendered sites
3. Validate extraction quality before scaling to full dataset
4. Document dual extractions clearly to avoid confusion in downstream pipelines

---

**Decision made by**: Shannon Goddard  
**Implemented by**: Amazon Q  
**Date**: January 17, 2026
