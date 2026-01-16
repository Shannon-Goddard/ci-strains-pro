# ILGM JavaScript Extraction Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Approach
Extract comprehensive product data from JavaScript-rendered HTML files stored in S3 `html_js/` folder.

## Data Sources
1. **Product Table** - `flex justify-between` structure with label/value pairs
2. **Text Content** - THC, CBD, flowering time, yield, height
3. **Effects & Flavors** - Keyword extraction from descriptions
4. **Genetics** - Lineage and parent strain identification
5. **Meta Tags** - SEO descriptions and structured data

## Target Fields (50+)
- Strain identification (name, breeder)
- Cannabinoids (THC min/max/avg, CBD)
- Cultivation specs (flowering time, yield, height)
- Genetics (lineage, indica/sativa ratio)
- Effects and flavors
- Growing difficulty and climate
- Pricing and availability

## Quality Assurance
- Field counting for completeness tracking
- Pattern matching with multiple fallbacks
- UTF-8 encoding for special characters
- Error handling per strain
