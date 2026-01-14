# Multiverse Beans Maximum Extraction

**Status:** Ready for Production  
**Target:** 799 Multiverse Beans strains  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Overview

Comprehensive data extraction system for Multiverse Beans cannabis strain data, designed to capture 50+ data points per strain for maximum market value.

## Files

- `multiverse_beans_max_extractor.py` - Main extraction script
- `methodology.md` - Detailed extraction methodology
- `README.md` - This file

## Usage

```bash
python multiverse_beans_max_extractor.py
```

## Expected Output

- `multiverse_beans_maximum_extraction.csv` - Complete dataset
- `multiverse_beans_extraction_report.md` - Comprehensive analysis report

## Data Capture Strategy

### 8 Extraction Methods
1. **JSON-LD Data** - Structured e-commerce data
2. **Meta Tags** - SEO and social intelligence  
3. **Tables** - Specification data
4. **Pricing** - Multi-currency business intelligence
5. **Cannabis Data** - THC/CBD, effects, terpenes
6. **Media Assets** - Images and visual content
7. **Awards** - Certifications and recognition
8. **Genetics** - Lineage and breeding data

### Quality Scoring
- Weighted field importance
- Market tier classification
- Completeness metrics

## Market Tiers

- **Enterprise** (80%+) - Premium cultivation + business data
- **Professional** (60-79%) - Strong cultivation data
- **Standard** (40-59%) - Good baseline data  
- **Basic** (<40%) - Limited data

## Results

### Extraction Complete ✅
- **528 strains** successfully processed
- **137 columns** of comprehensive data captured
- **1.3MB dataset** generated
- **Average 56.7 fields** per strain

### The Gap Explained:
- **1,212 URLs** found in your URL mapping for Multiverse Beans
- **528 strains** actually processed = **43.6% coverage**

**Reasons for the gap:**
1. **Missing HTML files** - Not all URLs were successfully scraped/archived in S3
2. **Failed downloads** - Some pages may have been inaccessible during collection
3. **URL changes** - Some URLs may have become invalid since mapping

### Quality Distribution
- **521 Basic tier** - Limited source data
- **7 Standard tier** - Good data completeness
- **0 Professional/Enterprise** - Pages less data-rich than other banks

## Requirements

```
boto3
pandas
beautifulsoup4
```

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**