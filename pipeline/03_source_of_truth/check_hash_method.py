#!/usr/bin/env python3
import boto3
import json

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

# Get first few metadata files
response = s3.list_objects_v2(Bucket=bucket, Prefix='metadata/', MaxKeys=5)

for obj in response.get('Contents', []):
    key = obj['Key']
    print(f"\nFile: {key}")
    
    # Read metadata content
    content = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    metadata = json.loads(content)
    
    print(f"URL: {metadata.get('url', 'N/A')}")
    print(f"Hash: {metadata.get('url_hash', 'N/A')}")
    
    # Test hash generation
    import hashlib
    url = metadata.get('url', '')
    if url:
        md5_full = hashlib.md5(url.encode()).hexdigest()
        md5_16 = md5_full[:16]
        sha256_16 = hashlib.sha256(url.encode()).hexdigest()[:16]
        
        print(f"MD5 full: {md5_full}")
        print(f"MD5[:16]: {md5_16}")
        print(f"SHA256[:16]: {sha256_16}")
        print(f"Match MD5[:16]: {md5_16 == metadata.get('url_hash')}")