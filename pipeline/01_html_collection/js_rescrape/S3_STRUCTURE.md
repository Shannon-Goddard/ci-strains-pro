# S3 Storage Structure - JavaScript Rescrape

## Bucket: `ci-strains-html-archive`

### Original Static HTML
```
html/
├── {url_hash}.html          # Original static HTML (no JS rendering)
└── Example: 0017fbd840f2539f.html
```

### JavaScript-Rendered HTML (NEW)
```
html_js/
├── {url_hash}_js.html       # JavaScript-rendered HTML
└── Example: 0017fbd840f2539f_js.html
```

## Key Details

### URL Hash Generation
```python
import hashlib
url_hash = hashlib.md5(url.encode()).hexdigest()[:16]
```
- First 16 characters of MD5 hash
- Matches existing S3 inventory naming

### File Naming Convention
- **Static**: `{hash}.html` (original)
- **JS-rendered**: `{hash}_js.html` (new)
- Same hash, different suffix

### S3 Metadata (JS files)
```python
Metadata = {
    'scrape_method': 'javascript_render',
    'scrape_date': '2026-01-15T...',
    'seed_bank': 'ILGM' or 'Seedsman',
    'tool': 'scrapingbee'
}
```

## Seed Banks Processed

### ILGM
- **Count**: 133 strains
- **Location**: `s3://ci-strains-html-archive/html_js/*_js.html`
- **Filter**: URLs containing `ilgm.com`
- **Success Rate**: 100%

### Seedsman  
- **Count**: 878 strains
- **Location**: `s3://ci-strains-html-archive/html_js/*_js.html`
- **Filter**: URLs containing `seedsman.com`
- **Success Rate**: 100%

## How to Access

### Python (boto3)
```python
import boto3
s3 = boto3.client('s3')

# Get JS-rendered HTML
obj = s3.get_object(
    Bucket='ci-strains-html-archive',
    Key=f'html_js/{url_hash}_js.html'
)
html = obj['Body'].read().decode('utf-8')
```

### AWS CLI
```bash
# List all JS-rendered files
aws s3 ls s3://ci-strains-html-archive/html_js/

# Download specific file
aws s3 cp s3://ci-strains-html-archive/html_js/0017fbd840f2539f_js.html .
```

## Extraction Scripts

### ILGM Extractor
```python
# Load from S3 inventory
inv = pd.read_csv('pipeline/03_s3_inventory/s3_html_inventory.csv')
ilgm = inv[inv['url'].str.contains('ilgm.com')]

# Fetch JS-rendered HTML
for row in ilgm.iterrows():
    key = f"html_js/{row['url_hash']}_js.html"
    obj = s3.get_object(Bucket='ci-strains-html-archive', Key=key)
    html = obj['Body'].read().decode('utf-8')
    # Extract data...
```

### Seedsman Extractor
```python
# Same pattern as ILGM
seedsman = inv[inv['url'].str.contains('seedsman.com')]
# Use html_js/{hash}_js.html files
```

## Why Two Versions?

### Keep Both:
1. **Original** (`html/`) - Baseline, proof of initial state
2. **JS-rendered** (`html_js/`) - Enhanced with full data

### Benefits:
- ✅ Data integrity (never overwrite raw data)
- ✅ Before/after comparison
- ✅ Fallback if JS version has issues
- ✅ Cost: $0.04/month (negligible)

## Integration with S3 Inventory

### Update inventory CSV (optional):
```python
# Add new column for JS version
inv['has_js_version'] = inv['url'].str.contains('ilgm.com|seedsman.com')
inv['js_html_key'] = inv['url_hash'] + '_js.html'
```

## Rescrape Details

- **Date**: January 15, 2026
- **Tool**: ScrapingBee (JavaScript rendering)
- **Parameters**: `render_js=true`, `wait=5000ms`
- **Success Rate**: 100% (1,011/1,011)
- **Cost**: $0.00 (within existing plan)

## Attribution
**Designed and executed by Amazon Q**  
**Funded by Shannon Goddard**  
**Project: CI-Strains-Pro Phase 3 Enhancement**

---

*This structure allows seamless extraction from either static or JS-rendered HTML without conflicts.*
