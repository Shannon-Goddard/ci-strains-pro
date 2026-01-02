# Cannabis Intelligence Database - Data Dictionary
**Version 1.0 | Generated: January 2026**

## Overview
This data dictionary describes the structure and contents of the Cannabis Intelligence Database, containing 15,768+ validated cannabis strain records processed through AI-enhanced extraction and human verification.

---

## Column Definitions

### Source & Identity
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `source_url` | String | Original webpage URL where strain data was scraped | `https://www.cannabis-seeds-bank.co.uk/...` |
| `strain_name` | String | Cleaned strain name | `Blue Dream`, `OG Kush` |
| `strain_id` | Integer | Unique identifier for each strain record | `1`, `2`, `3` |
| `breeder_name` | String | Cannabis breeder/genetics company | `DNA Genetics`, `Barney's Farm` |
| `bank_name` | String | Seed bank/retailer | `The Attitude Seed Bank`, `Neptune Seed Bank` |

### Genetics & Breeding
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `primary_generation` | String | Generation marker (F1, F2, S1, etc.) | `F1`, `S1`, `IBL` |
| `breeding_method` | String | Method used to create strain | `Cross`, `Backcross`, `Selfed` |
| `phenotype` | String | Specific phenotype identifier | `#1`, `#3`, `Pheno A` |
| `lineage` | String | Parent strain genetics | `Blueberry X Haze`, `OG Kush X Diesel` |
| `sativa_percentage` | Float | Percentage of Sativa genetics | `70.0`, `100.0` |
| `indica_percentage` | Float | Percentage of Indica genetics | `30.0`, `0.0` |
| `ruderalis_percentage_validated` | Float | Percentage of Ruderalis genetics (autoflower) | `10.0`, `0.0` |

### Cannabinoids
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `thc_min` | Float | Minimum THC percentage | `15.0`, `20.0` |
| `thc_max` | Float | Maximum THC percentage | `25.0`, `30.0` |
| `thc` | Float | Single THC value (when range not available) | `22.0` |
| `cbd_min` | Float | Minimum CBD percentage | `0.1`, `5.0` |
| `cbd_max` | Float | Maximum CBD percentage | `1.0`, `15.0` |
| `cbd` | Float | Single CBD value (when range not available) | `0.5` |

### Cultivation
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `seed_gender` | String | Seed type | `Feminized`, `Regular`, `Autoflowering` |
| `flowering_behavior` | String | Flowering trigger type | `Photoperiod`, `Autoflowering` |
| `flowering_days_min` | Float | Minimum flowering time in days | `56.0`, `63.0` |
| `flowering_days_max` | Float | Maximum flowering time in days | `70.0`, `77.0` |
| `height_indoor_description` | String | Indoor height category | `Short`, `Stretch Medium`, `Stretch Tall` |
| `height_indoor_cm` | Float | Indoor height in centimeters | `100.0`, `150.0` |
| `grow_difficulty` | String | Cultivation difficulty level | `Easy`, `Intermediate`, `Advanced` |

### Yields
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `yield_decription` | String | Yield category description | `Heavy`, `Medium`, `High` |
| `indoor_yield_min_g` | Float | Minimum indoor yield in grams | `400.0` |
| `indoor_yield_max_g` | Float | Maximum indoor yield in grams | `600.0` |
| `outdoor_yield_min_g` | Float | Minimum outdoor yield in grams | `500.0` |
| `outdoor_yield_max_g` | Float | Maximum outdoor yield in grams | `1000.0` |

### Effects & Characteristics
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `effects` | String | Reported effects (comma-separated) | `relaxing, euphoric, creative` |
| `flavors` | String | Flavor profile (comma-separated) | `citrus, pine, earthy` |
| `terpenes` | String | Primary terpenes | `Limonene, Myrcene, Pinene` |

### Data Quality & Processing
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `scraped_at` | DateTime | Timestamp of data collection | `2025-11-25T13:54:33.603173` |
| `processing_timestamp` | DateTime | Timestamp of data processing | `2025-01-02T00:53:50.069` |
| `quality_score` | Float | Data completeness score (1-5) | `3.0`, `4.0` |
| `confidence_score` | Float | AI validation confidence | `0.85`, `0.92` |
| `confidence_notes` | String | Validation methodology notes | `Extracted from scraped data` |
| `validation_notes` | String | AI validation comments | `THC range validated by Gemini` |
| `scrape_success` | Boolean | Successful data extraction | `True`, `False` |
| `scrape_error` | String | Error message if scraping failed | `Page not found` |

### Validated Fields
All fields ending in `_validated` represent AI-processed and verified versions of the original scraped data:
- `thc_min_validated`, `thc_max_validated`
- `cbd_min_validated`, `cbd_max_validated`
- `sativa_percentage_validated`, `indica_percentage_validated`
- `flowering_days_min_validated`, `flowering_days_max_validated`
- `effects_validated`, `flavors_validated`
- `lineage_validated`, `phenotype_validated`

---

## Data Processing Notes

### Extraction Logic
- **THC/CBD Ranges**: Pattern `(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%` creates `_min`, `_max`, and `_avg` columns
- **Genetics**: Pattern `(\d+)%\s*Sativa` / `(\d+)%\s*Indica` for genetic ratios
- **Lineage**: Detects "Cross:", "Genetics:", or "Parents:" followed by "X" notation

### Quality Scoring (1-5 Scale)
- **5**: Complete data with THC, CBD, genetics, flowering time, effects, flavors
- **4**: Most fields present, minor gaps
- **3**: Core data present (genetics, flowering time)
- **2**: Basic strain info, limited details
- **1**: Minimal data, name and breeder only

### Data Integrity Rules
- **Never overwrite raw data** - Always create `_cleaned` or `_processed` versions
- **Use `latin-1` encoding** for CSV reads to handle special cannabis breeder characters
- **Transparency logging** - Every processing step documented in methodology files

---

## Usage Examples

### Filter by High THC Strains
```sql
SELECT strain_name, thc_max, breeder_name 
FROM cannabis_database 
WHERE thc_max >= 25.0 
ORDER BY thc_max DESC;
```

### Find Sativa-Dominant Strains
```sql
SELECT strain_name, sativa_percentage, effects 
FROM cannabis_database 
WHERE sativa_percentage >= 70.0;
```

### Quick Flowering Strains
```sql
SELECT strain_name, flowering_days_min, flowering_days_max 
FROM cannabis_database 
WHERE flowering_days_max <= 60.0;
```

---

## Methodology Attribution
**Logic designed by Amazon Q, verified by Shannon Goddard.**

**Data Sources**: 15,768+ strain records from major seed banks and breeders  
**Processing**: Gemini Flash 2.0 validation with 99.17% success rate  
**Last Updated**: January 2, 2026  

---

**🌿 Cannabis Intelligence Database - Enabling innovation through validated data.**