# Methodology: Source of Truth Viewer

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Project Overview

The Source of Truth Viewer is a secure, production-grade web application that provides time-limited access to 21,706 archived HTML files representing cannabis strain data from 20 seed banks. This system proves the authenticity and provenance of every strain in the CI Strains Pro database.

---

## Architecture Design

### Core Principle: Zero Trust Security

Every component follows the principle of least privilege:
- S3 bucket is 100% private (no public access)
- CloudFront requires signed URLs (5-minute expiration)
- Lambda has read-only access to inventory files
- API Gateway enforces rate limiting (10 req/sec)

### Technology Stack

**Backend:**
- AWS Lambda (Python 3.12) - Serverless compute
- AWS S3 - Private HTML archive storage
- AWS CloudFront - Secure content delivery with signed URLs
- AWS API Gateway - REST API with throttling

**Frontend:**
- Vanilla HTML/CSS/JavaScript (no frameworks)
- Sandboxed iframe for HTML rendering
- Client-side expiration countdown

---

## Implementation Logic

### 1. Lambda Function Design

**Purpose**: Validate URL exists in inventory and generate time-limited signed URL.

**Key Decisions:**
- Load both inventories (main + JS) into memory on cold start
- Use CloudFront signed URLs instead of S3 presigned URLs (better caching, edge delivery)
- 5-minute expiration balances security with user experience
- Return metadata (seed bank, collection date) for transparency

**Security Considerations:**
- No direct S3 access from frontend
- URL validation prevents unauthorized file access
- Signed URLs can't be shared or reused after expiration
- Lambda has minimal IAM permissions (read inventory only)

### 2. CloudFront Configuration

**Purpose**: Secure delivery of HTML archives via edge locations.

**Key Decisions:**
- Origin Access Identity (OAI) prevents direct S3 access
- HTTPS-only (redirect HTTP to HTTPS)
- Signed URLs required (no public access)
- Legacy key pairs used (simpler than trusted key groups for MVP)

**Why CloudFront over S3 Presigned URLs:**
- Global edge locations (faster delivery)
- Better caching (reduces S3 requests)
- More granular access control
- Professional appearance (custom domain support)

### 3. API Gateway Design

**Purpose**: REST endpoint with rate limiting and CORS.

**Key Decisions:**
- POST method (URL in request body, not query string)
- Lambda proxy integration (simplifies response handling)
- 10 req/sec throttling (prevents abuse)
- CORS enabled (allows frontend to call API)

**Why API Gateway over Lambda Function URL:**
- Built-in throttling and rate limiting
- Request/response transformation
- API versioning support
- Better monitoring and logging

### 4. Frontend Design

**Purpose**: Minimal, clean interface for URL lookup.

**Key Decisions:**
- No JavaScript frameworks (reduces complexity, faster load)
- Sandboxed iframe (prevents malicious HTML from affecting parent page)
- Client-side countdown timer (visual feedback on expiration)
- Gradient design (professional, modern aesthetic)

**Security Considerations:**
- Iframe sandbox attribute prevents downloads, popups
- URL validation before API call
- Error handling for expired URLs
- No sensitive data stored in browser

---

## Data Flow

1. **User enters URL** → Frontend validates format
2. **Frontend calls API Gateway** → POST request with URL
3. **API Gateway invokes Lambda** → Passes request body
4. **Lambda loads inventories** → From S3 (cached on warm start)
5. **Lambda validates URL** → Checks if exists in inventory
6. **Lambda generates signed URL** → CloudFront signed URL (5-min expiration)
7. **Lambda returns response** → Signed URL + metadata
8. **Frontend displays HTML** → Loads in sandboxed iframe
9. **Countdown timer starts** → Visual feedback on expiration
10. **URL expires after 5 minutes** → User must request new URL

---

## Security Model

### Layer 1: S3 Bucket
- Block all public access enabled
- Only CloudFront OAI can read objects
- Direct S3 URLs return 403 Forbidden

### Layer 2: CloudFront
- Signed URLs required (no public access)
- 5-minute expiration (time-limited access)
- HTTPS-only (encrypted in transit)

### Layer 3: Lambda
- Read-only access to inventory files
- No write permissions to S3
- Validates URL before generating signed URL

### Layer 4: API Gateway
- Rate limiting (10 req/sec per IP)
- CORS configured (prevents unauthorized domains)
- Request validation (requires URL parameter)

### Layer 5: Frontend
- Sandboxed iframe (prevents malicious HTML)
- Client-side validation (reduces invalid API calls)
- No sensitive data stored locally

---

## Cost Optimization

### Monthly Costs (Estimated for 10K requests/month)

**CloudFront:**
- Data transfer: ~$0.85 (10 GB @ $0.085/GB)
- Requests: ~$0.01 (10K @ $0.0075 per 10K)

**Lambda:**
- Compute: ~$0.00 (free tier: 1M requests, 400K GB-seconds)
- Requests: ~$0.00 (free tier: 1M requests)

**API Gateway:**
- Requests: ~$0.04 (10K @ $3.50 per million)

**S3:**
- Storage: ~$0.50 (already paying)
- Requests: ~$0.01 (10K GET @ $0.0004 per 1K)

**Total: ~$1.41/month** for enterprise-grade security

---

## Testing Strategy

### Unit Tests (Lambda)
- Test inventory loading from S3
- Test URL validation (exists vs. not exists)
- Test signed URL generation
- Test error handling (missing env vars, S3 errors)

### Integration Tests (API Gateway)
- Test POST request with valid URL
- Test POST request with invalid URL
- Test rate limiting (exceed 10 req/sec)
- Test CORS headers

### End-to-End Tests (Frontend)
- Test URL lookup for each seed bank (20 tests)
- Test JS-rendered files (ILGM, Seedsman)
- Test expiration (wait 5 minutes, verify URL fails)
- Test error handling (404, 500, rate limit)

---

## Deployment Checklist

### CloudFront Setup
- ✅ Create Origin Access Identity (OAI)
- ✅ Update S3 bucket policy (allow OAI)
- ✅ Create CloudFront distribution
- ✅ Generate CloudFront key pair
- ✅ Test signed URL generation

### Lambda Setup
- ✅ Create Lambda function (Python 3.12)
- ✅ Upload deployment package (code + dependencies)
- ✅ Configure environment variables
- ✅ Update IAM role (S3 read permissions)
- ✅ Test with sample URLs

### API Gateway Setup
- ✅ Create REST API
- ✅ Create /lookup resource
- ✅ Create POST method
- ✅ Enable CORS
- ✅ Configure throttling
- ✅ Deploy to production stage

### Frontend Setup
- ✅ Update API endpoint in app.js
- ✅ Deploy to S3 + CloudFront (or local hosting)
- ✅ Test end-to-end flow
- ✅ Verify expiration countdown

---

## Future Enhancements

### Phase 1 (MVP) - Current
- Basic URL lookup
- 5-minute signed URLs
- Sandboxed iframe viewer

### Phase 2 (Planned)
- Search by seed bank dropdown
- Batch URL lookup (CSV upload)
- Usage analytics dashboard
- Custom domain (ci-strains.pro)

### Phase 3 (Future)
- API key system for commercial partners
- Webhook notifications for new strains
- Change detection (track seed bank updates)
- Side-by-side strain comparison

---

## Lessons Learned

### What Worked Well
- CloudFront signed URLs (better than S3 presigned URLs)
- Lambda proxy integration (simplified API Gateway setup)
- Minimal frontend (no framework overhead)
- Sandboxed iframe (security without complexity)

### What Could Be Improved
- Inventory loading on every cold start (could use DynamoDB for faster lookups)
- No caching of inventory in Lambda (could use global variable)
- Manual CloudFront key pair management (could use Secrets Manager)

### Why This Approach
- **Simplicity**: Minimal moving parts, easy to debug
- **Security**: Zero trust, least privilege, time-limited access
- **Cost**: ~$1.41/month for enterprise-grade infrastructure
- **Scalability**: Serverless, auto-scales to demand
- **Transparency**: Every strain backed by immutable HTML archive

---

## Attribution

**Architecture & Implementation**: Amazon Q  
**Verification & Deployment**: Shannon Goddard  
**Project Vision**: Shannon Goddard  
**Funding**: Shannon Goddard ($101.01 invested over 13 days)

---

**This is not AI-generated. This is AI-accelerated, human-directed, and human-verified.**

The AI provided the code. The human provided the vision, the grind, and the coffee budget.

🌿 Built in public. Verified in production. Backed by timestamped HTML archives.
