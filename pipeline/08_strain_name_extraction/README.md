# Phase 8: Strain Name Extraction

## Purpose
Extract clean, standardized strain names from URLs and raw strain names across all 19 seed banks. Removes breeder names, generation markers, seed types (feminized/autoflowering), pack sizes, and other metadata to produce pure botanical strain names suitable for cross-bank matching and deduplication.

## Results
- **Total Strains Processed**: 21,361
- **Success Rate**: 100% extraction across all seed banks
- **Output**: Single master file (`all_strains_extracted.csv`) with `strain_name_extracted` column
- **Quality**: Preserves strain numbers, handles aka names, removes metadata noise

### Extraction Breakdown by Seed Bank

| Seed Bank              | Strains | Extraction Method                          |
|------------------------|---------|-------------------------------------------|
| Attitude Seed Bank     | 7,673   | URL slug + breeder/keyword removal        |
| Crop King              | 3,336   | URL slug + keyword removal                |
| North Atlantic         | 2,727   | URL slug + suffix/generation removal      |
| Gorilla Seed Bank      | 2,000   | Raw name + keyword removal                |
| Neptune                | 1,995   | URL slug + breeder detection (140 found)  |
| Seedsman               | 866     | URL split on seed type keywords           |
| Herbies Seeds          | 753     | URL slug + breeder detection (28 found)   |
| Multiverse Beans       | 518     | URL slug + breeder detection (18+13)      |
| Seed Supreme           | 353     | URL split on seed type keywords           |
| Mephisto Genetics      | 245     | URL slug (preserves Illuminauto series)   |
| Exotic Genetix         | 216     | URL slug + suffix removal (11 filtered)   |
| Amsterdam Marijuana    | 163     | URL slug + keyword removal                |
| ILGM                   | 133     | URL slug + suffix removal                 |
| Sensi Seeds            | 115     | URL slug (simple extraction)              |
| Barney's Farm          | 88      | URL split on strain keywords              |
| Royal Queen Seeds      | 67      | URL slug + prefix/suffix removal          |
| Dutch Passion          | 54      | URL slug + auto prefix removal            |
| Seeds Here Now         | 43      | URL slug + breeder/keyword removal        |
| Great Lakes Genetics   | 16      | URL slug + breeder detection (16 found)   |

## Files Structure

### Input
- `input/09_autoflower_classified.csv` - Source data with URLs and raw strain names

### Output
- `output/all_strains_extracted.csv` - Master file with 21,361 strains
- `output/attitude_strain_names_v2.csv` - Attitude extractions (7,673)
- `output/cropking_extracted.csv` - Crop King extractions (3,336)
- `output/gorilla_extracted.csv` - Gorilla extractions (2,000)
- `output/north_atlantic_extracted.csv` - North Atlantic extractions (2,727)
- `output/neptune_extracted.csv` - Neptune extractions (1,995)
- `output/seedsman_extracted.csv` - Seedsman extractions (866)
- `output/amsterdam_extracted.csv` - Amsterdam extractions (163)
- `output/herbies_extracted.csv` - Herbies extractions (753)
- `output/sensi_seeds_extracted.csv` - Sensi Seeds extractions (115)
- `output/multiverse_beans_extracted.csv` - Multiverse Beans extractions (518)
- `output/seed_supreme_extracted.csv` - Seed Supreme extractions (353)
- `output/mephisto_genetics_extracted.csv` - Mephisto extractions (245)
- `output/exotic_extracted.csv` - Exotic Genetix extractions (216)
- `output/ilgm_extracted.csv` - ILGM extractions (133)
- `output/dutch_passion_extracted.csv` - Dutch Passion extractions (54)
- `output/barneys_farm_extracted.csv` - Barney's Farm extractions (88)
- `output/royal_queen_seeds_extracted.csv` - Royal Queen Seeds extractions (67)
- `output/seeds_here_now_extracted.csv` - Seeds Here Now extractions (43)
- `output/great_lakes_genetics_extracted.csv` - Great Lakes extractions (16)

### Scripts
- `scripts/extraction_helpers.py` - Shared utility functions for all extractors
- `scripts/extract_attitude.py` - Attitude Seed Bank extraction
- `scripts/extract_cropking.py` - Crop King extraction
- `scripts/extract_gorilla.py` - Gorilla Seed Bank extraction
- `scripts/extract_north_atlantic.py` - North Atlantic extraction
- `scripts/extract_neptune.py` - Neptune extraction with breeder detection
- `scripts/extract_seedsman.py` - Seedsman extraction
- `scripts/extract_amsterdam.py` - Amsterdam Marijuana extraction
- `scripts/extract_herbies.py` - Herbies Seeds extraction with breeder detection
- `scripts/extract_sensi_seeds.py` - Sensi Seeds extraction
- `scripts/extract_multiverse_beans.py` - Multiverse Beans extraction
- `scripts/extract_seed_supreme.py` - Seed Supreme extraction
- `scripts/extract_mephisto_genetics.py` - Mephisto Genetics extraction
- `scripts/extract_exotic.py` - Exotic Genetix extraction
- `scripts/extract_ilgm.py` - ILGM extraction
- `scripts/extract_dutch_passion.py` - Dutch Passion extraction
- `scripts/extract_barneys_farm.py` - Barney's Farm extraction
- `scripts/extract_royal_queen_seeds.py` - Royal Queen Seeds extraction
- `scripts/extract_seeds_here_now.py` - Seeds Here Now extraction
- `scripts/extract_great_lakes_genetics.py` - Great Lakes Genetics extraction
- `scripts/merge_all_banks.py` - Combines all 19 seed bank outputs into master file

### Documentation
- `docs/URL_PATTERNS.md` - Complete extraction logic and patterns for all 19 seed banks

## Key Extraction Rules
1. **Preserve strain numbers** (e.g., "Project 4516", "Haze 13")
2. **Remove "Auto" suffix** unless at start of name (preserve "Auto 1", "Auto Moonrocks")
3. **Remove breeder names** using frequency detection (5+ occurrences)
4. **Remove generation markers** (F1, S1, BX1, R1, etc.)
5. **Remove seed types** (Feminized, Autoflowering, Regular)
6. **Remove pack sizes** (3 Pack, 5 Seeds, etc.)
7. **Preserve aka names** in Gorilla format "(aka Name)"
8. **Filter box-sets** in Exotic Genetix (mixed strain packs)

## Usage
Run individual seed bank extraction:
```bash
python scripts/extract_cropking.py
```

Merge all extractions:
```bash
python scripts/merge_all_banks.py
```

## Next Steps
- Phase 9: Cross-bank strain matching and deduplication
- Phase 10: Master strain consolidation with unified naming

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
