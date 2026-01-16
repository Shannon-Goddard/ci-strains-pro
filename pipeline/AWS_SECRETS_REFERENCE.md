# AWS Secrets Manager Configuration - Cannabis Intelligence Project

**For Amazon Q Implementation Reference**

## Configured Secrets (us-east-1)

### 1. Bright Data API
- **Secret Name**: `cannabis_bright_data_api`
- **Contains**: Bright Data Web Unlocker credentials
- **Balance**: $133.71 available
- **Usage**: Primary HTML scraping service

### 2. ScrapingBee API  
- **Secret Name**: `cannabis_scrapingbee_api`
- **Contains**: ScrapingBee API key
- **Credits**: 250,000 API credits available
- **Usage**: Fallback scraping service

### 3. Google Cloud (Vertex AI)
- **Secret Name**: `cannabis_google_cloud_api`
- **Contains**: Google Cloud service account JSON
- **Usage**: Gemini AI validation
- **Credits**: Free tier available

### 4. CloudFront Key Pair (Source of Truth Viewer)
- **Key Pair ID**: `APKASPK2KPPM2XK4DMPI`
- **Private Key File**: `pk-APKASPK2KPPM2XK4DMPI.pem` (stored securely, NOT in repo)
- **Public Key File**: `rsa-APKASPK2KPPM2XK4DMPI.pem`
- **Usage**: Generate signed URLs for time-limited HTML archive access
- **Distribution**: `ci-strains-source-of-truth` (d36gqaqkk0n97a.cloudfront.net)

## Python Implementation Template

```python
import boto3
import json
from botocore.exceptions import ClientError

class SecretsManager:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)
    
    def get_secret(self, secret_name):
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            raise e
    
    def get_bright_data_creds(self):
        return self.get_secret('cannabis_bright_data_api')
    
    def get_scrapingbee_key(self):
        return self.get_secret('cannabis_scrapingbee_api')['api_key']
    
    def get_google_cloud_creds(self):
        return self.get_secret('cannabis_google_cloud_api')
```

## JavaScript/Node.js Implementation Template

```javascript
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";

const client = new SecretsManagerClient({ region: "us-east-1" });

async function getSecret(secretName) {
    try {
        const response = await client.send(
            new GetSecretValueCommand({
                SecretId: secretName,
                VersionStage: "AWSCURRENT"
            })
        );
        return JSON.parse(response.SecretString);
    } catch (error) {
        throw error;
    }
}

// Usage examples:
const brightDataCreds = await getSecret('cannabis_bright_data_api');
const scrapingBeeKey = await getSecret('cannabis_scrapingbee_api');
const googleCloudCreds = await getSecret('cannabis_google_cloud_api');
```

## Implementation Notes for Amazon Q

**When implementing HTML collection scripts:**
1. Use SecretsManager class for credential management
2. Bright Data is primary scraping service ($133.71 budget)
3. ScrapingBee is fallback service (250K credits)
4. All secrets are in us-east-1 region
5. Error handling is critical for production use

**Project Context:**
- Cannabis Intelligence Database with 15,778 strains
- Target: ~12K unique URLs for HTML collection
- Bulletproof scraping with multi-layer fallbacks
- S3 storage with secure access via API Gateway

**Ready for immediate implementation without credential setup delays.**