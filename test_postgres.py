"""
Test PostgreSQL connection and insert sample data
Run this script to verify the database setup
"""

import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import random

def create_connection():
    """Connect to PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="stock_db",
            user="postgres",
            password="postgres"
        )
        print("✓ Connected to PostgreSQL")
        return conn
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return None

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
    print("PostgreSQL Test Script")
    print("=" * 50)
    
    conn = create_connection()
    if conn:
        insert_sample_data(conn)
        verify_data(conn)
        conn.close()
        print("\n✓ Test completed successfully!")
    else:
        print("\n✗ Test failed. Make sure PostgreSQL is running.")
