import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OKLINK_API_KEY')

headers = {
    "Ok-Access-Key": api_key,
    "Content-Type": "application/json",
}

def fetch_transactions(address, page=1):
    url = f"https://www.oklink.com/api/v5/explorer/btc/transaction-list"
    params = {"address": address, "page": page, "limit": 10}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f'HTTP Status Code: {response.status_code}')
        print(f'Response Message: {response.text}')
        return None


def get_transaction_history(address):
    transactions = []
    page = 1

    while True:
        data = fetch_transactions(address, page)

        if not data or 'data' not in data or not data['data']:
            break

        transactions.extend(data['data'][0]['inscriptionsList'])
        if len(transactions) >= 20:  # stop when we have 10 transactions
            break
        page += 1

    # convert to dataframe for easier manipulation
    df = pd.DataFrame(transactions)

    # keep only the columns we want, in the order we want them
    df = df[['time', 'token', 'txId', 'blockHeight', 'state', 'actionType', 'amount', 'fromAddress', 'toAddress']]

    # simplify the address columns
    df['fromAddress'] = df['fromAddress'].apply(lambda x: x[:3] + '...' + x[-3:])
    df['toAddress'] = df['toAddress'].apply(lambda x: x[:3] + '...' + x[-3:])
    df['txId'] = df['txId'].apply(lambda x: x[:5] + '...' + x[-4:])

    # Convert the UNIX timestamp (in ms) to a datetime object and use it as the new 'time' column
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    return df
