#!/usr/bin/env python3
"""
Cannabis Intelligence Database - Scrape & Judge Validation Pipeline
==================================================================

Phase 1: 100-strain pilot validation using Bright Data + Gemini Flash 2.5
Author: Shannon Goddard & Amazon Q
Dataset: 15,783 cannabis strains with 16,330 AI-extracted data points

This pipeline validates and enhances existing strain data by:
1. Scraping source URLs with Bright Data Web Unlocker
2. Sending scraped content + existing data to Gemini Flash 2.5
3. Extracting/validating: THC/CBD, flowering days, genetics, height, yield, effects, flavors
4. Returning confidence-scored JSON with corrections
5. Batch processing with resumable progress tracking
"""

import os
import sys
import json
import time
import sqlite3
import logging
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
# Import will be done in setup_apis method
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import traceback
from aws_secrets import get_aws_credentials

# Configuration
@dataclass
class Config:
    # File paths
    INPUT_CSV: str = 'REMOVE_strain_data/Cannabis_Database.csv'
    OUTPUT_CSV: str = 'REMOVE_strain_data/Cannabis_Database_Validated.csv'
    PROGRESS_DB: str = 'scrape_judge_progress.db'
    LOG_FILE: str = 'scrape_judge_pipeline.log'
    
    # Processing parameters
    BATCH_SIZE: int = 10
    PILOT_SIZE: int = 100
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2
    REQUEST_TIMEOUT: int = 30
    RATE_LIMIT_DELAY: float = 1.0
    
    # Validation thresholds
    MIN_CONFIDENCE_SCORE: float = 7.0
    MAX_THC_PERCENTAGE: float = 35.0
    MAX_CBD_PERCENTAGE: float = 25.0
    MIN_FLOWERING_DAYS: int = 30
    MAX_FLOWERING_DAYS: int = 120
    
    def __post_init__(self):
        """Load credentials from AWS Secrets Manager"""
        aws_creds = get_aws_credentials()
        self.GEMINI_API_KEY = aws_creds['GEMINI_API_KEY']
        self.BRIGHT_DATA_USERNAME = aws_creds['BRIGHT_DATA_USERNAME']
        self.BRIGHT_DATA_PASSWORD = aws_creds['BRIGHT_DATA_PASSWORD']
        self.BRIGHT_DATA_ENDPOINT = aws_creds['BRIGHT_DATA_ENDPOINT']

@dataclass
class ValidationResult:
    """Structure for Gemini validation results"""
    strain_id: str
    confidence_score: float
    thc_min: Optional[float] = None
    thc_max: Optional[float] = None
    cbd_min: Optional[float] = None
    cbd_max: Optional[float] = None
    flowering_days_min: Optional[int] = None
    flowering_days_max: Optional[int] = None
    sativa_percentage: Optional[float] = None
    indica_percentage: Optional[float] = None
    ruderalis_percentage: Optional[float] = None
    height_indoor_cm: Optional[float] = None
    indoor_yield_min_g: Optional[float] = None
    indoor_yield_max_g: Optional[float] = None
    outdoor_yield_min_g: Optional[float] = None
    outdoor_yield_max_g: Optional[float] = None
    effects: Optional[str] = None
    flavors: Optional[str] = None
    primary_generation: Optional[str] = None
    breeding_method: Optional[str] = None
    phenotype: Optional[str] = None
    lineage: Optional[str] = None
    seed_gender: Optional[str] = None
    flowering_behavior: Optional[str] = None
    validation_notes: Optional[str] = None
    scrape_success: bool = False
    scrape_error: Optional[str] = None
    processing_timestamp: str = datetime.now().isoformat()

class ScrapeAndJudgePipeline:
    """Main pipeline class for cannabis strain validation"""
    
    def __init__(self, config: Config):
        self.config = config
        self.setup_logging()
        self.setup_apis()
        self.setup_database()
        self.setup_session()
        
    def setup_logging(self):
        """Configure comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("=== Cannabis Intelligence Database - Scrape & Judge Pipeline Started ===")
        
    def setup_apis(self):
        """Initialize API connections"""
        # Configure Gemini
        if not self.config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in AWS Secrets Manager")
        
        # Use Vertex AI with proper gcloud authentication (no API key needed)
        from google import genai
        self.genai_client = genai.Client(
            vertexai=True,
            project="gen-lang-client-0100184589",
            location="us-central1"
        )
        self.logger.info("Gemini 2.0 Flash (Vertex AI - Authenticated) initialized")
        
        # Validate Bright Data credentials
        if not self.config.BRIGHT_DATA_USERNAME or not self.config.BRIGHT_DATA_PASSWORD:
            self.logger.warning("Bright Data credentials not fully configured")
            
    def setup_database(self):
        """Initialize SQLite progress tracking database"""
        self.conn = sqlite3.connect(self.config.PROGRESS_DB)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS validation_progress (
                strain_id TEXT PRIMARY KEY,
                source_url TEXT,
                batch_number INTEGER,
                processing_status TEXT,
                confidence_score REAL,
                scrape_success INTEGER,
                scrape_error TEXT,
                validation_result TEXT,
                processing_timestamp TEXT,
                retry_count INTEGER DEFAULT 0
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS batch_summary (
                batch_number INTEGER PRIMARY KEY,
                total_strains INTEGER,
                successful_scrapes INTEGER,
                successful_validations INTEGER,
                average_confidence REAL,
                processing_time_seconds REAL,
                batch_timestamp TEXT
            )
        ''')
        self.conn.commit()
        self.logger.info("Progress tracking database initialized")
        
    def setup_session(self):
        """Configure HTTP session with retries and proxies"""
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.config.MAX_RETRIES,
            backoff_factor=self.config.RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Bright Data API configuration (no proxy needed)
        if self.config.BRIGHT_DATA_USERNAME and self.config.BRIGHT_DATA_PASSWORD:
            self.logger.info(f"Bright Data API configured: zone={self.config.BRIGHT_DATA_USERNAME}")
        
    def load_strain_data(self) -> pd.DataFrame:
        """Load cannabis strain dataset"""
        try:
            # Try different encodings to handle the CSV file
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(self.config.INPUT_CSV, encoding=encoding)
                    self.logger.info(f"Successfully loaded CSV with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("Could not read CSV file with any supported encoding")
                
            self.logger.info(f"Loaded {len(df)} strains from {self.config.INPUT_CSV}")
            
            # Validate required columns
            required_columns = ['source_url', 'strain_name']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
                
            # Create strain_id if not exists
            if 'strain_id' not in df.columns:
                df['strain_id'] = df.index.astype(str)
                
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to load strain data: {e}")
            raise
            
    def get_unprocessed_strains(self, df: pd.DataFrame, limit: Optional[int] = None) -> pd.DataFrame:
        """Get strains that haven't been processed yet"""
        processed_ids = set()
        
        cursor = self.conn.execute(
            "SELECT strain_id FROM validation_progress WHERE processing_status = 'completed'"
        )
        processed_ids = {row[0] for row in cursor.fetchall()}
        
        unprocessed_df = df[~df['strain_id'].isin(processed_ids)].copy()
        
        if limit:
            unprocessed_df = unprocessed_df.head(limit)
            
        self.logger.info(f"Found {len(unprocessed_df)} unprocessed strains (limit: {limit})")
        return unprocessed_df
        
    def scrape_strain_url(self, url: str, strain_id: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Scrape strain URL using Bright Data API"""
        try:
            self.logger.debug(f"Scraping URL for strain {strain_id}: {url}")
            
            # Use Bright Data API instead of proxy
            api_url = "https://api.brightdata.com/request"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.config.BRIGHT_DATA_PASSWORD}'
            }
            
            payload = {
                "zone": self.config.BRIGHT_DATA_USERNAME,  # This is actually the zone name
                "url": url,
                "format": "raw"
            }
            
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                content = response.text
                self.logger.debug(f"Successfully scraped {len(content)} characters for strain {strain_id}")
                return True, content, None
            else:
                error_msg = f"HTTP {response.status_code}: {response.reason}"
                self.logger.warning(f"Scrape failed for strain {strain_id}: {error_msg}")
                return False, None, error_msg
                
        except Exception as e:
            error_msg = f"Scraping error: {str(e)}"
            self.logger.error(f"Scrape failed for strain {strain_id}: {error_msg}")
            return False, None, error_msg
            
    def create_gemini_prompt(self, existing_data: Dict, scraped_content: str) -> str:
        """Create comprehensive Gemini validation prompt"""
        
        prompt = f"""
You are an expert cannabis strain data validator. Compare the existing database record with freshly scraped webpage content and extract/validate cultivation data.

EXISTING DATABASE RECORD:
- Strain Name: {existing_data.get('strain_name', 'N/A')}
- THC Min/Max: {existing_data.get('thc_min', 'N/A')}/{existing_data.get('thc_max', 'N/A')}%
- CBD Min/Max: {existing_data.get('cbd_min', 'N/A')}/{existing_data.get('cbd_max', 'N/A')}%
- Flowering Days: {existing_data.get('flowering_days_min', 'N/A')}-{existing_data.get('flowering_days_max', 'N/A')} days
- Sativa/Indica/Ruderalis: {existing_data.get('sativa_percentage', 'N/A')}/{existing_data.get('indica_percentage', 'N/A')}/{existing_data.get('ruderalis_percentage', 'N/A')}%
- Height Indoor: {existing_data.get('height_indoor_cm', 'N/A')} cm
- Indoor Yield: {existing_data.get('indoor_yield_min_g', 'N/A')}-{existing_data.get('indoor_yield_max_g', 'N/A')} g
- Outdoor Yield: {existing_data.get('outdoor_yield_min_g', 'N/A')}-{existing_data.get('outdoor_yield_max_g', 'N/A')} g
- Effects: {existing_data.get('effects', 'N/A')}
- Flavors: {existing_data.get('flavors', 'N/A')}
- Generation: {existing_data.get('primary_generation', 'N/A')}
- Breeding Method: {existing_data.get('breeding_method', 'N/A')}
- Phenotype: {existing_data.get('phenotype', 'N/A')}
- Lineage: {existing_data.get('lineage', 'N/A')}
- Seed Gender: {existing_data.get('seed_gender', 'N/A')}
- Flowering Behavior: {existing_data.get('flowering_behavior', 'N/A')}

SCRAPED WEBPAGE CONTENT:
{scraped_content[:8000]}  # Limit content to avoid token limits

VALIDATION INSTRUCTIONS:
1. Extract accurate THC/CBD percentages (0-35% THC, 0-25% CBD)
2. Find flowering time and convert weeks to days (30-120 days range)
3. Identify sativa/indica/ruderalis percentages (modern genetics include ruderalis)
4. Extract height in centimeters (convert from feet/inches if needed)
5. Extract yield in grams (convert from ounces if needed)
6. List primary effects (euphoric, relaxing, energetic, creative, etc.)
7. List primary flavors and terpene profiles
8. Extract breeding information:
   - Generation: F1, F2, F3, IBL, etc.
   - Breeding Method: Regular, Feminized, Autoflower
   - Phenotype: #1, #2, Pheno A, etc.
   - Lineage: Parent strain names (e.g., "Blue Dream x OG Kush")
   - Seed Gender: Regular, Feminized
   - Flowering Behavior: Photoperiod, Autoflower
9. Note any major discrepancies between existing data and scraped content
10. Provide confidence score (1-10) based on data quality and consistency

CRITICAL VALIDATION RULES:
- Only extract data explicitly mentioned in the scraped content
- Convert all measurements to metric (cm, grams, days)
- Extract sativa/indica/ruderalis percentages (may not sum to 100% due to hybrid complexity)
- Flag suspicious values (THC >35%, CBD >25%, flowering <30 or >120 days)
- Prioritize scraped content over existing data when conflicts exist
- If no relevant data found in scraped content, return null values

Return ONLY valid JSON in this exact format:
{{
    "confidence_score": 8.5,
    "thc_min": 18.0,
    "thc_max": 22.0,
    "cbd_min": 0.5,
    "cbd_max": 1.2,
    "flowering_days_min": 56,
    "flowering_days_max": 63,
    "sativa_percentage": 30.0,
    "indica_percentage": 60.0,
    "ruderalis_percentage": 10.0,
    "height_indoor_cm": 90.0,
    "indoor_yield_min_g": 400.0,
    "indoor_yield_max_g": 500.0,
    "outdoor_yield_min_g": 600.0,
    "outdoor_yield_max_g": 800.0,
    "effects": "Relaxing, Euphoric, Creative, Pain Relief",
    "flavors": "Citrus, Pine, Earthy, Sweet",
    "primary_generation": "F1",
    "breeding_method": "Feminized",
    "phenotype": "#2",
    "lineage": "Blue Dream x OG Kush",
    "seed_gender": "Feminized",
    "flowering_behavior": "Photoperiod",
    "validation_notes": "Scraped data confirms existing THC range. Updated flowering time from weeks to days. Added missing yield data and breeding information."
}}
"""
        return prompt
        
    def validate_with_gemini(self, existing_data: Dict, scraped_content: str, strain_id: str) -> ValidationResult:
        """Send data to Gemini Flash 2.5 for validation"""
        try:
            prompt = self.create_gemini_prompt(existing_data, scraped_content)
            
            self.logger.debug(f"Sending validation request to Gemini for strain {strain_id}")
            
            response = self.genai_client.models.generate_content(
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
                validation_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse Gemini JSON response for strain {strain_id}: {e}")
                self.logger.debug(f"Raw response: {response_text}")
                return ValidationResult(
                    strain_id=strain_id,
                    confidence_score=1.0,
                    validation_notes=f"JSON parsing error: {str(e)}",
                    scrape_success=True
                )
            
            # Validate and sanitize extracted data
            result = ValidationResult(
                strain_id=strain_id,
                confidence_score=self.validate_confidence_score(validation_data.get('confidence_score', 1.0)),
                thc_min=self.validate_percentage(validation_data.get('thc_min'), 0, self.config.MAX_THC_PERCENTAGE),
                thc_max=self.validate_percentage(validation_data.get('thc_max'), 0, self.config.MAX_THC_PERCENTAGE),
                cbd_min=self.validate_percentage(validation_data.get('cbd_min'), 0, self.config.MAX_CBD_PERCENTAGE),
                cbd_max=self.validate_percentage(validation_data.get('cbd_max'), 0, self.config.MAX_CBD_PERCENTAGE),
                flowering_days_min=self.validate_integer(validation_data.get('flowering_days_min'), self.config.MIN_FLOWERING_DAYS, self.config.MAX_FLOWERING_DAYS),
                flowering_days_max=self.validate_integer(validation_data.get('flowering_days_max'), self.config.MIN_FLOWERING_DAYS, self.config.MAX_FLOWERING_DAYS),
                sativa_percentage=self.validate_percentage(validation_data.get('sativa_percentage'), 0, 100),
                indica_percentage=self.validate_percentage(validation_data.get('indica_percentage'), 0, 100),
                ruderalis_percentage=self.validate_percentage(validation_data.get('ruderalis_percentage'), 0, 100),
                height_indoor_cm=self.validate_positive_float(validation_data.get('height_indoor_cm')),
                indoor_yield_min_g=self.validate_positive_float(validation_data.get('indoor_yield_min_g')),
                indoor_yield_max_g=self.validate_positive_float(validation_data.get('indoor_yield_max_g')),
                outdoor_yield_min_g=self.validate_positive_float(validation_data.get('outdoor_yield_min_g')),
                outdoor_yield_max_g=self.validate_positive_float(validation_data.get('outdoor_yield_max_g')),
                effects=self.validate_string(validation_data.get('effects')),
                flavors=self.validate_string(validation_data.get('flavors')),
                primary_generation=self.validate_string(validation_data.get('primary_generation')),
                breeding_method=self.validate_string(validation_data.get('breeding_method')),
                phenotype=self.validate_string(validation_data.get('phenotype')),
                lineage=self.validate_string(validation_data.get('lineage')),
                seed_gender=self.validate_string(validation_data.get('seed_gender')),
                flowering_behavior=self.validate_string(validation_data.get('flowering_behavior')),
                validation_notes=self.validate_string(validation_data.get('validation_notes')),
                scrape_success=True
            )
            
            # Log genetics information for review
            genetics_info = []
            if result.sativa_percentage is not None:
                genetics_info.append(f"Sativa: {result.sativa_percentage}%")
            if result.indica_percentage is not None:
                genetics_info.append(f"Indica: {result.indica_percentage}%")
            if result.ruderalis_percentage is not None:
                genetics_info.append(f"Ruderalis: {result.ruderalis_percentage}%")
            if genetics_info:
                self.logger.debug(f"Strain {strain_id} genetics: {', '.join(genetics_info)}")
                    
            self.logger.debug(f"Gemini validation completed for strain {strain_id} (confidence: {result.confidence_score})")
            return result
            
        except Exception as e:
            self.logger.error(f"Gemini validation failed for strain {strain_id}: {e}")
            return ValidationResult(
                strain_id=strain_id,
                confidence_score=1.0,
                validation_notes=f"Gemini API error: {str(e)}",
                scrape_success=True
            )
            
    def validate_confidence_score(self, value: Any) -> float:
        """Validate confidence score (1-10)"""
        try:
            score = float(value)
            return max(1.0, min(10.0, score))
        except (TypeError, ValueError):
            return 1.0
            
    def validate_percentage(self, value: Any, min_val: float = 0, max_val: float = 100) -> Optional[float]:
        """Validate percentage values"""
        try:
            if value is None:
                return None
            pct = float(value)
            if min_val <= pct <= max_val:
                return pct
            return None
        except (TypeError, ValueError):
            return None
            
    def validate_integer(self, value: Any, min_val: int, max_val: int) -> Optional[int]:
        """Validate integer values within range"""
        try:
            if value is None:
                return None
            val = int(float(value))
            if min_val <= val <= max_val:
                return val
            return None
        except (TypeError, ValueError):
            return None
            
    def validate_positive_float(self, value: Any) -> Optional[float]:
        """Validate positive float values"""
        try:
            if value is None:
                return None
            val = float(value)
            if val > 0:
                return val
            return None
        except (TypeError, ValueError):
            return None
            
    def validate_string(self, value: Any) -> Optional[str]:
        """Validate and clean string values"""
        if value is None or value == "":
            return None
        try:
            cleaned = str(value).strip()
            return cleaned if cleaned else None
        except:
            return None
            
    def process_strain_batch(self, batch_df: pd.DataFrame, batch_number: int) -> Dict[str, Any]:
        """Process a batch of strains"""
        batch_start_time = time.time()
        results = []
        successful_scrapes = 0
        successful_validations = 0
        confidence_scores = []
        
        self.logger.info(f"Processing batch {batch_number} with {len(batch_df)} strains")
        
        for idx, row in batch_df.iterrows():
            strain_id = str(row['strain_id'])
            source_url = row['source_url']
            
            try:
                # Record processing start
                self.conn.execute(
                    "INSERT OR REPLACE INTO validation_progress (strain_id, source_url, batch_number, processing_status, processing_timestamp) VALUES (?, ?, ?, ?, ?)",
                    (strain_id, source_url, batch_number, 'processing', datetime.now().isoformat())
                )
                self.conn.commit()
                
                # Scrape URL
                scrape_success, scraped_content, scrape_error = self.scrape_strain_url(source_url, strain_id)
                
                if scrape_success and scraped_content:
                    successful_scrapes += 1
                    
                    # Validate with Gemini
                    existing_data = row.to_dict()
                    validation_result = self.validate_with_gemini(existing_data, scraped_content, strain_id)
                    validation_result.scrape_success = True
                    
                    if validation_result.confidence_score >= self.config.MIN_CONFIDENCE_SCORE:
                        successful_validations += 1
                        
                    confidence_scores.append(validation_result.confidence_score)
                    
                else:
                    # Scrape failed
                    validation_result = ValidationResult(
                        strain_id=strain_id,
                        confidence_score=1.0,
                        scrape_success=False,
                        scrape_error=scrape_error,
                        validation_notes=f"Scrape failed: {scrape_error}"
                    )
                
                results.append(validation_result)
                
                # Update progress database
                self.conn.execute(
                    """UPDATE validation_progress 
                       SET processing_status = ?, confidence_score = ?, scrape_success = ?, 
                           scrape_error = ?, validation_result = ?, processing_timestamp = ?
                       WHERE strain_id = ?""",
                    ('completed', validation_result.confidence_score, validation_result.scrape_success,
                     validation_result.scrape_error, json.dumps(asdict(validation_result)), 
                     datetime.now().isoformat(), strain_id)
                )
                self.conn.commit()
                
                # Rate limiting
                time.sleep(self.config.RATE_LIMIT_DELAY)
                
            except Exception as e:
                self.logger.error(f"Failed to process strain {strain_id}: {e}")
                self.logger.debug(traceback.format_exc())
                
                # Record failure
                error_result = ValidationResult(
                    strain_id=strain_id,
                    confidence_score=1.0,
                    scrape_success=False,
                    scrape_error=str(e),
                    validation_notes=f"Processing error: {str(e)}"
                )
                results.append(error_result)
                
                self.conn.execute(
                    """UPDATE validation_progress 
                       SET processing_status = ?, scrape_error = ?, processing_timestamp = ?
                       WHERE strain_id = ?""",
                    ('failed', str(e), datetime.now().isoformat(), strain_id)
                )
                self.conn.commit()
        
        # Calculate batch statistics
        batch_time = time.time() - batch_start_time
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        batch_summary = {
            'batch_number': batch_number,
            'total_strains': len(batch_df),
            'successful_scrapes': successful_scrapes,
            'successful_validations': successful_validations,
            'average_confidence': avg_confidence,
            'processing_time_seconds': batch_time,
            'results': results
        }
        
        # Save batch summary
        self.conn.execute(
            """INSERT INTO batch_summary 
               (batch_number, total_strains, successful_scrapes, successful_validations, 
                average_confidence, processing_time_seconds, batch_timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (batch_number, len(batch_df), successful_scrapes, successful_validations,
             avg_confidence, batch_time, datetime.now().isoformat())
        )
        self.conn.commit()
        
        self.logger.info(f"Batch {batch_number} completed: {successful_scrapes}/{len(batch_df)} scrapes successful, "
                        f"{successful_validations}/{len(batch_df)} high-confidence validations, "
                        f"avg confidence: {avg_confidence:.2f}, time: {batch_time:.1f}s")
        
        return batch_summary
        
    def save_results(self, all_results: List[ValidationResult], original_df: pd.DataFrame):
        """Save validation results to enhanced CSV"""
        try:
            # Create results DataFrame
            results_data = []
            for result in all_results:
                results_data.append(asdict(result))
            
            results_df = pd.DataFrame(results_data)
            
            # Merge with original data
            enhanced_df = original_df.copy()
            
            # Add validation columns
            validation_columns = [
                'confidence_score', 'thc_min_validated', 'thc_max_validated',
                'cbd_min_validated', 'cbd_max_validated', 'flowering_days_min_validated',
                'flowering_days_max_validated', 'sativa_percentage_validated',
                'indica_percentage_validated', 'ruderalis_percentage_validated',
                'height_indoor_cm_validated',
                'indoor_yield_min_g_validated', 'indoor_yield_max_g_validated',
                'outdoor_yield_min_g_validated', 'outdoor_yield_max_g_validated',
                'effects_validated', 'flavors_validated',
                'primary_generation_validated', 'breeding_method_validated',
                'phenotype_validated', 'lineage_validated',
                'seed_gender_validated', 'flowering_behavior_validated',
                'validation_notes', 'scrape_success', 'scrape_error', 'processing_timestamp'
            ]
            
            # Initialize validation columns
            for col in validation_columns:
                enhanced_df[col] = None
                
            # Merge validation results
            for result in all_results:
                mask = enhanced_df['strain_id'] == result.strain_id
                if mask.any():
                    enhanced_df.loc[mask, 'confidence_score'] = result.confidence_score
                    enhanced_df.loc[mask, 'thc_min_validated'] = result.thc_min
                    enhanced_df.loc[mask, 'thc_max_validated'] = result.thc_max
                    enhanced_df.loc[mask, 'cbd_min_validated'] = result.cbd_min
                    enhanced_df.loc[mask, 'cbd_max_validated'] = result.cbd_max
                    enhanced_df.loc[mask, 'flowering_days_min_validated'] = result.flowering_days_min
                    enhanced_df.loc[mask, 'flowering_days_max_validated'] = result.flowering_days_max
                    enhanced_df.loc[mask, 'sativa_percentage_validated'] = result.sativa_percentage
                    enhanced_df.loc[mask, 'indica_percentage_validated'] = result.indica_percentage
                    enhanced_df.loc[mask, 'ruderalis_percentage_validated'] = result.ruderalis_percentage
                    enhanced_df.loc[mask, 'height_indoor_cm_validated'] = result.height_indoor_cm
                    enhanced_df.loc[mask, 'indoor_yield_min_g_validated'] = result.indoor_yield_min_g
                    enhanced_df.loc[mask, 'indoor_yield_max_g_validated'] = result.indoor_yield_max_g
                    enhanced_df.loc[mask, 'outdoor_yield_min_g_validated'] = result.outdoor_yield_min_g
                    enhanced_df.loc[mask, 'outdoor_yield_max_g_validated'] = result.outdoor_yield_max_g
                    enhanced_df.loc[mask, 'effects_validated'] = result.effects
                    enhanced_df.loc[mask, 'flavors_validated'] = result.flavors
                    enhanced_df.loc[mask, 'primary_generation_validated'] = result.primary_generation
                    enhanced_df.loc[mask, 'breeding_method_validated'] = result.breeding_method
                    enhanced_df.loc[mask, 'phenotype_validated'] = result.phenotype
                    enhanced_df.loc[mask, 'lineage_validated'] = result.lineage
                    enhanced_df.loc[mask, 'seed_gender_validated'] = result.seed_gender
                    enhanced_df.loc[mask, 'flowering_behavior_validated'] = result.flowering_behavior
                    enhanced_df.loc[mask, 'validation_notes'] = result.validation_notes
                    enhanced_df.loc[mask, 'scrape_success'] = result.scrape_success
                    enhanced_df.loc[mask, 'scrape_error'] = result.scrape_error
                    enhanced_df.loc[mask, 'processing_timestamp'] = result.processing_timestamp
            
            # Save enhanced dataset
            enhanced_df.to_csv(self.config.OUTPUT_CSV, index=False)
            self.logger.info(f"Enhanced dataset saved to {self.config.OUTPUT_CSV}")
            
            # Generate summary report
            self.generate_summary_report(enhanced_df, all_results)
            
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            raise
            
    def generate_summary_report(self, enhanced_df: pd.DataFrame, all_results: List[ValidationResult]):
        """Generate comprehensive validation summary report"""
        try:
            total_processed = len(all_results)
            successful_scrapes = sum(1 for r in all_results if r.scrape_success)
            high_confidence = sum(1 for r in all_results if r.confidence_score >= self.config.MIN_CONFIDENCE_SCORE)
            
            # Calculate data enhancement metrics
            original_thc_count = enhanced_df['thc_min'].notna().sum()
            validated_thc_count = enhanced_df['thc_min_validated'].notna().sum()
            thc_improvement = validated_thc_count - original_thc_count
            
            original_cbd_count = enhanced_df['cbd_min'].notna().sum()
            validated_cbd_count = enhanced_df['cbd_min_validated'].notna().sum()
            cbd_improvement = validated_cbd_count - original_cbd_count
            
            original_flowering_count = enhanced_df['flowering_days_min'].notna().sum()
            validated_flowering_count = enhanced_df['flowering_days_min_validated'].notna().sum()
            flowering_improvement = validated_flowering_count - original_flowering_count
            
            avg_confidence = sum(r.confidence_score for r in all_results) / total_processed if total_processed > 0 else 0
            
            report = f"""
=== CANNABIS INTELLIGENCE DATABASE - SCRAPE & JUDGE VALIDATION REPORT ===
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PROCESSING SUMMARY:
- Total Strains Processed: {total_processed:,}
- Successful Scrapes: {successful_scrapes:,} ({successful_scrapes/total_processed*100:.1f}%)
- High Confidence Validations: {high_confidence:,} ({high_confidence/total_processed*100:.1f}%)
- Average Confidence Score: {avg_confidence:.2f}/10.0

DATA ENHANCEMENT RESULTS:
- THC Data: {original_thc_count:,} → {validated_thc_count:,} (+{thc_improvement:,} strains, {thc_improvement/original_thc_count*100:.1f}% improvement)
- CBD Data: {original_cbd_count:,} → {validated_cbd_count:,} (+{cbd_improvement:,} strains, {cbd_improvement/original_cbd_count*100:.1f}% improvement)
- Flowering Data: {original_flowering_count:,} → {validated_flowering_count:,} (+{flowering_improvement:,} strains, {flowering_improvement/original_flowering_count*100:.1f}% improvement)

QUALITY METRICS:
- Minimum Confidence Threshold: {self.config.MIN_CONFIDENCE_SCORE}/10.0
- Validation Success Rate: {high_confidence/successful_scrapes*100:.1f}% (of successful scrapes)
- Overall Pipeline Success: {high_confidence/total_processed*100:.1f}% (end-to-end)

NEXT STEPS:
1. Review low-confidence validations (score < {self.config.MIN_CONFIDENCE_SCORE})
2. Manually verify suspicious data points
3. Scale to full dataset ({15783 - total_processed:,} remaining strains)
4. Implement continuous validation for new strain additions

Enhanced dataset saved to: {self.config.OUTPUT_CSV}
Progress database: {self.config.PROGRESS_DB}
Full logs: {self.config.LOG_FILE}
"""
            
            # Save report with UTF-8 encoding
            report_file = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            print(report)
            self.logger.info(f"Validation report saved to {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate summary report: {e}")
            
    def run_pilot_validation(self):
        """Run Phase 1 pilot validation on 100 strains"""
        try:
            self.logger.info(f"Starting Phase 1 pilot validation ({self.config.PILOT_SIZE} strains)")
            
            # Load data
            df = self.load_strain_data()
            
            # Get unprocessed strains for pilot
            pilot_df = self.get_unprocessed_strains(df, limit=self.config.PILOT_SIZE)
            
            if len(pilot_df) == 0:
                self.logger.info("No unprocessed strains found for pilot validation")
                return
                
            # Process in batches
            all_results = []
            total_batches = (len(pilot_df) + self.config.BATCH_SIZE - 1) // self.config.BATCH_SIZE
            
            for batch_num in range(total_batches):
                start_idx = batch_num * self.config.BATCH_SIZE
                end_idx = min(start_idx + self.config.BATCH_SIZE, len(pilot_df))
                batch_df = pilot_df.iloc[start_idx:end_idx]
                
                batch_summary = self.process_strain_batch(batch_df, batch_num + 1)
                all_results.extend(batch_summary['results'])
                
                # Progress update
                processed_count = len(all_results)
                self.logger.info(f"Progress: {processed_count}/{len(pilot_df)} strains processed "
                               f"({processed_count/len(pilot_df)*100:.1f}%)")
            
            # Save results
            self.save_results(all_results, df)
            
            self.logger.info("Phase 1 pilot validation completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Pilot validation failed: {e}")
            self.logger.debug(traceback.format_exc())
            raise
            
    def run_full_validation(self):
        """Run full validation on all remaining strains"""
        try:
            self.logger.info("Starting full dataset validation")
            
            # Load data
            df = self.load_strain_data()
            
            # Get all unprocessed strains
            unprocessed_df = self.get_unprocessed_strains(df)
            
            if len(unprocessed_df) == 0:
                self.logger.info("All strains have been processed")
                return
                
            # Process in batches
            all_results = []
            total_batches = (len(unprocessed_df) + self.config.BATCH_SIZE - 1) // self.config.BATCH_SIZE
            
            # Get the highest existing batch number to continue from
            cursor = self.conn.execute("SELECT MAX(batch_number) FROM batch_summary")
            max_batch = cursor.fetchone()[0] or 0
            
            for batch_num in range(total_batches):
                start_idx = batch_num * self.config.BATCH_SIZE
                end_idx = min(start_idx + self.config.BATCH_SIZE, len(unprocessed_df))
                batch_df = unprocessed_df.iloc[start_idx:end_idx]
                
                # Use incremental batch numbering from where pilot left off
                actual_batch_number = max_batch + batch_num + 1
                batch_summary = self.process_strain_batch(batch_df, actual_batch_number)
                all_results.extend(batch_summary['results'])
                
                # Progress update
                processed_count = len(all_results)
                self.logger.info(f"Progress: {processed_count}/{len(unprocessed_df)} strains processed "
                               f"({processed_count/len(unprocessed_df)*100:.1f}%)")
            
            # Save results
            self.save_results(all_results, df)
            
            self.logger.info("Full dataset validation completed successfully!")
            
        except Exception as e:
            self.logger.error(f"Full validation failed: {e}")
            self.logger.debug(traceback.format_exc())
            raise
            
    def __del__(self):
        """Cleanup database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    """Main execution function"""
    print("=== Cannabis Intelligence Database - Scrape & Judge Pipeline ===")
    print("Phase 1: 100-strain pilot validation")
    print()
    
    # Check environment variables
    config = Config()
    
    if not config.GEMINI_API_KEY:
        print("ERROR: Gemini API key not found in AWS Secrets Manager")
        print("Please ensure 'cannabis-db/gemini-api-key' secret exists with 'api_key' field")
        return 1
    
    try:
        # Initialize pipeline
        pipeline = ScrapeAndJudgePipeline(config)
        
        # Run pilot validation
        pipeline.run_pilot_validation()
        
        print("\n=== PILOT VALIDATION COMPLETED ===")
        print("Review the results and run full validation when ready:")
        print("python scrape_and_judge_pipeline.py --full")
        
        return 0
        
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return 1

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        # Run full validation
        try:
            config = Config()
            pipeline = ScrapeAndJudgePipeline(config)
            pipeline.run_full_validation()
        except Exception as e:
            print(f"FATAL ERROR: {e}")
            sys.exit(1)
    else:
        # Run pilot validation
        sys.exit(main())