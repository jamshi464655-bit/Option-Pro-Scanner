import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="EasyCharts Pro - Ultra Scanner", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg,#6a11cb,#2575fc);
    padding:35px;
    border-radius:20px;
    text-align:center;
    color:white;
    margin-bottom:25px;
}
.card {
    background:#161b22;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border:1px solid #30363d;
    margin-bottom:10px;
}
.value {
    font-size:28px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="main-header">
<h1>🚀 EasyCharts Pro - Ultra Scanner</h1>
<p>Multi-Index Master Scanner</p>
</div>
""", unsafe_allow_html=True)

# ---------- FUNCTION ----------
def get_index_price(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="5m", progress=False)
        if df.empty:
            return None
        return round(float(df["Close"].iloc[-1]), 2)
    except:
        return None

# ---------- BUTTON ----------
if st.button("🚀 START MARKET SCAN"):

    with st.spinner("Fetching live data..."):
        nifty = get_index_price("^NSEI")
        bank = get_index_price("^NSEBANK")
        vix = get_index_price("^INDIAVIX")

    st.success(f"✅ Scan Completed at {datetime.now().strftime('%I:%M:%S %p')}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <h3>NIFTY 50</h3>
            <div class="value">{nifty if nifty else "Data Error"}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <h3>BANK NIFTY</h3>
            <div class="value">{bank if bank else "Data Error"}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <h3>INDIA VIX</h3>
            <div class="value">{vix if vix else "Data Error"}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("Click START MARKET SCAN to load data.")
