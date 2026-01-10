## Cannabinoid Data Extraction Process

**Date**: December 2025  
**Performed by**: Amazon Q AI Assistant  
**Script**: `REMOVE_strain_data/extract_cannabinoids.py`

### Overview
Extracted numerical cannabinoid and genetic data from the `strain_info` column to populate THC, CBD, and genetic ratio columns.

### Data Extracted

| Column | Results | Examples |
|--------|---------|----------|
| **sativa_percentage** | 0 entries | 70% Sativa |
| **indica_percentage** | 1 entry | 100% Indica |
| **thc_min, thc_max, thc** | 34 entries | THC: 20-25%, THC: 17% |
| **cbd_min, cbd_max, cbd** | 54 entries | CBD: 1-3%, CBD: 6% |

**Total Cannabinoid Data Points**: 89 numerical values extracted

### Technical Details

**Source Data**: `strain_info` column containing strain descriptions  
**Processing Method**: Regex pattern matching for numerical extraction  
**Patterns Used**:
- Genetic ratios: `(\d+)%\s*Sativa`, `(\d+)%\s*Indica`
- THC ranges: `THC[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%`
- CBD ranges: `CBD[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%`
- Single values: `THC[:\s]*(\d+(?:\.\d+)?)%`, `CBD[:\s]*(\d+(?:\.\d+)?)%`

### Results
- **Input**: Cannabis_Database.csv (15,670+ rows)
- **Output**: Cannabis_Database_cannabinoids_extracted.csv
- **Enhancement**: Added 89 numerical cannabinoid data points