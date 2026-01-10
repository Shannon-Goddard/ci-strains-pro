# Seedsman S3 Processing Methodology

## Overview
This script processes pre-collected Seedsman HTML files from S3 storage using a proven 4-method extraction approach adapted from the original Seedsman scraper.

## Architecture Pattern
Following the successful Neptune S3 processing pattern:
- **URL Hash Mapping**: Convert URLs to MD5 hashes for S3 file lookup
- **S3 Structure**: `html/{url_hash}.html` format
- **Extraction Logic Reuse**: Seedsman-specific parsing from Phase 1 scraper

## 4-Method Extraction Strategy

### Method 1: Structured Extraction
- Targets Seedsman's `product-attribute-specs-table`
- Extracts: SKU, Brand/breeder, Parental lines, THC/CBD content, Yields, Flowering time, Climates, Aroma
- Maps Seedsman field labels to standardized schema

### Method 2: Description Mining
- Processes product description sections
- Extracts genetics, effects, and flavor patterns using regex
- Handles multi-paragraph descriptions

### Method 3: Advanced Patterns
- Seedsman-specific URL and content analysis
- Strain name extraction and cleaning
- Seed type detection (Auto/Feminized/Regular)
- Growth type classification

### Method 4: Fallback Extraction
- Meta description and title fallbacks
- Ensures minimum data capture for all pages

## Quality Scoring
Weighted scoring system optimized for Seedsman's data strengths:
- Core fields (strain_name, seed_bank): 10 points each
- Seedsman strengths (THC content, yields, flowering time): 8-9 points
- Enhanced fields (descriptions, patterns): 4-7 points

## Data Processing Rules Compliance
- **File Integrity**: Processes existing S3 HTML without modification
- **Transparency**: Logic designed by Amazon Q, verified by Shannon Goddard
- **Encoding**: Uses latin-1 for CSV reads to handle special characters

## Expected Outcomes
- Target: 95%+ success rate on Seedsman URLs
- Quality: 80%+ Premium/High tier classifications
- Coverage: Comprehensive specifications, breeder attribution, multi-climate data

Logic designed by Amazon Q, verified by Shannon Goddard.