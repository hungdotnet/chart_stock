# 📈 Professional Stock Analysis Dashboard

A modern, professional stock analysis dashboard built with Streamlit, PostgreSQL, and Tailwind CSS. Features advanced technical indicators and real-time data visualization.

## 🚀 Features

- **Technical Indicators**: Ichimoku (with DG65/DG129 lines), RSI, MACD with histogram
- **Modern UI**: Clean Tailwind CSS interface with professional styling
- **PostgreSQL Integration**: Real-time data from PostgreSQL database
- **Advanced Analytics**: Statistical summaries and data visualization
- **Responsive Design**: Mobile-friendly interface with hover effects

## 🛠️ Tech Stack

- **Frontend**: Streamlit with Tailwind CSS
- **Backend**: Python 3.9+
- **Database**: PostgreSQL
- **Visualization**: Matplotlib, mplfinance
- **Deployment**: Vercel (Serverless)

## 📋 Prerequisites

- Python 3.9 or higher
- PostgreSQL database
- Git

## 🚀 Local Development

1. **Clone the repository**

   ```bash
   git clone https://github.com/hungdotnet/chart_stock.git
   cd chart_stock
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🌐 Vercel Deployment

### Option 1: Direct GitHub Integration

1. Go to [Vercel](https://vercel.com)
2. Click "New Project"
3. Import from GitHub: `hungdotnet/chart_stock`
4. Configure build settings:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: `./`
5. Add environment variables (if needed)
6. Deploy!

### Option 2: Manual Deployment

1. **Install Vercel CLI**

   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

## 🔧 Configuration

### Database Setup

Create a PostgreSQL table with the following structure:

```sql
CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(50),
    date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT
);
```

### Environment Variables

For production deployment, set these environment variables in Vercel:

- `DB_HOST`: Database host
- `DB_PORT`: Database port (default: 5432)
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password

## 📊 Usage

1. **Database Configuration**: Set up your PostgreSQL connection in the sidebar
2. **Data Selection**: Choose stock symbol and time period
3. **Technical Indicators**: Select primary and additional indicators
4. **Analysis**: View charts, metrics, and analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**hungdotnet** - [GitHub](https://github.com/hungdotnet)

## 🙏 Acknowledgments

- Streamlit for the amazing web app framework
- Tailwind CSS for modern styling
- mplfinance for financial charting
- PostgreSQL for reliable data storage
