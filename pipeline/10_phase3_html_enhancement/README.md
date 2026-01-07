# Phase 3 HTML Enhancement Pipeline 🌿

**Transform 14,075 HTML files into strategic data enhancements**

Logic designed by Amazon Q, verified by Shannon Goddard.

---

## Overview

The Phase 3 HTML Enhancement Pipeline adds 8 strategic columns and fills critical gaps in your comprehensive cannabis strain dataset using 14,075 collected HTML files from S3.

### Key Features
- ✅ **8 Strategic Columns Added**: Enhancement metadata and quality scores
- ✅ **Gap Filling**: THC/CBD ranges, terpene profiles, growing information
- ✅ **Quality Assurance**: Confidence scoring and data validation
- ✅ **Comprehensive Logging**: Full audit trail and error tracking
- ✅ **Data Integrity**: Never overwrites existing data

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials
Ensure your AWS credentials are configured for S3 access:
```bash
aws configure
# or set environment variables:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
```

### 3. Run Tests (Recommended)
```bash
python test_pipeline.py
```

### 4. Execute Enhancement Pipeline
```bash
python phase3_html_enhancer.py
```

---

## Strategic Enhancements

### 8 Strategic Columns Added

| Column | Type | Description |
|--------|------|-------------|
| `html_enhanced` | Boolean | Whether strain was enhanced with HTML data |
| `enhancement_confidence` | Float (0.0-1.0) | Quality confidence score |
| `enhancement_timestamp` | ISO DateTime | When enhancement was performed |
| `data_completeness_score` | Float (0.0-1.0) | Overall data completeness |

### Data Gap Filling

| Target Area | Columns Enhanced | Expected Fill Rate |
|-------------|------------------|-------------------|
| **Cannabinoids** | `thc_min/max`, `cbd_min/max` | 70%+ |
| **Terpenes** | `terpenes` | 60%+ |
| **Effects** | `effects` | 80%+ |
| **Flavors** | `flavors` | 80%+ |
| **Growing Info** | `flowering_day_min/max`, `grow_difficulty` | 75%+ |
| **Genetics** | `lineage` | 50%+ |

---

## File Structure

```
10_phase3_html_enhancement/
├── phase3_html_enhancer.py    # Main enhancement pipeline
├── config.py                  # Configuration settings
├── test_pipeline.py           # Test suite
├── methodology.md             # Detailed methodology
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## Processing Flow

### 1. Data Loading
- Loads `revert_manual_review_cleaning.csv`
- Identifies strains with `source_of_truth = True`
- Initializes S3 client for HTML retrieval

### 2. HTML Processing
- Retrieves HTML files from S3 using URL hash
- Applies 15+ regex patterns for data extraction
- Validates extracted data against quality thresholds

### 3. Enhancement Logic
- **Priority 1**: Fill missing cannabinoid data (THC/CBD)
- **Priority 2**: Add terpene profiles to empty columns
- **Priority 3**: Enhance effects and flavors
- **Priority 4**: Complete growing information
- **Priority 5**: Add genetic lineage

### 4. Quality Assurance
- Calculates confidence scores (0.0-1.0)
- Validates data ranges and formats
- Tracks enhancement statistics

### 5. Output Generation
- Enhanced dataset: `cannabis_database_phase3_enhanced.csv`
- Enhancement report: `phase3_enhancement_report.md`
- Processing log: `phase3_enhancement.log`

---

## Configuration

### AWS S3 Settings
```python
S3_CONFIG = {
    'bucket_name': 'ci-strains-html-archive',
    'html_prefix': 'html_files/',
    'region': 'us-east-1'
}
```

### Data Validation Thresholds
```python
VALIDATION_THRESHOLDS = {
    'thc_min': 0.0, 'thc_max': 40.0,
    'cbd_min': 0.0, 'cbd_max': 30.0,
    'flowering_min_days': 30, 'flowering_max_days': 120,
    'confidence_threshold': 0.8
}
```

---

## Expected Results

### Data Completeness Improvements
- **Overall Completeness**: Increase from ~65% to >85% per strain
- **THC/CBD Coverage**: Fill 70%+ of missing cannabinoid ranges
- **Terpene Profiles**: Add detailed terpenes for 60%+ of strains
- **Growing Information**: Complete 75%+ of missing flowering times

### Quality Metrics
- **Enhancement Coverage**: 14,075 strains with HTML sources (90.8%)
- **Average Confidence**: >0.8 for extracted data
- **Processing Success Rate**: >95% completion rate
- **New Data Points**: 5,000+ terpene profiles, 3,000+ cannabinoid ranges

---

## Output Files

### 1. Enhanced Dataset
**File**: `cannabis_database_phase3_enhanced.csv`
- Original 39 columns + 4 strategic enhancement columns
- Enhanced data in existing columns (never overwrites)
- UTF-8 encoding for international characters

### 2. Enhancement Report
**File**: `phase3_enhancement_report.md`
- Comprehensive before/after analysis
- Enhancement statistics by category
- Quality metrics and confidence distributions
- Data completeness improvements

### 3. Processing Log
**File**: `phase3_enhancement.log`
- Detailed processing information
- Error tracking and debugging data
- Performance metrics and timing

---

## Error Handling

### Graceful Degradation
- **S3 Retrieval Failures**: Continues processing, logs errors
- **HTML Parsing Errors**: Preserves original data, tracks failures
- **Data Validation Failures**: Applies confidence penalties, continues

### Data Integrity
- **Never Overwrites**: Only fills missing values
- **Audit Trail**: Complete enhancement tracking
- **Reversibility**: Original data always preserved

---

## Performance

### Processing Capacity
- **Dataset Size**: Handles 15,000+ strain records
- **Processing Speed**: ~100 strains per minute
- **Memory Usage**: Optimized for large datasets
- **S3 Efficiency**: Connection pooling and retry logic

### Monitoring
- Progress logging every 100 records
- Real-time statistics tracking
- Error rate monitoring
- Performance metrics collection

---

## Troubleshooting

### Common Issues

1. **AWS Credentials Not Configured**
   ```bash
   aws configure
   # or set environment variables
   ```

2. **S3 Access Denied**
   - Verify bucket permissions
   - Check IAM role/policy
   - Confirm bucket name in config

3. **Memory Issues with Large Datasets**
   - Reduce batch size in config
   - Monitor system memory usage
   - Consider processing in chunks

4. **Low Enhancement Success Rate**
   - Check HTML file availability in S3
   - Verify URL hash generation
   - Review extraction patterns

### Debug Mode
Enable detailed logging:
```python
logging.getLogger().setLevel(logging.DEBUG)
```

---

## Success Criteria

- [ ] Process 100% of strains with HTML sources (14,075 records)
- [ ] Achieve >85% overall data completeness per strain
- [ ] Fill >70% of missing THC/CBD ranges
- [ ] Add detailed terpene profiles for >60% of strains
- [ ] Maintain >0.8 average confidence score
- [ ] Generate comprehensive enhancement analytics

---

## Support

For issues or questions:
1. Check the processing log: `phase3_enhancement.log`
2. Review the methodology: `methodology.md`
3. Run the test suite: `python test_pipeline.py`
4. Verify AWS S3 access and permissions

---

**🌿 Ready to maximize the value of your comprehensive cannabis strain database using 14,075 HTML sources.**

*Logic designed by Amazon Q, verified by Shannon Goddard.*