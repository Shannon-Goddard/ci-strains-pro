# Cannabis Intelligence Database - Full Dataset Validation Setup

## Prerequisites

### 1. Python Environment
```bash
# Ensure Python 3.12+ is installed
python --version

# Install required packages
pip install -r requirements.txt
```

### 2. Google Cloud Setup
```bash
# Install Google Cloud CLI
# Download from: https://cloud.google.com/sdk/docs/install

# Authenticate with your Google account
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Configure application default credentials for Vertex AI
gcloud auth application-default login
```

### 3. AWS CLI Setup
```bash
# Install AWS CLI v2
# Download from: https://aws.amazon.com/cli/

# Configure AWS credentials
aws configure

# Test AWS CLI access
aws sts get-caller-identity
```

### 4. AWS Secrets Manager Configuration

Create two secrets in AWS Secrets Manager:

**Secret 1: `cannabis-gemini-api`**
```json
{
  "cannabis-gemini-api": "YOUR_GEMINI_API_KEY"
}
```

**Secret 2: `cannabis-brightdata-api`**
```json
{
  "api_key": "YOUR_BRIGHT_DATA_API_KEY",
  "zone": "cannabis_strain_scraper",
  "customer": "YOUR_CUSTOMER_ID"
}
```

### 5. Bright Data Configuration
- Service: Web Unlocker API
- Zone: cannabis_strain_scraper
- Authentication: Bearer token via API method
- Endpoint: https://api.brightdata.com/request

## Running the Pipeline

### Test Credentials
```bash
python test_secrets.py
```

### Run Pilot Validation (100 strains)
```bash
python scrape_and_judge_pipeline.py
```

### Run Full Dataset Validation
```bash
python scrape_and_judge_pipeline.py --full
```

### Analyze Results
```bash
python analyze_validation_results.py
```

## File Structure
```
04_full_dataset_validation/
├── FULL_DATASET_VALIDATION.md     # Complete documentation
├── scrape_and_judge_pipeline.py   # Main validation pipeline
├── aws_secrets.py                 # AWS Secrets Manager integration
├── analyze_validation_results.py  # Results analysis script
├── test_secrets.py               # Credential testing
├── requirements.txt              # Python dependencies
└── SETUP_INSTRUCTIONS.md         # This file
```

## Expected Outputs
- `Cannabis_Database_Validated.csv` - Enhanced dataset with AI validation
- `scrape_judge_progress.db` - SQLite progress tracking database
- `scrape_judge_pipeline.log` - Detailed processing logs
- `validation_report_YYYYMMDD_HHMMSS.txt` - Summary reports

## Troubleshooting

### Common Issues
1. **AWS Credentials**: Ensure AWS CLI is configured and has access to Secrets Manager
2. **Google Cloud**: Verify Vertex AI is enabled and authenticated
3. **Bright Data**: Check API key and zone configuration
4. **CSV Encoding**: Dataset uses latin-1 encoding for special characters

### Support
- Check logs in `scrape_judge_pipeline.log`
- Review progress in SQLite database
- Verify credentials with `test_secrets.py`