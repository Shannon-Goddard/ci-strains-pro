# Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Gorilla Seed Bank Extraction

### 9-Method Pipeline
1. **Strain Name & Breeder** - h1.page-title and h3.product-manufacturer
2. **Top Attributes Table** - product-topattributes table with th/td pairs
3. **Product Features** - product-features list (THC, flowering, etc.)
4. **Overview** - product attribute overview div
5. **Description** - description-main text
6. **THC/CBD** - Cannabinoid extraction from text
7. **Yield** - Indoor/outdoor gr/m2 and gr/plant
8. **Effects** - Psychoactive profile
9. **Flavors** - Terpene/taste profile

### Gorilla-Specific Structure
- Uses `product-topattributes` table with th/td rows
- Fields prefixed with `spec_` for table data
- Features list contains key cultivation data
