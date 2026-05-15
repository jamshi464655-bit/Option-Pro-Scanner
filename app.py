import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="EasyCharts Pro - Ultra Scanner", layout="wide", page_icon="🚀")

# ====================== BEAUTIFUL UI ======================
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #6b46c1, #7c3aed);
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #ec4899, #f472b6);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        height: 130px;
    }
    .panel-title {
        background: linear-gradient(135deg, #f59e0b, #fb923c);
        color: white;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        margin: 15px 0 10px 0;
    }
    .positive { color: #4ade80; font-weight: bold; }
    .negative { color: #f87171; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>🚀 EasyCharts Pro - Ultra Scanner</h1>
    <p>AI-Powered Multi-Index & Option Master Scanner</p>
</div>
""", unsafe_allow_html=True)

st.button("🚀 START MARKET SCAN", type="primary", use_container_width=True)

# ================== DATA FETCHING ==================
@st.cache_data(ttl=30)
def get_index_data(ticker):
    try:
        data = yf.download(ticker, period="2d", interval="15m", progress=False)
        if not data.empty:
            h, l, c = data['High'].iloc[-2], data['Low'].iloc[-2], data['Close'].iloc[-2]
            p = (h + l + c) / 3
            curr = round(data['Close'].iloc[-1], 2)
            return {
                "curr": curr,
                "R1": round(2*p - l, 2), "S1": round(2*p - h, 2),
                "R2": round(p + (h-l), 2), "S2": round(p - (h-l), 2)
            }
    except:
        return None

nifty = get_index_data("^NSEI")
banknifty = get_index_data("^NSEBANK")
vix = get_index_data("^INDIAVIX")

# ================== METRIC CARDS (നിങ്ങൾ കാണിച്ച ഡിസൈൻ പോലെ) ==================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <h1 style="margin:0;">{nifty['curr'] if nifty else '—'}</h1>
        <p>NIFTY 50</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #22c55e, #86efac); color:black;">
        <h1 style="margin:0;color:black;">{banknifty['curr'] if banknifty else '—'}</h1>
        <p style="color:black;">BANK NIFTY</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #a855f7, #c084fc);">
        <h1 style="margin:0;">{vix['curr'] if vix else '—'}</h1>
        <p>INDIA VIX</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Option Chain & Pivot Levels
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="panel-title">📍 NIFTY 50 Pivot Levels</div>', unsafe_allow_html=True)
    if nifty:
        st.write(f"**Current**: {nifty['curr']}")
        st.write(f"R1: {nifty['R1']} | S1: {nifty['S1']}")
        st.write(f"R2: {nifty['R2']} | S2: {nifty['S2']}")

with col2:
    st.markdown('<div class="panel-title">📊 Option Chain (ATM Strikes)</div>', unsafe_allow_html=True)
    st.info("Option Chain display ഇവിടെ ചേർക്കാം (നിങ്ങൾക്ക് വേണമെങ്കിൽ പറയൂ)")

st.caption(f"🕒 Last Updated: {datetime.now().strftime('%I:%M:%S %p')} | Beautiful UI by Grok")

if st.button("🔄 Refresh Data"):
    st.rerun()