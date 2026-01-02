#!/usr/bin/env python3
"""
AWS Secrets Manager Integration for Cannabis Intelligence Database
================================================================

Secure credential management for Bright Data and Google Gemini API keys
Author: Shannon Goddard & Amazon Q
"""

import subprocess
import json
import logging
from typing import Dict, Optional

class AWSSecretsManager:
    """Secure credential retrieval using AWS CLI"""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize AWS CLI integration"""
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
            self.logger.debug(f"Retrieving secret: {secret_name}")
            
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
                    self.logger.error(f"Secret {secret_name} does not contain SecretString")
                    return None
            else:
                error_msg = result.stderr.strip()
                if 'ResourceNotFoundException' in error_msg:
                    self.logger.error(f"Secret {secret_name} not found")
                elif 'AccessDenied' in error_msg:
                    self.logger.error(f"Access denied for secret {secret_name}")
                else:
                    self.logger.error(f"AWS CLI error for {secret_name}: {error_msg}")
                return None
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Timeout retrieving secret {secret_name}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse AWS CLI response for {secret_name}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            return None
    
    def get_cannabis_db_credentials(self) -> Dict[str, Optional[str]]:
        """Retrieve all Cannabis Intelligence Database credentials"""
        credentials = {
            'GEMINI_API_KEY': None,
            'BRIGHT_DATA_USERNAME': None,
            'BRIGHT_DATA_PASSWORD': None,
            'BRIGHT_DATA_ENDPOINT': None
        }
        
        # Try to get Gemini API key from separate secret first
        gemini_secret = self.get_secret('cannabis-gemini-api')
        if gemini_secret:
            # Handle both possible field names
            api_key = gemini_secret.get('api_key') or gemini_secret.get('cannabis-gemini-api')
            if api_key:
                credentials['GEMINI_API_KEY'] = api_key
        
        # Get Bright Data credentials for API method
        bright_data_secret = self.get_secret('cannabis-brightdata-api')
        if bright_data_secret:
            # Map the actual field names from your secret for API method
            api_key = bright_data_secret.get('api_key')
            zone = bright_data_secret.get('zone')
            gemini_key = bright_data_secret.get('gemini_api_key')
            
            if api_key and zone:
                # For Bright Data API method:
                # USERNAME = zone name (cannabis_strain_scraper)
                # PASSWORD = API token
                credentials['BRIGHT_DATA_USERNAME'] = zone
                credentials['BRIGHT_DATA_PASSWORD'] = api_key
                credentials['BRIGHT_DATA_ENDPOINT'] = "api.brightdata.com"  # Not used for API method
            
            # Use Gemini key from Bright Data secret if not found in separate secret
            if gemini_key and not credentials['GEMINI_API_KEY']:
                credentials['GEMINI_API_KEY'] = gemini_key
        
        # Log credential status (without exposing values)
        available_creds = [k for k, v in credentials.items() if v is not None]
        missing_creds = [k for k, v in credentials.items() if v is None]
        
        if available_creds:
            self.logger.info(f"Retrieved credentials: {', '.join(available_creds)}")
        if missing_creds:
            self.logger.warning(f"Missing credentials: {', '.join(missing_creds)}")
        
        return credentials

def get_aws_credentials() -> Dict[str, Optional[str]]:
    """Convenience function to get all Cannabis DB credentials from AWS"""
    try:
        secrets_manager = AWSSecretsManager()
        return secrets_manager.get_cannabis_db_credentials()
    except Exception as e:
        logging.error(f"Failed to retrieve AWS credentials: {e}")
        return {
            'GEMINI_API_KEY': None,
            'BRIGHT_DATA_USERNAME': None,
            'BRIGHT_DATA_PASSWORD': None,
            'BRIGHT_DATA_ENDPOINT': None
        }