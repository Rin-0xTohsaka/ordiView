# OrdiView: BTC Address Token Analyzer

## Project Overview

OrdiView is a powerful web application designed to analyze and display data associated with Bitcoin (BTC) addresses. The frontend is powered by Streamlit and the backend relies on the OKLink API. The goal of the project is to deliver a user-friendly tool for visualizing and understanding different aspects of BTC address activity, offering functionalities such as:

1. Transaction History Analysis: Analyze and visualize the transaction history of a specific BTC address.
2. Token Holding Analysis: Display all tokens held by a specific BTC address, visualizing their quantities.
3. Real-time Updating: Fetch and display updated data at regular intervals.
4. Top Tokens Dashboard: Display the top tokens in the BTC blockchain.
5. Address Comparison: Enable the user to compare different BTC addresses based on their transaction histories and token holdings.
6. Network Status: Display the current status of the BTC network.
7. Data Filtering and Searching: Enable the user to filter and search data based on various criteria.

## Project Structure

ordiView
├── init.py
├── .env
├── .gitignore
├── config.py
├── README.md
├── requirements.txt
├── fileCreator.py
├── reorganize.py
└── ordiView
├── init.py
├── app
│ ├── init.py
│ ├── app.py
│ ├── api
│ │ ├── init.py
│ │ ├── brc20_api.py
│ │ ├── data.py
│ │ ├── transaction_history.py
│ │ ├── token_holdings.py
│ │ └── env
│ └── templates
└── pycache


## Installation

1. Clone this repository:
`git clone https://github.com/{your_username}/ordiView.git`


2. Install the required Python packages:
`pip install -r requirements.txt`


3. Copy your OKLink API key into the `.env` file:
`echo "OKLINK_API_KEY={your_api_key}" > .env`


4. Run the application:
`streamlit run app/app.py`


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update the tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

