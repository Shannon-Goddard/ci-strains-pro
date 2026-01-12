#!/usr/bin/env python3
"""
Seedsman DynamoDB to CSV Extractor
Extract Seedsman data from DynamoDB and save as CSV
"""

import boto3
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_seedsman_to_csv():
    """Extract Seedsman data from DynamoDB to CSV"""
    
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('cannabis-strains-universal')
    
    logger.info("Scanning DynamoDB for Seedsman data...")
    
    # Scan for Seedsman records
    response = table.scan(
        FilterExpression='seed_bank = :sb',
        ExpressionAttributeValues={':sb': 'Seedsman'}
    )
    
    items = response['Items']
    
    # Handle pagination
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression='seed_bank = :sb',
            ExpressionAttributeValues={':sb': 'Seedsman'},
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        items.extend(response['Items'])
    
    logger.info(f"Found {len(items)} Seedsman records")
    
    if not items:
        logger.error("No Seedsman data found in DynamoDB!")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(items)
    
    # Convert Decimal types to float for CSV
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"seedsman_extracted_{timestamp}.csv"
    filepath = f"c:\\Users\\uthin\\OneDrive\\Desktop\\ci-strains-pro\\pipeline\\04_seedsman_collection\\data\\{filename}"
    
    # Save to CSV
    df.to_csv(filepath, index=False, encoding='utf-8')
    
    logger.info(f"Seedsman data exported to: {filepath}")
    logger.info(f"Records: {len(df)}")
    logger.info(f"Columns: {list(df.columns)}")
    
    # Print summary stats
    if 'quality_tier' in df.columns:
        quality_dist = df['quality_tier'].value_counts()
        logger.info(f"Quality distribution: {dict(quality_dist)}")
    
    if 'data_completeness_score' in df.columns:
        avg_quality = df['data_completeness_score'].mean()
        logger.info(f"Average quality score: {avg_quality:.1f}%")
    
    print(f"\n✅ SUCCESS: {len(df)} Seedsman strains exported to CSV")
    print(f"📁 File: {filepath}")
    
    return filepath

if __name__ == "__main__":
    extract_seedsman_to_csv()