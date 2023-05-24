import asyncio
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from ratelimiter import RateLimiter
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OKLINK_API_KEY')

headers = {
    "Ok-Access-Key": api_key,
    "Content-Type": "application/json",
}

limit = 20
url = "https://www.oklink.com/api/v5/explorer/btc/address-balance-list"

rate_limiter = RateLimiter(max_calls=5, period=1)  # Define the rate limiter

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_address_tokens(address, page):
    with rate_limiter:
        params = {"address": address, "page": page, "limit": limit}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'HTTP Status Code: {response.status_code}')
            print(f'Response Message: {response.text}')
            return None

async def parallel_fetch(address):
    all_results = []  # a list to store all fetched results

    # First fetch the initial page
    initial_result = await fetch_address_tokens(address, 1)
    total_pages = int(initial_result['data'][0]['totalPage']) if initial_result and 'data' in initial_result and initial_result['data'] else 0
    all_results.append(initial_result)

    # Then, fetch the rest of the pages based on the 'totalPage' value
    if total_pages > 1:
        tasks = [asyncio.ensure_future(fetch_address_tokens(address, i)) for i in range(2, total_pages + 1)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):  # If an exception is returned
                print(f"Exception occurred: {result}")
                continue  # Skip this iteration

            # Check if 'data' and 'balanceList' exists in result
            if 'data' not in result or not isinstance(result['data'], list) or len(result['data']) == 0 or 'balanceList' not in result['data'][0]:
                print(f"Unexpected result: {result}")
                continue  # Skip this iteration

            all_results.append(result)  # add the result to the list

    return all_results  # return all results

def clean_data(fetched_data):
    cleaned_data = []
    for page_data in fetched_data:
        # Check if 'data' and 'balanceList' exists in page_data
        if 'data' in page_data and isinstance(page_data['data'], list) and len(page_data['data']) > 0 and 'balanceList' in page_data['data'][0]:
            balance_list = page_data['data'][0]['balanceList']
            cleaned_data.extend(balance_list)
    return cleaned_data

# New function to run the async function in a separate thread
def fetch_address_tokens_sync(address):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(parallel_fetch(address))
        # Clean the data before returning
        cleaned_data = clean_data(result)
        return cleaned_data
    finally:
        loop.close()

