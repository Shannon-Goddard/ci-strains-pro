## Genetics Data Extraction Process

**Date**: December 2025  
**Performed by**: Amazon Q AI Assistant  
**Script**: `data-processing/extract_genetics.py`

### Overview
Extracted genetic information from the `about_info_cleaned` column to populate three previously empty columns in the Cannabis Database.

### Data Extracted

| Column | Pattern | Results | Examples |
|--------|---------|---------|----------|
| **generation** | `F\d+` | 824 entries | F1, F2, F3, F4, F5 |
| **phenotype** | `#\d+` | 3,995 entries | #1, #2, #33, #44 |
| **lineage** | Cross patterns | 5,758 entries | AK 47 X Blueberry, Gelato 33 x OG Kush |

### Technical Details

**Source Data**: `about_info_cleaned` column containing strain descriptions  
**Processing Method**: Regex pattern matching  
**Total New Data Points**: 10,577 genetic attributes extracted

**Lineage Extraction Patterns**:
- `Genetics: StrainA x StrainB`
- `Lineage: StrainA x StrainB` 
- `Cross: StrainA x StrainB`
- `Parents: StrainA x StrainB`

**Encoding Issue Resolved**: Used `latin-1` encoding to handle special characters in CSV

### Results
- **Input**: Cannabis_Database.csv (15,670+ rows)
- **Output**: Cannabis_Database_genetics_extracted.csv
- **Enhancement**: Added 10,577 genetic data points to previously empty columns
- **Success Rate**: High extraction rate from strain descriptions

### Script Location
`cannabis-intelligence-database/data-processing/extract_genetics.py`

---
*This extraction significantly enhanced the database's genetic intelligence, providing structured lineage, generation, and phenotype data for cannabis research and analysis.*