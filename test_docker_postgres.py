"""
Test PostgreSQL connection with Docker container
Run this script to verify the database setup with Docker
"""

import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import random

def create_connection():
    """Connect to PostgreSQL in Docker"""
    try:
        conn = psycopg2.connect(
            host="localhost",  # or the IP of your Docker host
            port=5432,
            database="n8n",  # from docker-compose.yml
            user="n8n",      # from docker-compose.yml
            password="${POSTGRES_PASSWORD}"  # from docker-compose.yml
        )
        print("✓ Connected to PostgreSQL (Docker)")
        return conn
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("Note: Make sure PostgreSQL container is running and POSTGRES_PASSWORD is set")
        return None

def create_stock_table(conn):
    """Create stock table if it doesn't exist"""
    try:
        cursor = conn.cursor()

        # Create stock table
        cursor.execute("""
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
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticker_date ON stock(ticker, date DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticker ON stock(ticker);")

        conn.commit()
        print("✓ Stock table created successfully")
        cursor.close()
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        conn.rollback()

def insert_sample_data(conn):
    """Insert sample stock data"""
    try:
        cursor = conn.cursor()

        # Generate sample data for AAPL
        base_price = 180.0
        for i in range(30):
            date = datetime.now().date() - timedelta(days=30-i)
            price_change = random.uniform(-2, 2)
            close = base_price + price_change
            base_price = close

            query = sql.SQL("""
                INSERT INTO stock (ticker, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticker, date) DO NOTHING
            """)

            cursor.execute(query, (
                'AAPL',
                date,
                close - random.uniform(0.5, 1.5),
                close + random.uniform(0.5, 1.5),
                close - random.uniform(0.5, 2.0),
                close,
                random.randint(40000000, 60000000)
            ))

        conn.commit()
        print(f"✓ Inserted {30} sample records")
        cursor.close()
    except Exception as e:
        print(f"✗ Insert failed: {e}")
        conn.rollback()

def verify_data(conn):
    """Verify data in database"""
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM stock WHERE ticker = 'AAPL'
        """)
        count = cursor.fetchone()[0]
        print(f"✓ Found {count} records for AAPL")

        cursor.execute("""
            SELECT date, close, volume FROM stock
            WHERE ticker = 'AAPL'
            ORDER BY date DESC
            LIMIT 5
        """)

        print("\nRecent data:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: Close=${row[1]:.2f}, Volume={row[2]:,}")

        cursor.close()
    except Exception as e:
        print(f"✗ Verify failed: {e}")

if __name__ == "__main__":
    print("PostgreSQL Test Script (Docker)")
    print("=" * 50)

    conn = create_connection()
    if conn:
        create_stock_table(conn)
        insert_sample_data(conn)
        verify_data(conn)
        conn.close()
        print("\n✓ Test completed successfully!")
        print("\nNow you can run the Streamlit app with:")
        print("  Database: n8n")
        print("  User: n8n")
        print("  Table: stock")
    else:
        print("\n✗ Test failed. Make sure:")
        print("  1. Docker containers are running (docker-compose up)")
        print("  2. POSTGRES_PASSWORD environment variable is set")
        print("  3. PostgreSQL port 5432 is accessible")
