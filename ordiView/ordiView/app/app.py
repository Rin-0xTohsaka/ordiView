import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from api.brc20_wallet_tokens import fetch_address_tokens_sync
from api.transaction_history import get_transaction_history
from api.token_holdings import fetch_token_holdings, plot_token_holdings
from api.transaction_volume import fetch_transaction_volume

st.set_page_config(layout="wide")

st.title('OrdiView: BTC Address Token Analyzer')

st.sidebar.header('Categories')
category = st.sidebar.radio('Choose a category',
                            ['Wallet View', 'BRC20_Analytics'],
                            index=0)

address = st.text_input('Enter the BTC Chain Address:')

if category == 'Wallet View':
    if address:
        st.subheader('Token Analytics')
        
        tab1, tab2 = st.tabs(["Token Holdings", "Transaction History"])
        
        # Token Holdings Tab
        with tab1:
            st.markdown('### Wallet Holdings', unsafe_allow_html=True)
            with st.spinner('Fetching Token Holdings...'):
                token_data = fetch_token_holdings(address)
                # Display the dataframe with HTML/CSS workaround
                tab1.write(f"""
                    <div style='height:350px;overflow:auto;width:100%;'>
                        <style>
                            table {{
                                width: 100%;
                            }}
                        </style>
                        {token_data.to_html(index=False)}
                    </div>
                """, unsafe_allow_html=True)
                
                if not token_data.empty:
                    st.markdown('### Wallet Tokens Distribution', unsafe_allow_html=True)
                    plot_token_holdings(token_data)
            
        # Transaction History Tab
        with tab2:
            with st.spinner('Fetching Transaction History...'):
                transaction_data = get_transaction_history(address)
                # Display the dataframe with HTML/CSS workaround
                tab2.write(f"""
                    <div style='height:300px;overflow:auto;width:100%;'>
                        <style>
                            table {{
                                width: 100%;
                            }}
                        </style>
                        {transaction_data.to_html(index=False)}
                    </div>
                """, unsafe_allow_html=True)
                
                # Transaction Volume Tab
        tab3 = st.expander('Transaction Volume Over Time')
        with tab3:
            st.markdown('### Transaction Volume Over Time', unsafe_allow_html=True)
            start_date = st.date_input('Start Date')
            end_date = st.date_input('End Date')
            
            with st.spinner('Fetching Transaction Volume...'):
                df = fetch_transaction_volume(address, start_date, end_date)
                if df is not None:
                    plt.figure(figsize=(12,6))
                    plt.plot(df, marker='o', linestyle='-')
                    plt.title('Transaction Volume Over Time')
                    plt.xlabel('Date')
                    plt.ylabel('Transaction Count')
                    plt.grid(True)
                    plt.tight_layout()
                    st.pyplot()
                else:
                    st.error('Failed to fetch transaction volume data.')

elif category == 'BRC20_Analytics':
    if address:
        brc20_data = fetch_address_tokens_sync(address)
        st.subheader('BRC20 Tokens')
        st.dataframe(brc20_data)
