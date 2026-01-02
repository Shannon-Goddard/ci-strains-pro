#!/usr/bin/env python3
"""
Test AWS Secrets Manager retrieval for Cannabis Intelligence Database
"""

from aws_secrets import AWSSecretsManager
import json

def test_secrets():
    print("Testing AWS Secrets Manager retrieval...")
    
    try:
        secrets_manager = AWSSecretsManager()
        
        # Test Gemini secret
        print("\n1. Testing cannabis-gemini-api:")
        gemini_secret = secrets_manager.get_secret('cannabis-gemini-api')
        if gemini_secret:
            print(f"   Keys found: {list(gemini_secret.keys())}")
            print(f"   Full content: {gemini_secret}")
        else:
            print("   Secret not found or empty")
        
        # Test Bright Data secret
        print("\n2. Testing cannabis-brightdata-api:")
        bright_secret = secrets_manager.get_secret('cannabis-brightdata-api')
        if bright_secret:
            print(f"   Keys found: {list(bright_secret.keys())}")
            print(f"   Full content: {bright_secret}")
        else:
            print("   Secret not found or empty")
        
        # Test full credential retrieval
        print("\n3. Testing full credential retrieval:")
        credentials = secrets_manager.get_cannabis_db_credentials()
        for key, value in credentials.items():
            status = "✓ Found" if value else "✗ Missing"
            print(f"   {key}: {status}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_secrets()