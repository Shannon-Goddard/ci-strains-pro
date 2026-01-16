# CloudFront Distribution Setup Guide

**Purpose**: Secure delivery of HTML archives via signed URLs with 5-minute expiration.

## Prerequisites
- S3 bucket: `ci-strains-html-archive` (already exists)
- HTML files in `html/` and `html_js/` prefixes

---

## Step 1: Create CloudFront Origin Access Identity (OAI)

1. Go to **CloudFront Console** → **Origin Access Identities**
2. Click **Create Origin Access Identity**
3. Name: `ci-strains-html-oai`
4. Click **Create**
5. **Copy the OAI ID** (format: `E1234567890ABC`)

---

## Step 2: Update S3 Bucket Policy

1. Go to **S3 Console** → `ci-strains-html-archive` → **Permissions** → **Bucket Policy**
2. Add this policy (replace `<OAI_ID>` with your OAI ID):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity <OAI_ID>"
      },
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::ci-strains-html-archive/html/*",
        "arn:aws:s3:::ci-strains-html-archive/html_js/*"
      ]
    }
  ]
}
```

3. Click **Save**

---

## Step 3: Create CloudFront Distribution

1. Go to **CloudFront Console** → **Create Distribution**
2. **Origin Settings**:
   - Origin Domain: `ci-strains-html-archive.s3.us-east-1.amazonaws.com`
   - Origin Path: (leave blank)
   - Name: `ci-strains-s3-origin`
   - Origin Access: **Legacy access identities**
   - Origin Access Identity: Select `ci-strains-html-oai`
   - Bucket Policy: **Yes, update the bucket policy**

3. **Default Cache Behavior**:
   - Viewer Protocol Policy: **Redirect HTTP to HTTPS**
   - Allowed HTTP Methods: **GET, HEAD**
   - Restrict Viewer Access: **Yes** (enable signed URLs)
   - Trusted Key Groups: (skip for now, use legacy key pairs)

4. **Distribution Settings**:
   - Price Class: **Use all edge locations**
   - Alternate Domain Names (CNAMEs): (optional, add custom domain later)
   - SSL Certificate: **Default CloudFront Certificate**
   - Default Root Object: (leave blank)

5. Click **Create Distribution**
6. **Copy the Distribution Domain Name** (format: `d1234567890abc.cloudfront.net`)

---

## Step 4: Create CloudFront Key Pair (for Signed URLs)

1. Go to **AWS Account** → **Security Credentials** → **CloudFront Key Pairs**
2. Click **Create New Key Pair**
3. Download both:
   - `pk-<KEY_PAIR_ID>.pem` (private key)
   - `rsa-<KEY_PAIR_ID>.pem` (public key)
4. **Copy the Key Pair ID** (format: `APKA1234567890ABC`)

---

## Step 5: Store Private Key in Lambda Environment

1. Open `pk-<KEY_PAIR_ID>.pem` in a text editor
2. Copy the entire contents (including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`)
3. You'll add this to Lambda environment variables in the next step

---

## Step 6: Test CloudFront Distribution

1. Wait for distribution status to change from **Deploying** to **Enabled** (~5-10 minutes)
2. Try accessing a file directly (should fail without signed URL):
   ```
   https://d1234567890abc.cloudfront.net/html/00019a017d135d9e.html
   ```
3. Expected result: **403 Forbidden** (this is correct - signed URLs required)

---

## Configuration Summary

**Save these values for Lambda configuration:**

- **CLOUDFRONT_DOMAIN**: `d1234567890abc.cloudfront.net`
- **CLOUDFRONT_KEY_PAIR_ID**: `APKA1234567890ABC`
- **CLOUDFRONT_PRIVATE_KEY**: (contents of `pk-<KEY_PAIR_ID>.pem`)

---

## Security Verification Checklist

- ✅ S3 bucket has **Block all public access** enabled
- ✅ Only CloudFront OAI can access S3 objects
- ✅ Direct S3 URLs return 403 Forbidden
- ✅ CloudFront requires signed URLs
- ✅ Signed URLs expire after 5 minutes

---

**Next Step**: Configure Lambda function with CloudFront credentials.
