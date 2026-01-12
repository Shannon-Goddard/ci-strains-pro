# Methodology: Seed Bank Mapping Update

## Objective
Replace "Processing..." placeholders in s3_complete_inventory.csv with actual seed bank names based on URL domain mapping.

## Process
1. Read existing CSV with url_hash and placeholder seed_bank values
2. Connect to S3 bucket 'ci-strains-html-archive'
3. Use S3 pagination (MaxKeys=1000) to process all 14,840 metadata files
4. For each url_hash, read corresponding metadata/{hash}.json file
5. Extract URL from metadata and match domain to seed bank using predefined mapping
6. Update seed_bank column with actual seed bank name
7. Save CSV using latin-1 encoding (CI rules requirement)

## Domain Mappings
- northatlanticseed.com → North Atlantic
- neptuneseedbank.com → Neptune
- multiversebeans.com → Multiverse Beans
- mephistogenetics.com → Mephisto Genetics
- seedsupreme.com → Seed Supreme
- seedsherenow.com → Seeds Here Now
- royalqueenseeds.com → Royal Queen Seeds
- greatlakesgenetics.com → Great Lakes Genetics
- dutch-passion.us → Dutch Passion
- cannabis-seeds-bank.co.uk → Attitude Seed Bank
- seedsman.com → Seedsman

## Technical Notes
- **S3 Pagination**: Use MaxKeys=1000 with ContinuationToken for all 14,840 files
- **CSV Encoding**: latin-1 encoding required per CI data processing rules
- **File Structure**: metadata/{hash}.json contains URL field for domain matching

Logic designed by Amazon Q, verified by Shannon Goddard.