-- CSE MARKET INTELLIGENCE DATABASE SCHEMA - SIMPLIFIED
-- Drop existing tables
DROP TABLE IF EXISTS fact_daily_prices CASCADE;
DROP TABLE IF EXISTS fact_market_indices CASCADE;
DROP TABLE IF EXISTS fact_sector_performance CASCADE;
DROP TABLE IF EXISTS fact_market_summary CASCADE;
DROP TABLE IF EXISTS dim_stocks CASCADE;
DROP TABLE IF EXISTS dim_sectors CASCADE;
DROP TABLE IF EXISTS pipeline_execution_log CASCADE;

-- Stocks Dimension
CREATE TABLE dim_stocks (
    stock_id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(200) NOT NULL,
    sector VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sectors Dimension
CREATE TABLE dim_sectors (
    sector_id SERIAL PRIMARY KEY,
    sector_name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Daily Stock Prices
CREATE TABLE fact_daily_prices (
    price_id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES dim_stocks(stock_id),
    trade_date DATE NOT NULL,
    open_price DECIMAL(12,2),
    high_price DECIMAL(12,2),
    low_price DECIMAL(12,2),
    close_price DECIMAL(12,2),
    volume INT DEFAULT 0,
    turnover_lkr DECIMAL(15,2) DEFAULT 0,
    price_change DECIMAL(12,2),
    price_change_pct DECIMAL(8,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_id, trade_date)
);

-- Market Indices
CREATE TABLE fact_market_indices (
    index_id SERIAL PRIMARY KEY,
    index_name VARCHAR(50) NOT NULL,
    trade_date DATE NOT NULL,
    index_value DECIMAL(12,2) NOT NULL,
    index_change DECIMAL(12,2),
    index_change_pct DECIMAL(8,2),
    volume BIGINT,
    turnover_lkr DECIMAL(18,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(index_name, trade_date)
);

-- Sector Performance
CREATE TABLE fact_sector_performance (
    sector_perf_id SERIAL PRIMARY KEY,
    sector_id INT REFERENCES dim_sectors(sector_id),
    trade_date DATE NOT NULL,
    sector_index DECIMAL(12,2),
    sector_change_pct DECIMAL(8,2),
    total_volume BIGINT,
    total_turnover_lkr DECIMAL(18,2),
    advancing_count INT,
    declining_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sector_id, trade_date)
);

-- Market Summary
CREATE TABLE fact_market_summary (
    summary_id SERIAL PRIMARY KEY,
    trade_date DATE UNIQUE NOT NULL,
    total_trades INT,
    total_volume BIGINT,
    total_turnover_lkr DECIMAL(18,2),
    advancing_stocks INT,
    declining_stocks INT,
    unchanged_stocks INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pipeline Execution Log
CREATE TABLE pipeline_execution_log (
    execution_id SERIAL PRIMARY KEY,
    execution_date TIMESTAMP NOT NULL,
    pipeline_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    records_loaded INT,
    execution_time_seconds INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_daily_prices_date ON fact_daily_prices(trade_date);
CREATE INDEX idx_daily_prices_stock ON fact_daily_prices(stock_id);
CREATE INDEX idx_market_indices_date ON fact_market_indices(trade_date);
CREATE INDEX idx_sector_perf_date ON fact_sector_performance(trade_date);

-- Views
CREATE OR REPLACE VIEW vw_latest_market_status AS
SELECT 
    mi.index_name,
    mi.index_value,
    mi.index_change,
    mi.index_change_pct,
    ms.total_trades,
    ms.total_volume,
    ms.total_turnover_lkr,
    ms.advancing_stocks,
    ms.declining_stocks,
    mi.trade_date
FROM fact_market_indices mi
LEFT JOIN fact_market_summary ms ON mi.trade_date = ms.trade_date
WHERE mi.trade_date = (SELECT MAX(trade_date) FROM fact_market_indices)
ORDER BY mi.index_name;

CREATE OR REPLACE VIEW vw_top_gainers AS
SELECT 
    s.symbol,
    s.company_name,
    s.sector,
    p.close_price,
    p.price_change,
    p.price_change_pct,
    p.volume,
    p.trade_date
FROM fact_daily_prices p
JOIN dim_stocks s ON p.stock_id = s.stock_id
WHERE p.trade_date = (SELECT MAX(trade_date) FROM fact_daily_prices)
  AND p.price_change_pct > 0
ORDER BY p.price_change_pct DESC
LIMIT 10;

CREATE OR REPLACE VIEW vw_top_losers AS
SELECT 
    s.symbol,
    s.company_name,
    s.sector,
    p.close_price,
    p.price_change,
    p.price_change_pct,
    p.volume,
    p.trade_date
FROM fact_daily_prices p
JOIN dim_stocks s ON p.stock_id = s.stock_id
WHERE p.trade_date = (SELECT MAX(trade_date) FROM fact_daily_prices)
  AND p.price_change_pct < 0
ORDER BY p.price_change_pct ASC
LIMIT 10;

CREATE OR REPLACE VIEW vw_most_active AS
SELECT 
    s.symbol,
    s.company_name,
    s.sector,
    p.close_price,
    p.volume,
    p.turnover_lkr,
    p.trade_date
FROM fact_daily_prices p
JOIN dim_stocks s ON p.stock_id = s.stock_id
WHERE p.trade_date = (SELECT MAX(trade_date) FROM fact_daily_prices)
ORDER BY p.turnover_lkr DESC
LIMIT 10;

-- Insert Sample Data
INSERT INTO dim_sectors (sector_name) VALUES
('Banking, Finance and Insurance'),
('Manufacturing'),
('Diversified Holdings'),
('Hotels and Travels'),
('Power and Energy'),
('Telecommunications'),
('Land and Property'),
('Stores and Supplies');

INSERT INTO dim_stocks (symbol, company_name, sector) VALUES
('COMB.N0000', 'Commercial Bank of Ceylon PLC', 'Banking, Finance and Insurance'),
('HNB.N0000', 'Hatton National Bank PLC', 'Banking, Finance and Insurance'),
('SAMP.N0000', 'Sampath Bank PLC', 'Banking, Finance and Insurance'),
('JKH.N0000', 'John Keells Holdings PLC', 'Diversified Holdings'),
('DIAL.N0000', 'Dialog Axiata PLC', 'Telecommunications'),
('CTC.N0000', 'Ceylon Tobacco Company PLC', 'Manufacturing'),
('LOLC.N0000', 'LOLC Holdings PLC', 'Banking, Finance and Insurance'),
('NDB.N0000', 'National Development Bank PLC', 'Banking, Finance and Insurance'),
('DFCC.N0000', 'DFCC Bank PLC', 'Banking, Finance and Insurance'),
('CIC.N0000', 'CIC Holdings PLC', 'Diversified Holdings');

SELECT 'Database schema created successfully!' AS status;
