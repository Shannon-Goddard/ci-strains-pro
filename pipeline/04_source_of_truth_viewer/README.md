# Pipeline 04: Source of Truth Viewer 🔒

**Status**: Ready to Build (Jan 16, 2026)  
**Architecture**: S3 + CloudFront + Lambda + API Gateway (Enterprise-Grade)  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## 🎯 Mission

Build a **secure, production-grade HTML viewer** that proves every strain in our database is backed by real, timestamped source data.

**The Pitch**:
> "CI-Strains-Pro: The only cannabis database where you can verify every single data point against the original source. 21,395 strains, 20 seed banks, 100% backed by timestamped HTML archives."

## 🏗 Architecture: Enterprise AWS Stack

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────┐
│  Static Website (CloudFront)    │  ← Frontend HTML/JS
│  - Search interface             │
│  - URL input form               │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  API Gateway (REST API)         │  ← Rate limiting, CORS
│  - /lookup endpoint             │
│  - Request validation           │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  Lambda Function (Python)       │  ← Business logic
│  - Validate URL in inventory    │
│  - Generate signed CloudFront   │
│  - Return time-limited URL      │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  CloudFront Distribution        │  ← Secure delivery
│  - Private origin (S3)          │
│  - Signed URLs (5-min expire)   │
│  - No direct S3 access          │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  S3 Bucket (PRIVATE)            │  ← Source of truth
│  - ci-strains-html-archive      │
│  - 21,706 static HTML files     │
│  - 1,011 JS-rendered files      │
│  - NO public access             │
└─────────────────────────────────┘
```

## 🔒 Security Features

### Tier 1: Access Control
- ✅ **S3 Bucket**: 100% private, zero public access
- ✅ **CloudFront Origin Access Identity (OAI)**: Only CloudFront can access S3
- ✅ **Signed URLs**: Time-limited (5-minute expiration)
- ✅ **Lambda IAM Role**: Minimal permissions (read S3, sign URLs only)

### Tier 2: Rate Limiting & Abuse Prevention
- ✅ **API Gateway Throttling**: 10 requests/second per IP
- ✅ **Lambda Validation**: URL must exist in inventory
- ✅ **CloudFront Geo-Restrictions**: Optional (block specific countries)
- ✅ **WAF (Optional)**: DDoS protection, bot filtering

### Tier 3: View-Only Enforcement
- ✅ **Iframe Sandbox**: Disable downloads, right-click
- ✅ **Content-Security-Policy**: Prevent embedding elsewhere
- ✅ **X-Frame-Options**: Control where viewer can be embedded
- ✅ **Watermark Overlay (Optional)**: Visual "Source of Truth" branding

## 📋 Build Plan (3 Hours)

### Phase 1: CloudFront Setup (45 min)
1. Create CloudFront distribution
   - Origin: S3 bucket (private)
   - Origin Access Identity (OAI)
   - Viewer Protocol Policy: HTTPS only
   - Price Class: Use all edge locations
2. Create CloudFront Key Pair for signed URLs
3. Configure cache behaviors
4. Test signed URL generation

### Phase 2: Lambda Function (45 min)
1. Create Lambda function (Python 3.12)
   - Runtime: Python 3.12
   - Memory: 256 MB
   - Timeout: 10 seconds
2. Install dependencies: `boto3`, `cryptography`
3. Implement logic:
   - Load inventory CSV from S3
   - Validate user-provided URL
   - Generate CloudFront signed URL (5-min expiration)
   - Return JSON response
4. Configure IAM role:
   - Read S3 inventory
   - Sign CloudFront URLs
5. Test with sample URLs

### Phase 3: API Gateway (30 min)
1. Create REST API
2. Create `/lookup` POST endpoint
3. Integrate with Lambda function
4. Configure CORS (allow frontend domain)
5. Enable throttling (10 req/sec)
6. Deploy to production stage
7. Test with Postman/curl

### Phase 4: Frontend Interface (45 min)
1. Create static website (HTML/CSS/JS)
   - URL input form
   - Search by seed bank dropdown
   - Results display in iframe
2. Implement JavaScript:
   - Call API Gateway `/lookup`
   - Display signed URL in sandboxed iframe
   - Handle errors (URL not found, rate limit)
3. Deploy to S3 + CloudFront (separate distribution)
4. Configure custom domain (optional)

### Phase 5: Testing & Documentation (15 min)
1. End-to-end testing
   - Test all 20 seed banks
   - Test static HTML files
   - Test JS-rendered files
   - Test expiration (wait 5 min)
2. Document usage
3. Create demo video/screenshots

## 💰 Cost Breakdown

### Monthly Costs (Estimated)
- **CloudFront**: $1-5/month (depends on traffic)
  - First 1 TB: $0.085/GB
  - Requests: $0.0075 per 10,000
- **Lambda**: ~$0/month (free tier: 1M requests)
- **API Gateway**: ~$0-1/month (free tier: 1M requests)
- **S3 Storage**: $0.50/month (already paying)
- **S3 Requests**: ~$0.10/month

**Total: $2-7/month for enterprise security**

### One-Time Setup
- Domain (optional): $12/year
- SSL Certificate: $0 (AWS Certificate Manager free)

## 📁 Folder Structure

```
pipeline/04_source_of_truth_viewer/
├── README.md                    # This file
├── lambda/
│   ├── lookup_function.py       # Lambda function code
│   ├── requirements.txt         # Python dependencies
│   └── deploy.sh                # Deployment script
├── frontend/
│   ├── index.html               # Main interface
│   ├── styles.css               # Styling
│   ├── app.js                   # Frontend logic
│   └── assets/                  # Images, logos
├── infrastructure/
│   ├── cloudfront_config.json   # CloudFront distribution config
│   ├── api_gateway_config.json  # API Gateway config
│   └── iam_policies.json        # IAM roles and policies
├── docs/
│   ├── SETUP_GUIDE.md           # Step-by-step setup
│   ├── API_DOCUMENTATION.md     # API endpoint docs
│   └── SECURITY_AUDIT.md        # Security review
└── tests/
    ├── test_lambda.py           # Lambda unit tests
    └── test_api.py              # API integration tests
```

## 🚀 Expected Features

### User Experience
1. **Simple Interface**: Paste URL → View HTML
2. **Search by Seed Bank**: Dropdown to browse by bank
3. **Metadata Display**: Show collection date, seed bank, file size
4. **Responsive Design**: Works on mobile/tablet/desktop
5. **Fast Loading**: CloudFront edge caching

### Admin Features (Future)
1. **Usage Analytics**: Track most-viewed strains
2. **Access Logs**: Monitor for abuse
3. **Batch Lookup**: Upload CSV of URLs
4. **API Key System**: For commercial partners

## 🎯 Success Criteria

### Functional
- ✅ User can view any of 21,706 static HTML files
- ✅ User can view any of 1,011 JS-rendered HTML files
- ✅ URLs expire after 5 minutes
- ✅ Invalid URLs return proper error messages
- ✅ Rate limiting prevents abuse

### Security
- ✅ S3 bucket has zero public access
- ✅ Direct S3 URLs don't work
- ✅ Signed URLs can't be reused after expiration
- ✅ Lambda has minimal IAM permissions
- ✅ API Gateway throttling active

### Performance
- ✅ Page load < 2 seconds
- ✅ API response < 500ms
- ✅ CloudFront cache hit ratio > 80%

## 📊 Competitive Advantage

**No other cannabis database has this.**

- Leafly: No source verification
- Wikileaf: No archived HTML
- Seedfinder: No timestamped proof
- AllBud: No transparency

**CI-Strains-Pro**: Every strain backed by immutable, timestamped HTML archives.

## 🔗 Integration Points

### Current Systems
- **S3 Inventory**: `pipeline/03_s3_inventory/s3_html_inventory.csv`
- **JS Inventory**: `pipeline/03_s3_inventory/s3_js_html_inventory.csv`
- **S3 Bucket**: `ci-strains-html-archive`
- **Metadata**: `metadata/{hash}.json`

### Future Integrations
- **Commercial API**: Paid access for partners
- **Bulk Export**: Download multiple HTMLs
- **Comparison Tool**: Side-by-side strain comparison
- **Change Detection**: Track when seed banks update pages

## 📝 Notes for Tomorrow

### Pre-Build Checklist
- [ ] AWS credentials configured
- [ ] CloudFront key pair generated
- [ ] S3 bucket permissions reviewed
- [ ] Inventory CSVs accessible
- [ ] Python 3.12 environment ready

### Build Order
1. Start with Lambda (easiest to test)
2. Then API Gateway (test with Postman)
3. Then CloudFront (test signed URLs)
4. Finally frontend (visual confirmation)

### Testing Strategy
- Test with 1 URL from each seed bank (20 tests)
- Test with ILGM JS-rendered file
- Test with Seedsman JS-rendered file
- Test expiration (wait 5 min, try again)
- Test rate limiting (spam requests)

## 🎉 Why This Matters

This isn't just a viewer - it's **proof of authenticity**.

Every competitor claims they have "accurate data." We can **prove it**.

This is the foundation for:
- Commercial licensing
- API partnerships
- Research collaborations
- Legal defensibility

**Tomorrow we build the most transparent cannabis database on Earth.** 🌿🔒

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

**Ready to build: January 16, 2026** 🚀
