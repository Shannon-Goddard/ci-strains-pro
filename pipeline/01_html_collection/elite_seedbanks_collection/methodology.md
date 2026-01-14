# Pipeline 06 Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Overview

Pipeline 06 applies proven methodologies from Pipelines 01, 04, and 05 to 8 elite seedbanks, targeting the 20,000-strain milestone through systematic URL discovery, bulletproof HTML collection, and maximum-value extraction.

## Phase 1: Intelligent URL Discovery

### Multi-Pattern Pagination Handling

**Standard Page Numbers:**
- Herbies Head Shop: `/page/{n}`
- Amsterdam Marijuana Seeds: `/page/{n}/`
- Exotic Genetix: `/page/{n}/`

**Query Parameters:**
- Gorilla Seeds Bank: `?page={n}`
- Zamnesia: `?p={n}`

**Single-Page Catalogs:**
- Original Seeds Store: No pagination
- Tiki Madman: Single strain list
- Compound Genetics: Collection-based

### Selector Strategy

Each seedbank uses specific CSS selectors based on their HTML structure:
- Product links: `a.product-item-link`, `a.woocommerce-LoopProduct-link`
- Strain links: `a.strain-link`, `a.product-name`
- Title links: `a.product-item__title`

### Deduplication

- URL normalization (trailing slashes, query parameters)
- Hash-based duplicate detection
- Cross-seedbank URL comparison

## Phase 2: Bulletproof HTML Collection

### Three-Layer Fallback System

**Layer 1: Bright Data (Primary)**
- Residential proxy network
- JavaScript rendering
- Geographic rotation
- Success rate: 85-90%

**Layer 2: ScrapingBee (Fallback)**
- Premium JavaScript rendering
- Anti-bot bypass
- Custom headers support
- Success rate: 90-95%

**Layer 3: Direct Requests (Final)**
- Standard HTTP requests
- Custom user agents
- Rate limiting
- Success rate: 60-70%

### 8-Point HTML Validation

1. **Status Code:** 200 OK
2. **Content Length:** >5KB minimum
3. **HTML Structure:** Valid opening/closing tags
4. **Product Indicators:** Strain name, price, or description present
5. **No Error Pages:** No 404/403 content
6. **JavaScript Content:** Rendered dynamic content
7. **Image Presence:** Product images loaded
8. **Text Density:** Sufficient text content

**Validation Score:** Weighted average (0.0-1.0)
**Acceptance Threshold:** 0.75

### S3 Storage Architecture

**Bucket:** `ci-strains-html-archive`
**Structure:**
```
pipeline06/
├── herbies/
│   ├── [url_hash].html
│   └── metadata.json
├── amsterdam/
├── gorilla/
├── zamnesia/
├── exotic/
├── original/
├── tiki/
└── compound/
```

**Encryption:** AES-256
**Metadata:** URL, timestamp, validation score, collection method

## Phase 3: Maximum Extraction

### 8-Method Extraction Pipeline

**Method 1: JSON-LD Structured Data**
- Schema.org Product markup
- Pricing, availability, ratings
- Breeder information
- Weight: 15%

**Method 2: Comprehensive Meta Tags**
- Open Graph tags
- Twitter Cards
- SEO metadata
- Weight: 10%

**Method 3: Structured Tables**
- Specification tables
- Growing parameters
- Cannabinoid profiles
- Weight: 20%

**Method 4: Advanced Pricing Intelligence**
- Multi-currency support
- Package variations
- Bulk pricing
- Weight: 15%

**Method 5: Cannabis-Specific Mining**
- THC/CBD percentages
- Flowering time
- Yield estimates
- Effects and flavors
- Weight: 25%

**Method 6: Media Asset Harvesting**
- Product images
- Gallery counts
- Video presence
- Weight: 5%

**Method 7: Awards & Certifications**
- Cup wins
- Certifications
- Recognition
- Weight: 5%

**Method 8: Enhanced Genetics Analysis**
- Parent strains
- Lineage tracking
- Breeder information
- Seed type classification
- Weight: 5%

### Quality Scoring Formula

```python
quality_score = (
    (premium_fields_filled / total_premium_fields) * 10 +
    (high_value_fields_filled / total_high_value_fields) * 6 +
    (standard_fields_filled / total_standard_fields) * 3
) / 19 * 100
```

**Premium Fields (Weight: 10):**
- THC/CBD percentages
- Flowering time
- Yield estimates
- Genetics/lineage
- Pricing data
- Awards

**High Value Fields (Weight: 6):**
- Effects
- Flavors
- Package options
- Breeder information
- Growing difficulty
- Media assets

**Standard Fields (Weight: 3):**
- Strain name
- Description
- Seed type
- Image count
- Availability

### Market Tier Classification

**Enterprise Tier (80%+):**
- Complete cultivation data
- Full business intelligence
- Premium genetics information
- Multi-currency pricing
- Target: Exotic Genetix, Tiki Madman, Compound

**Professional Tier (60-79%):**
- Strong cultivation data OR genetics
- Good pricing intelligence
- Solid media presence
- Target: Herbies, Gorilla, Zamnesia

**Standard Tier (40-59%):**
- Good baseline data
- Basic cultivation info
- Standard pricing
- Target: Amsterdam, Original Seeds

**Basic Tier (<40%):**
- Limited data availability
- Minimal specifications
- Basic product info
- Target: <5% of total

## Data Integrity Rules

### File Integrity
- NEVER overwrite raw HTML
- Always create `_cleaned` or `_processed` versions
- Use `latin-1` encoding for special characters

### Transparency Log
- Every script generates `methodology.md`
- Attribution: "Logic designed by Amazon Q, verified by Shannon Goddard"

### Naming Conventions
- Folders: `pipeline/06_elite_seedbanks_collection/`
- CSVs: `lowercase_with_underscores.csv`
- Scripts: `descriptive_action.py`

## Success Criteria

### URL Discovery
- ✅ 95%+ of expected URLs discovered
- ✅ <2% duplicate rate
- ✅ Valid URL format (HTTP/HTTPS)
- ✅ Seedbank-specific URL patterns matched

### HTML Collection
- ✅ 100% collection attempt rate
- ✅ 85%+ successful collection rate
- ✅ 0.75+ average validation score
- ✅ Complete S3 storage with metadata

### Extraction
- ✅ 70-140 columns per seedbank
- ✅ 50-75% average quality score
- ✅ Multi-tier market distribution
- ✅ <1% extraction errors

## Performance Targets

**URL Discovery:** 30 minutes for 3,083 URLs
**HTML Collection:** 4-6 hours with multi-layer fallback
**Extraction:** 6-8 hours per seedbank (48-64 hours total)
**Total Pipeline:** 52-70 hours end-to-end

## Risk Mitigation

**Anti-Bot Detection:**
- Residential proxies (Bright Data)
- JavaScript rendering (ScrapingBee)
- Rate limiting (2-5 seconds between requests)
- User agent rotation

**Data Loss:**
- S3 redundancy
- Local backup copies
- Progress tracking database
- Resumable operations

**Quality Issues:**
- Multi-method extraction
- Weighted scoring system
- Manual spot-checking
- Automated validation

---

**This methodology ensures Pipeline 06 maintains the quality standards established in Pipelines 01-05 while scaling to elite and boutique seedbanks.**

**Logic designed by Amazon Q, verified by Shannon Goddard.**
