"""Data Loader - Error-Free with UPSERT"""
from datetime import datetime
from src.utils import get_logger, get_db_connection

logger = get_logger(__name__)

class DataLoader:
    """Loads data into PostgreSQL with UPSERT"""
    
    def get_stock_id(self, symbol):
        """Get stock_id for symbol"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT stock_id FROM dim_stocks WHERE symbol = %s", (symbol,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting stock_id: {e}")
            return None
    
    def get_sector_id(self, sector_name):
        """Get sector_id for sector"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT sector_id FROM dim_sectors WHERE sector_name = %s", (sector_name,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting sector_id: {e}")
            return None
    
    def load_market_indices(self, df):
        """Load market indices with UPSERT"""
        logger.info("Loading market indices...")
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for _, row in df.iterrows():
                # Safely convert values
                volume = int(row['volume']) if pd.notna(row['volume']) else None
                turnover = float(row['turnover_lkr']) if pd.notna(row['turnover_lkr']) else None
                
                cursor.execute("""
                    INSERT INTO fact_market_indices 
                    (index_name, trade_date, index_value, index_change, index_change_pct, volume, turnover_lkr)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (index_name, trade_date) 
                    DO UPDATE SET
                        index_value = EXCLUDED.index_value,
                        index_change = EXCLUDED.index_change,
                        index_change_pct = EXCLUDED.index_change_pct,
                        volume = EXCLUDED.volume,
                        turnover_lkr = EXCLUDED.turnover_lkr
                """, (
                    row['index_name'],
                    row['trade_date'],
                    float(row['index_value']),
                    float(row['index_change']),
                    float(row['index_change_pct']),
                    volume,
                    turnover
                ))
            
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"Loaded {len(df)} market index records")
            return len(df)
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            logger.error(f"Error loading indices: {e}")
            raise
    
    def load_market_summary(self, summary):
        """Load market summary with UPSERT"""
        logger.info("Loading market summary...")
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO fact_market_summary 
                (trade_date, total_trades, total_volume, total_turnover_lkr,
                 advancing_stocks, declining_stocks, unchanged_stocks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (trade_date)
                DO UPDATE SET
                    total_trades = EXCLUDED.total_trades,
                    total_volume = EXCLUDED.total_volume,
                    total_turnover_lkr = EXCLUDED.total_turnover_lkr,
                    advancing_stocks = EXCLUDED.advancing_stocks,
                    declining_stocks = EXCLUDED.declining_stocks,
                    unchanged_stocks = EXCLUDED.unchanged_stocks
            """, (
                summary['trade_date'],
                summary['total_trades'],
                summary['total_volume'],
                summary['total_turnover_lkr'],
                summary['advancing_stocks'],
                summary['declining_stocks'],
                summary['unchanged_stocks']
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("Market summary loaded")
            return 1
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            logger.error(f"Error loading summary: {e}")
            raise
    
    def load_stock_prices(self, df):
        """Load stock prices with UPSERT"""
        logger.info("Loading stock prices...")
        
        df = df.copy()
        df['stock_id'] = df['symbol'].apply(self.get_stock_id)
        df = df[df['stock_id'].notna()]
        
        if len(df) == 0:
            logger.warning("No stocks to load")
            return 0
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO fact_daily_prices 
                    (stock_id, trade_date, open_price, high_price, low_price, close_price,
                     volume, turnover_lkr, price_change, price_change_pct)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (stock_id, trade_date)
                    DO UPDATE SET
                        open_price = EXCLUDED.open_price,
                        high_price = EXCLUDED.high_price,
                        low_price = EXCLUDED.low_price,
                        close_price = EXCLUDED.close_price,
                        volume = EXCLUDED.volume,
                        turnover_lkr = EXCLUDED.turnover_lkr,
                        price_change = EXCLUDED.price_change,
                        price_change_pct = EXCLUDED.price_change_pct
                """, (
                    int(row['stock_id']),
                    row['trade_date'],
                    float(row['open_price']),
                    float(row['high_price']),
                    float(row['low_price']),
                    float(row['close_price']),
                    int(row['volume']),
                    float(row['turnover_lkr']),
                    float(row['price_change']),
                    float(row['price_change_pct'])
                ))
            
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"Loaded {len(df)} stock price records")
            return len(df)
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            logger.error(f"Error loading prices: {e}")
            raise
    
    def load_sector_performance(self, df):
        """Load sector performance with UPSERT"""
        logger.info("Loading sector performance...")
        
        df = df.copy()
        df['sector_id'] = df['sector_name'].apply(self.get_sector_id)
        df = df[df['sector_id'].notna()]
        
        if len(df) == 0:
            logger.warning("No sectors to load")
            return 0
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO fact_sector_performance 
                    (sector_id, trade_date, sector_index, sector_change_pct, total_volume,
                     total_turnover_lkr, advancing_count, declining_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (sector_id, trade_date)
                    DO UPDATE SET
                        sector_index = EXCLUDED.sector_index,
                        sector_change_pct = EXCLUDED.sector_change_pct,
                        total_volume = EXCLUDED.total_volume,
                        total_turnover_lkr = EXCLUDED.total_turnover_lkr,
                        advancing_count = EXCLUDED.advancing_count,
                        declining_count = EXCLUDED.declining_count
                """, (
                    int(row['sector_id']),
                    row['trade_date'],
                    float(row['sector_index']),
                    float(row['sector_change_pct']),
                    int(row['total_volume']),
                    float(row['total_turnover_lkr']),
                    int(row['advancing_count']),
                    int(row['declining_count'])
                ))
            
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"Loaded {len(df)} sector records")
            return len(df)
        except Exception as e:
            if conn:
                conn.rollback()
                conn.close()
            logger.error(f"Error loading sectors: {e}")
            raise
    
    def log_execution(self, status, records=0, exec_time=0, error=None):
        """Log pipeline execution"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pipeline_execution_log 
                (execution_date, pipeline_name, status, records_loaded, execution_time_seconds, error_message)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (datetime.now(), 'CSE ETL', status, records, exec_time, error))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            logger.error(f"Error logging: {e}")
    
    def load_all_data(self, data):
        """Load all data"""
        logger.info("Starting data loading...")
        start = datetime.now()
        total = 0
        
        try:
            total += self.load_market_indices(data['market_indices'])
            total += self.load_market_summary(data['market_summary'])
            total += self.load_stock_prices(data['stock_prices'])
            total += self.load_sector_performance(data['sector_performance'])
            
            exec_time = int((datetime.now() - start).total_seconds())
            self.log_execution('SUCCESS', total, exec_time)
            
            logger.info(f"Loading completed: {total} records in {exec_time}s")
            return {'status': 'SUCCESS', 'records': total, 'time': exec_time}
        except Exception as e:
            exec_time = int((datetime.now() - start).total_seconds())
            self.log_execution('FAILED', total, exec_time, str(e))
            raise

import pandas as pd
