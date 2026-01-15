# Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Herbies Seeds Extraction

### 9-Method Pipeline
1. **Properties Table** - properties-list table with name/value pairs
2. **THC/CBD** - Cannabinoid percentages
3. **Yield** - oz/ft² indoor, oz/plant outdoor
4. **Flowering Time** - Days to harvest
5. **Height** - Inches indoor/outdoor
6. **Genetics** - Lineage and Sativa/Indica ratio
7. **Effects** - Psychoactive profile
8. **Flavors** - Terpene/taste profile
9. **Strain Name** - From URL if not in HTML

### Herbies-Specific Structure
- Uses `properties-list` table with tr.properties-list__item rows
- Fields prefixed with `herb_` for clarity
- Clean data with specific units (oz, inches, days)
