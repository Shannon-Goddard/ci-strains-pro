# Cannabis Intelligence Database - HTML Collection Methodology

**Date**: January 3, 2026  
**Phase**: 2 - Bulletproof HTML Collection  
**Status**: Implementation Ready  

---

## Methodology Statement

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Executive Summary

This methodology document outlines the bulletproof HTML collection system designed to capture complete HTML snapshots of 15,778 cannabis strain URLs with a 99.5% success rate target. The system implements a multi-layer fallback architecture with comprehensive quality validation and secure cloud storage.

---

## System Architecture

### 1. URL Deduplication Pipeline

**Objective**: Reduce 15,778 strain records to unique URLs for efficient collection.

**Process**:
1. Load Cannabis_Database_Validated_Complete.csv (15,778 records)
2. Clean and validate URLs (remove nulls, empty strings)
3. Generate SHA-256 hash for each unique URL (16-character prefix)
4. Create mapping structure: `{url_hash: {url, strain_ids[], metadata}}`
5. Store in SQLite database for progress tracking

**Expected Results**:
- Input: 15,778 strain records
- Estimated Output: ~12,000-13,000 unique URLs
- Deduplication Rate: ~20-25%

### 2. Multi-Layer Scraping Architecture

**Layer 1: Bright Data Web Unlocker (Primary)**
- Budget: $133.71 available
- Endpoint: brd-customer-hl_XXXXXXX-zone-web_unlocker
- Timeout: 60 seconds
- Retry attempts: 3 per layer

**Layer 2: ScrapingBee API (Fallback)**
- Credits: 250,000 API credits available
- Premium proxy enabled
- JavaScript rendering disabled for speed
- Timeout: 60 seconds

**Layer 3: Direct Requests (Final Fallback)**
- Rotating user agents (5 different browsers)
- Standard HTTP headers
- Timeout: 30 seconds

**Layer 4: Manual Queue**
- Failed URLs flagged for human intervention
- Export functionality for manual review

### 3. Quality Validation System

**HTML Validation Criteria** (75% threshold required):
- Minimum size: 5,000 bytes
- Maximum size: 5MB
- Contains `<title>` tag
- Contains cannabis-related keywords
- Not blocked (no captcha/access denied messages)
- No HTTP error codes (404, 403, 500)
- Valid HTML structure (`<html>`, `<body>`, `</html>`)
- Reasonable content-to-markup ratio

**Cannabis Keywords**: strain, cannabis, thc, cbd, seed, genetics, indica, sativa, hybrid, flowering, yield, terpene, cannabinoid

**Error Detection**: blocked, captcha, access denied, forbidden, rate limit, too many requests

### 4. Rate Limiting & Politeness

**Domain-Specific Delays**:
- seedsman.com: 3 seconds
- leafly.com: 2 seconds  
- allbud.com: 4 seconds
- attitude.co.uk: 2 seconds
- Default: 2 seconds

**Concurrency Controls**:
- Maximum concurrent requests: 10
- Per-host limit: 5
- Batch size: 50 URLs
- Exponential backoff: [1, 3, 7, 15, 30, 60] seconds

### 5. Storage & Security

**AWS S3 Configuration**:
- Bucket: ci-strains-html-archive
- Server-side encryption: AES-256
- Cross-region replication: us-west-2
- Versioning enabled

**Storage Structure**:
```
ci-strains-html-archive/
├── html/
│   └── {url_hash}.html
├── metadata/
│   └── {url_hash}.json
├── index/
│   ├── url_mapping.csv
│   └── collection_stats.json
└── logs/
    └── scraping_logs/
```

**Metadata Schema**:
```json
{
  "url": "original_url",
  "url_hash": "16_char_hash",
  "strain_ids": [1, 2, 3],
  "collection_date": "2026-01-03T10:30:00Z",
  "scrape_method": "bright_data",
  "validation_score": 0.875,
  "html_size": 45678,
  "validation_checks": {...}
}
```

### 6. Progress Tracking & Recovery

**SQLite Database Schema**:
```sql
CREATE TABLE scraping_progress (
    url_hash TEXT PRIMARY KEY,
    original_url TEXT NOT NULL,
    strain_ids TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    attempts INTEGER DEFAULT 0,
    last_attempt TIMESTAMP,
    html_size INTEGER,
    validation_score REAL,
    s3_path TEXT,
    error_message TEXT,
    scrape_method TEXT
);
```

**Status Values**: pending, processing, success, failed

**Checkpoint System**:
- Progress saved every 100 URLs
- Automatic recovery from interruptions
- Failed URL retry with exponential backoff
- Maximum 6 attempts per URL

### 7. Monitoring & Analytics

**Real-time Dashboard**:
- Overall progress statistics
- Success rate by scraping method
- Domain-specific performance
- Quality metrics (validation scores, HTML sizes)
- Failed URL analysis

**Key Performance Indicators**:
- Collection Rate: Target 99.5%
- Average Validation Score: Target >0.8
- Average Response Time: Target <2 seconds
- Data Quality: Target 95% valid HTML

---

## Implementation Workflow

### Phase 1: Setup & Deduplication
1. Execute `01_url_deduplication.py`
2. Verify unique URL count (~12K expected)
3. Review deduplication report
4. Validate database creation

### Phase 2: Collection Execution
1. Configure AWS credentials and S3 bucket
2. Execute `02_bulletproof_scraper.py`
3. Monitor progress with `03_progress_monitor.py --watch`
4. Handle failures and retries automatically

### Phase 3: Quality Assurance
1. Review collection statistics
2. Validate random HTML samples
3. Export failed URLs for manual review
4. Generate final collection report

### Phase 4: Data Validation
1. Cross-reference with original strain data
2. Verify S3 storage integrity
3. Test API access patterns
4. Document collection completeness

---

## Risk Mitigation Strategies

### Technical Risks
- **API Rate Limits**: Multi-service fallback chain
- **Storage Failures**: Cross-region replication + versioning
- **Data Corruption**: SHA-256 checksums + validation
- **Network Issues**: Exponential backoff + retry logic

### Operational Risks
- **Cost Overruns**: Budget monitoring ($133.71 Bright Data, 250K ScrapingBee credits)
- **Legal Compliance**: Respectful scraping with delays
- **Data Loss**: Multiple backup strategies
- **Performance Issues**: Concurrency controls + monitoring

### Quality Risks
- **Invalid HTML**: Multi-criteria validation system
- **Incomplete Collection**: Manual review queue for failures
- **Data Inconsistency**: Comprehensive metadata tracking
- **Access Issues**: Multiple authentication methods

---

## Success Metrics

### Primary Targets
- **Collection Rate**: ≥99.5% successful HTML captures
- **Data Quality**: ≥95% validation score average
- **Performance**: <2 seconds average response time
- **Reliability**: 99.9% system uptime

### Quality Assurance
- Manual review of failed URLs
- Random sampling of collected HTML (5% sample)
- Cross-validation with original scrape data
- User feedback integration for Phase 3

---

## Cost Analysis

### Infrastructure Costs
- **AWS S3**: ~$5/month (500MB HTML + metadata)
- **AWS Lambda**: ~$2/month (future API calls)
- **AWS Secrets Manager**: ~$1/month
- **Total Operational**: ~$8/month

### Collection Costs (One-time)
- **Bright Data**: ~$30-50 (12,000 URLs)
- **ScrapingBee**: ~$20 (backup usage)
- **Total Collection**: ~$50-70

### ROI Justification
- Creates immutable source of truth
- Protects against URL rot and content changes
- Enables advanced Phase 3 analysis
- Supports commercial monetization goals

---

## Data Governance

### Privacy & Compliance
- Public website data only
- No personal information collected
- Respectful scraping practices
- GDPR/CCPA compliant storage

### Data Retention
- HTML stored indefinitely (research value)
- Metadata preserved for lineage tracking
- Logs retained for 90 days
- Failed URLs archived for analysis

### Access Controls
- S3 bucket private with IAM controls
- API Gateway with rate limiting
- CloudFront CDN for global access
- Audit logging enabled

---

## Future Enhancements

### Phase 3 Integration
- Enhanced strain data extraction
- AI-powered content analysis
- Automated quality scoring
- Real-time monitoring dashboard

### Scalability Improvements
- Kubernetes deployment for larger datasets
- Distributed scraping across regions
- Machine learning for failure prediction
- Advanced retry strategies

### Commercial Features
- API monetization layer
- Premium data access tiers
- Real-time collection updates
- Custom extraction services

---

## Conclusion

This bulletproof HTML collection methodology represents a comprehensive approach to preserving cannabis strain data at scale. The multi-layer architecture ensures maximum success rates while maintaining data quality and operational efficiency.

The system is designed for:
- **Reliability**: 99.5% collection success rate
- **Quality**: Comprehensive validation and monitoring
- **Scalability**: Cloud-native architecture
- **Maintainability**: Clear documentation and monitoring

Upon successful implementation, this system will create the world's most comprehensive cannabis strain HTML archive, supporting the Cannabis Intelligence ecosystem's growth from research to commercial success.

---

**Implementation Team**:
- **System Architecture**: Amazon Q
- **Domain Expertise**: Shannon Goddard  
- **Verification**: Shannon Goddard
- **Quality Assurance**: Human-AI Partnership

**Next Phase**: Enhanced strain data extraction and AI-powered analysis (Phase 3)

---

*This methodology serves as the technical foundation for Cannabis Intelligence Database Phase 2, establishing bulletproof data collection practices that will scale through commercial deployment.*