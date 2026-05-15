import streamlit as st
import yfinance as yf
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
    .scan-btn {
        background: linear-gradient(135deg, #ef4444, #f87171);
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        margin: 15px 0;
        cursor: pointer;
    }
    .metric-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        min-height: 140px;
    }
    .nifty-card { background: linear-gradient(135deg, #a855f7, #c084fc); }
    .bank-card { background: linear-gradient(135deg, #22c55e, #86efac); color: black; }
    .vix-card { background: linear-gradient(135deg, #f59e0b, #fbbf24); color: black; }
    .status-bar {
        background: #ecfdf5;
        color: #166534;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 15px 0;
    }
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
        try:
            nifty = yf.download("^NSEI", period="2d", interval="5m", progress=False)
            banknifty = yf.download("^NSEBANK", period="2d", interval="5m", progress=False)
            vix = yf.download("^INDIAVIX", period="2d", interval="5m", progress=False)

            nifty_price = round(nifty['Close'].iloc[-1], 2) if not nifty.empty else 0
            bank_price = round(banknifty['Close'].iloc[-1], 2) if not banknifty.empty else 0
            vix_price = round(vix['Close'].iloc[-1], 2) if not vix.empty else 0

            st.success(f"✅ Scan Completed at {datetime.now().strftime('%I:%M:%S %p')}")

            # ====================== METRIC CARDS ======================
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card nifty-card">
                    <h3>NIFTY 50</h3>
                    <h1>{nifty_price}</h1>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card bank-card">
                    <h3>BANK NIFTY</h3>
                    <h1>{bank_price}</h1>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card vix-card">
                    <h3>INDIA VIX</h3>
                    <h1>{vix_price}</h1>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.info("📍 Pivot Levels, Option Chain, Heatmap എന്നിവ ചേർക്കാൻ വേണമെങ്കിൽ പറയൂ — ഞാൻ ഉടനെ ചേർത്തു തരാം.")

        except Exception as e:
            st.error(f"Data Error: {str(e)}")
            st.info("യാഹൂ ഫിനാൻസ് ഡാറ്റ ലഭ്യമല്ല. കുറച്ച് സമയം കഴിഞ്ഞ് വീണ്ടും ശ്രമിക്കുക.")

else:
    st.info("👆 'START MARKET SCAN' ബട്ടൺ ക്ലിക്ക് ചെയ്താൽ Live Data വരും")

st.caption("Beautiful Ultra Scanner UI • Live NSE Data • Made with ❤️")
