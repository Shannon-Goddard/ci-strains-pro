# Neptune HTML Processing Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Overview

Process stored Neptune Seed Bank HTML files from S3 to extract comprehensive strain data into CSV format using the proven 4-method extraction approach.

## 4-Method Extraction System

### Method 1: Structured WooCommerce Table
- Extract from `woocommerce-product-attributes` table
- Maps Neptune-specific fields: `feelings`, `grow_difficulty`
- Handles `#REF!` errors in value fields

### Method 2: H1 Title Extraction
- Clean strain names from page titles
- Remove Neptune-specific formatting patterns

### Method 3: Breeder Link Extraction
- Extract breeder names from `breeder-link` class elements
- Preserve breeder attribution

### Method 4: Description Mining
- Extract THC/CBD content with regex patterns
- Mine full product descriptions
- Pattern matching for additional strain details

## Data Schema

Preserves Neptune's unique fields:
- `feelings` - Emotional effects (calm, euphoric, relaxed)
- `grow_difficulty` - Cultivation difficulty rating
- Standard fields: strain_name, breeder_name, strain_type, flowering_time, yield, etc.

## Processing Flow

1. Read URL mapping from S3 to identify Neptune URLs
2. For each Neptune URL hash, fetch HTML from S3
3. Apply 4-method extraction to HTML content
4. Compile results into pandas DataFrame
5. Export to timestamped CSV file

## Expected Output

CSV with columns:
- source_url, seed_bank, scraped_at
- strain_name, breeder_name, strain_type
- feelings, grow_difficulty (Neptune unique)
- flowering_time, yield, plant_height, seed_type
- description, thc_content, cbd_content