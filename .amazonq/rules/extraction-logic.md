# Extraction Patterns (Verified)

## Genetics
- Pattern: `(\d+)%\s*Sativa` / `(\d+)%\s*Indica`
- Lineage: Detect "Cross:", "Genetics:", or "Parents:" followed by "X".

## Cannabinoids
- THC Range: `THC[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%`
- Handle single values vs. ranges by creating `_min`, `_max`, and `_avg` columns.