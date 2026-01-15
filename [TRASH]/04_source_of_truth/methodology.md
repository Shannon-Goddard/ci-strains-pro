# Find Missing HTML URLs - Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Purpose
Identify URLs from the master strain list that don't have corresponding HTML files in the S3 archive.

## Method
1. Read master URL list from `s3_complete_inventory.csv` (URL column only)
2. Generate expected hash for each URL using MD5[:16] method
3. List all metadata files in S3 `ci-strains-html-archive/metadata/`
4. Compare expected hashes against actual S3 metadata files
5. Report URLs with missing HTML files

## Output
- Console report of missing URLs count
- `missing_html_urls.csv` if any URLs are missing HTML files

## Usage
```bash
cd pipeline/02_source_of_truth
python find_missing_html.py
```

## Expected Result
Based on documentation showing 100% coverage, should find 0 missing URLs.