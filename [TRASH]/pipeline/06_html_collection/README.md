# Cannabis Intelligence Database - Bulletproof HTML Collection System

![Status: Ready for Deployment](https://img.shields.io/badge/Status-Ready_for_Deployment-green)
![Target: 99.5% Success Rate](https://img.shields.io/badge/Target-99.5%25_Success-blue)
![URLs: ~12K Unique](https://img.shields.io/badge/URLs-~12K_Unique-orange)

**Logic designed by Amazon Q, verified by Shannon Goddard**

## 🎯 Mission

Create an immutable source of truth for cannabis strain data by collecting complete HTML snapshots with bulletproof reliability, targeting 99.5% success rate across ~12,000 unique URLs.

## 🏗️ System Architecture

### Multi-Layer Fallback System
1. **Bright Data Web Unlocker** (Primary) - $133.71 budget
2. **ScrapingBee API** (Fallback) - 250K credits available  
3. **Direct Requests** (Final fallback) - Rotating user agents
4. **Manual Queue** (Human intervention) - Export for review

### Quality Validation Pipeline
- 8-point HTML validation system (75% threshold)
- Cannabis-specific keyword detection
- Error pattern recognition
- Size and structure validation

### Secure Cloud Storage
- AWS S3 with AES-256 encryption
- Cross-region replication (us-west-2)
- Structured metadata storage
- API-ready access patterns

## 📁 Directory Structure

```
pipeline/06_html_collection/
├── scripts/
│   ├── 01_url_deduplication.py    # Process 15,778 → ~12K unique URLs
│   ├── 02_bulletproof_scraper.py  # Multi-layer scraping engine
│   ├── 03_progress_monitor.py     # Real-time monitoring & recovery
│   └── run_collection.py          # Main orchestration script
├── config/
│   └── scraper_config.py          # System configuration
├── data/                          # Generated during execution
│   ├── scraping_progress.db       # SQLite progress tracking
│   ├── url_mapping.json          # URL deduplication results
│   └── unique_urls.csv           # Analysis-ready format
├── logs/                         # Execution logs
├── requirements.txt              # Python dependencies
└── methodology.md               # Complete technical methodology
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (required for S3 storage)
aws configure
```

### 2. Update Configuration
Edit `config/scraper_config.py`:
- Set your S3 bucket name
- Adjust rate limits if needed
- Configure domain-specific delays

### 3. Run Complete Pipeline
```bash
# Full automated pipeline
python run_collection.py full

# Or step-by-step:
python run_collection.py dedupe    # URL deduplication
python run_collection.py collect   # HTML collection
python run_collection.py monitor   # Progress dashboard
```

### 4. Monitor Progress
```bash
# Real-time dashboard (refreshes every 30s)
python scripts/03_progress_monitor.py --watch

# One-time status check
python scripts/03_progress_monitor.py --action dashboard
```

## 📊 Expected Results

### Input Data
- **Source**: Cannabis_Database_Validated_Complete.csv
- **Total Records**: 15,778 strain entries
- **Raw URLs**: 15,778 (with duplicates)

### Deduplication Output
- **Unique URLs**: ~12,000-13,000 (estimated)
- **Deduplication Rate**: ~20-25%
- **Storage Savings**: Significant (no duplicate HTML)

### Collection Targets
- **Success Rate**: ≥99.5% (bulletproof target)
- **Quality Score**: ≥95% validation average
- **Response Time**: <2 seconds average
- **Data Volume**: ~500MB HTML + metadata

## 🛡️ Bulletproof Features

### Reliability
- **6-layer retry system** with exponential backoff
- **Multi-service fallbacks** (Bright Data → ScrapingBee → Direct)
- **Automatic recovery** from interruptions
- **Progress checkpoints** every 100 URLs

### Quality Assurance
- **8-point HTML validation** system
- **Cannabis keyword detection** (strain, THC, CBD, etc.)
- **Error pattern recognition** (captcha, blocks, etc.)
- **Size and structure validation**

### Monitoring & Recovery
- **Real-time dashboard** with live statistics
- **Failed URL export** for manual review
- **Stuck process recovery** (timeout handling)
- **Method performance tracking**

### Security & Compliance
- **Respectful rate limiting** (2-4 seconds per domain)
- **User agent rotation** (5 different browsers)
- **AWS encryption** (AES-256 server-side)
- **Access logging** and audit trails

## 🔧 Advanced Usage

### Recovery Operations
```bash
# Reset failed URLs for retry (if attempts < 3)
python scripts/03_progress_monitor.py --action reset-failed

# Reset stuck processing URLs (30min timeout)
python scripts/03_progress_monitor.py --action reset-stuck

# Export failed URLs for manual review
python scripts/03_progress_monitor.py --action export-failed --output failed_urls.csv
```

### Custom Configuration
```python
# Edit config/scraper_config.py
DOMAIN_DELAYS = {
    "your-domain.com": 5,  # Custom delay
    "default": 2
}

MAX_CONCURRENT_REQUESTS = 5  # Reduce for slower systems
BATCH_SIZE = 25             # Smaller batches for testing
```

## 📈 Performance Monitoring

### Key Metrics Tracked
- **Overall Progress**: Success/Failed/Pending counts
- **Success Rate**: Real-time percentage calculation
- **Method Performance**: Bright Data vs ScrapingBee vs Direct
- **Domain Statistics**: Success rates by seed bank
- **Quality Metrics**: Validation scores and HTML sizes

### Dashboard Features
- Live progress bar with percentage
- Method-specific success rates
- Domain performance breakdown
- Quality score averages
- Real-time refresh (30-second intervals)

## 💰 Cost Management

### Infrastructure (Monthly)
- **AWS S3**: ~$5 (500MB storage)
- **AWS Secrets Manager**: ~$1
- **Total Operational**: ~$6/month

### Collection (One-time)
- **Bright Data**: ~$30-50 (primary service)
- **ScrapingBee**: ~$20 (fallback usage)
- **Total Collection**: ~$50-70

### Budget Monitoring
- Bright Data: $133.71 available
- ScrapingBee: 250,000 credits available
- Automatic cost tracking in logs

## 🔍 Troubleshooting

### Common Issues

**Database not found**
```bash
# Run deduplication first
python run_collection.py dedupe
```

**AWS credentials missing**
```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

**High failure rate**
```bash
# Check domain-specific issues
python scripts/03_progress_monitor.py --action dashboard

# Export failed URLs for analysis
python scripts/03_progress_monitor.py --action export-failed
```

**Stuck processing URLs**
```bash
# Reset stuck processes (30min timeout)
python scripts/03_progress_monitor.py --action reset-stuck
```

## 📋 Next Steps

### Phase 3 Integration
1. **Enhanced Data Extraction**: AI-powered strain data parsing
2. **Quality Scoring**: Automated content quality assessment  
3. **API Development**: RESTful access to collected HTML
4. **Commercial Features**: Premium data access tiers

### Scalability Improvements
1. **Kubernetes Deployment**: Container orchestration
2. **Distributed Scraping**: Multi-region collection
3. **ML Failure Prediction**: Intelligent retry strategies
4. **Real-time Updates**: Continuous collection monitoring

## 🤝 Support & Contribution

### Getting Help
- Check `logs/` directory for detailed error messages
- Review `methodology.md` for technical specifications
- Use progress monitor for real-time diagnostics

### Human-AI Partnership
- **System Architecture**: Amazon Q
- **Domain Expertise**: Shannon Goddard
- **Quality Verification**: Shannon Goddard
- **Continuous Improvement**: Collaborative iteration

---

## 🌿 Cannabis Intelligence Ecosystem

This HTML collection system serves as the foundation for the Cannabis Intelligence Database, supporting:

- **Research Phase**: Comprehensive strain data analysis
- **Commercial Phase**: Premium data products and APIs
- **Community Phase**: Open-source cultivation insights
- **Innovation Phase**: AI-powered growing recommendations

**Target Revenue**: $15K (Phase 2) → $75K (Phase 3) → $300K (Phase 4)

---

*Ready to create the world's most comprehensive cannabis strain HTML archive! 🚀*