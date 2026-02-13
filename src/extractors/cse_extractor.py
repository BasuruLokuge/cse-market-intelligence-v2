"""CSE Data Extractor - Fixed Version"""
import pandas as pd
from datetime import datetime
import random
from src.utils import get_logger, CONFIG

logger = get_logger(__name__)

class CSEDataExtractor:
    """Extracts mock market data with proper value ranges"""
    
    def extract_market_summary(self):
        """Extract market summary - MOCK DATA"""
        logger.info("Extracting market summary...")
        
        summary_data = {
            'trade_date': datetime.now().date(),
            'aspi_value': 11234.56,
            'aspi_change': 45.23,
            'aspi_change_pct': 0.40,
            'sp20_value': 3456.78,
            'sp20_change': 12.34,
            'sp20_change_pct': 0.36,
            'total_trades': 1234,
            'total_volume': 12345678,
            'total_turnover': 1234567890.50,
            'advancing': 89,
            'declining': 67,
            'unchanged': 45
        }
        
        logger.info(f"Market summary extracted: ASPI {summary_data['aspi_value']}")
        return summary_data
    
    def extract_stock_prices(self):
        """Extract stock prices - MOCK DATA"""
        logger.info("Extracting stock prices...")
        
        stocks = [
            ('COMB.N0000', 115.50, 114.00),
            ('HNB.N0000', 245.00, 243.50),
            ('SAMP.N0000', 187.00, 185.50),
            ('JKH.N0000', 145.00, 144.00),
            ('DIAL.N0000', 12.50, 12.40),
            ('CTC.N0000', 1250.00, 1240.00),
            ('LOLC.N0000', 375.00, 372.00),
            ('NDB.N0000', 78.50, 77.90),
            ('DFCC.N0000', 98.00, 97.20),
            ('CIC.N0000', 67.50, 66.80),
        ]
        
        data = []
        for symbol, close, prev_close in stocks:
            change_factor = random.uniform(0.98, 1.02)
            close = round(close * change_factor, 2)
            change = close - prev_close
            change_pct = (change / prev_close) * 100
            
            data.append({
                'symbol': symbol,
                'trade_date': datetime.now().date(),
                'open_price': round(prev_close * random.uniform(0.99, 1.01), 2),
                'high_price': round(close * random.uniform(1.00, 1.02), 2),
                'low_price': round(close * random.uniform(0.98, 1.00), 2),
                'close_price': close,
                'volume': random.randint(10000, 2000000),
                'turnover_lkr': round(random.uniform(100000, 20000000), 2),
                'price_change': round(change, 2),
                'price_change_pct': round(change_pct, 2)
            })
        
        df = pd.DataFrame(data)
        logger.info(f"Extracted {len(df)} stock prices")
        return df
    
    def extract_sector_performance(self):
        """Extract sector performance - MOCK DATA"""
        logger.info("Extracting sector performance...")
        
        sectors = CONFIG.get('sectors', [])
        data = []
        
        for sector in sectors:
            data.append({
                'sector_name': sector,
                'trade_date': datetime.now().date(),
                'sector_index': round(random.uniform(1000, 5000), 2),
                'sector_change_pct': round(random.uniform(-2, 2), 2),
                'total_volume': random.randint(100000, 5000000),
                'total_turnover_lkr': round(random.uniform(1000000, 50000000), 2),
                'advancing_count': random.randint(5, 25),
                'declining_count': random.randint(5, 25)
            })
        
        df = pd.DataFrame(data)
        logger.info(f"Extracted {len(df)} sector records")
        return df
    
    def extract_all_data(self):
        """Extract all data"""
        logger.info("Starting data extraction...")
        
        data = {
            'market_summary': self.extract_market_summary(),
            'stock_prices': self.extract_stock_prices(),
            'sector_performance': self.extract_sector_performance(),
            'extraction_time': datetime.now()
        }
        
        logger.info("Data extraction completed")
        return data
