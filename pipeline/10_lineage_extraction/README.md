# Phase 10: Lineage Extraction

**Status:** ✅ COMPLETE  
**Coverage:** 76.1% (16,246/21,361 strains)  
**Date:** February 2, 2026

## Quick Start

### Input
- `input/all_strains_genetics_standardized.csv` - Starting dataset (21,361 strains, 85.6% missing lineage)

### Output
- `output/all_strains_lineage_final.csv` - Final dataset (76.1% lineage coverage)
- `output/*_sample.csv` - 100-row samples of all pipeline CSVs

### Run Extractions (in order)
```bash
python extract_attitude.py          # 6,082 extracted (79.3%)
python extract_barneys.py           # 74 extracted (84.1%)
python extract_cropking.py          # 2,190 extracted (65.7%)
python extract_exotic.py            # 60 extracted (26.4%)
python extract_gorilla.py           # 1,078 extracted (53.7%)
python extract_herbies.py           # 632 extracted (83.9%)
python extract_mephisto.py          # 172 extracted (70.2%)
python extract_neptune.py           # 486 extracted (24.4%)
python extract_north_atlantic.py    # 2,074 extracted (76.0%)
python extract_royal_queen.py       # 43 extracted (64.2%)
python extract_seedsman.py          # 270 extracted (31.2%)
python extract_seeds_here_now.py    # 1 extracted (2.3%)
```

### Analysis
```bash
python analyze_missing_lineage.py   # Show missing lineage by seed bank
```

## Documentation
- **PHASE_10_REPORT.md** - Full extraction report with methodology
- **LINEAGE_EXTRACTION_PATTERNS.md** - HTML patterns for each seed bank
- **methodology.md** - Data processing rules

## Lineage Schema (21 columns)
- Parent fields: `parent_1_display`, `parent_1_slug`, `parent_2_display`, `parent_2_slug`
- Grandparent fields: 8 columns (4 pairs)
- Generation markers: `generation_f`, `generation_s`, `generation_bx`
- Metadata: `lineage_formula`, `is_hybrid`, `is_polyhybrid`, etc.

## Key Insights
- **Seed bank-specific patterns required** - generic extraction failed
- **UTF-8 encoding** - handles special characters in strain names
- **Nested crosses** - split on last "x" for complex lineage
- **7 seed banks have no lineage data** - Multiverse, Seed Supreme, Amsterdam, ILGM, Sensi, Dutch Passion, Great Lakes

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
