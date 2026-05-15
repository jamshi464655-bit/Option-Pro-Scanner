import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="EasyCharts Pro - Ultra Scanner", layout="wide")

# ---------------- CSS ----------------
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
    background:#111827;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    margin-bottom:15px;
}
.pivot span {
    display:block;
    margin:4px 0;
}
.pos {background:#14532d;color:#4ade80;}
.neg {background:#7f1d1d;color:#f87171;}
.stock-grid {
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(90px,1fr));
    gap:6px;
}
.stock-box {
    padding:8px;
    border-radius:6px;
    font-size:12px;
    font-weight:bold;
    text-align:center;
}
.option-table td {
    padding:6px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
<h1>🚀 EasyCharts Pro - Ultra Scanner</h1>
<p>Pivot Levels | Full Option Chain | Heatmap</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------

def get_pivot(symbol):
    try:
        df = yf.download(symbol, period="2d", interval="1d", progress=False)
        if df.empty:
            return None
        h = df["High"].iloc[-2]
        l = df["Low"].iloc[-2]
        c = df["Close"].iloc[-2]
        p = (h + l + c) / 3
        return {
            "Price": round(df["Close"].iloc[-1],2),
            "R1": round(2*p - l,2),
            "S1": round(2*p - h,2),
            "R2": round(p + (h-l),2),
            "S2": round(p - (h-l),2)
        }
    except:
        return None

def full_option_chain(price, step):
    atm = round(price / step) * step
    strikes = [atm - step*3, atm - step*2, atm - step,
               atm,
               atm + step, atm + step*2, atm + step*3]
    
    table = []
    for s in strikes:
        if s < atm:
            status = "ITM"
        elif s == atm:
            status = "ATM"
        else:
            status = "OTM"
        table.append({"Type":status,"Strike":s})
    return pd.DataFrame(table)

def get_heatmap():
    tickers = [
        "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS",
        "ICICIBANK.NS","SBIN.NS","ITC.NS","BHARTIARTL.NS",
        "LT.NS","AXISBANK.NS","MARUTI.NS","TITAN.NS"
    ]
    try:
        df = yf.download(tickers, period="2d", interval="1d", progress=False)["Close"]
        change = ((df.iloc[-1] - df.iloc[-2]) / df.iloc[-2]) * 100
        return change
    except:
        return None

# ---------------- BUTTON ----------------

if st.button("🚀 START MARKET SCAN"):

    with st.spinner("Loading Market Data..."):
        nifty = get_pivot("^NSEI")
        bank = get_pivot("^NSEBANK")
        heatmap = get_heatmap()

    st.success(f"✅ Scan Completed at {datetime.now().strftime('%I:%M:%S %p')}")

    col1, col2 = st.columns(2)

    # ---------- NIFTY ----------
    if nifty:
        with col1:
            st.markdown(f"""
            <div class="card">
            <h3>NIFTY 50</h3>
            <h2>{nifty['Price']}</h2>
            <div class="pivot">
                <span>R1: {nifty['R1']}</span>
                <span>R2: {nifty['R2']}</span>
                <span>S1: {nifty['S1']}</span>
                <span>S2: {nifty['S2']}</span>
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("📊 NIFTY Full Option Chain")
            oc = full_option_chain(nifty["Price"],50)
            st.dataframe(oc,use_container_width=True,hide_index=True)

    # ---------- BANKNIFTY ----------
    if bank:
        with col2:
            st.markdown(f"""
            <div class="card">
            <h3>BANK NIFTY</h3>
            <h2>{bank['Price']}</h2>
            <div class="pivot">
                <span>R1: {bank['R1']}</span>
                <span>R2: {bank['R2']}</span>
                <span>S1: {bank['S1']}</span>
                <span>S2: {bank['S2']}</span>
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("📊 BANKNIFTY Full Option Chain")
            oc_bank = full_option_chain(bank["Price"],100)
            st.dataframe(oc_bank,use_container_width=True,hide_index=True)

    # ---------- HEATMAP ----------
    st.markdown("### 📈 Full Color Heatmap")

    if heatmap is not None:
        st.markdown("<div class='stock-grid'>", unsafe_allow_html=True)
        for stock, change in heatmap.items():
            symbol = stock.replace(".NS","")
            cls = "pos" if change >= 0 else "neg"
            st.markdown(
                f"<div class='stock-box {cls}'>{symbol}<br>{change:+.2f}%</div>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Heatmap data unavailable")

else:
    st.info("Click START MARKET SCAN to load data.")
