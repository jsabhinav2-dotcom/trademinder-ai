import streamlit as st
import yfinance as yf
import ta
import pandas as pd

st.set_page_config(page_title="TradeMind AI", layout="centered")

st.title("📈 TradeMind AI")
st.write("Your personal AI stock trading assistant")

stock = st.text_input("Enter NSE stock (Example: WIPRO.NS)", "WIPRO.NS")

if st.button("Analyze"):

    data = yf.download(stock, period="6mo", interval="1d")

    data["rsi"] = ta.momentum.RSIIndicator(data["Close"], 14).rsi()
    data["macd"] = ta.trend.MACD(data["Close"]).macd()

    latest = data.iloc[-1]

    score = 0

    if latest["rsi"] < 35:
        score += 2
    elif latest["rsi"] > 70:
        score -= 2

    if latest["macd"] > 0:
        score += 1
    else:
        score -= 1

    if score >= 2:
        action = "BUY"
        prob = "70%"
    elif score <= -2:
        action = "SELL"
        prob = "30%"
    else:
        action = "WAIT"
        prob = "45%"

    st.subheader(stock.replace(".NS",""))
    st.write("Price:", round(latest["Close"], 2))
    st.write("RSI:", round(latest["rsi"], 2))
    st.write("MACD:", round(latest["macd"], 2))
    st.write("Win Probability:", prob)

    st.subheader("Action: " + action)

    if action == "WAIT":
        st.write("Market is unclear. Risk is high.")
    elif action == "BUY":
        st.write("Buying momentum is strong.")
    else:
        st.write("Selling pressure is strong.")
