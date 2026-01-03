#!/usr/bin/env python3
"""
Check available credentials
"""
from aws_secrets import AWSSecretsManager

secrets_manager = AWSSecretsManager()
credentials = secrets_manager.get_cannabis_db_credentials()

print("Available credentials:")
for key, value in credentials.items():
    print(f"  {key}: {'***' if value else 'None'}")