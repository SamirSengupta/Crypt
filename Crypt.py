import requests
import pandas as pd
import streamlit as st

def get_cryptocurrency_recommendation(investment_amount):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin,litecoin,ripple&vs_currencies=inr"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df = df.transpose()
    df['inr'] = pd.to_numeric(df['inr'])
    df['value'] = investment_amount / df['inr']
    df = df.sort_values('value', ascending=False)
    recommendation = df.iloc[0].name
    change_url = f"https://api.coingecko.com/api/v3/coins/{recommendation}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    change_response = requests.get(change_url)
    change_data = change_response.json()
    change_percent = change_data['market_data']['price_change_percentage_24h']
    if change_percent > 0:
        reason = f"{recommendation} has increased by {change_percent:.2f}% in the last 24 hours."
    elif change_percent < 0:
        reason = f"{recommendation} has decreased by {abs(change_percent):.2f}% in the last 24 hours."
    else:
        reason = f"{recommendation} has remained stable in the last 24 hours."
    df['change_url'] = df.index.map(lambda x: f"https://api.coingecko.com/api/v3/coins/{x}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false")
    df['change_response'] = df['change_url'].map(requests.get)
    df['change_data'] = df['change_response'].map(lambda x: x.json())
    df['change_percent'] = df['change_data'].map(lambda x: x['market_data']['price_change_percentage_24h'])
    return recommendation, reason, df

st.title("Cryptocurrency Recommendation Tool")

investment_amount = st.number_input("Enter the amount you want to invest in INR:", value=1000, step=1000)
if investment_amount > 0:
    recommendation, reason, df = get_cryptocurrency_recommendation(investment_amount)
    st.write(f"Based on your investment amount of {investment_amount} INR, we recommend buying {recommendation}. {reason}")
    st.write("Here are the top 3 cryptocurrencies you may consider:")
    top_3 = df.iloc[1:4][['value', 'change_percent']]
    st.table(top_3)
    st.write("Here are the current values of all the cryptocurrencies:")
    st.table(df[['inr', 'change_percent']])
else:
    st.warning("Please enter a valid investment amount.")
