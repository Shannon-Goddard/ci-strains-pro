# Quick Start Deployment Guide

**Total Time: ~2 hours**  
**Cost: ~$1.41/month**

---

## 🎯 What You're Building

A secure web app that lets users view any of 21,706 archived HTML files via time-limited signed URLs. No one can access the HTML files directly - they must go through your API.

---

## 📋 Deployment Steps

### Step 1: CloudFront Setup (30 min)

Follow: `infrastructure/cloudfront_setup.md`

**You'll get:**
- CloudFront Distribution Domain: `d1234567890abc.cloudfront.net`
- CloudFront Key Pair ID: `APKA1234567890ABC`
- CloudFront Private Key: (contents of `.pem` file)

---

### Step 2: Lambda Setup (30 min)

Follow: `infrastructure/api_gateway_setup.md` (Steps 1-5)

**You'll create:**
- Lambda function: `ci-strains-lookup`
- Runtime: Python 3.12
- Environment variables configured
- IAM role with S3 read permissions

**Quick Deploy (from `lambda/` directory):**
```bash
pip install -r requirements.txt -t package/
cd package && zip -r ../lambda_deployment.zip . && cd ..
zip -g lambda_deployment.zip lookup_function.py
aws lambda update-function-code --function-name ci-strains-lookup --zip-file fileb://lambda_deployment.zip --region us-east-1
```

---

### Step 3: API Gateway Setup (30 min)

Follow: `infrastructure/api_gateway_setup.md` (Steps 6-12)

**You'll get:**
- API Endpoint: `https://abc123.execute-api.us-east-1.amazonaws.com/prod/lookup`

**Test with curl:**
```bash
curl -X POST https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/lookup \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.northatlanticseed.com/product/og-kush-f-3/"}'
```

---

### Step 4: Frontend Setup (15 min)

1. Open `frontend/app.js`
2. Update line 2 with your API endpoint:
   ```javascript
   const API_ENDPOINT = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/lookup';
   ```
3. Open `frontend/index.html` in browser
4. Test with sample URL

**Optional: Deploy to S3 + CloudFront**
```bash
aws s3 sync frontend/ s3://ci-strains-viewer/ --acl public-read
```

---

## 🧪 Testing Checklist

### Test URLs (one from each major seed bank):

**Static HTML:**
- North Atlantic: `https://www.northatlanticseed.com/product/og-kush-f-3/`
- Crop King: `https://www.cropkingseeds.com/feminized-seeds/bear-claw-feminized-seeds/`
- Neptune: `https://neptuneseedbank.com/product/super-boof-belts-strain/`

**JS-Rendered:**
- Seedsman: `https://www.seedsman.com/us-en/platinum-green-apple-candy-feminized-seeds-atl-pgac-fem`
- ILGM: `https://ilgm.com/products/critical-mass-feminized-seeds`

### Expected Results:
- ✅ Valid URL returns signed URL + metadata
- ✅ Invalid URL returns 404 error
- ✅ Signed URL loads HTML in iframe
- ✅ Countdown timer shows expiration
- ✅ After 5 minutes, URL fails to load

---

## 🔧 Troubleshooting

### Lambda returns 500 error
- Check CloudWatch Logs for Lambda function
- Verify environment variables are set correctly
- Verify IAM role has S3 read permissions

### CloudFront returns 403 Forbidden
- Verify OAI is configured correctly
- Check S3 bucket policy allows OAI
- Verify signed URL generation logic

### API Gateway returns CORS error
- Verify CORS is enabled on /lookup resource
- Check Access-Control-Allow-Origin header
- Verify OPTIONS method exists

### Frontend doesn't load HTML
- Check browser console for errors
- Verify API endpoint is correct in app.js
- Test API endpoint with curl first

---

## 📊 Success Metrics

**Functional:**
- ✅ 21,706 HTML files accessible via signed URLs
- ✅ URLs expire after 5 minutes
- ✅ Rate limiting prevents abuse (10 req/sec)

**Security:**
- ✅ S3 bucket has zero public access
- ✅ Direct S3 URLs don't work
- ✅ Signed URLs can't be reused after expiration

**Performance:**
- ✅ API response < 500ms
- ✅ HTML loads in < 2 seconds
- ✅ CloudFront cache hit ratio > 80%

---

## 💰 Cost Breakdown

**Monthly (10K requests):**
- CloudFront: $0.86
- Lambda: $0.00 (free tier)
- API Gateway: $0.04
- S3: $0.51
- **Total: $1.41/month**

**One-Time Setup:**
- Time: 2 hours
- AWS charges: $0 (free tier)

---

## 🚀 Next Steps After Deployment

1. **Test with all 20 seed banks** (verify coverage)
2. **Monitor CloudWatch Logs** (check for errors)
3. **Track API Gateway metrics** (requests, latency, errors)
4. **Document any issues** (for future improvements)
5. **Share demo** (prove the system works)

---

**Ready to deploy. Let's make Phase 4 legendary.** 🔒🌿
