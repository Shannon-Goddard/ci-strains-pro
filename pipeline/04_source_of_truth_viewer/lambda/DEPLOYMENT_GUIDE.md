# Lambda Function Deployment Guide

**Function Name**: `ci-strains-lookup`  
**Runtime**: Python 3.12  
**Architecture**: x86_64

---

## Step 1: Create Lambda Function

1. **Go to AWS Lambda Console**
2. **Click "Create function"**
3. **Configure**:
   - Function name: `ci-strains-lookup`
   - Runtime: Python 3.12
   - Architecture: x86_64
   - Execution role: Create new role with basic Lambda permissions

4. **Click "Create function"**

---

## Step 2: Upload Code

### Option A: Inline (Quick Test)
1. Copy contents of `lookup_function.py`
2. Paste into Lambda code editor
3. Click "Deploy"

### Option B: ZIP Package (Production)
```bash
cd pipeline/04_source_of_truth_viewer/lambda
pip install -r requirements.txt -t .
zip -r function.zip .
```
Then upload `function.zip` in Lambda console.

---

## Step 3: Configure Environment Variables

**Configuration → Environment variables → Edit**

Add these:

| Key | Value |
|-----|-------|
| `CLOUDFRONT_DOMAIN` | `d36gqaqkk0n97a.cloudfront.net` |
| `CLOUDFRONT_KEY_PAIR_ID` | `APKASPK2KPPM2XK4DMPI` |
| `S3_BUCKET` | `ci-strains-html-archive` |
| `INVENTORY_KEY` | `pipeline/03_s3_inventory/s3_html_inventory.csv` |
| `JS_INVENTORY_KEY` | `pipeline/03_s3_inventory/s3_js_html_inventory.csv` |
| `SECRET_NAME` | `cloudfront_private_key` |

---

## Step 4: Update IAM Role Permissions

**Configuration → Permissions → Execution role → Click role name**

Add these policies:

### 1. S3 Read Access
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::ci-strains-html-archive/pipeline/03_s3_inventory/*",
                "arn:aws:s3:::ci-strains-html-archive/html/*",
                "arn:aws:s3:::ci-strains-html-archive/html_js/*"
            ]
        }
    ]
}
```

### 2. Secrets Manager Access
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": "arn:aws:secretsmanager:us-east-1:170377509849:secret:cloudfront_private_key-*"
        }
    ]
}
```

---

## Step 5: Configure Function Settings

**Configuration → General configuration → Edit**

- **Memory**: 512 MB (inventory loading needs memory)
- **Timeout**: 30 seconds (allow time for S3 reads + signing)
- **Ephemeral storage**: 512 MB (default)

---

## Step 6: Test the Function

**Test → Create test event**

```json
{
    "body": "{\"url\": \"https://www.northatlanticseed.com/product/og-kush-f-3/\"}"
}
```

**Expected response**:
```json
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    },
    "body": "{\"signed_url\": \"https://d36gqaqkk0n97a.cloudfront.net/html/...\", \"seed_bank\": \"North Atlantic\", ...}"
}
```

---

## Step 7: Enable Function URL (Optional - Quick Test)

**Configuration → Function URL → Create function URL**

- **Auth type**: NONE (for testing)
- **CORS**: Enable
  - Allow origin: `*`
  - Allow methods: `POST`
  - Allow headers: `content-type`

**You'll get a URL like**:
```
https://abc123xyz.lambda-url.us-east-1.on.aws/
```

Test with:
```bash
curl -X POST https://abc123xyz.lambda-url.us-east-1.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.northatlanticseed.com/product/og-kush-f-3/"}'
```

---

## Troubleshooting

### Error: "Failed to load inventory"
- Check S3 bucket permissions
- Verify inventory CSV files exist at correct paths
- Check Lambda execution role has S3 read access

### Error: "Failed to generate signed URL"
- Check Secrets Manager permissions
- Verify secret name is `cloudfront_private_key`
- Check CloudFront key pair ID is correct

### Error: "URL not found in inventory"
- URL must exactly match inventory (including trailing slashes)
- Check if URL is in `s3_html_inventory.csv` or `s3_js_html_inventory.csv`

---

## Cost Estimate

**Lambda**:
- Free tier: 1M requests/month, 400K GB-seconds
- Your usage: ~1K requests/month = $0

**Secrets Manager**:
- Cost: $0.40/month per secret
- Your usage: 1 secret = $0.40/month

**Total**: ~$0.40/month

---

## Next Steps

After Lambda is working:
1. Create API Gateway REST API
2. Connect API Gateway to Lambda
3. Update frontend with API Gateway URL
4. Deploy frontend to CloudFront

---

**Ready to create the Lambda function in AWS Console!** 🚀
