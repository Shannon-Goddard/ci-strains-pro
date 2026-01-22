# Manual QA Review Guide

**Reviewer**: Shannon Goddard  
**Date**: January 20, 2026  
**Dataset**: `pipeline\06_clean_dataset\output\10d_categorical_standardized.csv`  
**Rows**: 21,360 strains  
**Purpose**: Identify patterns for Step 10 (Case Standardization) before Step 11 (Deduplication)

---

## Review Instructions

For each section below, document:
1. **Current values found** (variations, inconsistencies, typos)
2. **Standardized value** (what it should be)
3. **Count/examples** (how many, which rows if outliers)

---

## 1. Breeder Names (`breeder_name_raw`)

**Standardization Rules**: Proper case, consistent punctuation

### Findings:

```
Example format:
- "Barney's Farm" variations: "Barneys Farm", "Barney's farm", "BARNEYS FARM" (234 rows)
  → Standardize to: "Barney's Farm"

- "DNA Genetics" variations: "dna genetics", "DNA genetics" (89 rows)
  → Standardize to: "DNA Genetics"
```

**Your findings**:
```
Is empty
```

---

## 2. Dominant Type (`dominant_type_raw`)

**Target Values**: Indica, Sativa, Hybrid, Balanced

### Findings:

```
Example format:
- Found: "Indica Dominant", "Mostly Indica", "indica", "INDICA" (1,234 rows)
  → Standardize to: "Indica"

- Found: "50/50", "Balanced Hybrid", "balanced" (456 rows)
  → Standardize to: "Balanced"
```
---
**Your findings**:
```

```

---

## 3. Seed Type (`seed_type_raw`)

**Target Values**: Feminized, Regular, Autoflower

### Findings:

```
Example format:
- Found: "fem", "Fem", "feminized", "Feminized", "FEM" (5,678 rows)
  → Standardize to: "Feminized"

- Found: "auto", "Auto", "autoflower", "Autoflower" (3,944 rows)
  → Standardize to: "Autoflower"
```

**Your findings**:
```

```

---

## 4. Flowering Type (`flowering_type_raw`)

**Target Values**: Photoperiod, Autoflower

### Findings:

```
Example format:
- Found: "photo", "Photo", "photoperiod", "Photoperiod" (12,345 rows)
  → Standardize to: "Photoperiod"
```

**Your findings**:
```

```

---

## 5. Difficulty (`difficulty_raw`)

**Target Values**: Easy, Moderate, Difficult

### Findings:

```

```

**Your findings**:
```

```

---

## 6. THC/CBD Outliers

**Expected Range**: 0-35% (THC), 0-25% (CBD)

### Findings:

```
Example format:
- Row 1234: thc_max_raw = 250 (should be 25.0?)
- Row 5678: cbd_min_raw = -5 (invalid, should be NULL)
- Rows 9000-9100: thc_average_raw = "high" (placeholder missed)
```

**Your findings**:
```

```

---

## 7. Genetics Percentages

**Rule**: indica + sativa + ruderalis should = 100%

### Findings:

```
Example format:
- Row 2345: indica=60, sativa=60 (sum=120%, invalid)
- Row 6789: indica=50, sativa=30 (sum=80%, missing ruderalis=20%)
```

**Your findings**:
```

```
---

## 8. Height/Yield Outliers

**Expected Ranges**: 
- Height: 30-300 cm
- Yield indoor: 200-800 g/m²
- Yield outdoor: 50-1000 g/plant

### Findings:

```
Example format:
- Row 3456: height_indoor_cm_clean = 50000 (typo, should be 50?)
- Row 7890: yield_indoor_g_m2_clean = 5 (too low, data error?)
```

**Your findings**:
```

```

---

## 9. Strain Name Issues

**Check**: Normalization artifacts, AKA extraction errors

### Findings:

```
Example format:
- strain_name_normalized has trailing spaces (234 rows)
- AKA extraction left parentheses: "Blue Dream )" (12 rows)
- Common strain "OG Kush" appears as: "og kush", "ogkush", "og-kush"
```

**Your findings**:
```

```

---

## 10. Placeholders Missed

**Common patterns**: TBD, TBA, coming soon, contact us, varies, see description

### Findings:

```
Example format:
- cbd_content_raw contains "TBD" (45 rows)
- flowering_time_raw contains "varies" (23 rows)
```

**Your findings**:
```
[Fill in here]
```

---

## 11. Other Issues

**Anything else you noticed**

### Findings:

```

```

---

## Summary

**Total issues identified**: [count]  
**Critical issues** (must fix before deduplication): [ALL]  
**Nice-to-have fixes** (can do later): [0]  

**Estimated impact on deduplication**:
- Breeder name standardization will improve matching by: [X%]
- Categorical standardization will improve filtering by: [X%]

---

## Next Steps

1. Amazon Q builds Step 10: Case Standardization script
2. Apply all findings from this review
3. Generate before/after report
4. Update methodology.md
5. Proceed to Step 11: Deduplication

---

**Reviewed by**: Shannon Goddard  
**Verified by**: Amazon Q (automation)  
**Date completed**: 
