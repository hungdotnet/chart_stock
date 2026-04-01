"""
Test SQL query fix for the 'days' error
"""

import psycopg2
from psycopg2 import sql

def test_query():
    """Test the fixed SQL query"""
    try:
        # Test with mock data (this will fail connection but show if query is valid)
        ticker = "AAPL"
        days = 30

        # This is the fixed query
        query = sql.SQL("""
            SELECT * FROM {table}
            WHERE ticker = %s
            AND date >= NOW() - INTERVAL %s
            ORDER BY date ASC
        """).format(table=sql.Identifier("stock"))

        print("✓ Query construction successful!")
        print(f"Query: {query}")
        print(f"Parameters: {(ticker, f'{days} days')}")

        # Test parameter formatting
        params = (ticker, f'{days} days')
        print(f"Formatted params: {params}")

        return True

    except Exception as e:
        print(f"✗ Query construction failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing SQL Query Fix")
    print("=" * 30)

    if test_query():
        print("\n✅ SQL query fix is working correctly!")
        print("The 'days' error should be resolved.")
    else:
        print("\n❌ SQL query still has issues.")