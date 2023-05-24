import os

# Create directories
os.makedirs(os.path.join('ordiView', 'app', 'templates'), exist_ok=True)
os.makedirs(os.path.join('ordiView', 'app', 'api'), exist_ok=True)

# Create files
open(os.path.join('ordiView', '__init__.py'), 'a').close()
open(os.path.join('ordiView', 'app', '__init__.py'), 'a').close()

# Create app.py
with open(os.path.join('ordiView', 'app', 'app.py'), 'w') as f:
    f.write("import streamlit as st\n")

# Create brc20_api.py
with open(os.path.join('ordiView', 'app', 'api', 'brc20_api.py'), 'w') as f:
    f.write("""
import requests

def fetch_token_distribution(token, page=1, limit=20):
    url = "https://api.example.com/api/v5/explorer/btc/address-balance-list"
    headers = {"Content-Type": "application/json"}
    params = {"token": token, "page": page, "limit": limit}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None
    """)

# Create data.py
with open(os.path.join('ordiView', 'app', 'api', 'data.py'), 'w') as f:
    f.write("")

# Create home.html
with open(os.path.join('ordiView', 'app', 'templates', 'home.html'), 'w') as f:
    f.write("<h1>Welcome to OrdiView</h1>")

# Create config.py
with open(os.path.join('ordiView', 'config.py'), 'w') as f:
    f.write("")

# Create requirements.txt
with open(os.path.join('ordiView', 'requirements.txt'), 'w') as f:
    f.write("""
streamlit
requests
    """)

# Create README.md
with open(os.path.join('ordiView', 'README.md'), 'w') as f:
    f.write("# OrdiView\n")

# Create .gitignore
with open(os.path.join('ordiView', '.gitignore'), 'w') as f:
    f.write("*.pyc\n__pycache__")
