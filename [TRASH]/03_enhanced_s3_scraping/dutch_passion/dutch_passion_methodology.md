# Dutch Passion S3 Processing Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Overview
Dutch Passion S3 processor extracts strain data from archived HTML files using a 4-method extraction system adapted from the successful North Atlantic pattern.

## Data Source
- **Seed Bank**: Dutch Passion (established 1987)
- **HTML Archive**: S3 bucket `ci-strains-html-archive`
- **URL Pattern**: `dutch-passion` domains
- **Encoding**: UTF-8 for HTML processing

## 4-Method Extraction System

### Method 1: Structured Extraction
- Targets specification tables with regex patterns
- Extracts: genetics, flowering_time, thc_content, cbd_content, yield, height, seed_type
- Looks for structured data in divs/spans with spec/detail/info classes

### Method 2: Description Mining  
- Mines product description areas for detailed information
- Extracts flowering time (weeks), THC ranges, effects keywords
- Fallback to substantial text divs containing strain/cannabis keywords

### Method 3: Advanced Patterns
- Strain name extraction from h1 tags
- Seed type detection from URL patterns (/autoflower-seeds, /feminized-seeds, /regular-seeds)
- Terpene profile and awards extraction
- Growth type classification (Autoflower vs Photoperiod)

### Method 4: Universal Fallback
- URL-based strain name extraction from `/cannabis-seeds/` paths
- Title and meta description extraction
- Hardcoded seed bank and breeder assignment
- Timestamp and source URL recording

## Quality Scoring
Weighted scoring system (0-100):
- **Core fields** (10 points): strain_name, breeder_name
- **High value** (8 points): genetics, flowering_time, seed_type  
- **Medium value** (6 points): thc_content, yield, height
- **Bonus fields** (3-5 points): effects, terpene_profile, awards, etc.

## Quality Tiers
- **Premium**: 80-100 points
- **High**: 60-79 points  
- **Medium**: 40-59 points
- **Basic**: 20-39 points
- **Minimal**: 0-19 points

## Output Format
CSV with columns including:
- strain_name, seed_bank, breeder_name, source_url
- genetics, flowering_time, seed_type, growth_type
- thc_content, cbd_content, yield, height
- effects, terpene_profile, awards, about_info
- data_completeness_score, quality_tier, extraction_methods_used
- scraped_at timestamp

## File Integrity
- Raw HTML preserved in S3 archive
- Processed data saved as `dutch_passion.csv`
- No overwriting of source data
- UTF-8 encoding maintained throughout pipeline