import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random

st.set_page_config(page_title="AI Trading Mentor", layout="wide", page_icon="📈")
st.title("📊 AI Trading Mentor - Belajar Semua Strategi")

if 'trades' not in st.session_state:
    st.session_state.trades = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

menu = st.sidebar.radio("Navigasi", ["Dashboard", "Jurnal Trading", "Kalender Ekonomi", "AI Mentor"])

if menu == "Dashboard":
    st.header("Ringkasan Belajar")
    st.metric("Total Jurnal", len(st.session_state.trades))
    if st.session_state.trades:
        st.metric("Total PnL", sum([t['pnl'] for t in st.session_state.trades]))

elif menu == "Jurnal Trading":
    st.header("Jurnal Trading")
    with st.form("form_trade"):
        pair = st.text_input("Pair", "BTC")
        entry = st.number_input("Entry", 60000.0)
        exit_price = st.number_input("Exit", 61000.0)
        lot = st.number_input("Lot", 0.1)
        mode = st.radio("Mode", ["DEMO", "REAL"])
        analisa = st.text_area("Analisa")
        if st.form_submit_button("Simpan"):
            pnl = (exit_price - entry) * lot
            st.session_state.trades.append({
                "pair": pair, "entry": entry, "exit": exit_price,
                "lot": lot, "pnl": pnl, "mode": mode, "analisa": analisa,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("Tersimpan!")

elif menu == "Kalender Ekonomi":
    st.header("Kalender Ekonomi")
    st.table(pd.DataFrame({
        "Waktu": ["19:30", "16:00", "08:45"],
        "Event": ["NFP", "Retail Sales", "PMI"],
        "Dampak": ["TINGGI", "SEDANG", "TINGGI"]
    }))

elif menu == "AI Mentor":
    st.header("AI Mentor")
    user_input = st.text_input("Tanya soal trading:")
    if st.button("Kirim") and user_input:
        if "lot" in user_input.lower():
            st.info("Rumus lot: (Modal × Risiko%) / (SL × Nilai per pip)")
        elif "risk" in user_input.lower():
            st.info("RR ideal minimal 1:2")
        else:
            st.info("Coba tanya soal lot, risk, atau psikologi.")

st.sidebar.caption("Belajar Trading Tanpa Coding")
