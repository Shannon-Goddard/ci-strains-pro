#!/usr/bin/env python3
"""
AWS Secrets Manager Integration for Pipeline 06
Secure credential management for Bright Data and ScrapingBee APIs

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import subprocess
import json
import logging
from typing import Dict, Optional

class AWSSecretsManager:
    """Secure credential retrieval using AWS CLI"""
    
    def __init__(self, region_name: str = 'us-east-1'):
        self.region_name = region_name
        self.logger = logging.getLogger(__name__)
        
        # Verify AWS CLI is available
        try:
            result = subprocess.run(['aws', '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.logger.info(f"AWS CLI available: {result.stdout.strip()}")
            else:
                raise Exception("AWS CLI not properly configured")
        except Exception as e:
            self.logger.error(f"AWS CLI not available: {e}")
            raise
    
    def get_secret(self, secret_name: str) -> Optional[Dict]:
        """Retrieve secret using AWS CLI"""
        try:
            cmd = [
                'aws', 'secretsmanager', 'get-secret-value',
                '--secret-id', secret_name,
                '--region', self.region_name,
                '--output', 'json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                if 'SecretString' in response:
                    secret_data = json.loads(response['SecretString'])
                    self.logger.info(f"Successfully retrieved secret: {secret_name}")
                    return secret_data
            else:
                self.logger.error(f"Failed to retrieve secret {secret_name}: {result.stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            return None
    
    def get_html_collection_credentials(self) -> Dict[str, Optional[str]]:
        """Retrieve HTML collection credentials"""
        credentials = {
            'BRIGHT_DATA_USERNAME': None,
            'BRIGHT_DATA_PASSWORD': None,
            'BRIGHT_DATA_ENDPOINT': None,
            'SCRAPINGBEE_API_KEY': None
        }
        
        # Get Bright Data credentials (API method)
        bright_data_secret = self.get_secret('cannabis-brightdata-api')
        if bright_data_secret:
            api_key = bright_data_secret.get('api_key')
            zone = bright_data_secret.get('zone')
            
            if api_key and zone:
                credentials['BRIGHT_DATA_USERNAME'] = zone
                credentials['BRIGHT_DATA_PASSWORD'] = api_key
                credentials['BRIGHT_DATA_ENDPOINT'] = "https://api.brightdata.com/request"
        
        # Get ScrapingBee credentials
        scrapingbee_secret = self.get_secret('cannabis_scrapingbee_api')
        if scrapingbee_secret:
            credentials['SCRAPINGBEE_API_KEY'] = scrapingbee_secret.get('api_key')
        
        # Log credential status
        available_creds = [k for k, v in credentials.items() if v is not None]
        missing_creds = [k for k, v in credentials.items() if v is None]
        
        if available_creds:
            self.logger.info(f"Retrieved credentials: {', '.join(available_creds)}")
        if missing_creds:
            self.logger.warning(f"Missing credentials: {', '.join(missing_creds)}")
        
        return credentials

def get_aws_credentials() -> Dict[str, Optional[str]]:
    """Convenience function to get HTML collection credentials"""
    try:
        secrets_manager = AWSSecretsManager()
        return secrets_manager.get_html_collection_credentials()
    except Exception as e:
        logging.error(f"Failed to retrieve AWS credentials: {e}")
        return {
            'BRIGHT_DATA_USERNAME': None,
            'BRIGHT_DATA_PASSWORD': None,
            'BRIGHT_DATA_ENDPOINT': None,
            'SCRAPINGBEE_API_KEY': None
        }
