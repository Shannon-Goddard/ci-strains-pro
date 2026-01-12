# Multiverse Beans Web Scraping Methodology

**Date**: January 3, 2026  
**Phase**: Multiverse Beans HTML Collection  
**Status**: Implementation Ready  

---

## Methodology Statement

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Executive Summary

This methodology outlines the web scraping system for collecting HTML content from multiversebeans.com and storing it in the `ci-strains-html-archive` S3 bucket. The system uses a multi-layer fallback approach (ScrapingBee + Bright Data + Direct) to achieve 95%+ collection success rate for approximately 1,227 Multiverse Beans strain pages.

---

## System Architecture

### 1. Multi-Layer Scraping System

**Layer 1: ScrapingBee API (Primary)**
- Credits: 250,000 API credits available
- Premium proxy enabled
- JavaScript rendering disabled for speed
- Timeout: 60 seconds

**Layer 2: Bright Data Web Unlocker (Fallback)**
- Budget: $133.71 available
- Endpoint: brd-customer zone configuration
- Timeout: 60 seconds

**Layer 3: Direct Requests (Final Fallback)**
- Rotating user agents (2 different browsers)
- Standard HTTP headers
- Timeout: 30 seconds

### 2. URL Discovery Process

**Catalog Scraping**:
- Target URLs:
  - `https://multiversebeans.com/product-category/autoflower/`
  - `https://multiversebeans.com/product-category/photoperiod/`
  - `https://multiversebeans.com/product-category/feminized/`
- Pagination: Process up to 50 pages per category
- Product Detection: Links containing `/product/` path
- Deduplication: Set-based URL collection

**Expected Results**:
- Target: ~1,227 unique strain URLs
- Categories: Autoflower, Photoperiod, Feminized
- Format: Full URLs to individual product pages

### 3. HTML Collection Process

**Collection Strategy**:
1. Sequential processing (respectful to server)
2. 2-second delay between requests
3. Multi-method fallback for each URL
4. Immediate S3 storage upon success

**Quality Validation**:
- Minimum HTML size: 5,000 bytes
- Content validation: Presence of strain/seed/cannabis keywords
- Structure validation: Basic HTML tags present

### 4. S3 Storage Architecture

**Storage Structure**:
```
ci-strains-html-archive/
├── html/
│   └── {url_hash}.html          # HTML content
└── metadata/
    └── {url_hash}.json          # Collection metadata
```

**URL Hash Generation**:
- SHA-256 hash of full URL
- Truncated to 16 characters
- Ensures unique file naming

**Metadata Schema**:
```json
{
  "url": "https://multiversebeans.com/product/strain-name/",
  "url_hash": "16_char_hash",
  "strain_ids": [12345],
  "collection_date": "2026-01-03T10:30:00Z",
  "scrape_method": "scrapingbee",
  "validation_score": 0.85,
  "html_size": 245678,
  "validation_checks": {
    "min_size": true,
    "has_title": true,
    "has_cannabis_content": true,
    "not_blocked": true,
    "not_error": true,
    "has_structure": true,
    "reasonable_size": true,
    "has_content": true
  }
}
```

---

## Implementation Specifications

### Rate Limiting & Politeness
- **Request Delay**: 2 seconds between requests
- **Concurrent Requests**: 1 (sequential processing)
- **Timeout Handling**: Progressive timeouts (60s → 60s → 30s)
- **User Agent Rotation**: 2 different browser agents

### Error Handling
- **Method Fallbacks**: 3-layer fallback system
- **Retry Logic**: Each method attempted once per URL
- **Graceful Degradation**: Continue processing on individual failures
- **Comprehensive Logging**: All successes and failures logged

### AWS Integration
- **S3 Bucket**: `ci-strains-html-archive`
- **Encryption**: AES-256 server-side encryption
- **Content Types**: `text/html` for HTML, `application/json` for metadata
- **Access Control**: IAM role-based authentication

---

## Expected Results

### Quantitative Targets
- **Total URLs**: ~1,227 Multiverse strain pages
- **Success Rate**: ≥95% (based on bulletproof scraper benchmarks)
- **Collection Time**: 2-4 hours (with 2-second delays)
- **Data Volume**: ~500MB HTML content + metadata

### Quality Metrics
- **HTML Size**: Average 200-400KB per page
- **Content Quality**: Cannabis-specific content validation
- **Completeness**: All discovered product URLs processed
- **Integrity**: SHA-256 hash verification for storage

### Method Performance Expectations
- **ScrapingBee**: 70-80% success rate (primary method)
- **Bright Data**: 15-20% usage (fallback scenarios)
- **Direct Scraping**: 5-10% usage (final fallback)

---

## Risk Mitigation

### Technical Risks
- **Rate Limiting**: 2-second delays prevent server overload
- **IP Blocking**: Multi-service fallback provides IP diversity
- **Network Failures**: Automatic retry with different methods
- **Storage Failures**: AWS S3 reliability (99.999999999% durability)

### Operational Risks
- **Cost Management**: Monitor API usage (250K ScrapingBee credits, $133.71 Bright Data)
- **Legal Compliance**: Respectful scraping practices, public data only
- **Data Integrity**: Hash-based verification and metadata tracking
- **Process Interruption**: Stateless design allows restart from any point

---

## Success Metrics

### Primary KPIs
- **Collection Success Rate**: ≥95% of discovered URLs
- **Data Quality**: Valid HTML with cannabis content
- **Processing Speed**: Complete within 4 hours
- **Storage Integrity**: 100% successful S3 uploads

### Quality Assurance
- **Content Validation**: Automated checks for cannabis keywords
- **Size Validation**: Minimum 5KB HTML content
- **Structure Validation**: Basic HTML tag presence
- **Metadata Completeness**: All required fields populated

---

## Integration with Existing Pipeline

### S3 Archive Compatibility
- **Same Bucket**: Uses existing `ci-strains-html-archive`
- **Same Structure**: `html/` and `metadata/` prefixes
- **Same Format**: Compatible with existing extraction tools
- **Same Security**: AES-256 encryption and IAM controls

### Next Phase Integration
- **4-Method Extraction**: HTML ready for proven extraction pipeline
- **Quality Scoring**: Metadata supports quality assessment
- **Commercial Use**: Data structure supports API development
- **Scalability**: Architecture supports future expansion

---

## Cost Analysis

### API Costs (One-time Collection)
- **ScrapingBee**: ~$25-35 (primary usage, 1,227 requests)
- **Bright Data**: ~$5-10 (fallback usage, estimated 200 requests)
- **Total Collection Cost**: ~$30-45

### Infrastructure Costs (Monthly)
- **AWS S3**: ~$2-3 (500MB storage)
- **AWS Data Transfer**: ~$1 (minimal)
- **Total Operational**: ~$3-4/month

### ROI Justification
- **Data Asset Creation**: Permanent HTML archive for 1,227 strains
- **Commercial Value**: Supports $15K Phase 2 revenue target
- **Future-Proofing**: Protects against website changes
- **Quality Foundation**: Enables premium data products

---

## Conclusion

This web scraping methodology provides a robust, respectful, and efficient approach to collecting Multiverse Beans strain data. The multi-layer fallback system ensures maximum success rates while maintaining compliance with best practices.

The collected HTML will integrate seamlessly with the existing S3 archive structure, enabling immediate processing with proven 4-method extraction techniques. This positions Multiverse Beans data for inclusion in commercial Cannabis Intelligence Database offerings.

---

**Implementation Team**:
- **System Architecture**: Amazon Q
- **Domain Expertise**: Shannon Goddard  
- **Verification**: Shannon Goddard
- **Quality Assurance**: Human-AI Partnership

**Next Phase**: 4-Method data extraction and CSV generation for commercial use

---

*This methodology ensures Multiverse Beans integration into the Cannabis Intelligence ecosystem while maintaining the highest standards of data collection and storage.*