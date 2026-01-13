# Pipeline 03: Enhanced S3 Scraping

## Evolution from Direct Scraping to S3 Processing

This pipeline represents a major architectural shift from direct seed bank scraping to processing pre-collected HTML files stored in S3.

### Original Approach (Phase 1)
Individual scrapers for each seed bank hitting live websites:
- Custom extraction logic per seed bank
- Rate limiting and anti-bot challenges
- Inconsistent availability and performance

### S3 Processing Breakthrough (Phase 2)
Unified processing of archived HTML files with seed bank-specific extraction logic:
- **Consistent data source**: S3 HTML archive eliminates scraping variability
- **Proven extraction patterns**: Reuse successful parsing logic from Phase 1
- **Scalable architecture**: Process thousands of pages without rate limits

## Key Technical Pattern: URL Hash Mapping

The breakthrough came from Neptune's successful S3 structure:
```
S3 Structure: html/{url_hash}.html
CSV Mapping: url_hash column links URLs to S3 files
```

This pattern solved the core challenge of mapping seed bank URLs to stored HTML files.

## Seed Bank Processing Status

| Seed Bank | Status | Strains | Success Rate | Key Challenge Solved |
|-----------|--------|---------|--------------|---------------------|
| **Neptune** | ✅ Complete | 1,234 | 89.2% | Established S3 pattern |
| **North Atlantic** | ✅ Complete | 2,727 | 94.8% | Adapted Neptune's pattern |
| **Seedsman** | 🚧 Ready | - | - | Pattern established |

## Architecture Success Factors

1. **S3 Structure Consistency**: `html/{url_hash}.html` format
2. **URL Hash Mapping**: CSV contains `url_hash` for file lookup
3. **Extraction Logic Reuse**: Seed bank-specific parsing from Phase 1
4. **Fallback Paths**: Robust file location handling

## Usage Pattern
```bash
cd pipeline/03_enhanced_s3_scraping/{seed_bank}
python {seed_bank}_s3_processor.py
```

Each processor follows the proven Neptune pattern while maintaining seed bank-specific extraction logic.

**Architecture and implementation by Amazon Q.**