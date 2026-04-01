# Stock Analysis Dashboard - PostgreSQL Setup Guide

## Prerequisites

- PostgreSQL 10+ installed and running (local or Docker)
- Python 3.8+
- Required packages: `streamlit`, `pandas`, `matplotlib`, `psycopg2-binary`

## Setup Instructions

### Option 1: Local PostgreSQL

Open PostgreSQL shell (psql) and run:

```sql
CREATE DATABASE stock_db;
\c stock_db;

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

CREATE INDEX idx_ticker_date ON stock(ticker, date DESC);
CREATE INDEX idx_ticker ON stock(ticker);
```

### Option 2: Docker PostgreSQL (from your docker-compose.yml)

If you're using the Docker setup from your `docker-compose.yml`, the PostgreSQL container is already configured.

Run the test script to create the stock table:

```bash
python test_docker_postgres.py
```

This will:

- Connect to the Docker PostgreSQL container
- Create the `stock` table
- Insert sample data
- Verify the setup

### 2. Insert Sample Data

**For Local PostgreSQL:**

```bash
psql -U postgres -d stock_db -f setup_database.sql
```

**For Docker PostgreSQL:**

```bash
python test_docker_postgres.py
```

**Using Python script (works for both):**

```bash
python test_postgres.py
```

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

### 4. Configure in the App

### 4. Configure in the App

**For Local PostgreSQL:**

- **Database Host**: `14.225.217.46`
- **Database Port**: `5432`
- **Database Name**: `n8n`
- **Database User**: `n8n`
- **Database Password**: Hungnet@100204
- **Table Name**: `stock`

**For Docker PostgreSQL:**

- **Database Host**: `localhost` (or Docker host IP)
- **Database Port**: `5432`
- **Database Name**: `n8n`
- **Database User**: `n8n`
- **Database Password**: your `${POSTGRES_PASSWORD}` value
- **Table Name**: `stock`

- **Stock Ticker**: e.g., `AAPL`, `MSFT`, `GOOGL`
- **Days of Data**: number of days to fetch (1-365)

## Data Format Required

The `stock` table must have these columns:

- `id` (SERIAL): Primary key
- `ticker` (VARCHAR): Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
- `date` (DATE): The date of the stock data
- `open` (NUMERIC): Opening price
- `high` (NUMERIC): Highest price of the day
- `low` (NUMERIC): Lowest price of the day
- `close` (NUMERIC): Closing price
- `volume` (BIGINT): Trading volume

## Common Issues

### Connection Refused

- Ensure PostgreSQL service is running
- Check if port 5432 is accessible
- Verify credentials are correct

### No Data Found

- Verify the table exists and has data
- Check that the ticker exists in the database
- Increase the "Days of Data" slider

### Import Error: psycopg2

```bash
pip install psycopg2-binary
```

## Example Insert Query

```sql
INSERT INTO stock (ticker, date, open, high, low, close, volume)
VALUES ('AAPL', '2026-04-01', 175.50, 177.00, 175.00, 176.50, 50000000);
```

## Testing Connection

**For Local PostgreSQL:**

```bash
python test_postgres.py
```

**For Docker PostgreSQL:**

```bash
python test_docker_postgres.py
```

Both scripts will verify the connection and show recent data.

## Troubleshooting

### Common Errors and Solutions

#### 1. "Database Error: 'days'"

**Cause:** SQL query parameter formatting issue (fixed in current version)
**Solution:** Update to the latest code ✅

#### 2. "Connection refused" or "No route to host"

**Cause:** PostgreSQL server not running or wrong connection details
**Solutions:**

- For local PostgreSQL: Ensure PostgreSQL service is running
- For Docker: Run `docker-compose up -d`
- Check host, port, database name, username, and password
- Use the "Test Connection" button in the sidebar

#### 3. "Relation 'stock' does not exist"

**Cause:** Database table not created
**Solutions:**

- Run `python test_postgres.py` (for local PostgreSQL)
- Run `python test_docker_postgres.py` (for Docker PostgreSQL)
- Or execute the SQL in `setup_database.sql`

#### 4. "No data found for [TICKER]"

**Cause:** No stock data in the database for the selected ticker/days
**Solutions:**

- Check if data exists: `SELECT * FROM stock WHERE ticker='AAPL' LIMIT 5;`
- Insert sample data using the test scripts
- Increase the "Days of Data" slider
- Verify ticker symbol spelling

#### 5. App shows warnings about insufficient data

**Cause:** Not enough data points for calculations
**Solution:** This is normal - the app handles it gracefully by:

- Showing change as 0% when only 1 data point
- Skipping moving averages when insufficient data (<20 points for MA20, <50 for MA50)
- Displaying available data only

### Debug Features

The app now includes:

- **Test Connection button** in sidebar to verify database connectivity
- **Detailed error messages** with specific solutions
- **Debug information panel** when no data is found
- **Graceful handling** of edge cases (insufficient data, missing columns)

### Performance Tips

- Use indexes on `ticker` and `date` columns for faster queries
- Limit data range using the "Days of Data" slider
- Database connections are properly closed automatically
