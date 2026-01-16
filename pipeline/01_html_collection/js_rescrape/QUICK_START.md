# Quick Start Guide

## Prerequisites
```bash
pip install requests boto3 pandas
```

## AWS Credentials
Make sure AWS credentials are configured (already done!):
- API key automatically fetched from AWS Secrets Manager
- No manual key entry needed! ✅

## Run the Rescrape

### Option 1: Both seed banks (recommended)
```bash
python rescrape_js.py --seed-bank all
```

### Option 2: ILGM only (133 strains)
```bash
python rescrape_js.py --seed-bank ilgm
```

### Option 3: Seedsman only (878 strains)
```bash
python rescrape_js.py --seed-bank seedsman
```

### Option 4: Test run (no S3 upload)
```bash
python rescrape_js.py --seed-bank ilgm --upload-s3 false
```

## Expected Output
```
2026-01-14 - Loading S3 inventory...
2026-01-14 - Starting ILGM scrape: 133 URLs
2026-01-14 - ✅ [1/133] ILGM: https://ilgm.com/products/...
2026-01-14 - Progress: 25/133 | Success: 24 | Failed: 1
...
2026-01-14 - ✅ ILGM complete: 127/133 successful
2026-01-14 - Starting Seedsman scrape: 878 URLs
...
╔══════════════════════════════════════╗
║   JavaScript Rescrape Complete! 🎉   ║
╠══════════════════════════════════════╣
║  Success:  960                       ║
║  Failed:    51                       ║
║  Total:   1011                       ║
║  Rate:    95.0%                      ║
╚══════════════════════════════════════╝
```

## Results Location
- `results/scrape_log.csv` - Full log
- `results/success_count.txt` - Summary stats
- `results/failed_urls.txt` - URLs that failed
- S3: `s3://ci-strains-html-archive/html_js/`

## Estimated Time
- **ILGM**: 2 minutes
- **Seedsman**: 90 seconds
- **Total**: ~5 minutes (including S3 upload)

## Cost
**$0.00** - Within your existing ScrapingBee plan

## Next Steps
After successful rescrape:
1. Run ILGM extractor on new HTML
2. Run Seedsman extractor on new HTML
3. Compare before/after data quality
4. Update Phase 3 status to ✅ Complete

---

**Ready? Let's go!** 🚀
