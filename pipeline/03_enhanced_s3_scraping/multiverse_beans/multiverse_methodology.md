# Multiverse Beans S3 Processing Methodology

## Overview
This script processes pre-collected Multiverse Beans HTML files from S3 storage using a proven 4-method extraction approach adapted from the original Multiverse scraper.

## Architecture Pattern
Following the successful Neptune/Seedsman S3 processing pattern:
- **URL Hash Mapping**: Convert URLs to MD5 hashes for S3 file lookup
- **S3 Structure**: `html/{url_hash}.html` format
- **Extraction Logic Reuse**: Multiverse-specific parsing from Phase 1 scraper

## 4-Method Extraction Strategy

### Method 1: Structured Extraction
- Targets Multiverse's `.attribute-row` structure
- Extracts: Flowering Time, Plant Size, Yield, THC Content, Effects, Flavors, Genetics, Breeder
- Maps Multiverse field labels to standardized schema

### Method 2: Description Mining
- Processes WooCommerce product descriptions
- Autoflower-specific pattern recognition
- Extracts THC/CBD content, flowering time, genetics, effects using regex

### Method 3: Advanced Patterns
- Multiverse-specific URL and content analysis
- Strain name extraction and cleaning (removes pack sizes, F2, Auto suffixes)
- Breeder detection from known Multiverse partners (Mephisto, Night Owl, etc.)
- Growth type classification (Autoflower vs Photoperiod from URL)
- WooCommerce product attributes parsing

### Method 4: Fallback Extraction
- URL-based strain name extraction
- Meta description and title fallbacks
- Default seed type assignment (Feminized)

## Quality Scoring
Weighted scoring system optimized for Multiverse's data strengths:
- Core fields (strain_name, breeder_name, seed_bank): 10 points each
- Multiverse strengths (genetics, flowering_time, growth_type): 8 points
- Secondary fields (yield, THC content, effects): 4-6 points

## Multiverse Specializations
- **Autoflower Focus**: Enhanced autoflower detection and classification
- **Breeder Attribution**: Recognition of premium genetics partners
- **Pack Size Handling**: Removes pack quantities from strain names
- **Growth Type Detection**: URL-based autoflower vs photoperiod classification

## Data Processing Rules Compliance
- **File Integrity**: Processes existing S3 HTML without modification
- **Transparency**: Logic designed by Amazon Q, verified by Shannon Goddard
- **Encoding**: Uses latin-1 for CSV reads to handle special characters

## Expected Outcomes
- Target: 95%+ success rate on Multiverse URLs
- Quality: 80%+ Premium/High tier classifications
- Coverage: Comprehensive autoflower and photoperiod strain data

Logic designed by Amazon Q, verified by Shannon Goddard.