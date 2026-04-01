-- PostgreSQL Database Setup for Stock Analysis App

-- Create database
CREATE DATABASE stock_db;

-- Connect to the database
-- \c stock_db;

-- Create stock table
CREATE TABLE IF NOT EXISTS stock (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(10, 2),
    high NUMERIC(10, 2),
    low NUMERIC(10, 2),
    close NUMERIC(10, 2) NOT NULL,
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticker, date)
);

-- Create index for faster queries
CREATE INDEX idx_ticker_date ON stock(ticker, date DESC);
CREATE INDEX idx_ticker ON stock(ticker);

-- Sample data insert (replace with real data)
INSERT INTO stock (ticker, date, open, high, low, close, volume) VALUES
('AAPL', '2026-03-20', 175.50, 176.80, 175.00, 176.20, 50000000),
('AAPL', '2026-03-21', 176.20, 177.50, 176.00, 177.00, 52000000),
('AAPL', '2026-03-22', 177.00, 178.20, 176.80, 177.80, 51000000),
('AAPL', '2026-03-23', 177.80, 179.00, 177.50, 178.90, 53000000),
('AAPL', '2026-03-24', 178.90, 180.00, 178.50, 179.50, 55000000),
('AAPL', '2026-03-25', 179.50, 180.50, 179.00, 180.20, 54000000),
('AAPL', '2026-03-26', 180.20, 181.00, 179.80, 180.80, 52000000),
('AAPL', '2026-03-27', 180.80, 182.00, 180.50, 181.50, 56000000),
('AAPL', '2026-03-28', 181.50, 182.50, 181.00, 182.00, 54000000),
('AAPL', '2026-03-29', 182.00, 183.00, 181.80, 182.80, 57000000),
('AAPL', '2026-03-30', 182.80, 184.00, 182.50, 183.50, 58000000),
('AAPL', '2026-03-31', 183.50, 184.50, 183.00, 184.00, 59000000)
ON CONFLICT (ticker, date) DO NOTHING;

-- Verify data
SELECT * FROM stock WHERE ticker = 'AAPL' ORDER BY date DESC LIMIT 10;
