def get_cryptocurrency_recommendation(investment_amount):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin,litecoin,ripple&vs_currencies=inr"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to retrieve data from API.")
        return None, None, None
    data = response.json()
    df = pd.DataFrame(data)
    if 'inr' not in df.columns:
        st.error("Data does not contain 'inr' column.")
        return None, None, None
    df = df.transpose()
    df['value'] = investment_amount / df['inr']
    df = df.sort_values('value', ascending=False)
    recommendation = df.iloc[0].name
    change_url = f"https://api.coingecko.com/api/v3/coins/{recommendation}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    change_response = requests.get(change_url)
    if change_response.status_code != 200:
        st.error("Failed to retrieve data from API.")
        return None, None, None
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
