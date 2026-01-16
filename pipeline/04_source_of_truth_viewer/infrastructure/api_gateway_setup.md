# API Gateway Setup Guide

**Purpose**: REST API endpoint for URL lookup with rate limiting and CORS.

---

## Step 1: Create Lambda Function

1. Go to **Lambda Console** → **Create Function**
2. **Function Settings**:
   - Name: `ci-strains-lookup`
   - Runtime: **Python 3.12**
   - Architecture: **x86_64**
   - Execution Role: **Create a new role with basic Lambda permissions**

3. Click **Create Function**

---

## Step 2: Upload Lambda Code

1. In the Lambda function, go to **Code** tab
2. Upload `lookup_function.py` (or paste code directly)
3. Click **Deploy**

---

## Step 3: Add Lambda Dependencies

1. Create deployment package locally:
   ```bash
   cd lambda/
   pip install -r requirements.txt -t package/
   cd package/
   zip -r ../lambda_deployment.zip .
   cd ..
   zip -g lambda_deployment.zip lookup_function.py
   ```

2. Upload `lambda_deployment.zip` to Lambda function
3. Click **Deploy**

---

## Step 4: Configure Lambda Environment Variables

1. Go to **Configuration** → **Environment Variables**
2. Add these variables:
   - `CLOUDFRONT_DOMAIN`: `d1234567890abc.cloudfront.net` (from CloudFront setup)
   - `CLOUDFRONT_KEY_PAIR_ID`: `APKA1234567890ABC` (from CloudFront setup)
   - `CLOUDFRONT_PRIVATE_KEY`: (paste entire contents of `pk-<KEY_PAIR_ID>.pem`)
   - `S3_BUCKET`: `ci-strains-html-archive`
   - `INVENTORY_KEY`: `pipeline/03_s3_inventory/s3_html_inventory.csv`
   - `JS_INVENTORY_KEY`: `pipeline/03_s3_inventory/s3_js_html_inventory.csv`

3. Click **Save**

---

## Step 5: Update Lambda IAM Role

1. Go to **Configuration** → **Permissions**
2. Click on the **Execution Role** name
3. Click **Add Permissions** → **Attach Policies**
4. Create inline policy with this JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": [
        "arn:aws:s3:::ci-strains-html-archive/pipeline/03_s3_inventory/s3_html_inventory.csv",
        "arn:aws:s3:::ci-strains-html-archive/pipeline/03_s3_inventory/s3_js_html_inventory.csv"
      ]
    }
  ]
}
```

5. Name: `ci-strains-s3-read-inventory`
6. Click **Create Policy**

---

## Step 6: Create API Gateway

1. Go to **API Gateway Console** → **Create API**
2. Choose **REST API** (not private)
3. Click **Build**
4. **API Settings**:
   - API Name: `ci-strains-lookup-api`
   - Description: `Source of Truth Viewer API`
   - Endpoint Type: **Regional**

5. Click **Create API**

---

## Step 7: Create /lookup Resource

1. Click **Actions** → **Create Resource**
2. **Resource Settings**:
   - Resource Name: `lookup`
   - Resource Path: `/lookup`
   - Enable CORS: **Yes**

3. Click **Create Resource**

---

## Step 8: Create POST Method

1. Select `/lookup` resource
2. Click **Actions** → **Create Method** → **POST**
3. **Integration Settings**:
   - Integration Type: **Lambda Function**
   - Use Lambda Proxy Integration: **Yes** (check this box)
   - Lambda Region: `us-east-1`
   - Lambda Function: `ci-strains-lookup`

4. Click **Save**
5. Click **OK** to grant API Gateway permission to invoke Lambda

---

## Step 9: Enable CORS

1. Select `/lookup` resource
2. Click **Actions** → **Enable CORS**
3. **CORS Settings**:
   - Access-Control-Allow-Origin: `*` (or specific domain)
   - Access-Control-Allow-Headers: `Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token`
   - Access-Control-Allow-Methods: `POST,OPTIONS`

4. Click **Enable CORS and replace existing CORS headers**

---

## Step 10: Configure Throttling

1. Click **Stages** → **Create Stage**
2. **Stage Settings**:
   - Stage Name: `prod`
   - Deployment: (select latest deployment)

3. Click **Create**
4. Go to **Settings** tab
5. **Throttling Settings**:
   - Rate: `10` requests per second
   - Burst: `20` requests

6. Click **Save Changes**

---

## Step 11: Deploy API

1. Click **Actions** → **Deploy API**
2. **Deployment Settings**:
   - Deployment Stage: `prod`
   - Deployment Description: `Initial production deployment`

3. Click **Deploy**
4. **Copy the Invoke URL** (format: `https://abc123.execute-api.us-east-1.amazonaws.com/prod`)

---

## Step 12: Test API

1. Use curl or Postman to test:

```bash
curl -X POST https://abc123.execute-api.us-east-1.amazonaws.com/prod/lookup \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.northatlanticseed.com/product/og-kush-f-3/"}'
```

2. Expected response:
```json
{
  "signed_url": "https://d1234567890abc.cloudfront.net/html/00019a017d135d9e.html?Expires=...",
  "seed_bank": "Other",
  "collection_date": "2026-01-03T09:09:46.484328",
  "expires_in_minutes": 5
}
```

---

## Configuration Summary

**Save this value for frontend:**

- **API_ENDPOINT**: `https://abc123.execute-api.us-east-1.amazonaws.com/prod/lookup`

---

## Security Verification Checklist

- ✅ Lambda has minimal IAM permissions (read inventory only)
- ✅ API Gateway throttling enabled (10 req/sec)
- ✅ CORS configured for frontend domain
- ✅ Lambda validates URL exists before generating signed URL
- ✅ Signed URLs expire after 5 minutes

---

**Next Step**: Build frontend interface.
