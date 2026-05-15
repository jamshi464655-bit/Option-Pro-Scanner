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
    .panel {
        background: linear-gradient(135deg, #f59e0b, #fb923c);
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
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

if st.button("🚀 START MARKET SCAN", type="primary", use_container_width=True):
    with st.spinner("Fetching Live Market Data..."):
        # Fetch Data
        nifty = yf.download("^NSEI", period="2d", interval="15m", progress=False)
        banknifty = yf.download("^NSEBANK", period="2d", interval="15m", progress=False)
        vix = yf.download("^INDIAVIX", period="2d", interval="15m", progress=False)

        nifty_price = round(nifty['Close'].iloc[-1], 2) if not nifty.empty else 0
        bank_price = round(banknifty['Close'].iloc[-1], 2) if not banknifty.empty else 0
        vix_price = round(vix['Close'].iloc[-1], 2) if not vix.empty else 0

        # Pivot Levels for Nifty
        def get_pivots(df):
            if df.empty: return {}
            h, l, c = df['High'].iloc[-2], df['Low'].iloc[-2], df['Close'].iloc[-2]
            p = (h + l + c) / 3
            return {
                "R1": round(2*p - l, 2), "R2": round(p + (h-l), 2), "R3": round(h + 2*(p-l), 2),
                "S1": round(2*p - h, 2), "S2": round(p - (h-l), 2), "S3": round(l - 2*(h-p), 2)
            }

        nifty_pivot = get_pivots(nifty)

        st.success(f"✅ Scan Completed at {datetime.now().strftime('%I:%M:%S %p')}")

        # ====================== METRIC CARDS ======================
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #a855f7, #c084fc);">
                <h2>NIFTY 50</h2>
                <h1>{nifty_price}</h1>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #22c55e, #86efac); color:black;">
                <h2>BANK NIFTY</h2>
                <h1 style="color:black;">{bank_price}</h1>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f59e0b, #fbbf24); color:black;">
                <h2>INDIA VIX</h2>
                <h1 style="color:black;">{vix_price}</h1>
            </div>
            """, unsafe_allow_html=True)

        # Pivot Levels & Option Chain
        st.markdown('<div class="panel">📍 NIFTY 50 Pivot Levels</div>', unsafe_allow_html=True)
        if nifty_pivot:
            st.write(f"**R1:** {nifty_pivot['R1']} | **R2:** {nifty_pivot['R2']} | **R3:** {nifty_pivot['R3']}")
            st.write(f"**S1:** {nifty_pivot['S1']} | **S2:** {nifty_pivot['S2']} | **S3:** {nifty_pivot['S3']}")

        st.markdown('<div class="panel">📊 Option Chain (ATM Strikes)</div>', unsafe_allow_html=True)
        st.info("Option Chain display ഇവിടെ ചേർക്കാം. നിങ്ങൾക്ക് വേണമെങ്കിൽ പറയൂ — ഞാൻ full option chain ചേർത്തു തരാം.")

else:
    st.info("👆 'START MARKET SCAN' ബട്ടൺ ക്ലിക്ക് ചെയ്ത് സ്കാൻ തുടങ്ങൂ")

st.caption("Beautiful Ultra Scanner UI • Powered by yfinance • Made with ❤️")
