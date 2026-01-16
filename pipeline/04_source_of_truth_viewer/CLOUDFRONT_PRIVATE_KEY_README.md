# CloudFront Private Key - DO NOT COMMIT

**File**: `pk-APKASPK2KPPM2XK4DMPI.pem`  
**Key Pair ID**: `APKASPK2KPPM2XK4DMPI`  
**Created**: January 16, 2026

## ⚠️ SECURITY WARNING

This private key is used to generate signed URLs for CloudFront distribution `ci-strains-source-of-truth`.

**NEVER**:
- Commit to Git/GitHub
- Share publicly
- Email or message
- Store in plain text in code

## 🔒 Secure Storage Options

### Option 1: AWS Secrets Manager (Recommended for Production)
```bash
# Store private key in Secrets Manager
aws secretsmanager create-secret \
    --name cloudfront-private-key \
    --description "CloudFront key pair for signed URLs" \
    --secret-string file://pk-APKASPK2KPPM2XK4DMPI.pem \
    --region us-east-1
```

### Option 2: Lambda Environment Variables (Encrypted)
1. Go to Lambda function configuration
2. Add environment variable:
   - Key: `CLOUDFRONT_PRIVATE_KEY`
   - Value: (paste contents of .pem file)
3. Lambda encrypts at rest automatically

### Option 3: Local Secure Storage
- Store in password manager (1Password, LastPass)
- Store in encrypted folder
- Keep backup in secure location

## 📝 Usage in Lambda

```python
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load from environment variable
private_key_pem = os.environ['CLOUDFRONT_PRIVATE_KEY']

# Or load from Secrets Manager
import boto3
secrets = boto3.client('secretsmanager')
response = secrets.get_secret_value(SecretId='cloudfront-private-key')
private_key_pem = response['SecretString']

# Use for signing
private_key = serialization.load_pem_private_key(
    private_key_pem.encode('utf-8'),
    password=None,
    backend=default_backend()
)
```

## 🔑 Key Pair Details

**Key Pair ID**: `APKASPK2KPPM2XK4DMPI`  
**Distribution**: `ci-strains-source-of-truth`  
**Distribution ID**: `EYOCL6B8MFZ7F`  
**Domain**: `d36gqaqkk0n97a.cloudfront.net`  
**Alternate Domain**: `strains.loyal9.app` (pending SSL)

## 🗑️ Key Rotation

If key is compromised:
1. Go to AWS Console → Account → Security Credentials
2. Delete compromised key pair
3. Create new key pair
4. Update Lambda environment variables
5. Redeploy Lambda function

## ✅ .gitignore Entry

Make sure this is in your `.gitignore`:
```
# CloudFront private keys
*.pem
pk-*.pem
rsa-*.pem
```

---

**This file is safe to commit (no secrets). The .pem files are NOT.**
