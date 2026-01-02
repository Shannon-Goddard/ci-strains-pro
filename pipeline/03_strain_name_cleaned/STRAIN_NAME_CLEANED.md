# Strain Name Cleaning & Standardization

**Date**: December 2025  
**Performed by**: Shannon Goddard | Loyal9 LLC  
**Software**: Microsoft® Excel® 2019 (Build 16.0.19426.20218) 64-bit

## 📝 Overview
This stage involved the manual standardization of 15,670+ raw strain entries. The primary goal was to separate composite strings into structured, filterable genetic columns.

## 📊 Data Transformation Summary
| Cleaned Column | Purpose | Example Value |
| :--- | :--- | :--- |
| `strain_name_cleaned` | Primary name without generation noise | White Runtz |
| `primary_generation` | Standardized generation (F1, F2, R1, etc.) | F2 |
| `breeding_method` | Breeding technique (BX, IBL, S1) | BX |
| `phenotype` | Specific selection number | #1 |

## 🛠 Methodology
- **Column Expansion**: Created 3 new structural columns, resulting in **47,082 newly structured data points**.
- **Normalization**: 
    - Resolved special characters and encoding artifacts from the raw CSV.
    - Used **Advanced Filtering** to isolate and correct inconsistent naming conventions.
    - Standardized "AKA" entries by expanding them into unique rows to ensure no lineage data was lost.
- **Deduplication**: Successfully identified and removed hundreds of non-cannabis rows (e.g., merchandise, stickers) to ensure a 100% botanical dataset.

## ✅ Results
- **Input**: 15,694 raw rows.
- **Output**: 15,783 unique, structured strain rows.
- **Success Rate**: 100% of rows now feature structured generation and breeding metadata.