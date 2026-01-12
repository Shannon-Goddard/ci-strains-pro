# Great Lakes Genetics S3 Processing Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Overview
Great Lakes Genetics S3 processor extracts US boutique breeder strain data from archived HTML files using a specialized 4-method extraction system optimized for their unique site structure.

## Data Source
- **Seed Bank**: Great Lakes Genetics (US boutique genetics distributor)
- **HTML Archive**: S3 bucket `ci-strains-html-archive`
- **URL Pattern**: `greatlakesgenetics` domains
- **Encoding**: UTF-8 for HTML processing

## 4-Method Extraction System

### Method 1: Structured Container Extraction
- Targets `.et_pb_module_inner` containers (Divi theme structure)
- Extracts breeder-strain pairs from H3 format: "Breeder - Strain Name (pack info)"
- Maps structured fields from strong tags:
  - Genetics, Seeds in pack, Sex, Type, Yield
  - Flowering Time, Growing Area, Cultivation Notes

### Method 2: Description Mining
- Mines Notes sections for detailed cultivation information
- Extracts pattern-based data:
  - Effects patterns (euphoric, creative, relaxing, etc.)
  - Aroma patterns (spicy, hash, lemon, fuel, sweet, etc.)
  - Structure patterns (christmas tree, uniform, branching)
  - Resin patterns (production, impressive coverage)

### Method 3: Advanced US Genetics Patterns
- URL-based strain name extraction from product paths
- Seed type detection (autoflower, feminized, regular)
- US breeder identification from keyword matching:
  - Forest, Jaws, Cannarado, Ethos, In House, Compound
  - Thug Pug, Exotic Genetix, Oni Seed, Clearwater, Bloom
- Growth type classification (Autoflower vs Photoperiod)

### Method 4: Universal Fallback
- Title and meta description extraction
- H1-H6 heading analysis for strain context
- Comprehensive strain name cleaning and normalization
- Fallback content extraction for missing core fields

## Quality Scoring (Optimized for GLG)
Weighted scoring system emphasizing GLG strengths:
- **Core fields** (10 points): strain_name, seed_bank
- **GLG strengths** (9-10 points): breeder_name, genetics, cultivation_notes
- **Cultivation data** (7-8 points): flowering_time, yield, strain_type, sex
- **Enhanced patterns** (5-7 points): effects, aroma, structure, resin
- **Classification** (5 points): growth_type, seed_type
- **US genetics** (3 points): us_genetics indicator

## Quality Tiers
- **Premium**: 80-100 points (comprehensive cultivation data)
- **High**: 60-79 points (good breeder + genetics info)
- **Medium**: 40-59 points (basic strain identification)
- **Basic**: 20-39 points (minimal data)
- **Minimal**: 0-19 points (insufficient data)

## Output Format
CSV with GLG-specific columns:
- **Core**: strain_name, seed_bank, breeder_name, source_url
- **Genetics**: genetics, strain_type, sex, seed_type, growth_type
- **Cultivation**: flowering_time, yield, growing_area, cultivation_notes
- **Enhanced**: effects_pattern, aroma_pattern, structure_pattern, resin_pattern
- **Metadata**: data_completeness_score, quality_tier, extraction_methods_used
- **Timestamps**: scraped_at

## US Boutique Breeder Focus
Great Lakes Genetics specializes in:
- Premium US genetics from craft breeders
- Detailed cultivation notes and growing guidance
- Clear breeder attribution and lineage tracking
- Indoor/outdoor growing recommendations
- Pack size and seed type specifications

## File Integrity
- Raw HTML preserved in S3 archive
- Processed data saved as `great_lakes_genetics.csv`
- No overwriting of source data
- UTF-8 encoding maintained throughout pipeline
- Comprehensive extraction method tracking