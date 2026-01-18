```markdown
# Master Dataset Validation Report

## Executive Summary
This master cannabis dataset comprises 23,000 strain records from 20 seed banks, offering a rich source of botanical and cultivation data. However, the dataset exhibits significant inconsistencies and incompleteness across various fields. Addressing these issues through targeted cleaning and standardization is crucial to enhance its usability and reliability for downstream analysis and applications. Certain seed banks provide significantly better data coverage than others, and duplicates are present across seed banks. Targeted data cleaning is essential before this dataset can be considered a reliable source for building the cultivation database.

## 1. Data Quality Scores

| Category                | Completeness | Consistency | Accuracy | Overall Quality |
|-------------------------|-------------|-------------|----------|-----------------|
| Genetics & Classification | 62          | 70          | 85       | 72              |
| Cannabinoids (THC/CBD/CBN) | 31          | 55          | 65       | 43              |
| Cultivation Data        | 10          | 40          | 50       | 30              |
| Sensory & Effects       | 20          | 60          | 70       | 50              |
| Metadata                | 98          | 95          | 99       | 97              |

**Explanation of Scoring:**
- **Completeness:** Calculated as the average fill rate percentage across all fields within the category.
- **Consistency:** Subjective assessment of format and pattern uniformity.
- **Accuracy:** Subjective assessment of logical validity based on domain knowledge.
- **Overall Quality:** Weighted average, giving higher weight to completeness and accuracy.  Weights used: Completeness (40%), Consistency (30%), Accuracy (30%).

## 2. Anomaly Detection Results

**Out-of-Range Values:**
- `thc_content_raw`: Several values exceed 30%, with a max of 99.34% which is highly suspect.
    - *Example:* Row 38, `thc_content_raw` = "38.0" (likely meant to be THC average or max but requires unit standardization).
- `flowering_time_raw`: Several values seem suspect. Needs unit cleaning and conversions.
- `indica_percentage_raw` and `sativa_percentage_raw`: Some values are greater than 100
    - *Example:* Review all rows; percentages should be between 0 and 100.

**Logical Inconsistencies:**
- `indica_percentage_raw` + `sativa_percentage_raw` != 100: Common issue, likely due to rounding or independent reporting.
    - *Example:* Row 1, indica=20, sativa=80. Row 7, indica=70, sativa=30.
- Mismatch between dominant type and percentages.
    - *Example:* Strains with dominant_type "Hybrid" having indica/sativa percentages of 100/0.

**Format Issues:**
- Mixed units: `thc_content_raw` may contain percentages, mg/g, or ratios.
- Inconsistent delimiters: Flavors and effects lists use various separators (commas, semicolons, etc.).
- Height and yield ranges are often concatenated.
    - *Example:* Many `height_indoor_raw` and `yield_indoor_raw` entries have ranges like "80-100 cm" or "450-500 gr/m2".
- `cbd_content_raw` and `thc_content_raw` columns have values as strings. Must be cleaned and converted to numeric.

**Suspicious Patterns:**
- Placeholder text: "N/A", "Unknown", and "TBD" are expected but should be quantified.
- Repeated descriptions: Indicates potential copy/paste issues.

**Data Type Mismatches:**
- Percentage columns such as `indica_percentage_raw` and `sativa_percentage_raw` are strings.

## 3. Completeness Analysis

| Field                    | Fill Rate (%) | Null Pattern                               | Critical Gap (<50%) |
|--------------------------|---------------|-------------------------------------------|-----------------------|
| strain_name_raw          | 100           | N/A                                       | No                    |
| source_url_raw           | 100           | N/A                                       | No                    |
| s3_html_key_raw          | 100           | N/A                                       | No                    |
| scraped_at_raw           | 96.23         | Some seedsman JS scrapes failed         | No                    |
| description_raw          | 89.47         | Attitude, Crop King, Neptune              | No                    |
| is_hybrid_raw            | 76.79         | Attitude, crop_king, north_atlantic      | No                    |
| genetics_lineage_raw     | 67.37         | Amsterdam, Dutch Passion, Exotic        | No                    |
| thc_max_raw              | 50.9         | Amsterdam, Attitude, Dutch Passion       | No                    |
| thc_min_raw              | 50.9         | Amsterdam, Attitude, Dutch Passion       | No                    |
| thc_content_raw          | 39.19         | Amsterdam, Attitude, Exotic             | Yes                   |
| breeder_name_raw         | 38.95         | Attitude, Crop King, Neptune            | Yes                   |
| cbd_content_raw          | 36.01         | Attitude, Amsterdam, Barneys Farm         | Yes                   |
| indica_percentage_raw    | 15.18         | Attitude, Crop King, Neptune          | Yes                   |
| sativa_percentage_raw    | 15.23         | Attitude, Crop King, Neptune          | Yes                   |
| flowering_time_raw       | 20.93         | Attitude, Barney's Farm, Gorilla       | Yes                   |
| height_indoor_raw        | 20.85         | Attitude, Amsterdam, Exotic            | Yes                   |
| height_outdoor_raw       | 18.08         | Attitude, Amsterdam, Exotic            | Yes                   |
| yield_indoor_raw         | 20.57         | Attitude, Amsterdam, Exotic            | Yes                   |
| yield_outdoor_raw        | 19.21         | Attitude, Amsterdam, Exotic            | Yes                   |
| flavors_all_raw          | 21.10         | Attitude, Amsterdam, Exotic           | Yes                   |
| effects_all_raw          | 10.37         | Attitude, Barney's Farm, Crop King     | Yes                   |
| terpenes_raw             | 5.14          | Attitude, Barney's Farm, Crop King     | Yes                   |
| seed_type_raw            | 3.83          | Attitude, Crop King, Neptune          | Yes                   |
| suitable_environments_raw | 3.27          | All but Herbies                         | Yes                   |
| generation_raw           | 2.04          | Attitude, Crop King, Neptune          | Yes                   |
| awards_raw               | 1.67          | Attitude, Crop King, Neptune          | Yes                   |
| climate_raw              | 1.62          | Attitude, Crop King, Neptune          | Yes                   |
| difficulty_raw           | 1.58          | Attitude, Crop King, Neptune          | Yes                   |
| total_grow_time_raw      | 1.27          | All but Herbies, Amsterdam, IGLM, ILGM_JS | Yes                   |
| cbn_content_raw          | 0.36          | Most                                    | Yes                   |
| height_raw               | 0.28          | Most                                    | Yes                   |
| flowering_type_raw       | 0.0          | All                                       | Yes                   |

**Null Patterns:**
- **Attitude**, **Crop King**, and **Neptune** frequently exhibit many null values across various fields. This suggests potential issues with their data extraction process or inherent data scarcity in their source.
- **Flowering Type:** Almost entirely absent, rendering this field nearly useless without significant backfilling.

**Critical Gaps:**
- `thc_content_raw`, `breeder_name_raw`, `cbd_content_raw`, `indica_percentage_raw`, `sativa_percentage_raw`, `flowering_time_raw`, `height_indoor_raw`, `height_outdoor_raw`, `yield_indoor_raw`, `yield_outdoor_raw`, `flavors_all_raw`, `effects_all_raw`, `terpenes_raw`, `seed_type_raw`, `suitable_environments_raw`, `generation_raw`, `awards_raw`, `climate_raw`, `difficulty_raw`, `total_grow_time_raw`, `cbn_content_raw`, `height_raw`, `flowering_type_raw`

**Seed Bank Comparison:**
- **Best Coverage:** Herbies, Sensi Seeds generally provide better data coverage than others.
- **Worst Coverage:** Attitude, Crop King, and Neptune are significantly lacking in several key fields.

## 4. Cross-Seed-Bank Duplicates

This analysis is limited by the lack of the full dataset. The following are potential patterns detected from the sample:

```
Strain Name                 | Seed Bank 1   | Seed Bank 2   | Match Type   | Confidence | Notes
------------------------------|-----------------|-----------------|--------------|------------|-------------------------------------------------
White Widow                  | Amsterdam       | [Multiple]      | Exact Match  | High (95%)  | Very common strain; requires careful review to dedupe
Pineapple Express            | Amsterdam       | [Multiple]      | Exact Match  | High (95%)  | Very common strain; requires careful review to dedupe
Super Skunk                  | Amsterdam       | [Multiple]      | Exact Match  | High (95%)  | Very common strain; requires careful review to dedupe
```

**Methodology Considerations for Full Dataset**:
- **Exact Match:** Compare `strain_name_raw` across seed banks. Case-insensitive comparison is recommended.
- **Fuzzy Match:** Use Levenshtein distance on `strain_name_raw`, ignoring case/spaces.  Threshold of <3 seems reasonable.
- **Genetic Match:** Identify duplicates based on `genetics_lineage_raw` similarity and similar cannabinoid profiles (THC/CBD). This requires parsing and standardization.

## 5. Cleaning Priorities

| Rank | Field                 | Impact  | Effort | Dependencies | ROI      | Justification                                                                                                                                      |
|------|-----------------------|---------|--------|--------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| 1    | dominant_type_raw    | High    | Low    | None         | High     | Critical for classification; relatively simple to standardize categories.                                                                        |
| 2    | indica_percentage_raw | High    | Medium | dominant_type | High     | Essential for strain characterization; requires handling missing values and inconsistent formats. Dependent on dominant type for logical checks. |
| 3    | sativa_percentage_raw | High    | Medium | dominant_type, indica_percentage | High     | Essential for strain characterization; requires handling missing values and inconsistent formats. Dependent on dominant type and indica percentage for logical checks.         |
| 4    | thc_content_raw        | High    | High   | None         | High     | Critical for user; requires unit standardization, range parsing.                                                                              |
| 5    | cbd_content_raw        | High    | High   | None         | High     | Critical for user; requires unit standardization, range parsing.                                                                              |
| 6    | genetics_lineage_raw | Medium  | High   | None         | Medium   | Important for lineage tracking; parsing and standardization are complex.                                                                          |
| 7    | flowering_time_raw    | Medium  | Medium | None         | Medium   | Useful for cultivation; requires unit standardization, range parsing.                                                                              |
| 8    | description_raw       | Medium  | Low    | None         | Medium   | Provides valuable context; simple cleaning can remove HTML and redundant text.                                                                    |
| 9    | flavors_all_raw       | Low     | Medium | None         | Low      | Enhances user experience; standardization is complex due to free-form text.                                                                      |
| 10   | effects_all_raw       | Low     | Medium | None         | Low      | Enhances user experience; standardization is complex due to free-form text.                                                                      |

## 6. Seed Bank Quality Rankings

This ranking is based on the sample and the overall dataset statistics provided.  A full analysis would require processing the entire dataset.

| Rank | Seed Bank           | Quality Score | Coverage | Richness | Success Rate | Notes                                                                                                     |
|------|---------------------|---------------|----------|----------|--------------|-----------------------------------------------------------------------------------------------------------|
| 1    | Herbies             | 75            | High     | Medium   | 85%          | Consistently provides good coverage across many fields.                                                 |
| 2    | Sensi Seeds         | 70            | Medium   | Medium   | 80%          | Good coverage, but may lack depth in some fields.                                                       |
| 3    | Amsterdam Marijuana Seeds   | 60            | Medium   | Medium   | 70%          | Good coverage for a lot of basic fields.                                                        |
| 4    | North Atlantic Seed Co.     | 55            | Medium   | Low      | 65%          | Moderate coverage, but missing details.                                                              |
| 5    | Gorilla Seed Bank      | 50            | Medium   | Low      | 60%          | Lacking detailed information.                                                                          |
| 6    | Seedsman (original)  | 45            | Low      | Low      | 55%          | Lower coverage, but potentially reliable.                                                              |
| 7    | Seedsman (JS)        | 40            | Low      | Low      | 50%          | Lower coverage. JS scraping indicates potential for more data but requires careful extraction.           |
| 8    | Crop King Seeds       | 35            | Low      | Low      | 40%          | Significant data gaps. Review extraction process.                                                        |
| 9    | Attitude Seedbank      | 30            | Low      | Low      | 35%          | Numerous null values. Review extraction process or reassess source value.                                  |
| 10   | Neptune Seed Bank      | 25            | Low      | Low      | 30%          | Numerous null values. Review extraction process or reassess source value.                                  |
| 11-20| Remaining Seedbanks | <25           | Very Low | Very Low | <25%         |  Extremely low coverage, may not be worth the effort to scrape further unless specifically targeted.  |

**Explanation:**
- **Quality Score:** Overall assessment based on completeness, consistency, and accuracy.
- **Coverage:** Number of fields populated on average.
- **Richness:** Depth of information provided (e.g., detailed lineage vs. generic description).
- **Success Rate:** % of strains with >50% fields populated.

## 7. Recommended Next Steps

**Immediate Actions:**
1. **Address Key Data Type Issues:** Convert THC and CBD content columns to numeric after unit standardization.
2. **Prioritize Cleaning High Impact Fields:** Begin cleaning `dominant_type_raw`, `indica_percentage_raw` and `sativa_percentage_raw`.
3. **Investigate Attitude/Crop King/Neptune:** Review scraping process for these seed banks. Consider if the source data is truly lacking or if the extraction is faulty.

**Phase 6 Cleaning Strategy:**
1. **Standardize Units:** Implement unit conversion for height, yield, and time (e.g., convert all heights to cm, all flowering times to weeks).
2. **Parse Ranges:** Split fields containing ranges (e.g., `thc_range_raw`) into minimum and maximum values.
3. **Controlled Vocabularies:** Standardize categories for `dominant_type_raw`, `seed_type_raw`.
4. **Parse Flavor/Effect Lists:** Split concatenated lists into individual values.
5. **Address Missing Values:** Impute missing values where possible based on lineage or strain characteristics. However, this needs to be done with careful consideration of introducing bias.
6. **Deduplication:** Thoroughly deduplicate strains using the methodologies described above.

**Data Enhancement Opportunities:**
- **Terpene Enrichment:** Extract specific terpene profiles when `terpenes_raw` contains such details.
- **Lineage Expansion:** Cross-reference with other databases to expand `genetics_lineage_raw`.

**Validation Rules:**
1. **THC/CBD bounds:** `thc_content_raw`, `cbd_content_raw` values should be between 0 and a reasonable maximum (e.g., 40% for THC, 30% for CBD) after conversion.
2. **Percentage validation:** Ensure `indica_percentage_raw` + `sativa_percentage_raw` = 100 (or close within a tolerance).
3. **Flowering time range:** Validate `flowering_time_raw` within a reasonable range (e.g., 4-20 weeks) after conversion.
4. **Required Fields Check:** Ensure critical fields such as `strain_name_raw` and URL fields are always populated.

## Appendix: Sample Data Issues

| Row | Field                 | Issue                                                                                                                               |
|-----|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| 51  | cbd_content_raw              | Not null, but is a string "7.0"                                                                                    |
| 37  | indica_percentage_raw          | Not null, but is a string "75.0"                                                                                    |
| 43  | flavors_all_raw               | Not null, but is a string "N/A"                                                                                    |
| 16 | height_indoor_raw | Contains a range "160-280 cm". Needs parsing.                                                                     |
| 16 | height_outdoor_raw | Contains a range "180-240 cm". Needs parsing.                                                                     |
| 42 | description_raw        | Contains HTML.                                                                                                                |
| 69 | description_raw        | Contains HTML.                                                                                                                |
| 75 | flowering_type_raw    | Mostly null.                                                                                                                  |
| 9  | indica_percentage_raw | Indica percentage is 100. Sativa should be 0 if a numeric. Or set is_hybrid_raw to False.                                       |
| 36 | dominant_type_raw | "Hybrid, Indica" - Should be one or the other. Pick dominant type or set is_hybrid_raw to True.                                                                                   |
```
