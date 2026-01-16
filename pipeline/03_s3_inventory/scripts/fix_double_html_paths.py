#!/usr/bin/env python3
"""
Fix double html/ paths in S3 from elite seed bank consolidation
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import boto3

s3 = boto3.client('s3')
bucket = 'ci-strains-html-archive'

print("Scanning for files with double html/ path...")

# List all files in html/html/
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=bucket, Prefix='html/html/')

files_to_move = []
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            files_to_move.append(obj['Key'])

print(f"Found {len(files_to_move)} files to move")

# Move each file
moved = 0
for old_key in files_to_move:
    # New key: html/html/abc.html -> html/abc.html
    new_key = old_key.replace('html/html/', 'html/')
    
    # Copy to new location
    s3.copy_object(
        Bucket=bucket,
        CopySource={'Bucket': bucket, 'Key': old_key},
        Key=new_key
    )
    
    # Delete old location
    s3.delete_object(Bucket=bucket, Key=old_key)
    
    moved += 1
    if moved % 100 == 0:
        print(f"Moved {moved}/{len(files_to_move)} files...")

print(f"\nComplete! Moved {moved} files from html/html/ to html/")
