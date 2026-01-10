#!/usr/bin/env python3
"""
Cannabis Intelligence Database - Manual Review Validation
Validates 187 manually fixed URLs through Gemini Flash 2.0
"""

import pandas as pd
import sqlite3
import requests
import json
import time
import logging
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aws_secrets import AWSSecretsManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('manual_review_validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ManualReviewValidator:
    def __init__(self):
        self.secrets_manager = AWSSecretsManager()
        self.credentials = self.secrets_manager.get_cannabis_db_credentials()
        self.db_path = 'manual_review_progress.db'
        self.setup_database()
        
    def setup_database(self):
        """Initialize SQLite database for progress tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS validation_progress (
                strain_id INTEGER PRIMARY KEY,
                source_url TEXT,
                status TEXT,
                processed_at TIMESTAMP,
                confidence_score REAL,
                error_message TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def scrape_with_brightdata(self, url):
        """Scrape URL using Bright Data API"""
        try:
            # Use Bright Data API format from working script
            api_url = "https://api.brightdata.com/request"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.credentials["BRIGHT_DATA_PASSWORD"]}'
            }
            
            payload = {
                "zone": self.credentials['BRIGHT_DATA_USERNAME'],  # This is the zone name
                "url": url,
                "format": "raw"
            }
            
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Bright Data error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Scraping error for {url}: {str(e)}")
            return None
    
    def validate_with_gemini(self, strain_data, scraped_content):
        """Validate strain data using Gemini Flash 2.0"""
        try:
            from google import genai
            
            # Configure Gemini with Vertex AI
            client = genai.Client(
                vertexai=True,
                project="gen-lang-client-0100184589",
                location="us-central1"
            )
            
            prompt = f"""
            You are a cannabis strain data validator. Analyze the scraped webpage content and enhance the existing strain data.
            
            EXISTING STRAIN DATA:
            {json.dumps(strain_data, indent=2)}
            
            SCRAPED WEBPAGE CONTENT:
            {scraped_content[:8000]}  # Limit content size
            
            Please extract and validate:
            1. THC/CBD percentages (min/max ranges)
            2. Sativa/Indica/Ruderalis percentages
            3. Flowering time in days
            4. Effects (comma-separated)
            5. Flavors (comma-separated)
            6. Genetic lineage
            7. Breeding method and generation
            8. Seed gender and flowering behavior
            
            Return ONLY a JSON object with validated fields. Use null for missing data.
            Example format:
            {{
                "thc_min_validated": 18.0,
                "thc_max_validated": 22.0,
                "cbd_min_validated": 0.5,
                "flowering_days_min_validated": 56,
                "flowering_days_max_validated": 63,
                "sativa_percentage_validated": 30.0,
                "indica_percentage_validated": 70.0,
                "effects_validated": "relaxing, euphoric",
                "flavors_validated": "citrus, pine",
                "lineage_validated": "Blue Dream x OG Kush",
                "seed_gender_validated": "Feminized",
                "flowering_behavior_validated": "Photoperiod",
                "validation_notes": "Data extracted from webpage"
            }}
            """
            
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Clean up response (remove markdown formatting if present)
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            try:
                validated_data = json.loads(response_text)
                return validated_data, 0.85  # Default confidence score
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON response from Gemini: {response_text[:200]}...")
                return None, 0.0
                
        except Exception as e:
            logger.error(f"Gemini validation error: {str(e)}")
            return None, 0.0
    
    def process_strain(self, strain_row):
        """Process a single strain through scraping and validation"""
        # Use source_url as identifier since strain_id is missing
        source_url = strain_row.get('source_url') or strain_row.get('ï»¿source_url')
        strain_name = strain_row.get('strain_name', 'unknown')
        
        logger.info(f"Processing strain: {strain_name}")
        
        # Check if already processed (use source_url as key)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT status FROM validation_progress WHERE source_url = ?', (source_url,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == 'completed':
            logger.info(f"Strain {strain_name} already processed, skipping")
            return strain_row
        
        # Scrape webpage
        scraped_content = self.scrape_with_brightdata(source_url)
        
        if not scraped_content:
            self.update_progress(source_url, source_url, 'failed', 0.0, 'Scraping failed')
            return strain_row
        
        # Validate with Gemini
        strain_dict = strain_row.to_dict()
        validated_data, confidence = self.validate_with_gemini(strain_dict, scraped_content)
        
        if validated_data:
            # Update strain data with validated fields
            for key, value in validated_data.items():
                if key.endswith('_validated') or key in ['validation_notes', 'confidence_score']:
                    strain_row[key] = value
            
            strain_row['confidence_score'] = confidence
            strain_row['processing_timestamp'] = datetime.now().isoformat()
            strain_row['scrape_success'] = True
            strain_row['scrape_error'] = None
            
            self.update_progress(source_url, source_url, 'completed', confidence, None)
            logger.info(f"Successfully validated strain {strain_name}")
        else:
            self.update_progress(source_url, source_url, 'failed', 0.0, 'Validation failed')
            logger.error(f"Failed to validate strain {strain_name}")
        
        return strain_row
    
    def update_progress(self, identifier, source_url, status, confidence, error):
        """Update progress in SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO validation_progress 
                (strain_id, source_url, status, processed_at, confidence_score, error_message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (identifier, source_url, status, datetime.now().isoformat(), confidence, error))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
    
    def validate_dataset(self, input_file='failed_scrapes_fixed_187.csv'):
        """Main validation process"""
        logger.info(f"Starting validation of {input_file}")
        
        # Load dataset
        df = pd.read_csv(input_file, encoding='latin-1')
        logger.info(f"Loaded {len(df)} strains for validation")
        
        # Process each strain
        validated_rows = []
        for idx, row in df.iterrows():
            try:
                validated_row = self.process_strain(row)
                validated_rows.append(validated_row)
                
                # Add small delay to avoid rate limiting
                time.sleep(1)
                
                # Progress update every 10 strains
                if (idx + 1) % 10 == 0:
                    logger.info(f"Progress: {idx + 1}/{len(df)} strains processed")
                    
            except Exception as e:
                logger.error(f"Error processing strain {row.get('strain_id', 'unknown')}: {str(e)}")
                validated_rows.append(row)
        
        # Save validated dataset
        validated_df = pd.DataFrame(validated_rows)
        output_file = 'failed_scrapes_validated_187.csv'
        validated_df.to_csv(output_file, index=False, encoding='latin-1')
        
        logger.info(f"Validation completed! Results saved to {output_file}")
        return output_file

def main():
    """Main execution function"""
    validator = ManualReviewValidator()
    
    try:
        output_file = validator.validate_dataset()
        print(f"✅ Validation completed successfully!")
        print(f"📁 Output file: {output_file}")
        print(f"📊 Check manual_review_validation.log for detailed results")
        
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        print(f"❌ Validation failed. Check logs for details.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())