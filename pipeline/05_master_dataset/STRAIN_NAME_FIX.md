# Strain Name Fix - 100% Coverage Achieved

**Date**: January 16, 2026  
**Script**: `08_fix_strain_names.py`  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Problem

Initial master dataset had only **59.8% strain_name coverage** (13,750/23,009 strains).

After fixing mapping keywords to exact match (`strain_name` only, not `strain`), coverage improved to **91.8%** (21,127/23,009).

Still missing: **1,882 strains** across 5 seed banks.

---

## Root Cause Analysis

### Missing Strain Names by Seed Bank

| Seed Bank | Missing | Reason |
|-----------|---------|--------|
| Seedsman (regular) | 878 | No `strain_name` column in CSV (static HTML extraction failed) |
| Multiverse Beans | 527 | `strain_name` column exists but empty (failed extractions) |
| Seedsman JS | 417 | `strain_name` column exists but empty (partial extraction failures) |
| Exotic | 51 | `strain_name` column exists but empty |
| Gorilla | 9 | Non-strain pages (category/filter pages, not products) |

### Investigation

**Multiverse Beans Example**:
- URL: `https://multiversebeans.com/product/aeque-genetics-zwiesel-strain-auto-fem-3-pack/`
- `strain_name`: Empty
- `thc_content`: Empty
- `genetics_lineage`: Empty
- **Conclusion**: Failed extraction, but URL contains strain name

**Gorilla Example**:
- URL: `https://www.gorilla-cannabis-seeds.co.uk/autoflowering-seed-banks.html`
- **Conclusion**: Category page, not a product page - should be removed

---

## Solution

### Step 1: Remove Non-Strain Pages
**Target**: Gorilla's 9 category/filter pages

**Logic**:
```python
gorilla_bad = df[
    (df['seed_bank'] == 'gorilla') & 
    (df['strain_name_raw'].isna()) &
    (df['source_url_raw'].str.contains('seed-banks|cannabis-seeds', na=False))
]
df = df[~df.index.isin(gorilla_bad.index)]
```

**Result**: Removed 9 non-product pages

---

### Step 2: Extract Strain Names from URLs
**Target**: Remaining 1,873 strains with missing names

**Extraction Logic**:
1. Get last segment of URL path
2. Remove file extensions (`.html`, `.php`, `.aspx`)
3. Remove product ID patterns (`prod_1234`)
4. Replace hyphens/underscores with spaces
5. Clean extra whitespace

**Examples**:

| URL | Extracted Name |
|-----|----------------|
| `https://multiversebeans.com/product/aeque-genetics-zwiesel-strain-auto-fem-3-pack/` | `aeque genetics zwiesel strain auto fem 3 pack` |
| `https://www.seedsman.com/us-en/platinum-green-apple-candy-feminized-seeds-atl-pgac-fem` | `platinum green apple candy feminized seeds atl pgac fem` |
| `https://www.cannabis-seeds-bank.co.uk/archive-seeds-zwoosh/prod_9996` | `archive seeds zwoosh` |

**Code**:
```python
def extract_name_from_url(url):
    if pd.isna(url):
        return None
    parts = url.rstrip('/').split('/')
    name = parts[-1] if parts else None
    if name:
        name = re.sub(r'\.(html|php|aspx)$', '', name)
        name = re.sub(r'prod_\d+$', '', name)
        name = name.replace('-', ' ').replace('_', ' ')
        name = ' '.join(name.split())
        return name if name else None
    return None

df.loc[missing, 'strain_name_raw'] = df.loc[missing, 'source_url_raw'].apply(extract_name_from_url)
```

---

## Results

### Before
- **Total Strains**: 23,009
- **strain_name Coverage**: 91.8% (21,127/23,009)
- **Missing**: 1,882 strains

### After
- **Total Strains**: 23,000 (removed 9 non-products)
- **strain_name Coverage**: 100.0% (23,000/23,000)
- **Missing**: 0 strains

---

## Data Quality Notes

### URL-Extracted Names
**Pros**:
- 100% coverage achieved
- Names are human-readable
- Preserves breeder/genetics info often in URL

**Cons**:
- Not as clean as scraped names (e.g., "auto fem 3 pack" included)
- May include product codes (e.g., "atl pgac fem")
- Requires cleaning in next phase

**Decision**: Keep URL-extracted names in `_raw` field. Clean in Phase 6 (cleaned data):
- Remove pack sizes ("3 pack", "5 seeds")
- Remove product codes
- Standardize capitalization
- Extract true strain name

### Seedsman Regular HTML (878 strains)
- Still have URL-extracted names
- Original static HTML had no strain data (ScandiPWA architecture)
- JS version has proper names - will use for deduplication in cleaning phase

---

## Files Modified

1. **schema.py** - Fixed `strain_name_raw` mapping from `['strain_name', 'strain']` to `['strain_name']` (exact match only)
2. **08_fix_strain_names.py** - New script to remove non-products and extract names from URLs
3. **master_strains_raw.csv** - Updated with 100% strain_name coverage

---

## Validation

**Sample Check** (Multiverse Beans):
```
Before: strain_name_raw = NaN
After:  strain_name_raw = "aeque genetics zwiesel strain auto fem 3 pack"
URL:    https://multiversebeans.com/product/aeque-genetics-zwiesel-strain-auto-fem-3-pack/
```

**Sample Check** (Gorilla - Removed):
```
URL: https://www.gorilla-cannabis-seeds.co.uk/autoflowering-seed-banks.html
Reason: Category page, not a product
Action: Removed from dataset
```

---

## Attribution

**Problem Identified**: Shannon Goddard  
**Solution Designed**: Amazon Q  
**Verification**: Shannon Goddard  
**Execution**: Amazon Q  

---

**Status**: ✅ COMPLETE - 100% strain_name coverage achieved
