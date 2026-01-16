# Seedsman JavaScript Extraction Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Approach
Extract comprehensive product data from ScandiPWA (React-based PWA) JavaScript-rendered HTML files stored in S3 `html_js/` folder.

## Architecture Context
Seedsman uses ScandiPWA where all product data loads via GraphQL API after JavaScript execution. Static HTML contains only app shell - JS rendering is required.

## Data Sources
1. **Product Attributes** - Table rows and attribute divs
2. **Text Content** - THC, CBD, flowering, yield, height patterns
3. **Genetics** - Lineage and parent strain identification
4. **Effects, Flavors, Terpenes** - Keyword extraction
5. **JSON-LD** - Structured product data
6. **Meta Tags** - SEO descriptions

## Target Fields (60+)
- Strain identification (name, breeder, SKU)
- Cannabinoids (THC/CBD min/max/avg)
- Cultivation specs (flowering, yield, height)
- Genetics (lineage, parents, indica/sativa ratio)
- Effects, flavors, terpenes
- Seed type (feminized/auto/regular)
- Growing difficulty and climate
- Pricing (min/max/avg)
- Business data (JSON-LD structured data)

## Quality Assurance
- Multiple pattern fallbacks for each field
- Field counting for completeness tracking
- UTF-8 encoding for international characters
- Error handling per strain
- JSON-LD validation
