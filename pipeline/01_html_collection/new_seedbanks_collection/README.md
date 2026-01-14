# Cannabis Intelligence Database - New Seedbanks HTML Collection

![Status: Ready for Deployment](https://img.shields.io/badge/Status-Ready_for_Deployment-green)
![Target: 99.5% Success Rate](https://img.shields.io/badge/Target-99.5%25_Success-blue)
![New Banks: 5 Seedbanks](https://img.shields.io/badge/New_Banks-5_Seedbanks-orange)

**Logic designed by Amazon Q, verified by Shannon Goddard**

## 🎯 Mission

Extend the Cannabis Intelligence Database by collecting HTML snapshots from 5 additional premium seedbanks, adding to the existing S3 archive with the same bulletproof reliability.

## 🏪 Target Seedbanks

1. **Sensi Seeds** - https://sensiseeds.us/cannabis-seeds/
2. **Humboldt Seed Company** - https://californiahempseeds.com/shop-all/
3. **Crop King** - https://www.cropkingseeds.com/
4. **Barney's Farm** - https://www.barneysfarm.com/us/
5. **ILGM** - https://ilgm.com/categories/cannabis-seeds

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies (same as pipeline/01)
pip install -r requirements.txt

# AWS credentials already configured
```

### 2. Create URL Database
```bash
# Create new seedbank URLs database
python scripts/01_create_seedbank_urls.py
```

### 3. Run Collection
```bash
# Full automated pipeline
python scripts/02_bulletproof_scraper.py

# Monitor progress
python scripts/03_progress_monitor.py --watch
```

## 📊 Expected Results

### Target Collection
- **Sensi Seeds**: ~500-1000 strains
- **Humboldt**: ~200-500 strains  
- **Crop King**: ~300-600 strains
- **Barney's Farm**: ~400-800 strains
- **ILGM**: ~300-600 strains
- **Total Estimated**: 1,700-3,500 new strain pages

### Integration
- **Existing S3 Archive**: 13,163 pages
- **New Addition**: 1,700-3,500 pages
- **Combined Total**: ~15,000-17,000 pages
- **Storage**: Same S3 bucket with encryption

## 🛡️ Same Bulletproof Features

- Multi-layer fallback system (Bright Data → ScrapingBee → Direct)
- 8-point HTML validation (75% threshold)
- Cannabis keyword detection
- Respectful rate limiting per domain
- AWS S3 encrypted storage
- Progress tracking and recovery

---

*Ready to expand the Cannabis Intelligence ecosystem! 🌿*