# Pipeline 17: Gemini Re-Validation

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Objective

Use Vertex AI Gemini 2.0 Flash to validate, correct, and extract missing data from S3 HTML archives.

**Budget**: $1,200  
**Approach**: One field group at a time for maximum accuracy  
**Source**: S3 HTML archives (immutable, timestamped proof)

---

## Validation Groups

### Group 1: THC (thc_min, thc_max, thc_avg)
- **Strains**: 10,182 with THC data
- **Known issues**: 471 inconsistencies
- **Actions**: Validate ranges, correct values, extract missing

### Group 2: CBD (cbd_min, cbd_max, cbd_avg)
- **Strains**: 7,434 with CBD data
- **Known issues**: 90+ inconsistencies
- **Actions**: Validate ranges, correct values, extract missing

### Group 3: Genetics (indica_percentage, sativa_percentage, ruderalis_percentage, genetics_type)
- **Strains**: 5,069 with genetics data
- **Known issues**: 239 percentages don't add to 100%
- **Actions**: Extract ruderalis, validate totals = 100%, match genetics_type

### Group 4: Lineage (parent_1_display, parent_2_display, lineage_formula)
- **Strains**: 16,224 with lineage data
- **Known issues**: 3,046 missing formulas
- **Actions**: Validate parents match formula, extract missing

### Group 5: Flowering (flowering_days_min, flowering_days_max, flowering_days_avg)
- **Strains**: 12,413 with flowering data
- **Known issues**: 295 outliers
- **Actions**: Validate ranges, extract missing

### Groups 6-9: Height/Yield (Indoor/Outdoor)
- **Actions**: Validate ranges, extract missing

---

## Gemini Response Format

```json
{
  "field_name": {
    "current_value": 20,
    "gemini_value": 22,
    "confidence": "high|medium|low",
    "action": "keep|correction_suggested|flag_for_review|extract_new|impossible_value",
    "reasoning": "HTML shows '22-24% THC', avg should be 23",
    "source_text": "THC: 22-24%"
  }
}
```

---

## Checkpoints

- Progress bar every 500 strains
- Save intermediate results
- Log all API calls and costs

---

## Files

- `01_data_audit.py` - Initial audit (done)
- `02_validate_thc.py` - Group 1: THC validation
- `03_validate_cbd.py` - Group 2: CBD validation
- (etc.)

**Logic designed by Amazon Q, verified by Shannon Goddard.**
