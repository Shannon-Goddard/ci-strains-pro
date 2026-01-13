# Mephisto Genetics S3 Processing Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Overview
Mephisto Genetics S3 processor extracts premium autoflower strain data from the legendary breeder's archived HTML files, preserving their unique medicinal effects and growth odour classifications.

## Data Source
- **Seed Bank**: Mephisto Genetics (legendary autoflower specialists)
- **HTML Archive**: S3 bucket `ci-strains-html-archive`
- **URL Pattern**: `mephistogenetics` domains
- **Encoding**: UTF-8 for HTML processing

## 4-Method Extraction System

### Method 1: Structured Field Extraction
- Targets Mephisto's unique field classes:
  - `cycle-times-field`: Flowering time ("65 to 75 days from sprout")
  - `size-field`: Plant height ("40 to 60cm")
  - `yield-field`: Yield specifications ("60 to 90 grams")
  - `aroma-flavour-field`: Combined sensory profile
  - `effect-field`: Effects descriptions
  - `medicinal-effect-field`: **UNIQUE** - Medical applications
- Handles multiple `cannabinoids-field` uses:
  - First instance: Grow difficulty ratings
  - Second instance: **UNIQUE** - Growth odour intensity

### Method 2: Rich Tab Content Mining
- Extracts from Shopify tab structure:
  - `data-w-tab="Project"`: Breeding project history
  - `data-w-tab="Strain"`: Strain-specific growing information
- Pattern extraction for:
  - Genetics and lineage information
  - Indica/Sativa percentages
  - Breeding notes and selection criteria
  - Awards and recognition

### Method 3: Advanced Mephisto Patterns
- Strain name extraction with Mephisto-specific cleaning
- Limited edition detection:
  - Illuminauto series identification
  - Artisanal and Reserva releases
  - Limited availability indicators
- Breeding generation tracking (BX, F2, F3)
- Shopify JSON-LD extraction for pricing and availability

### Method 4: Shopify Structure Fallback
- URL-based strain name extraction from product paths
- Meta description and title fallbacks
- Product form analysis for stock status
- Sold out/availability detection

## Mephisto Genetics Specialization

### Unique Data Fields
- **medicinal_effect**: Medical applications (insomnia, appetite stimulation, etc.)
- **growth_odour**: Odor intensity ratings during cultivation
- **limited_edition**: Special release identification
- **breeding_generation**: Genetic generation tracking
- **aroma_flavour**: Combined sensory profiles

### Autoflower Focus
- **seed_type**: Always "Feminized" (100% feminized autoflowers)
- **growth_type**: Always "Autoflower" (exclusive specialization)
- **flowering_time**: Precise "days from sprout" specifications
- **plant_height**: Exact size measurements for indoor cultivation

## Quality Scoring (Mephisto-Optimized)
Weighted scoring emphasizing Mephisto's strengths:
- **Core fields** (10 points): strain_name, breeder_name
- **Mephisto strengths** (8-9 points): flowering_time, plant_height, yield, medicinal_effect
- **Autoflower specific** (5-7 points): effects, genetics, grow_difficulty, growth_odour
- **Breeding data** (3-6 points): about_info, breeding_generation, limited_edition
- **Sensory data** (3-6 points): aroma_flavour, availability

## Quality Tiers
- **Premium**: 80-100 points (complete cultivation + medicinal data)
- **High**: 60-79 points (good specs + effects)
- **Medium**: 40-59 points (basic autoflower data)
- **Basic**: 20-39 points (strain identification only)
- **Minimal**: 0-19 points (insufficient data)

## Output Format
CSV with Mephisto-specific columns:
- **Core**: strain_name, seed_bank, breeder_name, source_url
- **Autoflower specs**: flowering_time, plant_height, yield, growth_type, seed_type
- **Unique fields**: medicinal_effect, growth_odour, limited_edition, breeding_generation
- **Sensory**: aroma_flavour, effects, genetics
- **Metadata**: data_completeness_score, quality_tier, extraction_methods_used
- **Timestamps**: scraped_at

## Mephisto Genetics Legacy
Founded by autoflower pioneers, Mephisto Genetics represents:
- **Premium autoflower genetics** with photoperiod-quality potency
- **Medicinal focus** with detailed therapeutic applications
- **Cultivation precision** with exact timing and size specifications
- **Limited releases** through Illuminauto and Artisanal series
- **Community engagement** with detailed growing guidance

## File Integrity
- Raw HTML preserved in S3 archive
- Processed data saved as `mephisto_genetics.csv`
- No overwriting of source data
- UTF-8 encoding maintained throughout pipeline
- Unique field preservation for medicinal_effect and growth_odour