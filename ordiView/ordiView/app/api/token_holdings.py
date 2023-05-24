import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OKLINK_API_KEY')

headers = {
    "Ok-Access-Key": api_key,
    "Content-Type": "application/json",
}

def fetch_token_holdings(address, page=1):
    url = f"https://www.oklink.com/api/v5/explorer/btc/address-balance-list"
    params = {"address": address, "page": page, "limit": 20}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data and 'data' in data and data['data'] and 'balanceList' in data['data'][0]:
            balance_data = pd.json_normalize(data['data'][0]['balanceList'])
            balance_data.columns = balance_data.columns.str.strip()
            return balance_data
        else:
            print(f'No balance data found in response: {data}')
            return pd.DataFrame()  
    else:
        print(f'HTTP Status Code: {response.status_code}')
        print(f'Response Message: {response.text}')
        return pd.DataFrame()

def plot_token_holdings(data):
    df = pd.DataFrame(data)
    print(df)  
    if not df.empty and 'balance' in df.columns and 'token' in df.columns:
        print(df.head)
        df['balance'] = df['balance'].astype(float) / 1e9 
        df['log_balance'] = np.log(df['balance'] + 1)  
        df['distribution (%)'] = df['balance'] / df['balance'].sum() * 100

        col1, col2 = st.columns([7, 3])  # Split the page into 2 columns with a 70%/30% ratio
        with col1:
            fig = px.bar(df, x='token', y='log_balance', color='token')
            fig.update_layout(
                autosize=False,
                margin=dict(l=20, r=20, b=20, t=30),
                showlegend=False,
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                title='Log-transformed Token Holdings',
                title_x=0.5, # Center the title
                title_y=1, # Position title inside the plot
                title_font=dict(size=14),
                shapes=[
                    dict(
                        type='rect',
                        xref='paper', yref='paper',
                        x0=0, y0=0, x1=1, y1=1,
                        line=dict(color='Black', width=3)
                    )
                ]
            )
            st.plotly_chart(fig, use_container_width=True)  # add the parameter here
        with col2:
            st.write(f"""
            <div style='height:600px;overflow:auto;'>
                {df[['token', 'distribution (%)']].to_html(index=False)}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No token holdings found for this address or the dataframe does not contain 'balance' or 'token' field.")






