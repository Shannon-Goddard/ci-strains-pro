#!/usr/bin/env python3
"""
Consolidate S3 folders - Copy pipeline06/ to html/
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

logger.info("Copying pipeline06/ files to html/ folder...")

paginator = s3.get_paginator('list_objects_v2')
count = 0

for page in paginator.paginate(Bucket=bucket, Prefix='pipeline06/'):
    for obj in page.get('Contents', []):
        if obj['Key'].endswith('.html'):
            old_key = obj['Key']
            new_key = old_key.replace('pipeline06/', 'html/')
            
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': old_key},
                Key=new_key
            )
            
            count += 1
            if count % 100 == 0:
                logger.info(f"Copied {count} files...")

logger.info(f"Total files copied: {count}")
print(f"\nCOPY COMPLETE!")
print(f"Copied {count} files from pipeline06/ to html/")
