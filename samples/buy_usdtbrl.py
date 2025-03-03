import os
import pandas as pd
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def print_balance(client):
    account = client.get_account()
    for asset in account["balances"]:
        if float(asset["free"]) > 0:
            print(asset)

client = Client(API_KEY, SECRET_KEY)

print_balance(client)

# order = client.create_order(
#     symbol = "USDTBRL",
#     side = SIDE_BUY,
#     type = ORDER_TYPE_MARKET,
#     quantity = 5
# )

# print_balance(client)