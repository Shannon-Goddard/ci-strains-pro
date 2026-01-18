"""Test AWS Secrets Manager retrieval"""
import boto3
import json

session = boto3.session.Session()
client = session.client(service_name='secretsmanager', region_name='us-east-1')

try:
    response = client.get_secret_value(SecretId='cannabis-gemini-api')
    secret = response['SecretString']
    print("Secret retrieved successfully!")
    print(f"Type: {type(secret)}")
    print(f"Length: {len(secret)}")
    print(f"First 50 chars: {secret[:50]}")
    
    # Try parsing as JSON
    try:
        parsed = json.loads(secret)
        print(f"\nParsed as JSON: {type(parsed)}")
        print(f"Keys: {list(parsed.keys())}")
    except:
        print("\nNot JSON format - raw string")
        
except Exception as e:
    print(f"Error: {e}")
