import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Ultimate Pro Master Scanner", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
.stApp { background-color:#0b0e14; color:white; }
.card {
    background:#161b22;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border:1px solid #30363d;
    margin-bottom:15px;
}
.top-bar {
    display:flex;
    justify-content:space-around;
    background:#1f2937;
    padding:12px;
    border-radius:10px;
    margin-bottom:20px;
}
.stock-grid {
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(100px,1fr));
    gap:6px;
}
.pos { background:#1c2a1e; color:#44cf6c; padding:8px; border-radius:6px; }
.neg { background:#2a1c1c; color:#ff7b72; padding:8px; border-radius:6px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>🎯 Ultimate Option Pro Master Scanner</h2>", unsafe_allow_html=True)

# ---------- FUNCTIONS ----------

def get_index_price(symbol):
    try:
        df = yf.download(symbol, period="5d", interval="1d", progress=False)
        if df.empty:
            return None
        return round(float(df["Close"].iloc[-1]), 2)
    except:
        return None

def get_heatmap():
    tickers = [
        "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS",
        "ICICIBANK.NS","SBIN.NS","ITC.NS","BHARTIARTL.NS",
        "LT.NS","KOTAKBANK.NS"
    ]
    try:
        df = yf.download(tickers, period="2d", interval="1d", progress=False)["Close"]
        change = ((df.iloc[-1] - df.iloc[-2]) / df.iloc[-2]) * 100
        return change
    except:
        return None

# ---------- BUTTON ----------
if st.button("🚀 START MARKET SCAN"):

    with st.spinner("Fetching market data..."):
        nifty = get_index_price("^NSEI")
        bank = get_index_price("^NSEBANK")
        vix = get_index_price("^INDIAVIX")
        heatmap = get_heatmap()

    st.success(f"✅ Scan Completed at {datetime.now().strftime('%I:%M:%S %p')}")

    # ---------- TOP BAR ----------
    st.markdown(f"""
    <div class="top-bar">
        <span>📊 NIFTY: <b>{nifty if nifty else 'Unavailable'}</b></span>
        <span>🏦 BANKNIFTY: <b>{bank if bank else 'Unavailable'}</b></span>
        <span>🌪 INDIA VIX: <b>{vix if vix else 'Unavailable'}</b></span>
    </div>
    """, unsafe_allow_html=True)

    # ---------- CARDS ----------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>NIFTY 50</h3>
            <h1>{nifty if nifty else 'No Data'}</h1>
            <a href="https://www.tradingview.com/chart/?symbol=NSE:NIFTY" target="_blank">Open Chart</a>
