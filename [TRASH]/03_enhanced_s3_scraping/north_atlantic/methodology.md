# North Atlantic Seed Co S3 Batch Processing Methodology

## Overview
Batch processor for extracting commercial strain data from North Atlantic Seed Co using their proven 4-method extraction approach.

## Processing Strategy
- **Batch Size**: 50 strains per batch to avoid timeouts
- **Target**: All North Atlantic strains from northatlanticseed.com domain
- **Output**: Multiple CSV files that can be combined

## 4-Method Extraction Approach
1. **Structured Extraction**: Product details sections with regex patterns
2. **Product Meta**: Title cleaning, breeder extraction from strain names
3. **WooCommerce Attributes**: Systematic attribute table parsing
4. **Fallback Extraction**: URL parsing, description tabs, default values

## Commercial Data Fields
- strain_name, strain_id, seed_bank, source_url
- breeder_name, genetics, flowering_time, seed_type
- thc_content, cbd_content, yield, plant_height
- effects, about_info

## North Atlantic Specialties
- Known breeder recognition (Ethos, In House, Compound, etc.)
- Product detail section parsing
- WooCommerce attribute mapping
- Description tab content extraction

## Logic designed by Amazon Q, verified by Shannon Goddard.