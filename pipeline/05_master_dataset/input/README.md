# Input CSV Files

**Place all 20 seed bank CSV files here before starting pipeline 05.**

## Expected Files (21,706 total strains)

1. `attitude_seed_bank.csv` (7,673 strains)
2. `crop_king.csv` (3,336 strains)
3. `north_atlantic.csv` (2,727 strains)
4. `gorilla.csv` (2,009 strains)
5. `neptune.csv` (1,995 strains)
6. `seedsman.csv` (866 strains)
7. `multiverse_beans.csv` (799 strains)
8. `herbies.csv` (753 strains)
9. `sensi_seeds.csv` (620 strains)
10. `seed_supreme.csv` (353 strains)
11. `mephisto_genetics.csv` (245 strains)
12. `exotic_genetics.csv` (227 strains)
13. `amsterdam.csv` (163 strains)
14. `ilgm.csv` (133 strains)
15. `barneys_farm.csv` (88 strains)
16. `royal_queen_seeds.csv` (67 strains)
17. `dutch_passion.csv` (44 strains)
18. `seeds_here_now.csv` (43 strains)
19. `great_lakes_genetics.csv` (16 strains)
20. `compound.csv` (1 strain)

## File Requirements

- **Encoding**: UTF-8 or latin-1
- **Format**: CSV with headers
- **Required columns**: `url`, `seed_bank` (at minimum)
- **Source**: Extracted from `pipeline/02_s3_scraping/{seed_bank}/` folders

## ⚠️ Known Issues

**Seed Supreme CSV**: Contains ~1,400 headers (most are sparse/auto-generated). 
- **Do NOT pre-filter columns** - let the column analysis script identify which to keep
- Script will drop columns with <5% data coverage
- This is expected behavior from the extraction process

## S3 Inventory Reference

For URL-to-S3 mappings, reference:
- `pipeline/03_s3_inventory/s3_html_inventory.csv` (21,706 strains)
- `pipeline/03_s3_inventory/s3_js_html_inventory.csv` (1,011 JS-rendered strains)

---

**Once files are in place, run `scripts/01_column_analysis.py` to begin consolidation.**
