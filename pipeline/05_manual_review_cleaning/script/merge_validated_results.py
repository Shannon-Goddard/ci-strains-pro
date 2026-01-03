#!/usr/bin/env python3
"""
Cannabis Intelligence Database - Merge Validated Results
Merges 187 validated records back into main Cannabis_Database_Validated.csv
"""

import pandas as pd
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('merge_validation_results.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ValidationMerger:
    def __init__(self):
        self.main_dataset_path = '../../../manual_review_cleaning.csv'
        self.validated_batch_path = '../failed_scrapes_validated_187.csv'
        self.output_path = '../../../Cannabis_Database_Validated_Complete.csv'
    
    def load_datasets(self):
        """Load main dataset and validated batch"""
        logger.info("Loading datasets...")
        
        # Load main validated dataset
        main_df = pd.read_csv(self.main_dataset_path, encoding='latin-1')
        logger.info(f"Main dataset loaded: {len(main_df)} records")
        
        # Load validated batch (handle BOM)
        batch_df = pd.read_csv(self.validated_batch_path, encoding='utf-8-sig')
        logger.info(f"Validated batch loaded: {len(batch_df)} records")
        
        return main_df, batch_df
    
    def merge_datasets(self, main_df, batch_df):
        """Merge validated batch into main dataset"""
        logger.info("Merging datasets...")
        
        # Create strain_id for batch based on source_url (same logic as main dataset)
        batch_df['strain_id'] = range(len(main_df) + 1, len(main_df) + len(batch_df) + 1)
        
        # Align columns between datasets
        main_cols = set(main_df.columns)
        batch_cols = set(batch_df.columns)
        
        # Add missing columns to batch_df
        for col in main_cols - batch_cols:
            batch_df[col] = None
            
        # Reorder batch columns to match main dataset
        batch_df = batch_df[main_df.columns]
        
        # Simply append the validated batch (no removal needed since these were failed scrapes)
        merged_df = pd.concat([main_df, batch_df], ignore_index=True)
        
        logger.info(f"Final merged dataset: {len(merged_df)} records")
        return merged_df
    
    def validate_merge(self, original_count, merged_df):
        """Validate the merge operation"""
        logger.info("Validating merge results...")
        
        # Check total count (should be original + 187 validated records)
        expected_count = original_count + 187
        actual_count = len(merged_df)
        
        logger.info(f"Expected count: {expected_count}, Actual count: {actual_count}")
        
        if actual_count == expected_count:
            logger.info(f"✅ Merge validation passed: {actual_count} records")
            count_valid = True
        else:
            logger.warning(f"⚠️ Count mismatch: expected {expected_count}, got {actual_count}")
            count_valid = False
        
        # Check for duplicates
        duplicates = merged_df['strain_id'].duplicated().sum()
        if duplicates == 0:
            logger.info("✅ No duplicate strain_ids found")
            dup_valid = True
        else:
            logger.error(f"❌ Found {duplicates} duplicate strain_ids")
            dup_valid = False
        
        # Check scrape success rate
        success_rate = (merged_df['scrape_success'] == True).sum() / len(merged_df) * 100
        logger.info(f"📊 Final scrape success rate: {success_rate:.2f}%")
        
        return count_valid and dup_valid
    
    def generate_summary(self, merged_df):
        """Generate merge summary statistics"""
        logger.info("Generating merge summary...")
        
        summary = {
            'total_strains': len(merged_df),
            'successful_scrapes': (merged_df['scrape_success'] == True).sum(),
            'failed_scrapes': (merged_df['scrape_success'] == False).sum(),
            'success_rate': (merged_df['scrape_success'] == True).sum() / len(merged_df) * 100,
            'avg_confidence_score': merged_df['confidence_score'].mean(),
            'processing_date': datetime.now().isoformat()
        }
        
        logger.info("📊 Merge Summary:")
        logger.info(f"   Total Strains: {summary['total_strains']:,}")
        logger.info(f"   Successful Scrapes: {summary['successful_scrapes']:,}")
        logger.info(f"   Failed Scrapes: {summary['failed_scrapes']:,}")
        logger.info(f"   Success Rate: {summary['success_rate']:.2f}%")
        logger.info(f"   Avg Confidence Score: {summary['avg_confidence_score']:.2f}")
        
        return summary
    
    def save_merged_dataset(self, merged_df):
        """Save the final merged dataset"""
        logger.info(f"Saving merged dataset to {self.output_path}")
        
        merged_df.to_csv(self.output_path, index=False, encoding='latin-1')
        logger.info("✅ Merged dataset saved successfully")
    
    def merge_validation_results(self):
        """Main merge process"""
        try:
            # Load datasets
            main_df, batch_df = self.load_datasets()
            original_count = len(main_df)
            
            # Merge datasets
            merged_df = self.merge_datasets(main_df, batch_df)
            
            # Validate merge
            if not self.validate_merge(original_count, merged_df):
                raise ValueError("Merge validation failed")
            
            # Generate summary
            summary = self.generate_summary(merged_df)
            
            # Save merged dataset
            self.save_merged_dataset(merged_df)
            
            return summary
            
        except Exception as e:
            logger.error(f"Merge process failed: {str(e)}")
            raise

def main():
    """Main execution function"""
    merger = ValidationMerger()
    
    try:
        summary = merger.merge_validation_results()
        
        print("🎉 Merge completed successfully!")
        print(f"📊 Final Dataset: {summary['total_strains']:,} strains")
        print(f"✅ Success Rate: {summary['success_rate']:.2f}%")
        print(f"📁 Output: Cannabis_Database_Validated_Complete.csv")
        
        return 0
        
    except Exception as e:
        print(f"❌ Merge failed: {str(e)}")
        print("📋 Check merge_validation_results.log for details")
        return 1

if __name__ == "__main__":
    exit(main())