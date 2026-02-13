"""CSE Market Intelligence Dashboard - Simplified & Working"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
import pandas as pd
from datetime import datetime
from src.utils import get_engine

st.set_page_config(page_title="CSE Market Intelligence", page_icon="📈", layout="wide")
st.title("📈 CSE Market Intelligence Dashboard")

@st.cache_resource
def get_db_engine():
    return get_engine()

engine = get_db_engine()

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Market Overview", "📊 Stock Explorer", "🏭 Sectors"])

if st.sidebar.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()

try:
    last_update = pd.read_sql("SELECT MAX(trade_date) as last_date FROM fact_daily_prices", engine)['last_date'].iloc[0]
    st.sidebar.info(f"**Last Update:** {last_update}")
except:
    st.sidebar.info("**Last Update:** N/A")

# PAGE: MARKET OVERVIEW
if page == "🏠 Market Overview":
    st.header("Market Overview")
    
    try:
        indices = pd.read_sql("SELECT * FROM vw_latest_market_status ORDER BY index_name", engine)
        
        if not indices.empty:
            cols = st.columns(len(indices))
            for idx, row in indices.iterrows():
                with cols[idx]:
                    delta = f"{row['index_change_pct']:+.2f}%"
                    st.metric(row['index_name'], f"{row['index_value']:.2f}", delta)
            
            st.subheader("Market Summary")
            row = indices.iloc[0]
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Trades", f"{row.get('total_trades', 0):,}")
            col2.metric("Total Volume", f"{row.get('total_volume', 0):,}")
            col3.metric("Turnover (LKR)", f"{row.get('total_turnover_lkr', 0):,.0f}")
            adv = row.get('advancing_stocks', 0)
            dec = row.get('declining_stocks', 0)
            col4.metric("Adv/Dec", f"{adv}/{dec}")
        
        st.subheader("Top Movers")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Gainers**")
            gainers = pd.read_sql("SELECT * FROM vw_top_gainers LIMIT 5", engine)
            if not gainers.empty:
                st.dataframe(gainers[['symbol', 'company_name', 'close_price', 'price_change_pct']], hide_index=True)
        
        with col2:
            st.markdown("**Top Losers**")
            losers = pd.read_sql("SELECT * FROM vw_top_losers LIMIT 5", engine)
            if not losers.empty:
                st.dataframe(losers[['symbol', 'company_name', 'close_price', 'price_change_pct']], hide_index=True)
        
        st.subheader("Most Active")
        active = pd.read_sql("SELECT * FROM vw_most_active LIMIT 10", engine)
        if not active.empty:
            st.dataframe(active[['symbol', 'company_name', 'volume', 'turnover_lkr']], hide_index=True)
    
    except Exception as e:
        st.error(f"Error: {e}")

# PAGE: STOCK EXPLORER
elif page == "📊 Stock Explorer":
    st.header("Stock Explorer")
    
    try:
        query = """
        SELECT s.symbol, s.company_name, s.sector, p.close_price, p.price_change_pct, p.volume
        FROM dim_stocks s
        LEFT JOIN fact_daily_prices p ON s.stock_id = p.stock_id
        WHERE p.trade_date = (SELECT MAX(trade_date) FROM fact_daily_prices)
        ORDER BY p.turnover_lkr DESC
        """
        stocks = pd.read_sql(query, engine)
        
        if not stocks.empty:
            col1, col2 = st.columns(2)
            with col1:
                sectors = ['All'] + sorted(stocks['sector'].dropna().unique().tolist())
                selected_sector = st.selectbox("Sector", sectors)
            with col2:
                min_change = st.number_input("Min % Change", value=-100.0)
            
            filtered = stocks.copy()
            if selected_sector != 'All':
                filtered = filtered[filtered['sector'] == selected_sector]
            filtered = filtered[filtered['price_change_pct'] >= min_change]
            
            st.subheader(f"Results ({len(filtered)} stocks)")
            st.dataframe(filtered, hide_index=True, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error: {e}")

# PAGE: SECTORS
elif page == "🏭 Sectors":
    st.header("Sector Analysis")
    
    try:
        query = """
        SELECT s.sector_name, sp.sector_index, sp.sector_change_pct, sp.total_turnover_lkr
        FROM fact_sector_performance sp
        JOIN dim_sectors s ON sp.sector_id = s.sector_id
        WHERE sp.trade_date = (SELECT MAX(trade_date) FROM fact_sector_performance)
        ORDER BY sp.total_turnover_lkr DESC
        """
        sectors = pd.read_sql(query, engine)
        
        if not sectors.empty:
            st.dataframe(sectors, hide_index=True, use_container_width=True)
            st.bar_chart(sectors.set_index('sector_name')['sector_change_pct'])
    
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.markdown(f"<div style='text-align:center;color:gray'>CSE Market Intelligence © {datetime.now().year}</div>", unsafe_allow_html=True)
