# Pipeline 12: Botanical Data Extraction

Extract botanical cultivation data from 21,220 cannabis strain HTML files.

## Quick Start

All extractions complete. Output files in `output/` directory.

## Structure

```
12_botanical_extraction/
├── input/
│   └── pipeline_11_final.csv          # Input: 21,220 strains
├── output/
│   └── botanical_*.csv                # 19 output files (one per seed bank)
├── docs/
│   └── BOTANICAL_PATTERNS.md          # HTML patterns documented
├── methodology.md                      # Full extraction methodology
└── README.md                           # This file
```

## Results

- **Total Processed:** 21,220 strains (100%)
- **With Botanical Data:** 18,744 strains (88.3%)
- **No Data Available:** 2,476 strains (11.7%)

## Key Fields Extracted

- THC/CBD content (raw percentages)
- Flowering time (raw days/weeks)
- Yield (raw g/m² or g/plant)
- Height (raw cm/ft)
- Lineage/genetics
- Harvest time
- Terpenes

## Data Integrity

- No unit conversion (raw values preserved)
- latin-1 encoding
- Separate CSV per seed bank
- NULL for missing data

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
