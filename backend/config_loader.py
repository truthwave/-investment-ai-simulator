import json

def load_config(path='config.json'):
    with open(path, 'r') as f:
        return json.load(f)
# config_loader.py
SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "NVDA"
]
