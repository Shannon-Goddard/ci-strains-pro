# CI-Strains-Pro — Amazon Q Brain

## Project Context
- **Dataset**: 21,282 verified cannabis strains × 51 columns
- **S3 HTML Archive**: 21,706 HTML files from 19 seed banks (source of truth)
- **License**: CC BY 4.0 (data) / MIT (code) — free and open
- **Status**: Dataset complete and published. Validation refinements pending.
- **Tech Stack**: Python, AWS (S3/CloudFront/Lambda/Secrets Manager), Gemini 2.0 Flash, boto3

## Current State (July 2026)
- Pipeline phases 1–18 complete
- Final dataset: `raw-data.csv` (21,282 strains × 51 columns)
- Identity fields 100% human-verified (strain name, breeder, seed bank)
- Lineage coverage: 76.1%
- Botanical data: 88.3% coverage
- S3 HTML validation: 91.8% success (19,475/21,210)
- 691 high-confidence corrections identified, pending apply
- V2 validation script prepared but not yet executed
- Commercial terms removed — data is free under CC BY 4.0

## Infrastructure
- **S3 Bucket**: `ci-strains-html-archive`
  - `/html/` — 20,695 static HTML files
  - `/html_js/` — 1,011 JS-rendered files (ILGM, Seedsman)
  - `/frontend/` — Source of Truth Viewer
- **CloudFront**: `ci-strains-source-of-truth` (EYOCL6B8MFZ7F)
  - Currently serving: strains.loyal9.app
- **Lambda**: `ci-strains-lookup` (Python, URL validation + signed URL generation)
- **Secrets Manager**: CloudFront private key for signed URLs

## Domain Migration (Deferred)
- Current: `strains.loyal9.app`
- Target: `strains.poweredbyci.live`
- 51 references mapped across project files
- Will require: new ACM cert, CloudFront alternate domain, CORS update in Lambda, bulk find-replace in docs
- Separate repo `ci-strains-pro-landing` will serve the grower-facing strain tool

## Pending Work
1. Apply 691 high-confidence corrections from V1 validation
2. Run V2 validation (`validate_s3_html_v2.py`) with improved standardization rules
3. Review 387 low-confidence corrections manually
4. Domain migration (when ready)
5. `.amazonq/brain.md` domain refs will update with bulk sweep

## Data Quality Standards
- Every data point traceable to timestamped HTML archive in S3
- Never overwrite raw data — create cleaned versions
- Encoding: `latin-1` for CSV reads (cannabis breeder characters)
- Triple validation: extraction → AI validation → manual review

## Environment Variables Required
- `GCP_PROJECT_ID` — for Gemini validation scripts in pipeline 17

## Key Files
- `raw-data.csv` — the published dataset
- `DATA_LICENSE.md` — CC BY 4.0 terms
- `log/DAILY_LOG.md` — full build chronicle
- `pipeline/17_gemini_revalidation/scripts/validate_s3_html_v2.py` — next validation to run
- `pipeline/18_full_validation/output/high_confidence_corrections.csv` — pending corrections
