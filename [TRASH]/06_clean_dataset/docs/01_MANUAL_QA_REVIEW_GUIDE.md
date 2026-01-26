# Manual QA Review Guide

**Reviewer**: Shannon Goddard  
**Date**: January 17, 2026  
**Dataset**: `pipeline/06_clean_dataset/output/09_autoflower_classified.csv`  
**Rows**: 21,374 strains  
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
- breeder_name_raw has descriptions: ) this strain has become so strong that it stood o, -+, Bundles, Cannabis Seeds, Cannabis Seeds For Sale, Cannabis Seeds For Sale Online, Critical Mass Collective
* no breeder listed in cell

- breeder_name_raw has descriptions.
Appears as: 00 SeedsParental linesDo si dosVarietyIndica domin
Should be: 00 Seeds
Also: Buy

- "00 Seeds" variations: "00 Seed Bank"
→ Standardize to: "00 Seeds"

- "710 Genetics Seed Bank" variations: "710 OG Cannabis Seeds"
→ Standardize to: "710 Genetics Seed Bank"

- "Ace Seeds" variations: "Ace Seed Bank"
→ Standardize to: "Ace Seeds"

- "Advanced Seeds" variations: "Advanced Female Seeds", "Advanced Seed Bank"
→ Standardize to: "Advanced Seeds"

- "Archive Seeds" variations: "Archive Cannabis Seeds", "Archive Seed Bank"
→ Standardize to: "Archive Seeds"

- "Barney's Farm" variations: "Barneys Farm Seeds", "Barney's FarmParental"
→ Standardize to: "Barney's Farm"

- "Big Buddha Seeds" variations: "Big Bud Cannabis Seeds"
→ Standardize to: "Big Buddha Seeds"

- "Cali Connection" variations: "Cali Connection Seeds", "Cali ConnectionPack"
→ Standardize to: "Cali Connection"

- "Crockett Family Farms" variations: "Crockett Family Farms Seed Bank"
→ Standardize to: "Crockett Family Farms"

- breeder_name_raw has genetics_lineage_raw
Example: AC/DC x Good Medicine

FIRST 1,000 SORTED A-Z REVIEWED
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
- Found: "Balanced Hybrid"
  → Standardize to: "Balanced"

- Found: "Indica Dominant"
  → Standardize to: "Indica"

- Found: "Sativa Dominant"
  → Standardize to: "Sativa"

- Found Descriptions: Choose an optionHybridClear

100% REVIEWED
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
- Found: "CBD Dominate"
  → Standardize to: "CBD" and move to dominant_type_raw?

- Found: "Mostly Indica"
  → Standardize to: "Indica" and move to dominant_type_raw

- Found: "Mostly Sativa"
  → Standardize to: "Sativa" and move to dominant_type_raw

- Found: "Hybrid"
  → Move to dominant_type_raw

- Found: "Indica"
  → Move to dominant_type_raw

- Found: "Sativa"
  → Move to dominant_type_raw

- Found descriptions: "Fast Flowering, Semi-Full Term", "Full Term", "Hybrid, Indica", "Hybrid, Sativa"
  → delete

100% REVIEWED
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
No Entries
100% REVIEWED
```

---

## 5. Difficulty (`difficulty_raw`)

**Target Values**: Easy, Moderate, Difficult

### Findings:

```
Example format:
- Found: "beginner", "Beginner", "easy", "Easy" (2,345 rows)
  → Standardize to: "Easy"

- Found: "intermediate", "medium", "Moderate" (3,456 rows)
  → Standardize to: "Moderate"

- Found: "hard", "Hard", "difficult", "Difficult", "advanced" (1,234 rows)
  → Standardize to: "Difficult"
```

**Your findings**:
```
- Found: "Beginner-Friendly"
  → Standardize to: "Easy"

- Found: "Easy to Moderate"
  → Standardize to: "Easy, Moderate"

- Found: "Expert"
  → Standardize to: "Difficult"

- Found: "Expert, Moderate"
  → Standardize to: "Difficult, Moderate"

- Found: "Intermediate"
  → Standardize to: "Moderate"

- Found: "Medium"
  → Standardize to: "Moderate"

100% REVIEWED
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
thc_average_raw
- https://www.cropkingseeds.com/feminized-seeds/triple-scoop-strain-feminized-marijuana-seeds/ has 0.4
Should be: 19%

- https://www.cropkingseeds.com/feminized-seeds/mimosa-x-orange-punch-strain/ has 1.6
Should be: 30%
*note: thc_content_raw values appears to be more accurate and should override thc_average_raw values

thc_content_raw
- All cells with value = 0.03 should be ""; (empty)

- Found: "ÃƒÂ¢Ã‚Â€Ã‚Â“", "ÃƒÂ¢Ã‚Â€Ã‚Â“ ", " to ", (up to), " and ", 
  → Standardize to: "-"

- Found descriptive words: "average THC"
  → Remove

- *note: 0.03 value is being given by "All Seeds are considered HEMP Seeds by law. Every seed tested contained less than 0.03% THC"

- *note: Some have "%" and some don't. We should remove "%" for easy math functions. Rename as thc_content_percentage_clean

thc_max_raw
- All cells with value = 0 should be ""; (empty)

- All cells with value = 0.03 should be ""; (empty)

- All cells with value = 50 should be ""; (empty)

- *note: 0 value is being given by "Disclaimer: Cannabis seeds are sold as souvenirs, and collectibles only. They contain 0% THC"

- *note: 0.03 value is being given by "0.03% THC. ALL SEEDS ARE HEMP SEEDS BY LAW."

*note: went to all 3 urls with value=50 in thc_max_raw and each listed THC content was much lower

thc_min_raw
- All cells with value = 0 should be ""; (empty)

- All cells with value = 0.03 should be ""; (empty)

- All cells with value = 40 should be ""; (empty)

- *note: 0 value is being given by "Disclaimer: Cannabis seeds are sold as souvenirs, and collectibles only. They contain 0% THC"

- *note: 0.03 value is being given by "0.03% THC. ALL SEEDS ARE HEMP SEEDS BY LAW."

- *note: went to all 3 urls with value=40 in thc_max_raw and each listed THC content was much lower

thc_range_raw
- thc_range_raw data is wrong when thc_content_raw is present. thc_content_raw is accurate.

100% REVIEWED
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
- Added to 140. visited https://www.cannabis-seeds-bank.co.uk/kiwi-seeds-tasman-haze/prod_1350 "Sativa 80% / Indica 20%"

100% REVIEWED
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
comin up with average values, like "19529.6". Values are accurate for averages. However, we need to make yield_indoor-min_g_m2_clean, yield_indoor_max_g_m2_clean, yield_outdoor_min_g_plant_clean, yield_outdoor_max_g_plant_clean for accurate data.
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
Example format:
- strain_name_normalized has seed_type_raw data. 
  Appears as: strain_name_normalized cake bomb feminized 
  Should be: strain_name_normalized cake bomb seed_type_raw feminized 
  feminized also appears as: feminised, feminised seeds, (f), strain fem, (feminised) 
  autoflower also appears as: autoflowering cannabis seeds, auto, automatic
  regular also appears as: (r), strain regular marijuana, regular cannabis seeds

- strain_name_normalized has non strain items.
  Appears as: 1 free seed from qr code, assorted mix auto feminised seeds
  Should be: entire row should be removed

- strain_name_normalized has unknown characters or known description.
  Appears as: 6 cc 037 f6, cannabis seeds, strain, bulk cannabis seeds, com abpa, afga, seeds sman, also know, &#8211; 
  Should be removed
  * This strain is a good example because "cbd" is in it twice. Appears as: amnesia pure cbd auto feminised seeds hds amp cbd auto fem
  Should be: amnesia pure cbd

- strain_name_normalized has unknown characters or known description.
  Appears as: age verification
  *Has no strain name

- strain_name_normalized has breeder_name_normalized
  Appears as: 3rd shift genetics alien cake strain fem auto
  Should be: strain_name_normalized alien cake breeder_name_normalized 3rd shift genetics
  * other breeders names: 3rd coast genetics, growers choice, aeque genetics, herbies seeds usa, seeds ace, always be flowering genetics, barneys farm, royal queen seeds, happy valley genetics, elev8 seeds, rqs, fast buds, atlas

- strain_name_normalized has misinterpreted character encoding
  Appears as: 3rd coast genetics Ã£Â¢Ã¢Â€Ã¢Â“ cinder block
  Should be: strain_name_normalized cinder block breeder_name_normalized 3rd coast genetics
  * other misinterpreted character encoding: Ã£Â¢Ã¢Â€Ã¢Â‹Ã£Â¢Ã¢Â€Ã¢Â‹, Ã£Â¢Ã¢Â€Ã¢Âœ42Ã£Â¢Ã¢Â€Ã¢Â Ã£Â¢Ã¢Â€Ã¢Â“, Ã£Â¢Ã¢Â€Ã¢Âœ42Ã£Â¢Ã¢Â€Ã¢Â, Ã£ÂƒÃ¢Â€, Ã£Â¢Ã¢Â€Ã¢Â¯, bgs ag13s1, Ã£Â¢Ã¢Â€Ã¢Â™, gh alz, Ã£Â¢Ã¢Â€Ã¢Â¯, Ã£Â‚Ã¢Â©, Ã£Â¢Ã¢Â€Ã¢Â¯ 

- strain_name_normalized has breeder_name_normalized
  Appears as: 710 genetics, 710 genetics seed bank, advanced, advanced feminized cannabis seeds, advanced seeds, afghan selection, aficionado french connection, alpine, anesia, apothecary genetics, archive seeds, archive
  *strain_name_normalized strain name is missing

- strain_name_normalized has name of drop; deal
  Appears as: a.b. parfait (f) [the menthol drop]
  Should be: strain_name_normalized a.b. parfait
  Also: [exclusive], [february 2025 drop]
  * drop deals are seed bank specific

- strain_name_normalized has seed pack size.
  Appears as: 3 pack, - 11, seeds 5
  Should be: deleted due to being seed bank website specific data

- strain_name_normalized has genetics_lineage_raw
  Appears as: afghan hawaiian x laos x jamaican feminized
  Should be: afghan hawaiian x laos x jamaican
  Appears as: (animal cookies x gg4) x slurricane #44 (f) [slurricane #44 drop]
  Should be: (animal cookies x gg4) x slurricane #44
  Also: american haze / california haze
  * Some strains do not have names and are called by their genetic lineage, such as these examples. We need to make sure this info is also in genetics_lineage_raw column

- strain_name_normalized has filial_type_clean
  Appears as: airborne g13 s1 [limited edition tester]
  Should be: strain_name_normalized airborne g13 filial_type_clean s1
  Alos: r2, f4, f1

- Common strain "gorilla glue" appears as: "gg" 
- Common strain "gorilla glue #4" appears as: "gorilla glue 4", gg 4
- Common strain "amnesia mac ganja" appears as: "amg"

FIRST 1,000 SORTED A-Z REVIEWED
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
awards_raw
Example format:
- Found: "1", "2024", "1st at Highlife Cup 2014", "Multiple Cup Winner", "Sativa Cup Winner 2010", "FALSE" (345 rows)
  → Should be: Just clean up obvious errors (FALSE → NULL)

- total_grow_time_days_clean unneccessary column, delete

- flowering_time_days_clean, delete and create flowering_time_min_days_clean and flowering_time_max_days_clean

- height_indoor_cm_clean, delete and create height_indoor_min_cm_clean
and height_indoor_max_cm_clean

- height_outdoor_cm_clean, delete and create height_outdoor_min_cm_clean
and height_outdoor_max_cm_clean

- genetics_lineage_raw has misinterpreted character encoding

- Delete strain_name_no_aka
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
**Date completed**: 1-18-2026
