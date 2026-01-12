# Attitude Seedbank Batch Processing Methodology

## Overview
Batch processor for extracting commercial strain data from Attitude Seedbank's 7,734+ strains stored in S3 HTML archive.

## Processing Strategy
- **Batch Size**: 50 strains per batch to avoid timeouts
- **Target**: First 100 metadata files (testing phase)
- **Output**: Multiple CSV files that can be combined

## Extraction Methods
1. **Title Extraction**: H1 or title tags for strain names
2. **Genetics Parsing**: Sativa/Indica percentages via regex
3. **THC Analysis**: Range and single value detection with min/max/avg columns
4. **Lineage Detection**: Parent strain identification from genetics text

## Commercial Data Fields
- strain_name, strain_id, seed_bank
- sativa_percentage, indica_percentage  
- thc_min, thc_max, thc_avg
- parent1, parent2

## Logic designed by Amazon Q, verified by Shannon Goddard.