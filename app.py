import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(page_title="AI Trading Mentor", layout="wide", page_icon="📈")
st.title("📊 AI Trading Mentor - Belajar Semua Strategi")

# ========== INISIALISASI SESSION STATE ==========
if 'trades' not in st.session_state:
    st.session_state.trades = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ========== SIDEBAR NAVIGASI ==========
menu = st.sidebar.radio(
    "🧭 Navigasi",
    ["🏠 Dashboard", "📚 Explorer Strategi", "📝 Jurnal Trading", "📆 Kalender Ekonomi", "🧠 AI Mentor"]
)

# ========== 1. DASHBOARD ==========
if menu == "🏠 Dashboard":
    st.header("📊 Ringkasan Belajar")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Jurnal", len(st.session_state.trades))
        real_trades = [t for t in st.session_state.trades if t['mode'] == 'REAL']
        st.metric("Trade Real", len(real_trades))
    with col2:
        demo_trades = [t for t in st.session_state.trades if t['mode'] == 'DEMO']
        st.metric("Trade Demo", len(demo_trades))
        if st.session_state.trades:
            total_pnl = sum([t['pnl'] for t in st.session_state.trades])
            st.metric("Total PnL (All)", f"{total_pnl:.2f} $")
    
    st.subheader("🔥 Mode Trading (Spot vs Futures)")
    mode = st.radio("Pilih mode belajar:", ["Spot", "Futures"], horizontal=True)
    if mode == "Futures":
        st.info("💡 Mode Futures: Perhatikan *Funding Rate* dan *Leverage*. Di sini kita belajar manajemen risiko ketat!")
    else:
        st.info("💡 Mode Spot: Belajar akumulasi aset jangka panjang.")
    
    st.subheader("🎯 Progress Belajar Strategi")
    strategi_list = [
        "Trend Following (SMA/MACD)", 
        "Mean Reversion (Bollinger/RSI)", 
        "Breakout (Donchian)",
        "Volume Flow (VWAP)",
        "Volatility (ATR)",
        "Stat Arb (Pairs)",
        "Sentiment/On-Chain",
        "AI / ML"
    ]
    for s in strategi_list:
        st.progress(random.random(), text=s)

# ========== 2. EXPLORER STRATEGI ==========
elif menu == "📚 Explorer Strategi":
    st.header("📚 Ensiklopedia 8 Cluster Strategi")
    st.markdown("Pilih strategi di bawah, lihat logika, indikator, dan contoh sinyal di chart.")
    
    strategy_option = st.selectbox(
        "Pilih Cluster Strategi:",
        ["Trend Following", "Mean Reversion", "Momentum Breakout", "Volume Flow", 
         "Volatility-Based", "Stat Arbitrage", "Sentiment/On-Chain", "AI/ML"]
    )
    
    descriptions = {
        "Trend Following": "**Logika:** Ikuti arah tren. 'The trend is your friend.' \n\n **Indikator:** SMA Crossover, MACD, Parabolic SAR. \n **Cocok:** Pasar trending kuat (uptrend/downtrend). \n **Sinyal:** Beli saat harga > MA 200 dan MACD di atas 0.",
        "Mean Reversion": "**Logika:** Harga akan kembali ke rata-rata. 'Buy low, sell high.' \n **Indikator:** Bollinger Bands, RSI Extreme (oversold/overbought). \n **Cocok:** Pasar sideways (ranging). \n **Sinyal:** Beli saat harga menyentuh band bawah dan RSI < 30.",
        "Momentum Breakout": "**Logika:** Harga menembus level resistance/support kuat. \n **Indikator:** Donchian Channel, ADX. \n **Cocok:** Awal tren baru. \n **Sinyal:** Beli saat harga > Donchian 20 High.",
        "Volume Flow": "**Logika:** Volume adalah bahan bakar harga. \n **Indikator:** VWAP, OBV, CVD (Cumulative Volume Delta). \n **Cocok:** Konfirmasi sinyal lain. \n **Sinyal:** Beli jika harga di atas VWAP dan volume naik.",
        "Volatility-Based": "**Logika:** Volatilitas berubah siklus. \n **Indikator:** ATR, Keltner Channel. \n **Cocok:** Menentukan stop loss dinamis. \n **Sinyal:** Trailing stop berdasarkan 2x ATR.",
        "Stat Arbitrage": "**Logika:** Korelasi antar aset. \n **Indikator:** Cointegration test, Z-Score spread. \n **Cocok:** Pasar efisien. \n **Sinyal:** Beli aset undervalue, jual overvalue (Pairs trading).",
        "Sentiment/On-Chain": "**Logika:** Fear and Greed Index, Funding Rate, Whale Alert. \n **Indikator:** Sentimen media sosial. \n **Cocok:** Kontrarian. \n **Sinyal:** Beli saat Fear & Greed < 20 (Extreme Fear).",
        "AI/ML": "**Logika:** Mesin belajar pola historis. \n **Metode:** LSTM, Random Forest, Reinforcement Learning. \n **Cocok:** Data kompleks. \n **Sinyal:** Prediksi probabilitas arah harga."
    }
    
    st.markdown(descriptions.get(strategy_option, "Deskripsi belum tersedia."))
    
    st.subheader("📈 Contoh Chart & Sinyal")
    try:
        ticker = "BTC-USD"
        data = yf.download(ticker, period="1mo", interval="1d")
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
        fig.update_layout(height=400, title=f"{ticker} (Simulasi)")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("💡 Geser-geser chartnya untuk latihan analisa teknikal!")
    except:
        st.warning("Gagal ambil data, coba refresh.")

# ========== 3. JURNAL TRADING ==========
elif menu == "📝 Jurnal Trading":
    st.header("📝 Jurnal Otomatis (Real vs Demo)")
    
    with st.form("form_trade"):
        col1, col2, col3 = st.columns(3)
        with col1:
            pair = st.text_input("Pair (contoh: BTC)", "BTC")
            entry = st.number_input("Harga Entry", value=60000.0)
        with col2:
            exit_price = st.number_input("Harga Exit", value=61000.0)
            lot = st.number_input("Lot / Size", value=0.1)
        with col3:
            mode = st.radio("Mode Akun:", ["DEMO", "REAL"], horizontal=True)
            analisa = st.text_area("📝 Analisa kamu (belajar sadar diri):", "Saya entry karena support kuat.")
        
        submitted = st.form_submit_button("💾 Simpan Jurnal")
        if submitted:
            pnl = (exit_price - entry) * lot
            new_trade = {
                "id": len(st.session_state.trades) + 1,
                "pair": pair.upper(),
                "entry": entry,
                "exit": exit_price,
                "lot": lot,
                "pnl": round(pnl, 2),
                "mode": mode,
                "analisa": analisa,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.trades.append(new_trade)
            st.success(f"✅ Jurnal ID {new_trade['id']} tersimpan! PnL: {pnl:.2f} $")
    
    if st.session_state.trades:
        st.subheader("📋 Daftar Jurnal")
        df = pd.DataFrame(st.session_state.trades)
        st.dataframe(df[['id', 'pair', 'entry', 'exit', 'lot', 'pnl', 'mode', 'analisa', 'timestamp']], use_container_width=True)
        
        st.subheader("✏️ Koreksi Analisa (Biar Gak Ngandelin AI)")
        col1, col2 = st.columns([1, 3])
        with col1:
            trade_id = st.number_input("Masukkan ID Trade", min_value=1, step=1)
        with col2:
            new_analysis = st.text_input("Tulis analisa revisi kamu:")
        
        if st.button("🔄 Update Analisa"):
            for t in st.session_state.trades:
                if t['id'] == trade_id:
                    t['analisa'] = new_analysis
                    st.success(f"✅ ID {trade_id} berhasil dikoreksi! Sekarang analisa: {new_analysis}")
                    st.info("🧑‍🏫 *Pesan Mentor:* Bagus! Dengan mengoreksi, kamu melatih insting trading sendiri.")
                    break
            else:
                st.error("ID tidak ditemukan.")
    else:
        st.info("📭 Belum ada jurnal. Yuk catat trade pertama!")

# ========== 4. KALENDER EKONOMI ==========
elif menu == "📆 Kalender Ekonomi":
    st.header("📆 Kalender Ekonomi & Berita Global")
    st.markdown("Berikut jadwal berita **High Impact** yang berdampak ke **Forex, Crypto, Komoditas, Saham**.")
    
    calendar_data = {
        "Waktu": ["19:30 WIB", "16:00 WIB", "08:45 WIB", "20:15 WIB"],
        "Negara": ["🇺🇸 AS", "🇪🇺 EU", "🇨🇳 China", "🇬🇧 UK"],
        "Event": ["Non-Farm Payrolls", "Retail Sales", "Caixin PMI", "BOE Rate Decision"],
        "Dampak": ["🔴 SANGAT TINGGI", "🟡 SEDANG", "🔴 TINGGI", "🔴 SANGAT TINGGI"],
        "Aset Terdampak": ["USD, Crypto, Emas, Indeks", "EUR/USD, Saham EU", "AUD, NZD, Komoditas", "GBP, Saham UK"]
    }
    df_cal = pd.DataFrame(calendar_data)
    st.table(df_cal)
    
    st.subheader("📖 Penjelasan & Tips Navigasi News:")
    st.markdown("""
    - **NFP (Non-Farm Payrolls):** Data ketenagakerjaan AS. Jika naik > forecast, USD menguat, Crypto & Emas cenderung turun.
    - **Retail Sales EU:** Indikator belanja konsumen Eropa. Naik = EUR menguat.
    - **Caixin PMI:** Manufaktur China. Di atas 50 = ekspansi, baik untuk AUD dan komoditas batu bara/tembaga.
    - **BOE Rate:** Suku bunga Inggris. Naik = GBP menguat.
    
    ⚠️ **Aturan Main Saat News:**
    1. Jangan entry 15 menit sebelum dan sesudah berita **High Impact**.
    2. Tunggu *retest* level support/resistance setelah volatilitas reda.
    3. Perhatikan *Actual vs Forecast* - selisih besar = pergerakan liar!
    """)

# ========== 5. AI MENTOR ==========
elif menu == "🧠 AI Mentor":
    st.header("🧠 AI Mentor (Socratic Tutor)")
    st.markdown("Tanyakan soal **Analisa, Money Management, Psikologi**, atau **Risk Reward**. AI akan bimbing, BUKAN kasih sinyal 'beli/jual'.")
    
    user_input = st.text_input("💬 Ketik pertanyaanmu:", placeholder="Contoh: bagaimana cara menghitung lot ideal?")
    if st.button("Kirim ke Mentor"):
        if user_input:
            lower_input = user_input.lower()
            response = ""
            
            if "lot" in lower_input or "money" in lower_input or "modal" in lower_input:
                response = """📐 *Perhitungan Lot (Money Management)*
            Rumus: Lot = (Modal × Risiko %) / (Stop Loss dalam pip × Nilai per pip)
            Contoh: Modal 100jt, risiko 1% = 1jt. SL 100 pip, lot = 1.000.000 / 100 = 0.1.
            🔥 Ingat: *Disiplin lot lebih penting daripada prediksi harga!*"""
            
            elif "risk" in lower_input or "reward" in lower_input or "rr" in lower_input:
                response = """⚖️ *Risk Reward Ratio (RR)*
            RR = Potensi Untung / Potensi Rugi.
            Ideal minimal 1:2. Artinya, untung 200 pips, rugi 100 pips.
            Dengan RR 1:2, win rate 40% aja udah untung! 
            Jangan pernah entry kalau RR < 1:1.5."""
            
            elif "psikologi" in lower_input or "fomo" in lower_input or "takut" in lower_input or "emosi" in lower_input:
                response = """🧘 *Psikologi Trading*
            1. **FOMO:** Jangan kejar harga! Harga selalu balik kasih kesempatan.
            2. **Revenge:** Habis rugi, matikan HP, jalan dulu.
            3. **Disiplin:** Patuhi Stop Loss. SL adalah 'asuransi', bukan musuh.
            📖 Kata Bijak: *"Trader hebat bukan yang paling pintar, tapi yang paling sabar."*"""
            
            elif "support" in lower_input or "resistance" in lower_input:
                response = """📊 *Support & Resistance*
            Support = area pembeli kuat (lantai).
            Resistance = area penjual kuat (plafon).
            Tips: Cari konfirmasi di timeframe lebih tinggi (H4/D1) sebelum entry."""
            
            else:
                response = f"""🤔 Pertanyaan bagus tentang "{user_input[:30]}..."
            Coba spesifik ke:
            - Money Management (lot, modal)
            - Risk Reward (RR)
            - Psikologi (FOMO, disiplin)
            - Teknikal (Support/Resistance)
            
            Saya siap bimbing!"""
            
            st.session_state.chat_history.append(("Kamu", user_input))
            st.session_state.chat_history.append(("Mentor", response))
    
    for role, text in st.session_state.chat_history:
        if role == "Kamu":
            st.markdown(f"🧑 **Kamu:** {text}")
        else:
            st.markdown(f"🧠 **Mentor:** {text}")

st.sidebar.markdown("---")
st.sidebar.caption("📱 Dibuat khusus untuk Redmi 9A | Belajar Trading tanpa coding.")
