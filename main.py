"""Main ETL Pipeline - Simplified"""
import sys
from datetime import datetime
from src.utils import setup_logging, get_logger
from src.extractors import CSEDataExtractor
from src.transformers import DataTransformer
from src.loaders import DataLoader

setup_logging()
logger = get_logger(__name__)

def run_etl_pipeline():
    """Run the complete ETL pipeline"""
    
    print("=" * 60)
    print("CSE Market Intelligence ETL Pipeline")
    print("=" * 60)
    
    start_time = datetime.now()
    
    try:
        # EXTRACT
        print("\n[STEP 1/3] EXTRACTION")
        print("-" * 60)
        extractor = CSEDataExtractor()
        raw_data = extractor.extract_all_data()
        print("OK - Data extraction completed")
        
        # TRANSFORM
        print("\n[STEP 2/3] TRANSFORMATION")
        print("-" * 60)
        transformer = DataTransformer()
        transformed_data = transformer.transform_all_data(raw_data)
        print("OK - Data transformation completed")
        
        # LOAD
        print("\n[STEP 3/3] LOADING")
        print("-" * 60)
        loader = DataLoader()
        result = loader.load_all_data(transformed_data)
        print("OK - Data loading completed")
        
        # SUMMARY
        duration = (datetime.now() - start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("ETL Pipeline Completed Successfully!")
        print("=" * 60)
        print(f"Duration: {duration:.2f} seconds")
        print(f"Records Loaded: {result['records']}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("ETL Pipeline FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = run_etl_pipeline()
    sys.exit(0 if success else 1)
