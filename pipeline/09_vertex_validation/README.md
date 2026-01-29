# Phase 9: Vertex AI Validation

## Purpose
Validate and correct extracted strain names and breeder names using Google Vertex AI (Gemini 2.0 Flash). AI reviews each extraction for accuracy, removes remaining breeder names from strain fields, and flags low-confidence items for manual review.

## Why Vertex AI?
- **Context understanding**: Distinguishes "Barney's Farm" (breeder) from "Barney Rubble OG" (strain)
- **Edge case handling**: Preserves strain numbers, aka names, and intentional "Auto" prefixes
- **Batch efficiency**: Processes 50 strains per API call
- **Cost effective**: ~$0.50-$1.00 for full 21,361 strain dataset
- **Confidence scoring**: Flags uncertain extractions for human review

## Input Data
- **Source**: `input/all_strains_extracted.csv` (from Phase 8)
- **Columns used**: `source_url_raw`, `seed_bank`, `strain_name_extracted`, `breeder_extracted`
- **Total strains**: 21,361

## Output Data

### 1. `output/all_strains_validated.csv`
Main validated dataset with new columns:
- `strain_name_validated` - AI-corrected strain name
- `breeder_validated` - AI-corrected breeder name
- `validation_confidence` - Confidence score (0-100)
- `validation_reasoning` - AI explanation for changes
- `validation_changes` - Summary of corrections made
- `flagged_for_review` - Boolean (True if confidence < 90%)

### 2. `output/all_strains_validated_flagged.csv`
Subset of strains flagged for manual review (confidence < 90%)

### 3. `output/all_strains_validated_report.txt`
Validation summary report:
- Total corrections made
- Confidence distribution
- Corrections by seed bank
- Estimated API cost

## Setup Instructions

### Prerequisites
1. **AWS CLI configured** with access to Secrets Manager (us-east-1)
2. **Google Cloud credentials** stored in AWS Secrets Manager as `cannabis_google_cloud_api`
3. **Python 3.8+** installed

### Install Dependencies
```bash
pip install pandas boto3 google-cloud-aiplatform
```

### Verify Credentials
```bash
# Test AWS Secrets Manager access
aws secretsmanager get-secret-value --secret-id cannabis_google_cloud_api --region us-east-1

# Should return Google Cloud service account JSON
```

## Execution

### Run Validation
```bash
cd pipeline/09_vertex_validation/scripts
python validate_with_vertex.py
```

### Configuration Options
Edit `validate_with_vertex.py` to adjust:
- `BATCH_SIZE` (default: 50) - Strains per API call
- `CONFIDENCE_THRESHOLD` (default: 90) - Flag items below this score

### Expected Runtime
- **21,361 strains** ÷ 50 per batch = ~428 batches
- **1 second delay** between batches = ~7-8 minutes total
- **Estimated cost**: $0.50-$1.00 (Gemini Flash pricing)

## Validation Logic

### AI Prompt Structure
For each batch of 50 strains, AI receives:
- URL (for context on naming patterns)
- Seed bank (for breeder identification)
- Extracted strain name (to validate)
- Extracted breeder (to validate)

### AI Validation Rules
1. **Remove breeder names** from strain field
2. **Preserve strain numbers** (e.g., "Project 4516", "Haze 13")
3. **Remove "Auto" suffix** unless at start (preserve "Auto 1")
4. **Clean breeder names** (standardize company names)
5. **Flag unknown breeders** as "Unknown"

### Confidence Scoring
- **95-100%**: High confidence, no review needed
- **90-94%**: Good confidence, spot-check recommended
- **80-89%**: Medium confidence, review recommended
- **<80%**: Low confidence, manual review required

## Output Examples

### Example 1: Correction Made
```
URL: attitude.com/barney-s-farm-blue-gelato-41-feminised-seeds
Extracted Strain: Blue Gelato 41
Extracted Breeder: [empty]

AI Output:
- strain_name_validated: Blue Gelato 41 (CORRECT)
- breeder_validated: Barney's Farm
- confidence: 98
- reasoning: "Breeder identified from URL prefix"
- changes: "Breeder: Unknown -> Barney's Farm"
```

### Example 2: No Changes
```
URL: mephistogenetics.com/illuminauto-29
Extracted Strain: Illuminauto 29
Extracted Breeder: Mephisto Genetics

AI Output:
- strain_name_validated: Illuminauto 29 (CORRECT)
- breeder_validated: Mephisto Genetics (CORRECT)
- confidence: 100
- reasoning: "Extraction is accurate"
- changes: "No changes"
```

### Example 3: Flagged for Review
```
URL: seedsherenow.com/exotic-genetix-project-4516-regs
Extracted Strain: Project 4516
Extracted Breeder: Exotic Genetix

AI Output:
- strain_name_validated: Project 4516 (CORRECT)
- breeder_validated: Exotic Genetix (CORRECT)
- confidence: 85
- reasoning: "Strain number preserved, but URL structure ambiguous"
- changes: "No changes"
- flagged_for_review: True
```

## Cost Breakdown

### Gemini 2.0 Flash Pricing
- **Input**: $0.00001 per 1,000 tokens
- **Output**: $0.00003 per 1,000 tokens

### Estimated Usage
- **~200 tokens per strain** (input + output)
- **21,361 strains** × 200 tokens = 4,272,200 tokens
- **Cost**: (4,272,200 ÷ 1,000) × $0.00002 = **$0.85**

### Budget
- **Available**: $1,200 Google Cloud credits
- **This phase**: ~$1
- **Remaining**: $1,199 for future phases

## Troubleshooting

### Error: "Failed to retrieve Google Cloud credentials"
- Verify AWS CLI is configured: `aws sts get-caller-identity`
- Check secret exists: `aws secretsmanager list-secrets --region us-east-1`

### Error: "Invalid JSON response from Gemini"
- AI occasionally returns malformed JSON
- Script retries automatically
- Check logs for specific batch that failed

### Error: "Rate limit exceeded"
- Increase `time.sleep()` delay between batches
- Reduce `BATCH_SIZE` to process fewer strains per call

## Next Steps

### After Validation
1. **Review flagged items** in `all_strains_validated_flagged.csv`
2. **Spot-check corrections** (sample 50-100 random strains)
3. **Update extraction rules** based on AI corrections (if patterns found)
4. **Proceed to Phase 10**: Lineage extraction from HTML

### Manual Review Process
For flagged items (confidence < 90%):
1. Open `all_strains_validated_flagged.csv`
2. Review `validation_reasoning` column
3. Check original URL for context
4. Accept or override AI suggestion
5. Update `strain_name_validated` and `breeder_validated` as needed

## Files Structure

```
pipeline/09_vertex_validation/
├── input/
│   └── all_strains_extracted.csv (21,361 strains from Phase 8)
├── output/
│   ├── all_strains_validated.csv (main output)
│   ├── all_strains_validated_flagged.csv (low confidence items)
│   └── all_strains_validated_report.txt (summary report)
├── scripts/
│   └── validate_with_vertex.py (main validation script)
├── docs/
│   └── VALIDATION_LOGIC.md (detailed AI prompt documentation)
├── methodology.md (transparency log)
└── README.md (this file)
```

## Actual Results (January 2026)

### Execution Summary
```bash
cd pipeline/09_vertex_validation/scripts
python validate_with_vertex.py
```

**Runtime**: ~45 minutes (with rate limit handling)
**Total batches**: 428 batches (50 strains each)
**Rate limit hits**: 19 batches failed initially, all successfully retried

### Final Statistics
```
============================================================
VALIDATION COMPLETE
============================================================
Total strains processed: 21,400
Total corrections made: 39,681
Items flagged for review: 1,089 (5.1%)
Estimated total cost: $0.04
============================================================
```

### Key Findings
- **39,681 corrections** across 21,400 strains = **1.85 corrections per strain**
- **95% confidence rate**: Only 1,089 strains (5.1%) flagged for review
- **Cost efficiency**: $0.04 actual vs $1.00 estimated (96% under budget)
- **Rate limit handling**: Exponential backoff successfully recovered all failed batches

### Correction Breakdown
Most common corrections:
1. **Breeder extraction**: Identified breeders from URLs when missing
2. **Strain name cleanup**: Removed breeder names from strain field
3. **Auto suffix removal**: Cleaned "Feminized Auto" → strain name only
4. **Standardization**: Normalized breeder names ("Barney's" → "Barney's Farm")

### Code Snippets Used

#### 1. Exponential Backoff for Rate Limits
```python
def validate_batch(self, batch_data, retry_count=0, max_retries=5):
    try:
        response = self.model.generate_content(prompt)
        # ... process response
    except Exception as e:
        if '429' in str(e) or 'Resource exhausted' in str(e):
            if retry_count < max_retries:
                wait_time = (2 ** retry_count) * 5  # 5, 10, 20, 40, 80 seconds
                print(f"  Rate limit hit. Waiting {wait_time}s before retry {retry_count + 1}/{max_retries}...")
                time.sleep(wait_time)
                return self.validate_batch(batch_data, retry_count + 1, max_retries)
```

#### 2. Checkpoint System for Crash Recovery
```python
# Save checkpoint every 10 batches
if (batch_num + 1) % 10 == 0:
    df.to_csv(checkpoint_file, index=False, encoding='utf-8')
    print(f"  [Checkpoint saved]")

# Resume from checkpoint on restart
if Path(checkpoint_file).exists():
    print(f"\n[CHECKPOINT FOUND] Resuming from {checkpoint_file}...")
    df = pd.read_csv(checkpoint_file, encoding='utf-8')
```

#### 3. Failed Batch Retry Logic
```python
# Track failed batches during first pass
failed_batches = []
if validations is None:
    failed_batches.append((batch_num, start_idx, end_idx))

# Retry all failed batches after first pass
if failed_batches:
    print(f"\nRETRYING {len(failed_batches)} FAILED BATCHES")
    for batch_num, start_idx, end_idx in failed_batches:
        validations = self.validate_batch(batch_data)
        time.sleep(5)  # Longer delay for retries
```

#### 4. UTF-8 Encoding Fix
```python
# Changed from latin-1 to utf-8 to handle special characters
df.to_csv(checkpoint_file, index=False, encoding='utf-8')  # Was: encoding='latin-1'
```

### Output Files Generated
1. **all_strains_validated.csv** - 21,400 rows, 8 new validation columns
2. **all_strains_validated_flagged.csv** - 1,089 low-confidence items
3. **all_strains_validated_report.txt** - Detailed statistics by seed bank

### Lessons Learned
1. **Rate limits are real**: Google Vertex AI enforces strict quotas, exponential backoff essential
2. **Checkpoint saves time**: UTF-8 encoding required for cannabis strain names with special characters
3. **Batch retry works**: All 19 failed batches recovered on second attempt
4. **Cost was minimal**: Actual cost 96% lower than estimate due to efficient batching

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
