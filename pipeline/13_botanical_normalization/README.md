# Pipeline 13: Botanical Data Normalization

Convert raw botanical data into clean numeric columns with standardized units.

## Status
🔄 **Ready to Start** - Setup complete, awaiting execution

## Quick Reference

**Input:** 19 CSVs from `pipeline/12_botanical_extraction/output/`  
**Output:** Normalized CSVs with `_min`, `_max`, `_avg` columns  
**Goal:** Clean numeric data for analysis (THC%, days, cm, g/m², g/plant)

## Structure
```
13_botanical_normalization/
├── input/                    # (empty - references pipeline 12 output)
├── output/                   # Normalized CSVs will go here
├── scripts/                  # Normalization scripts
├── SETUP_INSTRUCTIONS.md     # Detailed normalization rules
└── README.md                 # This file
```

## Key Conversions
- **THC/CBD:** "18-22%" → min=18, max=22, avg=20
- **Flowering:** "7-8 weeks" → min=49, max=56, avg=52.5 days
- **Height:** "5 to 8 FT" → min=152.4, max=243.84 cm
- **Yield:** "450-550 gr/m2" → min=450, max=550 g/m²

## Data Integrity
- Keep all `*_raw` columns (never delete source data)
- NULL for unparseable values (no guessing)
- Validate: min ≤ max, reasonable ranges
- latin-1 encoding

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
