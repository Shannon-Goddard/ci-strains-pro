# Mephisto Genetics S3 Batch Processing Methodology

## Overview
Batch processor for extracting commercial strain data from Mephisto Genetics, the premium autoflower specialists.

## Processing Strategy
- **Batch Size**: 25 strains per batch (smaller for premium quality)
- **Target**: All Mephisto strains from mephistogenetics.com domain
- **Output**: Multiple CSV files that can be combined

## 4-Method Extraction Approach
1. **Product Title**: Clean strain name extraction with Mephisto-specific patterns
2. **Description Mining**: Autoflower-specific patterns, terpenes, effects
3. **Shopify Attributes**: Product forms, variant selectors, pack sizes
4. **Structured Data**: JSON-LD extraction, meta descriptions, URL fallback

## Commercial Data Fields
- strain_name, strain_id, seed_bank, source_url
- breeder_name (default: Mephisto Genetics), genetics, generation
- flowering_time, thc_content, cbd_content, yield, height
- effects, flavors, terpenes, about_info, pack_sizes
- growth_type (default: Autoflower), seed_type (default: Feminized)

## Mephisto Specialties
- Autoflower-focused extraction (all strains are autoflowers)
- Generation detection (F1, F2, etc.) from strain names
- Shopify platform-specific parsing
- Premium strain quality emphasis
- Pack size variant extraction

## Logic designed by Amazon Q, verified by Shannon Goddard.