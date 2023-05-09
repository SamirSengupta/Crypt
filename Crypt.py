import requests
import pandas as pd
import streamlit as st

# Fetch cryptocurrency data from CoinGecko API
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false"
    response = requests.get(url)
    data = response.json()
    return data

# Suggest cryptocurrency to buy based on investment amount and time duration
def suggest_crypto(investment_amount, investment_duration):
    data = fetch_crypto_data()
    df = pd.DataFrame(data)
    df = df[['id', 'symbol', 'current_price', 'market_cap_rank']]
    df['monthly_investment'] = investment_amount / investment_duration
    df['total_investment'] = investment_amount
    df['potential_profit'] = df['monthly_investment'] * df['market_cap_rank']
    df = df.sort_values(by='potential_profit', ascending=True)
    return df.head(1)

# Streamlit front-end
st.title("Crypt: A Crypto Investment Advisor")

investment_amount = st.number_input("Enter the total amount you're willing to invest (in USD):", min_value=1000.0, step=1000.0)
investment_duration = st.number_input("Enter the investment duration (in months):", min_value=1, max_value=12, step=1)

if st.button("Suggest Cryptocurrency"):
    suggestion = suggest_crypto(investment_amount, investment_duration)
    st.write(f"Based on your investment amount and duration, I suggest you invest in {suggestion.iloc[0]['id'].capitalize()} ({suggestion.iloc[0]['symbol'].upper()}).")

st.write("As for the platform to buy cryptocurrency, I recommend using reputable exchanges like Coinbase, Binance, or Kraken. Always do your own research and consider the fees, security, and user experience before choosing a platform.")
