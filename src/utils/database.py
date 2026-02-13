"""Database utilities - Simplified"""
import os
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'cse_intelligence'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
    
    def get_connection(self):
        """Get a new database connection"""
        return psycopg2.connect(**self.db_config)
    
    def get_engine(self):
        """Get SQLAlchemy engine"""
        conn_str = (
            f"postgresql://{self.db_config['user']}:{self.db_config['password']}"
            f"@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        )
        return create_engine(conn_str)
    
    def execute_script(self, script_path):
        """Execute SQL script"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            with open(script_path, 'r') as f:
                cursor.execute(f.read())
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            print(f"Error: {e}")
            return False

db_manager = DatabaseManager()

def get_db_connection():
    return db_manager.get_connection()

def get_engine():
    return db_manager.get_engine()
