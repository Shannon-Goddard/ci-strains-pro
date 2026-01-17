# Pipeline 05: Master Dataset Consolidation

**Goal**: Merge 21,706 strains from 20 seed banks into unified master dataset with API-ready structure.

## 📊 Source Data (20 Seed Banks)

**IMPORTANT**: All CSV files are located OUTSIDE this workspace. When starting pipeline 05:
1. Copy all 20 CSV files from their current location into `pipeline/05_master_dataset/input/`
2. CSV filenames should match seed bank folder names from `pipeline/02_s3_scraping/`
3. Reference S3 inventory for URL mappings: `pipeline/03_s3_inventory/s3_html_inventory.csv` and `s3_js_html_inventory.csv`

| Seed Bank              | Strains | Columns | Location |
|------------------------|---------|---------|----------|
| Attitude Seed Bank     | 7,673   | 95      | `pipeline/02_s3_scraping/attitude_seed_bank/` |
| Crop King              | 3,336   | 97      | `pipeline/02_s3_scraping/crop_king/` |
| North Atlantic         | 2,727   | 118     | `pipeline/02_s3_scraping/north_atlantic/` |
| Gorilla Seed Bank      | 2,009   | 51      | `pipeline/02_s3_scraping/gorilla/` |
| Neptune                | 1,995   | 111     | `pipeline/02_s3_scraping/neptune/` |
| Seedsman               | 866     | 79      | `pipeline/02_s3_scraping/seedsman/` |
| Multiverse Beans       | 799     | 83      | `pipeline/02_s3_scraping/multiverse_beans/` |
| Herbies Seeds          | 753     | 35      | `pipeline/02_s3_scraping/herbies/` |
| Sensi Seeds            | 620     | 131     | `pipeline/02_s3_scraping/sensi_seeds/` |
| Seed Supreme           | 353     | 1,477   | `pipeline/02_s3_scraping/seed_supreme/` |
| Mephisto Genetics      | 245     | 83      | `pipeline/02_s3_scraping/mephisto_genetics/` |
| Exotic Genetix         | 227     | 10      | `pipeline/02_s3_scraping/exotic_genetics/` |
| Amsterdam Marijuana    | 163     | 66      | `pipeline/02_s3_scraping/amsterdam/` |
| ILGM                   | 133     | 25      | `pipeline/02_s3_scraping/ilgm/` |
| Barney's Farm          | 88      | 94      | `pipeline/02_s3_scraping/barneys_farm/` |
| Royal Queen Seeds      | 67      | 115     | `pipeline/02_s3_scraping/royal_queen_seeds/` |
| Dutch Passion          | 44      | 160     | `pipeline/02_s3_scraping/dutch_passion/` |
| Seeds Here Now         | 43      | 150     | `pipeline/02_s3_scraping/seeds_here_now/` |
| Great Lakes Genetics   | 16      | 41      | `pipeline/02_s3_scraping/great_lakes_genetics/` |
| Compound Genetics      | 1       | 7       | `pipeline/02_s3_scraping/compound/` |

**Total**: 21,706 strains across 20 seed banks

## 🎯 Master Dataset Strategy

**Single unified CSV with column flags** (recommended for API flexibility):

```
master_strains.csv
├── Core Identity (always present)
│   ├── strain_id (UUID)
│   ├── strain_name
│   ├── seed_bank
│   ├── source_url
│   ├── s3_html_key
│   └── collection_date
├── Raw Data Columns (from extraction)
│   ├── thc_raw
│   ├── cbd_raw
│   ├── genetics_raw
│   ├── flowering_time_raw
│   └── ... (all original fields with _raw suffix)
├── Cleaned Data Columns (standardized)
│   ├── thc_min
│   ├── thc_max
│   ├── thc_avg
│   ├── cbd_min
│   ├── cbd_max
│   ├── cbd_avg
│   ├── genetics_cleaned
│   ├── flowering_time_days_min
│   ├── flowering_time_days_max
│   └── ... (standardized fields with _cleaned suffix)
├── AI-Enhanced Columns (future enrichment)
│   ├── genetics_verified (AI validation)
│   ├── terpene_profile_predicted
│   ├── effects_predicted
│   ├── grow_difficulty_predicted
│   └── ... (AI fields with _ai suffix)
└── Quality Flags
    ├── has_raw_data (boolean)
    ├── has_cleaned_data (boolean)
    ├── has_ai_data (boolean)
    ├── data_quality_score (0-100)
    └── completeness_score (0-100)
```

**API Filtering Strategy**:
- `/api/strains?tier=raw` → Return only `_raw` columns
- `/api/strains?tier=cleaned` → Return only `_cleaned` columns
- `/api/strains?tier=premium` → Return all columns including `_ai`
- `/api/strains?tier=full` → Return everything

## 📁 Pipeline Structure

```
05_master_dataset/
├── input/                          # Place all 20 CSV files here
│   ├── attitude_seed_bank.csv
│   ├── crop_king.csv
│   ├── north_atlantic.csv
│   └── ... (all 20 seed banks)
├── scripts/
│   ├── 01_column_analysis.py       # Analyze all headers across 20 CSVs
│   ├── 02_column_mapping.py        # Map similar columns to unified schema
│   ├── 03_merge_raw.py             # Merge all CSVs with _raw suffix
│   ├── 04_clean_data.py            # Standardize and clean data
│   ├── 05_quality_scoring.py       # Calculate quality/completeness scores
│   └── 06_validate_master.py      # Final validation and stats
├── output/
│   ├── master_strains.csv          # Final unified dataset
│   ├── column_mapping.json         # Documentation of column transformations
│   ├── quality_report.md           # Data quality analysis
│   └── api_schema.json             # API response schema definitions
├── docs/
│   ├── COLUMN_STANDARDIZATION.md   # Rules for cleaning/standardizing
│   ├── API_DESIGN.md               # API endpoint specifications
│   └── DATA_DICTIONARY.md          # Complete field documentation
├── methodology.md
└── README.md
```

## 🚀 AWS Infrastructure Plan

### Phase 1: Data Storage
- **S3 Bucket**: `ci-strains-master-data`
  - `master_strains.csv` (full dataset)
  - `master_strains.parquet` (optimized for queries)
  - Versioning enabled for data lineage

### Phase 2: Database Layer
- **Option A**: Amazon Athena (serverless SQL on S3)
  - Query CSV/Parquet directly
  - Pay per query ($5/TB scanned)
  - Best for analytics/reporting
  
- **Option B**: Amazon RDS PostgreSQL
  - Full relational database
  - Better for transactional queries
  - ~$15-30/month for small instance
  
- **Option C**: DynamoDB (NoSQL)
  - Ultra-fast key-value lookups
  - Pay per request ($0.25/million reads)
  - Best for high-traffic API

### Phase 3: API Layer
- **Lambda Function**: `ci-strains-api`
  - Python 3.12 with FastAPI or Flask
  - Query filtering by tier (raw/cleaned/premium)
  - Pagination, search, filters
  
- **API Gateway**: REST API
  - `/strains` - List/search strains
  - `/strains/{id}` - Get single strain
  - `/strains/search?name=OG+Kush`
  - `/strains/filter?seed_bank=Neptune&thc_min=20`
  
- **CloudFront**: CDN for API responses
  - Cache common queries
  - Reduce Lambda costs

### Phase 4: Authentication (Optional)
- **API Keys**: Free tier access (raw data only)
- **Paid Tier**: Premium access (cleaned + AI data)
- **Cognito**: User management

## 💰 Estimated AWS Costs

**Free Tier (First 12 Months)**:
- S3: 5GB storage = $0
- Lambda: 1M requests = $0
- API Gateway: 1M requests = $0
- CloudFront: 1M requests = $0

**After Free Tier**:
- S3: ~$0.50/month (20GB storage)
- Lambda: ~$1-5/month (100K requests)
- API Gateway: ~$3.50/month (1M requests)
- RDS (if used): ~$15-30/month
- **Total**: $5-40/month depending on traffic

## 🎯 Next Steps

1. **Column Analysis**: Run script to identify all unique columns across 20 CSVs
2. **Column Mapping**: Create unified schema and mapping rules
3. **Merge Raw**: Combine all CSVs with `_raw` suffix preservation
4. **Data Cleaning**: Standardize formats (THC ranges, flowering times, etc.)
5. **Quality Scoring**: Calculate completeness and quality metrics
6. **API Design**: Define endpoint structure and response schemas
7. **AWS Deployment**: Upload to S3, create Lambda API, configure API Gateway
8. **Search Implementation**: Add `/search?name=strain` endpoint to Lambda and wire up frontend search box

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
