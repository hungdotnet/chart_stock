import yfinance as yf
import pandas as pd

# Test download
print("Downloading AAPL data...")
df = yf.download("AAPL", period="1mo", interval="1d")
print("Data shape:", df.shape)

if not df.empty:
    print("Getting latest close...")
    latest_close = df["Close"].iloc[-1].item()
    print(f"Latest close type: {type(latest_close)}, value: {latest_close}")
    print(f"Formatted: {latest_close:.2f}")
    print("✓ Test passed!")
else:
    print("No data downloaded")
