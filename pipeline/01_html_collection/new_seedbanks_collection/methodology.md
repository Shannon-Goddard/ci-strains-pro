# Cannabis Intelligence Database - New Seedbanks Collection Methodology

**Date**: January 11, 2026  
**Phase**: 4 - New Seedbanks HTML Collection  
**Status**: Implementation Ready  

---

## Methodology Statement

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Executive Summary

This methodology extends the proven bulletproof HTML collection system to capture strain data from 5 premium seedbanks, integrating seamlessly with the existing S3 archive of 13,163 strain pages.

---

## Target Seedbanks Analysis

### 1. Sensi Seeds (sensiseeds.us)
- **Category Page**: https://sensiseeds.us/cannabis-seeds/
- **Product Example**: https://sensiseeds.com/en/feminized-seeds/sensi-seeds/big-bud-feminized
- **Estimated Strains**: 500-1000
- **Rate Limit**: 2 seconds (respectful)

### 2. Humboldt Seed Company (californiahempseeds.com)
- **Category Page**: https://californiahempseeds.com/shop-all/
- **Product Example**: https://humboldtseedcompany.com/appleblossom/
- **Estimated Strains**: 200-500
- **Rate Limit**: 2 seconds

### 3. Crop King (cropkingseeds.com)
- **Category Page**: https://www.cropkingseeds.com/?s=seeds&post_type=product
- **Product Example**: https://www.cropkingseeds.com/feminized-seeds/permanent-marker-strain-feminized-marijuana-seeds/
- **Estimated Strains**: 300-600
- **Rate Limit**: 2 seconds

### 4. Barney's Farm (barneysfarm.com)
- **Category Page**: https://www.barneysfarm.com/us/ (needs filter selection)
- **Product Example**: https://www.barneysfarm.com/us/pineapple-express-auto-autoflower-strain-37
- **Estimated Strains**: 400-800
- **Rate Limit**: 2 seconds

### 5. ILGM (ilgm.com)
- **Category Page**: https://ilgm.com/categories/cannabis-seeds
- **Product Example**: https://ilgm.com/products/blue-dream-autoflower-seeds?variant=UHJvZHVjdFZhcmlhbnQ6NzI=
- **Estimated Strains**: 300-600
- **Rate Limit**: 2 seconds

---

## System Architecture (Identical to Pipeline/01)

### Multi-Layer Scraping
1. **Bright Data Web Unlocker** (Primary)
2. **ScrapingBee API** (Fallback)
3. **Direct Requests** (Final fallback)
4. **Manual Queue** (Human intervention)

### Quality Validation
- 8-point HTML validation (75% threshold)
- Cannabis keyword detection
- Size and structure validation
- Error pattern recognition

### Storage Integration
- **Same S3 Bucket**: ci-strains-html-archive
- **Same Structure**: html/{url_hash}.html, metadata/{url_hash}.json
- **Same Encryption**: AES-256 server-side
- **Seamless Integration**: No conflicts with existing 13,163 pages

---

## Implementation Differences

### URL Discovery Method
Instead of processing existing CSV data, this pipeline will:
1. **Web Crawl**: Discover strain URLs from category pages
2. **URL Extraction**: Parse product links from listings
3. **Deduplication**: Generate unique hashes (same method)
4. **Database Creation**: Same SQLite structure

### Rate Limiting Updates
```python
DOMAIN_DELAYS = {
    "sensiseeds.us": 2,
    "sensiseeds.com": 2,
    "californiahempseeds.com": 2,
    "humboldtseedcompany.com": 2,
    "cropkingseeds.com": 2,
    "barneysfarm.com": 2,
    "ilgm.com": 2,
    "default": 2
}
```

---

## Expected Results

### Collection Targets
- **Total New URLs**: 1,700-3,500 strain pages
- **Success Rate**: ≥99.5% (same target)
- **Quality Score**: ≥95% validation average
- **Integration**: Seamless addition to existing archive

### Combined Archive
- **Existing Pages**: 13,163 (84.8% of original 15,524)
- **New Pages**: 1,700-3,500 (estimated)
- **Total Archive**: ~15,000-17,000 strain pages
- **Coverage**: Comprehensive multi-seedbank ecosystem

---

## Success Metrics

### Primary Targets (Same as Pipeline/01)
- **Collection Rate**: ≥99.5% successful HTML captures
- **Data Quality**: ≥95% validation score average
- **Performance**: <2 seconds average response time
- **Integration**: 100% compatibility with existing S3 structure

### Archive Enhancement
- **Coverage Expansion**: +15-25% more strain data
- **Seedbank Diversity**: 5 premium sources added
- **Data Freshness**: Current 2026 strain offerings
- **Commercial Value**: Enhanced dataset for Phase 3 analysis

---

## Conclusion

This extension maintains the proven bulletproof methodology while expanding the Cannabis Intelligence Database with premium seedbank data. The seamless S3 integration ensures a unified archive supporting the ecosystem's growth toward commercial success.

---

**Implementation Team**:
- **System Architecture**: Amazon Q
- **Domain Expertise**: Shannon Goddard  
- **Verification**: Shannon Goddard

**Next Phase**: Enhanced strain data extraction from expanded archive (Phase 3)

---

*Expanding the world's most comprehensive cannabis strain HTML archive! 🌿*