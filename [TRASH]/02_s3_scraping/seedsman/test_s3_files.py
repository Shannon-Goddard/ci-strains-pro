#!/usr/bin/env python3
"""
Simple test to check if S3 HTML files contain actual strain data
"""

import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError, ClientError

def test_s3_files():
    """Test a few S3 HTML files to see if they contain strain data"""
    
    # Read the CSV to get S3 keys
    df = pd.read_csv('seedsman_maximum_extraction.csv')
    
    # Test first 5 files
    test_keys = df['s3_key'].head(5).tolist()
    
    try:
        # Initialize S3 client
        s3 = boto3.client('s3')
        bucket = 'ci-strains-archive'
        
        print("Testing S3 HTML files for actual strain data...")
        print("=" * 60)
        
        for i, s3_key in enumerate(test_keys, 1):
            print(f"\n{i}. Testing: {s3_key}")
            
            try:
                # Get the HTML content
                response = s3.get_object(Bucket=bucket, Key=s3_key)
                html_content = response['Body'].read().decode('utf-8')
                
                # Check content length and key indicators
                print(f"   Content length: {len(html_content):,} characters")
                
                # Look for JavaScript blocking indicators
                js_blocked = any(phrase in html_content.lower() for phrase in [
                    'you need to enable javascript',
                    'javascript is disabled',
                    'enable javascript',
                    'javascript required'
                ])
                
                # Look for strain data indicators
                strain_indicators = any(phrase in html_content.lower() for phrase in [
                    'thc',
                    'cbd',
                    'indica',
                    'sativa',
                    'genetics',
                    'flowering time',
                    'yield'
                ])
                
                print(f"   JavaScript blocked: {js_blocked}")
                print(f"   Contains strain data: {strain_indicators}")
                
                # Show first 200 characters
                preview = html_content[:200].replace('\n', ' ').replace('\r', ' ')
                print(f"   Preview: {preview}...")
                
            except ClientError as e:
                print(f"   Error accessing file: {e}")
                
    except NoCredentialsError:
        print("AWS credentials not found. Please configure your credentials.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_s3_files()