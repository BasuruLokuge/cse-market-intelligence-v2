"""Database Setup Script"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.utils import db_manager

def setup_database():
    """Initialize database with schema"""
    
    print("=" * 60)
    print("Database Setup Started")
    print("=" * 60)
    
    schema_path = 'sql/schema/create_schema.sql'
    
    if not os.path.exists(schema_path):
        print(f"ERROR: Schema file not found: {schema_path}")
        return False
    
    print(f"Executing schema: {schema_path}")
    success = db_manager.execute_script(schema_path)
    
    if success:
        print("=" * 60)
        print("Database Setup Completed Successfully!")
        print("=" * 60)
        print("OK - Schema created")
        print("OK - Tables created")
        print("OK - Indexes created")
        print("OK - Views created")
        print("OK - Sample data inserted")
        print("=" * 60)
        return True
    else:
        print("ERROR: Database setup failed")
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
