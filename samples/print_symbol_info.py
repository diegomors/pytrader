import os
import pandas as pd
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def print_symbol_info(client, asset):
    symbol_info = client.get_symbol_info(asset)
    lot_size_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE')
    print(asset, lot_size_filter)

client = Client(API_KEY, SECRET_KEY)

print_symbol_info(client, "FETUSDT")