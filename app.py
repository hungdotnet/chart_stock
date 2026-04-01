import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': '''
        # Stock Analysis Dashboard
        Professional stock analysis tool with PostgreSQL integration.
        Features: Candlestick charts, Ichimoku indicators, RSI, MACD analysis.
        '''
    }
)

# Custom CSS for better styling
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<style>
    .main-header {
        @apply text-4xl font-bold text-center mb-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent;
    }
    .metric-card {
        @apply bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg p-4 my-2 border-l-4 border-blue-500 shadow-sm hover:shadow-md transition-shadow duration-200;
    }
    .sidebar-section {
        @apply bg-gray-50 p-4 rounded-lg my-4 border border-gray-200;
    }
    .chart-container {
        @apply bg-white rounded-lg p-4 shadow-lg my-4 border border-gray-100;
    }
    .stButton>button {
        @apply bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-md hover:shadow-lg;
    }
    .stTextInput>div>div>input {
        @apply border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200;
    }
    .stSelectbox>div>div>select {
        @apply border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200;
    }
    .stSlider>div>div>div {
        @apply text-blue-600;
    }
    .stExpander {
        @apply border border-gray-200 rounded-lg shadow-sm;
    }
    .stExpander:hover {
        @apply shadow-md transition-shadow duration-200;
    }
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        @apply bg-gray-100;
    }
    ::-webkit-scrollbar-thumb {
        @apply bg-blue-500 rounded-full;
    }
    ::-webkit-scrollbar-thumb:hover {
        @apply bg-blue-600;
    }
</style>
""", unsafe_allow_html=True)

# Main title with better styling
st.markdown('<h1 class="main-header">📈 Professional Stock Analysis Dashboard</h1>', unsafe_allow_html=True)

# Subtitle and description
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="text-center py-4 bg-gray-50 rounded-lg mb-8">
        <h3 class="text-gray-700 text-xl font-semibold mb-2">Advanced Technical Analysis Platform</h3>
        <p class="text-gray-500 text-sm">Real-time stock data analysis with PostgreSQL integration</p>
    </div>
    """, unsafe_allow_html=True)

st.title("📊 Stock Analysis Dashboard (PostgreSQL)")

# Sidebar with better organization
st.sidebar.markdown("""
<div class="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg mb-4 border border-blue-200">
    <h2 class="text-blue-800 text-lg font-bold mb-2">🎛️ Control Panel</h2>
    <p class="text-blue-600 text-sm">Configure your analysis parameters</p>
</div>
""", unsafe_allow_html=True)

# Database Configuration Section
with st.sidebar.expander("🔧 Database Configuration", expanded=True):
    st.markdown("**Connection Settings**")
    col1, col2 = st.columns(2)
    with col1:
        db_host = st.text_input("Host", "14.225.217.46", help="Database server address")
    with col2:
        db_port = st.number_input("Port", value=5432, step=1, help="Database port number")

    col1, col2 = st.columns(2)
    with col1:
        db_name = st.text_input("Database", "n8n", help="Database name")
    with col2:
        db_user = st.text_input("Username", "n8n", help="Database username")

    db_password = st.text_input("Password", "Hungnet@100204", type="password", help="Database password")
    db_table = st.text_input("Table", "stock", help="Data table name")

    # Test connection button with better styling
    if st.button("🔗 Test Database Connection", use_container_width=True):
        with st.spinner("Testing connection..."):
            try:
                conn = psycopg2.connect(
                    host=db_host,
                    port=int(db_port),
                    database=db_name,
                    user=db_user,
                    password=db_password
                )
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                conn.close()
                st.success("✅ Database connection successful!")
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)[:100]}...")

# Data Query Section
with st.sidebar.expander("📊 Data Selection", expanded=True):
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**Stock Parameters**")
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.text_input("Stock Symbol", "VNINDEX", help="Enter stock ticker symbol")
    with col2:
        days = st.slider("Time Period (Days)", 30, 365, 300, help="Number of days of historical data")
    st.markdown('</div>', unsafe_allow_html=True)

# Technical Analysis Section
with st.sidebar.expander("📈 Technical Indicators", expanded=True):
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("**Primary Indicator**")
    indicator_option = st.selectbox(
        "Main Indicator",
        ["MA20", "MA50", "Ichimoku"],
        index=2,
        help="Select primary technical indicator"
    )

    st.markdown("**Additional Indicators**")
    extra_indicators = st.multiselect(
        "Extra Indicators",
        ["RSI", "MACD"],
        default=["RSI", "MACD"],
        help="Select additional technical indicators"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer in sidebar
st.sidebar.markdown("""
<div class="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-lg mt-4 border border-green-200">
    <h3 class="text-green-800 text-lg font-semibold mb-2">📊 Dashboard Info</h3>
    <div class="text-green-700 text-sm">
        <p class="mb-1">Built with Streamlit & PostgreSQL</p>
        <p class="font-medium">Version 2.0 - Professional Edition</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Connect to PostgreSQL and fetch data
@st.cache_data
def load_data_from_postgres(host, port, database, user, password, table, ticker, days):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Fetch data from the last N days for the ticker
        query = sql.SQL("""
            SELECT * FROM {table}
            WHERE ticker = %s
            AND date >= NOW() - INTERVAL %s
            ORDER BY date ASC
        """).format(table=sql.Identifier(table))
        
        cursor.execute(query, (ticker, f'{days} days'))
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if data:
            df = pd.DataFrame(data, columns=columns)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            
            # Convert numeric columns to float to avoid decimal.Decimal issues
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = df[col].astype(float)
            
            return df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        error_msg = str(e)
        if "connection" in error_msg.lower() or "connect" in error_msg.lower():
            st.error("❌ **Database Connection Failed**")
            st.info("**Possible solutions:**\n- Check if PostgreSQL is running\n- Verify database credentials\n- Ensure correct host/port\n- For Docker: run `docker-compose up -d`")
        elif "relation" in error_msg.lower() or "table" in error_msg.lower():
            st.error("❌ **Table Not Found**")
            st.info(f"**Table '{table}' does not exist.**\nRun setup scripts to create the table.")
        else:
            st.error(f"❌ **Database Error:** {error_msg}")
        return pd.DataFrame()

df = load_data_from_postgres(db_host, db_port, db_name, db_user, db_password, db_table, ticker, days)

if df.empty:
    st.warning(f"⚠️ No data found for {ticker} in the last {days} days.")
    
    # Show debug info
    with st.expander("🔍 Debug Information"):
        st.write("**Database Config:**")
        st.json({
            "host": db_host,
            "port": db_port,
            "database": db_name,
            "user": db_user,
            "table": db_table,
            "ticker": ticker,
            "days": days
        })
        
        st.write("**Setup Instructions:**")
        st.markdown("""
        **For Local PostgreSQL:**
        - Database: `stock_db`, User: `postgres`
        - Run: `python test_postgres.py`

        **For Docker PostgreSQL (from docker-compose.yml):**
        - Database: `n8n`, User: `n8n`, Password: your POSTGRES_PASSWORD
        - Run: `python test_docker_postgres.py`

        **Table Structure Required:**
        - `id` (SERIAL), `ticker` (VARCHAR), `date` (DATE), `open`/`high`/`low`/`close` (NUMERIC), `volume` (BIGINT)
        """)
else:
    # Metrics
    latest_close = float(df["close"].iloc[-1]) if "close" in df.columns else float(df.iloc[-1, -1])
    
    # Handle case where there's only 1 row of data
    if len(df) >= 2:
        prev_close = float(df["close"].iloc[-2]) if "close" in df.columns else float(df.iloc[-2, -1])
        change = latest_close - prev_close
        change_pct = (change / prev_close) * 100
    else:
        prev_close = latest_close
        change = 0.0
        change_pct = 0.0
    
    volume = int(df["volume"].iloc[-1]) if "volume" in df.columns else int(df.iloc[-1, -1])

    # Define close column for calculations
    close_col = "close" if "close" in df.columns else df.columns[-1]

    # Professional metrics display
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 class="text-blue-600 font-semibold mb-2">Latest Price</h4>
            <h2 class="text-green-600 text-2xl font-bold">${:.2f}</h2>
        </div>
        """.format(latest_close), unsafe_allow_html=True)

    with col2:
        delta_color = "text-green-600" if change >= 0 else "text-red-600"
        st.markdown("""
        <div class="metric-card">
            <h4 class="text-blue-600 font-semibold mb-2">Daily Change</h4>
            <h2 class="{} text-2xl font-bold">${:.2f}</h2>
            <p class="{} text-sm">({:.2f}%)</p>
        </div>
        """.format(delta_color, change, delta_color, change_pct), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4 class="text-blue-600 font-semibold mb-2">Volume</h4>
            <h2 class="text-purple-600 text-2xl font-bold">{:,}</h2>
        </div>
        """.format(int(volume)), unsafe_allow_html=True)

    with col4:
        # Calculate additional metrics
        high_52w = df["high"].max() if "high" in df.columns else latest_close
        low_52w = df["low"].min() if "low" in df.columns else latest_close
        volatility = df[close_col].pct_change().std() * 100 if len(df) > 1 else 0

        st.markdown("""
        <div class="metric-card">
            <h4 class="text-blue-600 font-semibold mb-2">Volatility</h4>
            <h2 class="text-orange-600 text-2xl font-bold">{:.1f}%</h2>
        </div>
        """.format(volatility), unsafe_allow_html=True)

    # Additional info row
    st.markdown("### 📈 Market Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**52W High:** ${high_52w:.2f}")
    with col2:
        st.info(f"**52W Low:** ${low_52w:.2f}")
    with col3:
        data_points = len(df)
        st.info(f"**Data Points:** {data_points:,}")

    # Moving averages - use close column
    # close_col already defined above
    
    # Only calculate moving averages if we have enough data
    if len(df) >= 50:
        df["MA20"] = df[close_col].rolling(window=20).mean()
        df["MA50"] = df[close_col].rolling(window=50).mean()
    elif len(df) >= 20:
        df["MA20"] = df[close_col].rolling(window=20).mean()
        df["MA50"] = None  # Not enough data for MA50
    else:
        df["MA20"] = None  # Not enough data for MA20
        df["MA50"] = None  # Not enough data for MA50

    # Ichimoku components
    if "high" in df.columns and "low" in df.columns and "close" in df.columns:
        df["tenkan_sen"] = (df["high"].rolling(9).max() + df["low"].rolling(9).min()) / 2
        df["kijun_sen"] = (df["high"].rolling(17).max() + df["low"].rolling(17).min()) / 2
        df["senkou_span_a"] = ((df["tenkan_sen"] + df["kijun_sen"]) / 2).shift(26)
        df["senkou_span_b"] = ((df["high"].rolling(52).max() + df["low"].rolling(52).min()) / 2).shift(26)
        df["chikou_span"] = df["close"].shift(-26)
        # Additional DG lines
        df["DG65"] = (df["high"].rolling(65).max() + df["low"].rolling(65).min()) / 2
        df["DG129"] = (df["high"].rolling(129).max() + df["low"].rolling(129).min()) / 2

    # RSI and MACD calculations
    try:
        delta = df[close_col].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=14, min_periods=14).mean()
        avg_loss = loss.rolling(window=14, min_periods=14).mean()
        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))

        exp12 = df[close_col].ewm(span=12, adjust=False).mean()
        exp26 = df[close_col].ewm(span=26, adjust=False).mean()
        df["MACD"] = exp12 - exp26
        df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
        df["MACD_hist"] = df["MACD"] - df["MACD_signal"]
    except Exception:
        df["RSI"] = None
        df["MACD"] = None
        df["MACD_signal"] = None
        df["MACD_hist"] = None

    # Chart section with professional styling
    st.markdown("### 📊 Technical Analysis Chart")
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Chart
    st.subheader(f"📈 {ticker} - {indicator_option} Analysis")

    # Prepare data for mplfinance (ensure we have OHLC columns)
    chart_df = df.copy()
    
    # Ensure column names are in the format mplfinance expects
    if 'open' in chart_df.columns and 'high' in chart_df.columns and 'low' in chart_df.columns and 'close' in chart_df.columns:
        # Rename columns to standard OHLC format if needed
        ohlc_df = chart_df[['open', 'high', 'low', 'close']].copy()
        
        # Convert decimal.Decimal to float for mplfinance compatibility
        ohlc_df = ohlc_df.astype(float)
        
        if 'volume' in chart_df.columns:
            ohlc_df['volume'] = chart_df['volume'].astype(float)
        
        # Prepare additional plots based on selected indicator
        ap = []
        if indicator_option == "MA20" and "MA20" in chart_df.columns and chart_df["MA20"].notna().any():
            ma20_data = chart_df["MA20"].astype(float)
            ap.append(mpf.make_addplot(ma20_data, color='blue', width=1.5, alpha=0.7, label='MA20'))
        elif indicator_option == "MA50" and "MA50" in chart_df.columns and chart_df["MA50"].notna().any():
            ma50_data = chart_df["MA50"].astype(float)
            ap.append(mpf.make_addplot(ma50_data, color='red', width=1.5, alpha=0.7, label='MA50'))
        elif indicator_option == "Ichimoku":
            if chart_df["tenkan_sen"].notna().any():
                ap.append(mpf.make_addplot(chart_df["tenkan_sen"].astype(float), color='cyan', width=1, label='Tenkan-sen'))
            if chart_df["kijun_sen"].notna().any():
                ap.append(mpf.make_addplot(chart_df["kijun_sen"].astype(float), color='magenta', width=1, label='Kijun-sen'))
            if chart_df["senkou_span_a"].notna().any():
                ap.append(mpf.make_addplot(chart_df["senkou_span_a"].astype(float), color='green', width=1, alpha=0.6, label='Senkou Span A'))
            if chart_df["senkou_span_b"].notna().any():
                ap.append(mpf.make_addplot(chart_df["senkou_span_b"].astype(float), color='orange', width=1, alpha=0.6, label='Senkou Span B'))
            if chart_df["chikou_span"].notna().any():
                ap.append(mpf.make_addplot(chart_df["chikou_span"].astype(float), color='purple', width=1, alpha=0.6, label='Chikou Span'))
            # Add DG lines with thick width
            if chart_df["DG65"].notna().any():
                ap.append(mpf.make_addplot(chart_df["DG65"].astype(float), color='gold', width=3, alpha=0.8, label='DG65'))
            if chart_df["DG129"].notna().any():
                ap.append(mpf.make_addplot(chart_df["DG129"].astype(float), color='red', width=3, alpha=0.8, label='DG129'))
            # Fill between Span A and Span B
            if chart_df["senkou_span_a"].notna().any() and chart_df["senkou_span_b"].notna().any():
                # Use a single color for the cloud - green when bullish, red when bearish
                span_a = chart_df["senkou_span_a"].astype(float)
                span_b = chart_df["senkou_span_b"].astype(float)
                # Determine overall cloud color based on current Span A vs Span B
                current_a = span_a.iloc[-1] if not span_a.empty else 0
                current_b = span_b.iloc[-1] if not span_b.empty else 0
                cloud_color = 'lightgreen' if current_a > current_b else 'lightcoral'
                ap.append(mpf.make_addplot(span_a, fill_between=dict(y1=span_a.values, y2=span_b.values, color=cloud_color, alpha=0.2)))

        # Add extra indicators to mpf panels
        # panel 0 = price chart, panel 1 = volume (auto with volume=True)
        # Dynamic panel assignment for extra indicators
        next_panel = 2
        if "RSI" in extra_indicators and "RSI" in chart_df.columns and chart_df["RSI"].notna().any():
            ap.append(mpf.make_addplot(chart_df["RSI"].astype(float), panel=next_panel, color='purple', ylabel='RSI', ylim=(0,100)))
            next_panel += 1
        if "MACD" in extra_indicators and "MACD" in chart_df.columns and chart_df["MACD"].notna().any():
            ap.append(mpf.make_addplot(chart_df["MACD"].astype(float), panel=next_panel, color='blue', ylabel='MACD'))
            ap.append(mpf.make_addplot(chart_df["MACD_signal"].astype(float), panel=next_panel, color='red'))
            # Color histogram bars based on positive/negative values
            colors = ['green' if x >= 0 else 'red' for x in chart_df["MACD_hist"]]
            ap.append(mpf.make_addplot(chart_df["MACD_hist"].astype(float), type='bar', panel=next_panel, color=colors, alpha=0.7))

        # Create candlestick chart
        fig, axlist = mpf.plot(ohlc_df, type='candle', style='charles', volume=True, 
                              addplot=ap, figsize=(12, 8), returnfig=True)
        
        # Set title
        axlist[0].set_title(f"{ticker} Candlestick Chart", fontsize=16)
        
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Fallback to line chart if OHLC data is not available
        st.warning("⚠️ OHLC data not available. Showing line chart instead.")

        extra_count = 0
        if "RSI" in extra_indicators:
            extra_count += 1
        if "MACD" in extra_indicators:
            extra_count += 1

        if extra_count == 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            axes = [ax]
        else:
            fig, axes = plt.subplots(nrows=1 + extra_count, figsize=(12, 6 * (1 + extra_count)), sharex=True)
            if not isinstance(axes, (list, np.ndarray)):
                axes = [axes]

        main_ax = axes[0]
        main_ax.plot(chart_df.index, chart_df[close_col], label="Close", linewidth=2)

        if indicator_option == "MA20" and "MA20" in chart_df.columns and chart_df["MA20"].notna().any():
            main_ax.plot(chart_df.index, chart_df["MA20"], label="MA20", linewidth=1.5, alpha=0.7)
        if indicator_option == "MA50" and "MA50" in chart_df.columns and chart_df["MA50"].notna().any():
            main_ax.plot(chart_df.index, chart_df["MA50"], label="MA50", linewidth=1.5, alpha=0.7)
        if indicator_option == "Ichimoku":
            for line in ["tenkan_sen", "kijun_sen", "senkou_span_a", "senkou_span_b", "chikou_span"]:
                if line in chart_df.columns and chart_df[line].notna().any():
                    main_ax.plot(chart_df.index, chart_df[line], label=line.replace("_", " ").title(), linewidth=1, alpha=0.6)
            # Add DG lines with thick width
            if "DG65" in chart_df.columns and chart_df["DG65"].notna().any():
                main_ax.plot(chart_df.index, chart_df["DG65"], label="DG65", linewidth=3, color='gold', alpha=0.8)
            if "DG129" in chart_df.columns and chart_df["DG129"].notna().any():
                main_ax.plot(chart_df.index, chart_df["DG129"], label="DG129", linewidth=3, color='red', alpha=0.8)
            # Fill between Span A and Span B
            if "senkou_span_a" in chart_df.columns and "senkou_span_b" in chart_df.columns and chart_df["senkou_span_a"].notna().any() and chart_df["senkou_span_b"].notna().any():
                span_a = chart_df["senkou_span_a"]
                span_b = chart_df["senkou_span_b"]
                # Use single color based on current Span A vs Span B
                current_a = span_a.iloc[-1] if not span_a.empty else 0
                current_b = span_b.iloc[-1] if not span_b.empty else 0
                cloud_color = 'lightgreen' if current_a > current_b else 'lightcoral'
                main_ax.fill_between(chart_df.index, span_a, span_b, color=cloud_color, alpha=0.2)

        main_ax.set_title(f"{ticker} Price Chart")
        main_ax.set_ylabel("Price")
        main_ax.legend()
        main_ax.grid(True, alpha=0.3)

        idx = 1
        if "RSI" in extra_indicators and "RSI" in chart_df.columns and chart_df["RSI"].notna().any():
            rsi_ax = axes[idx]
            rsi_ax.plot(chart_df.index, chart_df["RSI"], label="RSI", color="purple")
            rsi_ax.axhline(70, color="red", linestyle="--", linewidth=0.8)
            rsi_ax.axhline(30, color="green", linestyle="--", linewidth=0.8)
            rsi_ax.set_ylabel("RSI")
            rsi_ax.legend()
            rsi_ax.grid(True, alpha=0.3)
            idx += 1

        if "MACD" in extra_indicators and "MACD" in chart_df.columns and chart_df["MACD"].notna().any():
            macd_ax = axes[idx]
            macd_ax.plot(chart_df.index, chart_df["MACD"], label="MACD", color="blue")
            if "MACD_signal" in chart_df.columns and chart_df["MACD_signal"].notna().any():
                macd_ax.plot(chart_df.index, chart_df["MACD_signal"], label="Signal", color="red")
            if "MACD_hist" in chart_df.columns and chart_df["MACD_hist"].notna().any():
                # Color bars based on positive/negative values
                colors = ['green' if x >= 0 else 'red' for x in chart_df["MACD_hist"]]
                for i, (x, y) in enumerate(zip(chart_df.index, chart_df["MACD_hist"])):
                    macd_ax.bar(x, y, color=colors[i], alpha=0.7, width=1)
            macd_ax.set_ylabel("MACD")
            macd_ax.legend()
            macd_ax.grid(True, alpha=0.3)

        fig.autofmt_xdate()
        st.pyplot(fig)

    # Professional data analysis section
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Recent Data")
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.dataframe(df.tail(20), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 📊 Statistical Summary")
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.dataframe(df.describe(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Additional analysis section
    st.markdown("### 🔍 Advanced Analytics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Price Distribution**")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(df[close_col].dropna(), bins=30, alpha=0.7, color='#1f77b4', edgecolor='black')
        ax.set_title('Price Distribution', fontsize=12)
        ax.set_xlabel('Price')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with col2:
        st.markdown("**Daily Returns**")
        fig, ax = plt.subplots(figsize=(6, 4))
        returns = df[close_col].pct_change().dropna()
        ax.hist(returns, bins=30, alpha=0.7, color='#28a745', edgecolor='black')
        ax.set_title('Daily Returns Distribution', fontsize=12)
        ax.set_xlabel('Return %')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with col3:
        st.markdown("**Volume Analysis**")
        if "volume" in df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(df.index[-20:], df["volume"].tail(20), alpha=0.7, color='#6f42c1')
            ax.set_title('Recent Volume', fontsize=12)
            ax.set_ylabel('Volume')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        else:
            st.info("Volume data not available")

# Professional footer
st.markdown("---")
st.markdown("""
<div class="text-center py-8 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg mt-8">
    <h4 class="text-gray-700 text-xl font-semibold mb-4">🚀 Professional Stock Analysis Dashboard</h4>
    <p class="text-gray-500 mb-2">
        Built with ❤️ using Streamlit & PostgreSQL | 
        <a href="#" class="text-blue-500 hover:text-blue-700 no-underline">Documentation</a> | 
        <a href="#" class="text-blue-500 hover:text-blue-700 no-underline">Support</a>
    </p>
    <p class="text-gray-500 text-sm">
        Version 2.0 - Advanced Technical Analysis Platform
    </p>
</div>
""", unsafe_allow_html=True)