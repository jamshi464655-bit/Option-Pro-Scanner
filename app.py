import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="Ultimate Pro Master Scanner", layout="wide")

# --- CSS STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .card { background-color: #161b22; padding: 15px; border-radius: 15px; border: 1px solid #30363d; text-align: center; margin-bottom: 20px; }
    .top-bar { display: flex; justify-content: space-around; background: #1f2937; padding: 12px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #3b82f6; align-items: center; }
    .levels-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin: 10px 0; font-size: 11px; }
    .res { color: #ff7b72; font-weight: bold; }
    .sup { color: #44cf6c; font-weight: bold; }
    .strike-table { width: 100%; font-size: 12px; border-collapse: collapse; margin-top: 10px; border-radius: 8px; overflow: hidden; }
    .strike-table td { padding: 6px; border: 1px solid #30363d; text-align: center; }
    .itm { background-color: #1c2a1e; color: #44cf6c; }
    .atm { background-color: #262c36; color: #ffab70; font-weight: bold; }
    .otm { color: #8b949e; }
    .chart-btn { display: inline-block; padding: 6px 12px; margin: 5px; border-radius: 5px; text-decoration: none; font-size: 11px; font-weight: bold; border: 1px solid #58a6ff; color: #58a6ff; }
    
    /* Heatmap Styling */
    .heatmap-container { background: #0d1117; padding: 15px; border-radius: 12px; border: 1px solid #333; }
    .stock-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 6px; }
    .stock-box { padding: 10px 5px; border-radius: 6px; font-size: 11px; font-weight: bold; text-align: center; border: 1px solid #222; }
    .pos { background-color: #1c2a1e; color: #44cf6c; border-color: #44cf6c; }
    .neg { background-color: #2a1c1c; color: #ff7b72; border-color: #ff7b72; }
</style>
""", unsafe_allow_html=True)

# Nifty 50 Tickers
NIFTY_50_TICKERS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS",
    "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LTIM.NS",
    "LT.NS", "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS",
    "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS",
    "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
    "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"
]

def get_data_and_pivots(ticker):
    try:
        data = yf.download(ticker, period="2d", interval="15m", progress=False)
        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
            h, l, c = data['High'].iloc[-2], data['Low'].iloc[-2], data['Close'].iloc[-2]
            p = (h + l + c) / 3
            return {
                "curr": round(data['Close'].iloc[-1], 2),
                "R3": round(h + 2*(p-l), 2), "R2": round(p + (h-l), 2), "R1": round(2*p - l, 2),
                "S1": round(2*p - h, 2), "S2": round(p - (h-l), 2), "S3": round(l - 2*(h-p), 2)
            }
    except: pass
    return None

def fetch_nifty50_data():
    try:
        df = yf.download(NIFTY_50_TICKERS, period="2d", interval="1d", progress=False)['Close']
        if not df.empty:
            change = ((df.iloc[-1] - df.iloc[-2]) / df.iloc[-2]) * 100
            return change
    except: pass
    return None

def get_option_chain_html(price, name):
    base = 50 if "NIFTY 50" in name else 100
    atm = round(price / base) * base
    html = "<table class='strike-table'>"
    for i in range(-2, 3):
        s = int(atm + (i * base))
        style = "itm" if s < atm else "atm" if s == atm else "otm"
        label = "ITM" if s < atm else "ATM" if s == atm else "OTM"
        html += f"<tr class='{style}'><td>{label}</td><td>{s}</td></tr>"
    return html + "</table>"

def display_heatmap(data_series):
    st.markdown('<div class="heatmap-container"><div class="stock-grid">', unsafe_allow_html=True)
    for stock, change in data_series.items():
        symbol = stock.replace(".NS", "")
        color_class = "pos" if change >= 0 else "neg"
        st.markdown(f'<div class="stock-box {color_class}">{symbol}<br>{change:+.2f}%</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

def main():
    st.markdown("<h2 style='text-align: center;'>🎯 Ultimate Option Pro Master Scanner</h2>", unsafe_allow_html=True)
    
    nifty = get_data_and_pivots("^NSEI")
    banknifty = get_data_and_pivots("^NSEBANK")
    vix = get_data_and_pivots("^INDIAVIX")
    heatmap_data = fetch_nifty50_data()

    # Top Bar
    st.markdown(f"""
    <div class="top-bar">
        <span>🌏 GIFT NIFTY: <b style="color:#58a6ff;">{nifty['curr']+15 if nifty else '0.00'}</b></span>
        <span>📊 INDIA VIX: <b style="color:#ff7b72;">{vix['curr'] if vix else 18.35}</b></span>
        <a href="https://www.tradingview.com/chart/" target="_blank" class="chart-btn">Open Full Chart</a>
    </div>
    """, unsafe_allow_html=True)

    idx_cols = st.columns(2)
    indices = [(nifty, "NIFTY 50", "NIFTY"), (banknifty, "BANK NIFTY", "BANKNIFTY")]

    for i, (data, name, sym) in enumerate(indices):
        if data:
            with idx_cols[i]:
                st.markdown(f"""
                <div class="card">
                    <h3 style="color:#8b949e; margin:0;">{name}</h3>
                    <h1 style="margin:10px 0;">{data['curr']}</h1>
                    <a href="https://www.tradingview.com/chart/?symbol=NSE:{sym}" target="_blank" class="chart-btn">📊 Spot</a>
                    <a href="https://www.tradingview.com/chart/?symbol=NSE:{sym}1!" target="_blank" class="chart-btn">📈 Future</a>
                    <div style="background:#0d1117; padding:10px; border-radius:10px; border:1px solid #333; margin-top:10px;">
                        <small>📍 Support & Resistance</small>
                        <div class="levels-grid">
                            <span class="res">R3: {data['R3']}</span><span class="res">R2: {data['R2']}</span><span class="res">R1: {data['R1']}</span>
                            <span class="sup">S1: {data['S1']}</span><span class="sup">S2: {data['S2']}</span><span class="sup">S3: {data['S3']}</span>
                        </div>
                    </div>
                    {get_option_chain_html(data['curr'], name)}
                </div>
                """, unsafe_allow_html=True)

    # --- NIFTY 50 HEATMAP SPLITTED INTO 2 PORTIONS ---
    st.markdown("<h3 style='text-align: center; color: #ffab70;'>📈 Nifty 50 Performance (Splitted)</h3>", unsafe_allow_html=True)
    if heatmap_data is not None:
        # Split data into 2 parts
        mid_point = len(heatmap_data) // 2
        part1 = heatmap_data.iloc[:mid_point]
        part2 = heatmap_data.iloc[mid_point:]
        
        hm_cols = st.columns(2)
        with hm_cols[0]:
            display_heatmap(part1)
        with hm_cols[1]:
            display_heatmap(part2)

    st.caption(f"🕒 Last Update: {datetime.now().strftime('%H:%M:%S')}")
    time.sleep(30)
    st.rerun()

if __name__ == "__main__":
    main()
