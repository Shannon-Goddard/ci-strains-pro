# Quick Start Guide - Phase 9 Vertex AI Validation

## For Next Chat Session

### What This Phase Does
Validates 21,361 extracted strain names and breeder names using Google Vertex AI (Gemini 2.0 Flash). AI reviews each extraction, corrects errors, and flags low-confidence items for manual review.

### Prerequisites Checklist
- [x] AWS CLI configured with Secrets Manager access
- [x] Google Cloud credentials stored in AWS Secrets Manager (`cannabis_google_cloud_api`)
- [x] Input data ready: `input/all_strains_extracted.csv` (21,361 strains from Phase 8)
- [ ] Python dependencies installed: `pip install pandas boto3 google-cloud-aiplatform`

### Run Validation (Single Command)
```bash
cd pipeline/09_vertex_validation/scripts
python validate_with_vertex.py
```

### Expected Output
1. **Console**: Real-time progress (batch X/428, corrections, flagged items, cost)
2. **File**: `output/all_strains_validated.csv` (main validated dataset)
3. **File**: `output/all_strains_validated_flagged.csv` (low confidence items)
4. **File**: `output/all_strains_validated_report.txt` (summary statistics)

### Expected Results
- **Runtime**: 7-8 minutes
- **Cost**: $0.50-$1.00
- **Corrections**: 400-1,000 strains (~2-5%)
- **Flagged**: 400-1,500 strains (~2-7%)

### After Validation
1. Review `output/all_strains_validated_report.txt` for summary
2. Open `output/all_strains_validated_flagged.csv` for manual review items
3. Spot-check 50-100 random strains in main output
4. Proceed to Phase 10 (lineage extraction)

### Troubleshooting
- **Error: "Failed to retrieve Google Cloud credentials"**
  - Run: `aws secretsmanager get-secret-value --secret-id cannabis_google_cloud_api --region us-east-1`
  - Verify JSON response contains `project_id` field

- **Error: "Invalid JSON response from Gemini"**
  - Script retries automatically
  - Check console logs for specific batch that failed
  - Re-run script (it will skip already-processed batches)

- **Error: "Rate limit exceeded"**
  - Increase delay in script: `time.sleep(2)` instead of `time.sleep(1)`
  - Reduce batch size: `BATCH_SIZE = 25` instead of `50`

### Configuration Options
Edit `validate_with_vertex.py` to adjust:
- `BATCH_SIZE = 50` - Strains per API call (lower = slower but safer)
- `CONFIDENCE_THRESHOLD = 90` - Flag items below this score (higher = more flagged)

### Files Created
```
pipeline/09_vertex_validation/
├── input/
│   └── all_strains_extracted.csv (21,361 strains)
├── output/
│   ├── all_strains_validated.csv (TO BE CREATED)
│   ├── all_strains_validated_flagged.csv (TO BE CREATED)
│   └── all_strains_validated_report.txt (TO BE CREATED)
├── scripts/
│   └── validate_with_vertex.py (READY TO RUN)
├── docs/
│   ├── VALIDATION_LOGIC.md (AI prompt documentation)
│   └── QUICK_START.md (this file)
├── methodology.md (transparency log)
└── README.md (comprehensive documentation)
```

### Success Criteria
- ✅ All 21,361 strains processed (100% completeness)
- ✅ Validation confidence scores assigned
- ✅ Corrections made where needed
- ✅ Low-confidence items flagged for review
- ✅ Cost < $2

### Next Phase Preview
**Phase 10: Lineage Extraction**
- Extract parent strains from HTML descriptions
- Parse genetics information (Indica/Sativa percentages)
- Build strain family trees
- Identify breeding lineages

---

**Ready to run. Just execute the script and review results.**

**Logic designed by Amazon Q, verified by Shannon Goddard.**
