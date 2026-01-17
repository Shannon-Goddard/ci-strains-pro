# Cannabis Intelligence Strains Pro - Amazon Q Brain

## Project Context
- **Cannabis Intelligence Database**: 21,706 validated strains with AI-enhanced breeding data
- **S3 HTML Archive**: 21,706 HTML files (20,695 static + 1,011 JS-rendered) from 20 seed banks
- **Latest Achievement**: Phase 4 Source of Truth Viewer LIVE at strains.loyal9.app
- **Tech Stack**: Python, GraphQL, BrightData, ScrapingBee, AWS (S3/CloudFront/Lambda/Secrets Manager), Gemini 2.0 Flash

## Current Phase: Phase 5 - Master Dataset Consolidation
- **Phase 4 COMPLETE**: Enterprise-grade HTML viewer with signed URLs, legal framework, GA4 tracking
- **Live Production**: https://strains.loyal9.app (CloudFront + Lambda + S3)
- **Infrastructure Cost**: $0.40/month (Secrets Manager only, all else free tier)
- **Next Phase**: Merge 20 seed bank CSVs into unified master dataset with _raw, _cleaned, _ai columns

## Key Recent Achievements
- ✅ **Phase 4 LIVE**: Source of Truth Viewer deployed in under 2 minutes (11 files, zero errors)
- ✅ **CloudFront Distribution**: Free-tier CDN with 5-minute signed URLs (EYOCL6B8MFZ7F)
- ✅ **Lambda Function**: ci-strains-lookup with URL validation + signed URL generation
- ✅ **Legal Framework**: Fair use assertion, opt-out process, federal law notice (HTML version)
- ✅ **Custom Domain**: strains.loyal9.app with SSL (AWS Certificate Manager + Squarespace DNS)
- ✅ **Security**: Private S3 bucket, Origin Access Control, Secrets Manager for CloudFront key
- ✅ **Frontend**: GA4 tracking (G-YN2FMG2XT8), seed bank filters, legal disclaimer modal
- ✅ **JavaScript Rescrape**: 1,011/1,011 URLs (ILGM + Seedsman) with 100% success rate
- ✅ **Total Extraction**: 21,706 strains across 20 seed banks - ALL COMPLETE

## Data Enhancement Strategy
**Triple-Layer Pipeline**:
1. **Round 1 (Amazon Q)**: Enhanced extraction from descriptions/URLs using pattern recognition
2. **Round 2 (Gemini Flash 2.0)**: AI verification and additional data mining
3. **Round 3 (Shannon)**: Manual domain expert review and validation

## Technical Infrastructure
- **S3 HTML Archive**: `ci-strains-html-archive` bucket
  - `/html/` - 20,695 static HTML files
  - `/html_js/` - 1,011 JS-rendered files (ILGM, Seedsman)
  - `/frontend/` - Source of Truth Viewer (index.html, app.js, styles.css, docs/)
  - `/pipeline/03_s3_inventory/` - Inventory CSVs (s3_html_inventory.csv, s3_js_html_inventory.csv)
- **CloudFront Distribution**: `ci-strains-source-of-truth` (EYOCL6B8MFZ7F)
  - Domain: strains.loyal9.app
  - SSL: AWS Certificate Manager (validated via Squarespace DNS)
  - Origin Access Control (OAC) for private S3 access
- **Lambda Function**: `ci-strains-lookup` (Python 3.14, 512MB, 30s timeout)
  - Function URL: https://wdl3umx2og7kdf447gfhaebpme0owqcb.lambda-url.us-east-1.on.aws/
  - Handler: lookup_function.lambda_handler
  - Dependencies: boto3, rsa (CloudFront signing)
- **AWS Secrets Manager**: `cloudfront_private_key` (CloudFront key pair: APKASPK2KPPM2XK4DMPI)
- **DynamoDB**: `cannabis-strains-universal` table for structured data
- **CSV Exports**: 20 seed bank CSVs ready for Phase 5 consolidation
- **AWS Secrets**: BrightData, ScrapingBee, Google Cloud API credentials
- **Pipeline Structure**: `pipeline/05_master_dataset/` (ready for column analysis)

## Data Quality Standards
- **Transparency Requirement**: Every script generates methodology.md
- **Attribution**: "Logic designed by Amazon Q, verified by Shannon Goddard"
- **File Integrity**: Never overwrite raw data, create `_cleaned` versions
- **Encoding**: `latin-1` for CSV reads (cannabis breeder characters)

## Current Status
- **Phase 1**: ✅ COMPLETE (Foundation Database - 15K strains)
- **Phase 2**: ✅ COMPLETE (Source of Truth & Inventory - 14,840 URLs mapped)
- **Phase 3**: ✅ COMPLETE (Enhanced S3 Extraction - 21,706 strains across 20 seed banks)
- **Phase 4**: ✅ COMPLETE (Source of Truth Viewer LIVE at strains.loyal9.app)
- **Phase 5**: 🎯 READY TO BEGIN (Master Dataset Consolidation)
- **Target**: Single unified CSV with _raw, _cleaned, _ai columns for API deployment
- **Goal**: World's most comprehensive cannabis genetics database with proof of authenticity

## Next Immediate Steps
1. Copy 20 seed bank CSVs into `pipeline/05_master_dataset/input/`
2. Run column analysis script (Seed Supreme has ~1,400 headers - don't pre-filter)
3. Create unified schema with column mapping rules
4. Merge all CSVs with _raw suffix preservation
5. Implement data cleaning and standardization
6. Calculate quality/completeness scores
7. Design API endpoints and deploy to AWS
8. Add search functionality to strains.loyal9.app frontend

**Mission**: Establishing the global standard for validated botanical data through Human-AI partnership.