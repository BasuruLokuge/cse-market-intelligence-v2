"""Data Transformer - Simplified"""
import pandas as pd
from datetime import datetime
from src.utils import get_logger

logger = get_logger(__name__)

class DataTransformer:
    """Transforms extracted data"""
    
    def transform_market_summary(self, summary):
        """Transform market summary"""
        logger.info("Transforming market summary...")
        
        indices = pd.DataFrame([
            {
                'index_name': 'ASPI',
                'trade_date': summary['trade_date'],
                'index_value': summary['aspi_value'],
                'index_change': summary['aspi_change'],
                'index_change_pct': summary['aspi_change_pct'],
                'volume': summary['total_volume'],
                'turnover_lkr': summary['total_turnover']
            },
            {
                'index_name': 'S&P SL20',
                'trade_date': summary['trade_date'],
                'index_value': summary['sp20_value'],
                'index_change': summary['sp20_change'],
                'index_change_pct': summary['sp20_change_pct'],
                'volume': None,
                'turnover_lkr': None
            }
        ])
        
        market_summary = {
            'trade_date': summary['trade_date'],
            'total_trades': summary['total_trades'],
            'total_volume': summary['total_volume'],
            'total_turnover_lkr': summary['total_turnover'],
            'advancing_stocks': summary['advancing'],
            'declining_stocks': summary['declining'],
            'unchanged_stocks': summary['unchanged']
        }
        
        return {'indices': indices, 'summary': market_summary}
    
    def transform_stock_prices(self, df):
        """Transform stock prices"""
        logger.info("Transforming stock prices...")
        logger.info(f"Transformed {len(df)} stock price records")
        return df
    
    def transform_all_data(self, raw_data):
        """Transform all data"""
        logger.info("Starting data transformation...")
        
        market_data = self.transform_market_summary(raw_data['market_summary'])
        stock_prices = self.transform_stock_prices(raw_data['stock_prices'])
        sector_performance = raw_data['sector_performance']
        
        transformed = {
            'market_indices': market_data['indices'],
            'market_summary': market_data['summary'],
            'stock_prices': stock_prices,
            'sector_performance': sector_performance
        }
        
        logger.info("Data transformation completed")
        return transformed
