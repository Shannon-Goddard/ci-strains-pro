import json
import boto3
import csv
from datetime import datetime, timedelta
from botocore.signers import CloudFrontSigner
import os
import rsa

# Environment variables
CLOUDFRONT_DOMAIN = os.environ.get('CLOUDFRONT_DOMAIN', 'd36gqaqkk0n97a.cloudfront.net')
CLOUDFRONT_KEY_PAIR_ID = os.environ.get('CLOUDFRONT_KEY_PAIR_ID', 'APKASPK2KPPM2XK4DMPI')
S3_BUCKET = os.environ.get('S3_BUCKET', 'ci-strains-html-archive')
INVENTORY_KEY = os.environ.get('INVENTORY_KEY', 'pipeline/03_s3_inventory/s3_html_inventory.csv')
JS_INVENTORY_KEY = os.environ.get('JS_INVENTORY_KEY', 'pipeline/03_s3_inventory/s3_js_html_inventory.csv')
SECRET_NAME = os.environ.get('SECRET_NAME', 'cloudfront_private_key')

s3_client = boto3.client('s3')
secrets_client = boto3.client('secretsmanager', region_name='us-east-1')

# Cache private key (loaded once per Lambda container)
_private_key_cache = None

def get_private_key():
    """Retrieve CloudFront private key from Secrets Manager (cached)."""
    global _private_key_cache
    
    if _private_key_cache is None:
        response = secrets_client.get_secret_value(SecretId=SECRET_NAME)
        _private_key_cache = response['SecretString']
    
    return _private_key_cache

def load_inventory():
    """Load both HTML inventories from S3 into memory."""
    inventory = {}
    
    # Load main inventory
    obj = s3_client.get_object(Bucket=S3_BUCKET, Key=INVENTORY_KEY)
    content = obj['Body'].read().decode('utf-8').splitlines()
    reader = csv.DictReader(content)
    for row in reader:
        inventory[row['url']] = {
            's3_key': row['s3_html_key'],
            'seed_bank': row['seed_bank'],
            'collection_date': row['collection_date']
        }
    
    # Load JS inventory
    obj = s3_client.get_object(Bucket=S3_BUCKET, Key=JS_INVENTORY_KEY)
    content = obj['Body'].read().decode('utf-8').splitlines()
    reader = csv.DictReader(content)
    for row in reader:
        inventory[row['url']] = {
            's3_key': row['html_key'],
            'seed_bank': row['seed_bank'],
            'collection_date': 'JS-rendered'
        }
    
    return inventory

def rsa_signer(message):
    """Sign message with CloudFront private key using rsa library."""
    private_key_pem = get_private_key()
    private_key = rsa.PrivateKey.load_pkcs1(private_key_pem.encode('utf-8'))
    return rsa.sign(message, private_key, 'SHA-1')

def generate_signed_url(s3_key, expiration_minutes=5):
    """Generate CloudFront signed URL with expiration."""
    url = f"https://{CLOUDFRONT_DOMAIN}/{s3_key}"
    expire_date = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    
    cloudfront_signer = CloudFrontSigner(CLOUDFRONT_KEY_PAIR_ID, rsa_signer)
    signed_url = cloudfront_signer.generate_presigned_url(
        url, date_less_than=expire_date
    )
    
    return signed_url

def lambda_handler(event, context):
    """Main Lambda handler for URL lookup."""
    
    # Parse request body
    try:
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        url = body.get('url', '').strip()
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Invalid request body'})
        }
    
    if not url:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'URL parameter is required'})
        }
    
    # Load inventory
    try:
        inventory = load_inventory()
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f'Failed to load inventory: {str(e)}'})}
    
    # Validate URL exists in inventory
    if url not in inventory:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'URL not found in inventory'})
        }
    
    # Generate signed URL
    try:
        strain_data = inventory[url]
        signed_url = generate_signed_url(strain_data['s3_key'])
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'signed_url': signed_url,
                'seed_bank': strain_data['seed_bank'],
                'collection_date': strain_data['collection_date'],
                'expires_in_minutes': 5,
                'legal_notice': 'Use subject to Legal Disclaimer: https://github.com/loyal9/ci-strains-pro/blob/main/pipeline/04_source_of_truth_viewer/docs/LEGAL_DISCLAIMER.md'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f'Failed to generate signed URL: {str(e)}'})
        }
