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

def fetch_transaction_volume(address, start_date, end_date):
    url = f"https://www.oklink.com/api/explorer/v5/btc/address-transaction-list"
    params = {"address": address, "start_time": start_date, "end_time": end_date}
    
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        df = pd.json_normalize(data['data']['list'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df = df.set_index('time')
        df = df.resample('D').size()

        return df
    else:
        print(f'HTTP Status Code: {response.status_code}')
        print(f'Response Message: {response.text}')
        return None
