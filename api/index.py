from flask import Flask, request, Response
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__)

@app.route('/')
def home():
    """
    Main route that serves the Streamlit app
    """
    try:
        # Import and run the main app logic
        from app import *

        # Return a simple response for now
        return """
        <html>
        <head>
            <title>Stock Analysis Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { color: #1f77b4; }
                .status { background: #e8f5e8; border: 1px solid #4caf50; padding: 20px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📈 Professional Stock Analysis Dashboard</h1>
                <div class="status">
                    <h2>✅ App Deployed Successfully!</h2>
                    <p>The Stock Analysis Dashboard is now running on Vercel.</p>
                    <p><strong>Note:</strong> This is a simplified version for Vercel deployment.</p>
                    <p>For full Streamlit functionality, consider using Streamlit Cloud or Railway.</p>
                </div>
                <p><a href="https://github.com/hungdotnet/chart_stock" target="_blank">View Source Code</a></p>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
        <body>
            <h1>Error</h1>
            <p>{str(e)}</p>
        </body>
        </html>
        """, 500

# Vercel expects this for serverless functions
def handler(event, context):
    """
    Vercel serverless function handler
    """
    with app.app_context():
        return home()

# For local development
if __name__ == "__main__":
    app.run(debug=True, port=8000)