# Squarespace DNS Setup for strains.loyal9.app

**Goal**: Point `strains.loyal9.app` subdomain to CloudFront distribution

---

## Step 1: Get CloudFront Distribution Domain

After creating your CloudFront distribution, you'll get a domain like:
```
d1234abcd5678.cloudfront.net
```

**Where to find it**:
1. Go to AWS Console → CloudFront
2. Click on your distribution
3. Copy the "Distribution domain name"

---

## Step 2: Add CNAME Record in Squarespace

1. **Log in to Squarespace**
   - Go to https://account.squarespace.com/
   - Navigate to your `loyal9.app` domain settings

2. **Open DNS Settings**
   - Click "Advanced DNS Settings" or "DNS Settings"
   - Look for "Custom Records" section

3. **Add CNAME Record**
   ```
   Type:  CNAME
   Host:  strains
   Data:  d1234abcd5678.cloudfront.net
   TTL:   3600 (or default)
   ```

   **Important**: 
   - Host is `strains` (NOT `strains.loyal9.app`)
   - Data is your CloudFront domain (NOT the full URL with https://)

4. **Save Changes**
   - DNS propagation takes 5-60 minutes

---

## Step 3: Add Alternate Domain Name in CloudFront

1. **Go to CloudFront Distribution Settings**
   - AWS Console → CloudFront → Your Distribution → Edit

2. **Add Alternate Domain Name (CNAME)**
   - Click "Edit" on General settings
   - Under "Alternate domain names (CNAMEs)", add:
     ```
     strains.loyal9.app
     ```

3. **Request SSL Certificate (if not already done)**
   - Click "Request certificate" (opens AWS Certificate Manager)
   - Request a public certificate for `strains.loyal9.app`
   - Choose DNS validation
   - Add the CNAME record ACM provides to Squarespace DNS
   - Wait for validation (5-30 minutes)

4. **Select SSL Certificate**
   - Back in CloudFront settings, select your validated certificate
   - Save changes

---

## Step 4: Update CORS in API Gateway

Your API Gateway needs to allow requests from `strains.loyal9.app`:

1. **Go to API Gateway Console**
   - Select your API → Resources → /lookup → POST

2. **Enable CORS**
   - Actions → Enable CORS
   - Add to "Access-Control-Allow-Origin":
     ```
     https://strains.loyal9.app
     ```

3. **Deploy API**
   - Actions → Deploy API → Select stage (prod)

---

## Step 5: Update Frontend Configuration

Update `frontend/app.js` with your API endpoint:

```javascript
const API_ENDPOINT = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/lookup';
```

Replace `YOUR_API_ID` with your actual API Gateway ID.

---

## Step 6: Test the Setup

1. **Wait for DNS propagation** (5-60 minutes)

2. **Test DNS resolution**:
   ```bash
   nslookup strains.loyal9.app
   ```
   Should return CloudFront IP addresses.

3. **Test HTTPS**:
   - Visit https://strains.loyal9.app
   - Should load without SSL warnings

4. **Test functionality**:
   - Enter a strain URL
   - Click "View Source"
   - Verify HTML loads in iframe

---

## Troubleshooting

### DNS not resolving
- **Wait longer**: DNS can take up to 24 hours (usually 5-60 min)
- **Check CNAME**: Make sure host is `strains` not `strains.loyal9.app`
- **Clear DNS cache**: `ipconfig /flushdns` (Windows) or `sudo dscacheutil -flushcache` (Mac)

### SSL certificate error
- **Verify certificate**: Must be for `strains.loyal9.app` in us-east-1 region
- **Check validation**: Certificate must be "Issued" status in ACM
- **Wait for propagation**: SSL changes can take 15-30 minutes

### CORS error in browser console
- **Check API Gateway CORS**: Must include `https://strains.loyal9.app`
- **Verify deployment**: Must deploy API after CORS changes
- **Check browser console**: Look for specific CORS error message

### CloudFront 403 error
- **Check S3 bucket policy**: Must allow CloudFront OAI
- **Verify OAI**: CloudFront distribution must have OAI configured
- **Check file paths**: S3 keys must match inventory (e.g., `html/{hash}.html`)

---

## Expected Timeline

| Step | Time |
|------|------|
| Add CNAME in Squarespace | 2 minutes |
| DNS propagation | 5-60 minutes |
| Request SSL certificate | 5 minutes |
| SSL validation | 5-30 minutes |
| CloudFront configuration | 10 minutes |
| CloudFront deployment | 15-30 minutes |
| **Total** | **45-120 minutes** |

---

## Cost Impact

**Squarespace**: $0 (included with domain)  
**AWS Certificate Manager**: $0 (free for CloudFront)  
**CloudFront custom domain**: $0 (no additional cost)

**Total additional cost**: $0/month

---

## Security Notes

- ✅ HTTPS enforced (CloudFront redirects HTTP → HTTPS)
- ✅ SSL certificate from AWS (trusted by all browsers)
- ✅ CORS restricted to `strains.loyal9.app` only
- ✅ No direct S3 access (CloudFront OAI required)

---

## Next Steps After Setup

1. **Update README.md** with live URL
2. **Test on mobile devices** (responsive design)
3. **Monitor CloudFront logs** (track usage)
4. **Set up CloudWatch alarms** (error rate, latency)
5. **Share with beta testers** (get feedback)

---

**Questions?** Contact Shannon Goddard or check AWS documentation:
- [CloudFront Custom Domains](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html)
- [AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/gs.html)
- [Squarespace DNS Settings](https://support.squarespace.com/hc/en-us/articles/205812378-Connecting-a-domain-to-your-site)

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**
