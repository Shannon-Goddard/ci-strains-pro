# Gemini Flash 2.0 Validation Request: Master Cannabis Dataset

## Context
You are analyzing the **master_strains_raw.csv** dataset - a consolidated collection of 23,000 cannabis strains extracted from 20 seed banks. This is Phase 5 of the CI-Strains-Pro project, which aims to create the world's most comprehensive validated cultivation database.

## Dataset Overview
- **Total Records**: 23,000 strains
- **Source Seed Banks**: 20 (Attitude, Amsterdam, Crop King, Neptune, Gorilla, etc.)
- **Columns**: 40 total (38 botanical fields + strain_id + seed_bank)
- **Data Integrity**: 100% source traceability (every strain has URL + S3 archive key)
- **Coverage Metrics**:
  - strain_name_raw: 100% (23,000/23,000)
  - source_url_raw: 100% (23,000/23,000)
  - s3_html_key_raw: 100% (23,000/23,000)
  - scraped_at_raw: 96.2% (22,143/23,000)

## Botanical Fields (38 Total)
**Genetics & Classification**:
- strain_name_raw, breeder_name_raw, genetics_lineage_raw
- dominant_type_raw, indica_percentage_raw, sativa_percentage_raw, is_hybrid_raw
- seed_type_raw, generation_raw

**Cannabinoids & Terpenes**:
- thc_content_raw, thc_min_raw, thc_max_raw, thc_average_raw, thc_range_raw
- cbd_content_raw, cbd_min_raw, cbd_max_raw, cbd_range_raw
- cbn_content_raw, terpenes_raw

**Cultivation Data**:
- flowering_time_raw, flowering_type_raw, difficulty_raw
- height_raw, height_indoor_raw, height_outdoor_raw
- yield_indoor_raw, yield_outdoor_raw, total_grow_time_raw
- climate_raw, suitable_environments_raw

**Sensory & Effects**:
- flavors_all_raw, effects_all_raw, description_raw, awards_raw

**Metadata**:
- source_url_raw, s3_html_key_raw, scraped_at_raw

## Data Extraction Notes
1. **Column Mapping**: 1,848 unique source columns mapped to 38 unified fields using keyword-based schema
2. **Commercial Data Excluded**: 236 columns (prices, SKUs, availability) removed for legal compliance
3. **Raw Data Preservation**: All values kept as-is with `_raw` suffix; no cleaning applied yet
4. **Intentional Duplicates**: Multiple extraction versions kept (Seedsman: 878 regular + 866 JS, ILGM: 3 versions) for quality comparison
5. **Strain Name Extraction**: 1,873 names extracted from URLs for failed scrapes (removed 9 non-product pages)

## Your Validation Tasks

### 1. Data Quality Scoring (0-100 scale)
For each botanical field category, provide:
- **Completeness Score**: % of non-null values
- **Consistency Score**: Format/pattern uniformity
- **Accuracy Score**: Logical validity (e.g., THC 0-100%, flowering 4-20 weeks)
- **Overall Quality Score**: Weighted average

**Categories to Score**:
- Genetics & Classification
- Cannabinoids (THC/CBD/CBN)
- Cultivation Data
- Sensory & Effects
- Metadata

### 2. Anomaly Detection
Identify and flag:
- **Out-of-Range Values**: THC >100%, flowering_time >30 weeks, negative percentages
- **Logical Inconsistencies**: indica% + sativa% ≠ 100%, hybrid flag mismatch
- **Format Issues**: Mixed units (%, mg/g, ratios), inconsistent delimiters
- **Suspicious Patterns**: Repeated identical values, placeholder text ("N/A", "Unknown", "TBD")
- **Data Type Mismatches**: Numbers stored as text, text in numeric fields

### 3. Completeness Analysis
For each field, report:
- **Fill Rate**: % of records with data
- **Null Patterns**: Are nulls random or clustered by seed bank?
- **Critical Gaps**: Which high-value fields have <50% coverage?
- **Seed Bank Comparison**: Which sources provide best/worst data coverage?

### 4. Cross-Seed-Bank Duplicate Identification
Detect potential duplicates using:
- **Exact Match**: Same strain_name_raw across seed banks
- **Fuzzy Match**: Similar names (Levenshtein distance <3, ignoring case/spaces)
- **Genetic Match**: Same genetics_lineage_raw + similar cannabinoid profiles
- **Confidence Levels**: High (95%+ match), Medium (80-95%), Low (60-80%)

**Output Format**:
```
Strain Name | Seed Bank 1 | Seed Bank 2 | Match Type | Confidence | Notes
```

### 5. Cleaning Priorities (Ranked 1-10)
Recommend cleaning order based on:
- **Impact**: How critical is this field for end users?
- **Effort**: How complex is the cleaning task?
- **Dependencies**: Does this field block other cleaning tasks?
- **ROI**: Effort vs. value gained

**Prioritize**:
- High-impact, low-effort (Quick wins)
- High-impact, high-effort (Strategic investments)
- Low-impact, low-effort (Nice-to-haves)
- Low-impact, high-effort (Deprioritize)

### 6. Seed Bank Data Quality Ranking
Rank all 20 seed banks by:
- **Overall Data Quality**: Completeness + consistency + accuracy
- **Field Coverage**: Number of fields populated
- **Data Richness**: Depth of information (e.g., detailed lineage vs. generic)
- **Extraction Success Rate**: % of strains with >50% fields populated

**Output Format**:
```
Rank | Seed Bank | Quality Score | Coverage | Richness | Success Rate | Notes
```

### 7. Recommended Next Steps
Provide actionable recommendations:
- **Immediate Actions**: Critical issues requiring urgent fixes
- **Phase 6 Cleaning Strategy**: Step-by-step cleaning roadmap
- **Data Enhancement Opportunities**: Fields that could be enriched (e.g., standardize units, parse ranges)
- **Validation Rules**: Automated checks to implement before production

## Output Format
Please structure your response as:

```markdown
# Master Dataset Validation Report

## Executive Summary
[3-5 sentence overview of dataset health]

## 1. Data Quality Scores
[Detailed scoring by category]

## 2. Anomaly Detection Results
[Flagged issues with examples]

## 3. Completeness Analysis
[Field-by-field coverage report]

## 4. Cross-Seed-Bank Duplicates
[Duplicate detection results]

## 5. Cleaning Priorities
[Ranked list with justification]

## 6. Seed Bank Quality Rankings
[Comparative analysis]

## 7. Recommended Next Steps
[Actionable roadmap]

## Appendix: Sample Data Issues
[5-10 specific examples with row references]
```

## Sample Data (First 100 Rows)
[Gemini will receive the first 100 rows of the CSV for analysis]

## Success Criteria
Your validation should help us:
1. **Identify critical data quality issues** before production deployment
2. **Prioritize cleaning efforts** for maximum ROI
3. **Detect duplicates** to avoid redundant data
4. **Rank seed bank quality** to inform future scraping priorities
5. **Create a Phase 6 roadmap** for data cleaning and standardization

---

**Note**: This is raw, unprocessed data. We expect issues - your job is to find them systematically and help us fix them efficiently.
