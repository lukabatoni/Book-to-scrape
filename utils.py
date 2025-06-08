import json
import os
import time
from bs4 import BeautifulSoup
import requests

def load_config():
    with open('config.json') as f:
        return json.load(f)

def make_request(url, retries=3, delay=1):
    for attempt in range(retries):
        try:
            time.sleep(delay)
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)  # exponential backoff

def save_data(data, filename):
    os.makedirs('output', exist_ok=True)
    with open(f'output/{filename}', 'w') as f:
        json.dump(data, f, indent=2)