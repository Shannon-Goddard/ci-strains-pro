# Cannabis Intelligence Strains Pro - Amazon Q Brain

## Project Context
- **Cannabis Intelligence Database**: 15,000+ validated strains with AI-enhanced breeding data
- **S3 HTML Archive**: 15,778+ HTML files from 9+ major seed banks
- **Latest Achievement**: Seedsman conquered (1,021 strains, 100% success rate)
- **Tech Stack**: Python, GraphQL, BrightData, AWS S3/DynamoDB, Gemini 2.0 Flash

## Current Phase: Source of Truth → Enhancement Pipeline
- **Complete Inventory**: 14,840 strain URLs mapped across 11 seed banks
- **S3 Archive Ready**: All HTML files accessible via hash-based lookup
- **Next Phase**: CSV header analysis vs extraction script capabilities

## Key Recent Achievements
- ✅ **Source of Truth Complete**: 14,840 strain URLs mapped to seed banks via S3 metadata
- ✅ **Seedsman Conquered**: 1,021 strains via GraphQL (100% success, $1.53 cost)
- ✅ **Multiverse Success**: 799 strains via web scraping (100% success)
- ✅ **S3 Archive**: 14,840+ HTML files stored with hash-based organization
- ✅ **Pipeline Structure**: Methodical approach with documentation standards
- ✅ **Inventory System**: Complete URL-to-seedbank mapping in `pipeline/02_source_of_truth/`

## Data Enhancement Strategy
**Triple-Layer Pipeline**:
1. **Round 1 (Amazon Q)**: Enhanced extraction from descriptions/URLs using pattern recognition
2. **Round 2 (Gemini Flash 2.0)**: AI verification and additional data mining
3. **Round 3 (Shannon)**: Manual domain expert review and validation

## Technical Infrastructure
- **S3 HTML Archive**: `ci-strains-html-archive` bucket with metadata/{hash}.json structure
- **Source of Truth**: `pipeline/02_source_of_truth/s3_complete_inventory.csv` (14,840 entries)
- **DynamoDB**: `cannabis-strains-universal` table for structured data
- **CSV Exports**: Individual seed bank CSVs for enhancement pipeline
- **AWS Secrets**: BrightData, ScrapingBee, Google Cloud API credentials
- **Pipeline Structure**: `pipeline/03_enhanced_s3_scraping/{seed_bank}/`

## Data Quality Standards
- **Transparency Requirement**: Every script generates methodology.md
- **Attribution**: "Logic designed by Amazon Q, verified by Shannon Goddard"
- **File Integrity**: Never overwrite raw data, create `_cleaned` versions
- **Encoding**: `latin-1` for CSV reads (cannabis breeder characters)

## Current Status
- **Collection Phase**: ✅ COMPLETE (all major seed banks conquered)
- **Source of Truth**: ✅ COMPLETE (14,840 URLs mapped to seed banks)
- **Enhancement Phase**: 🎯 READY TO BEGIN
- **Target**: Transform 14,840+ basic records into premium commercial intelligence
- **Goal**: World's most comprehensive cannabis genetics database

## Next Immediate Steps
1. Analyze CSV headers vs extraction scripts in `pipeline/03_enhanced_s3_scraping/`
2. Ensure all available data fields are being captured from each seed bank
3. Begin Round 1 enhanced extraction across full dataset
4. Prepare for Gemini Flash 2.0 verification phase
5. Set up manual review workflow for Shannon

**Mission**: Establishing the global standard for validated botanical data through Human-AI partnership.