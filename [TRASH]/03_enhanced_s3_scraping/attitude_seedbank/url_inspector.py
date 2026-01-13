import boto3
import json
from collections import Counter

def inspect_urls():
    """Inspect URLs in metadata to identify seed bank patterns"""
    s3_client = boto3.client('s3')
    
    # Get first 100 metadata files
    paginator = s3_client.get_paginator('list_objects_v2')
    metadata_files = []
    
    for page in paginator.paginate(Bucket='ci-strains-html-archive', Prefix='metadata/'):
        if 'Contents' in page:
            metadata_files.extend([obj['Key'] for obj in page['Contents']])
            if len(metadata_files) >= 100:
                break
    
    print(f"Inspecting first {len(metadata_files)} metadata files...")
    
    urls = []
    domains = []
    
    for metadata_key in metadata_files[:200]:  # Check first 200
        try:
            obj = s3_client.get_object(Bucket='ci-strains-html-archive', Key=metadata_key)
            metadata = json.loads(obj['Body'].read().decode('utf-8'))
            
            url = metadata.get('url', '')
            if url:
                urls.append(url)
                # Extract domain
                if '://' in url:
                    domain = url.split('://')[1].split('/')[0]
                    domains.append(domain)
                    
        except Exception as e:
            print(f"Error loading {metadata_key}: {e}")
            continue
    
    print(f"\nFound {len(urls)} URLs")
    print("\nSample URLs:")
    for url in urls[:10]:
        print(f"  {url}")
    
    print(f"\nDomain distribution:")
    domain_counts = Counter(domains)
    for domain, count in domain_counts.most_common(10):
        print(f"  {domain}: {count}")

if __name__ == "__main__":
    inspect_urls()