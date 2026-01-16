# JavaScript Rescrape Methodology

## Problem Statement
ILGM and Seedsman product pages require JavaScript execution to render full product data. Current S3 HTML archives contain only static shells without the dynamically-loaded content.

## Technical Analysis

### ILGM Architecture
- **Framework**: Custom JavaScript table renderer
- **Data Location**: Embedded in page, rendered on load
- **Load Time**: ~2-3 seconds
- **Target Elements**: `<tr class="flex justify-between">` rows
- **Fields Available**: 25+ (Plant Type, THC%, Flowering Time, etc.)

### Seedsman Architecture
- **Framework**: ScandiPWA (React-based Magento PWA)
- **Data Location**: GraphQL API calls
- **Load Time**: ~3-5 seconds
- **Target Elements**: Product specification tables
- **Fields Available**: 60+ (Full product specs, cannabinoids, genetics)

## Solution Design

### Tool Selection: ScrapingBee
**Rationale:**
1. Already subscribed ($49.99/month)
2. Built-in JavaScript rendering
3. Premium proxies included
4. Simple API integration
5. Cost-effective for this volume

**Alternative Considered:**
- Bright Data: More expensive, already spent budget
- Selenium + AWS Lambda: More complex, unnecessary
- Puppeteer: Requires infrastructure setup

### Technical Approach
```python
# ScrapingBee API call
params = {
    'render_js': 'true',      # Enable JavaScript
    'wait': 5000,             # Wait 5 seconds
    'premium_proxy': 'true',  # Use premium proxies
    'country_code': 'us'      # US-based proxies
}
```

**Wait Time Justification:**
- ILGM: 2-3 seconds actual load time + 2 second buffer = 5 seconds
- Seedsman: 3-4 seconds API calls + 1 second buffer = 5 seconds
- Consistent 5-second wait ensures all content loads

### Rate Limiting
- **ScrapingBee Limit**: 10 requests/second
- **Our Rate**: 10 requests/second (0.1s delay)
- **Reason**: Maximize throughput within limits

### Error Handling
1. **Retry Logic**: 3 attempts with exponential backoff (2^n seconds)
2. **Validation**: Check HTML size > 50KB
3. **Logging**: CSV log of every request
4. **Failure Tracking**: Separate file for failed URLs

## Data Storage

### S3 Structure
```
s3://ci-strains-html-archive/
├── html/              # Original static HTML
└── html_js/           # New JavaScript-rendered HTML
    ├── {hash}_js.html
    └── metadata:
        - scrape_method: javascript_render
        - scrape_date: ISO timestamp
        - seed_bank: ILGM/Seedsman
        - tool: scrapingbee
```

**Naming Convention:**
- Original: `{url_hash}.html`
- JS version: `{url_hash}_js.html`
- Keeps both versions for comparison

## Quality Assurance

### Success Criteria
- **Minimum**: 90% successful scrapes (909/1,011)
- **Target**: 95% successful scrapes (960/1,011)

### Validation Checks
1. HTTP 200 response
2. HTML size > 50KB
3. Contains target elements (tables/specs)
4. S3 upload successful

### Post-Scrape Validation
1. Random sample of 10 URLs
2. Manual inspection of rendered content
3. Compare to live site
4. Verify table data present

## Cost Analysis

### ScrapingBee Usage
- **Plan**: $49.99/month (150,000 calls included)
- **This Job**: 1,011 calls
- **Percentage**: 0.67% of monthly quota
- **Marginal Cost**: $0.00

### AWS S3 Costs
- **Storage**: 1,011 files × 2MB = 2GB
- **Monthly Cost**: $0.05
- **Transfer**: Free tier
- **Total**: $0.05/month

### Total Project Cost
**$0.00** - All within existing subscriptions

## Timeline

| Task | Duration | Details |
|------|----------|---------|
| Setup | 5 min | Load inventory, configure API |
| ILGM Scrape | 2 min | 133 URLs @ 10/sec |
| Seedsman Scrape | 90 sec | 878 URLs @ 10/sec |
| S3 Upload | 2 min | Batch upload |
| Validation | 5 min | Check results |
| **Total** | **~15 min** | End-to-end execution |

## Expected Improvements

### ILGM
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Columns | 22 | 50+ | +127% |
| THC Coverage | 6.8% | 95%+ | +1,297% |
| Complete Records | 9 | 126+ | +1,300% |

### Seedsman
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Columns | 0 | 60+ | ∞ |
| Data Coverage | 0% | 90%+ | ∞ |
| Usable Records | 0 | 790+ | ∞ |

## Risk Mitigation

### Risk 1: Rate Limiting
- **Mitigation**: Built-in 0.1s delay, retry logic
- **Fallback**: Reduce to 5 req/sec

### Risk 2: API Failures
- **Mitigation**: 3 retries with exponential backoff
- **Fallback**: Manual retry of failed URLs

### Risk 3: Content Not Loading
- **Mitigation**: 5-second wait time
- **Fallback**: Increase wait to 10 seconds for failures

### Risk 4: S3 Upload Failures
- **Mitigation**: Separate validation step
- **Fallback**: Local storage, manual upload

## Attribution
**Designed by**: Amazon Q  
**Funded by**: Shannon Goddard  
**Project**: CI-Strains-Pro Phase 3 Enhancement  
**Date**: January 2026

## Transparency Statement
This methodology follows CI data processing rules:
- ✅ Never overwrites raw data (new `_js` suffix)
- ✅ Transparency log included
- ✅ Attribution clearly stated
- ✅ Cost tracking documented

**Logic designed by Amazon Q, verified by Shannon Goddard.**
