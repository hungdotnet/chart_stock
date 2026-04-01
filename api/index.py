from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    """
    Main route that returns a success page
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Stock Analysis Dashboard - Vercel Deployment</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                max-width: 800px;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
            }
            .success-icon {
                font-size: 4rem;
                color: #10b981;
                margin-bottom: 20px;
            }
            h1 {
                color: #1f2937;
                font-size: 2.5rem;
                margin-bottom: 10px;
                font-weight: 700;
            }
            .subtitle {
                color: #6b7280;
                font-size: 1.2rem;
                margin-bottom: 30px;
            }
            .status-card {
                background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
                border: 2px solid #10b981;
                border-radius: 15px;
                padding: 25px;
                margin: 20px 0;
            }
            .status-card h2 {
                color: #065f46;
                font-size: 1.5rem;
                margin-bottom: 10px;
            }
            .status-card p {
                color: #047857;
                margin-bottom: 8px;
            }
            .links {
                margin-top: 30px;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                margin: 10px;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
            .note {
                background: #fef3c7;
                border: 1px solid #f59e0b;
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                color: #92400e;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-icon">🚀</div>
            <h1>Stock Analysis Dashboard</h1>
            <p class="subtitle">Successfully Deployed on Vercel</p>

            <div class="status-card">
                <h2>✅ Deployment Successful!</h2>
                <p><strong>Status:</strong> Serverless Function Running</p>
                <p><strong>Platform:</strong> Vercel</p>
                <p><strong>Framework:</strong> Flask (Python)</p>
            </div>

            <div class="note">
                <strong>📝 Note:</strong> This is a simplified deployment for Vercel compatibility.
                For the full interactive Streamlit dashboard experience, consider deploying to:
            </div>

            <div class="links">
                <a href="https://share.streamlit.io" class="btn" target="_blank">🚀 Streamlit Cloud</a>
                <a href="https://railway.app" class="btn" target="_blank">🚂 Railway</a>
                <a href="https://render.com" class="btn" target="_blank">⚡ Render</a>
            </div>

            <div class="links">
                <a href="https://github.com/hungdotnet/chart_stock" class="btn" target="_blank" style="background: linear-gradient(135deg, #333 0%, #666 100%);">📂 View Source Code</a>
            </div>
        </div>
    </body>
    </html>
    """

# Vercel serverless function handler
def handler(event, context):
    """
    Vercel serverless function entry point
    """
    try:
        with app.app_context():
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                },
                'body': home()
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': f'{{"error": "{str(e)}", "message": "Internal server error"}}'
        }

# For local development
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)