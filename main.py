import time
import os
import pandas as pd
from decimal import Decimal
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def get_symbol_info(client, asset):
    symbol_info = client.get_symbol_info(asset)
    return next(f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE')

def count_decimal_places_to_one(number):
    d = Decimal(str(number))
    d = d.normalize()
    return -d.as_tuple().exponent

def get_rounding_factor(client, asset):
    asset_info = get_symbol_info(client, asset)
    decimal_places = count_decimal_places_to_one(asset_info['minQty'])
    return 10 ** decimal_places

def get_prices(asset, interval):
    candles = client.get_klines(symbol = asset, interval = interval, limit = 1000)
    prices = pd.DataFrame(candles)
    prices.columns = ["tempo_abertura", "abertura", "maxima", "minima", "fechamento", "volume", "tempo_fechamento", "moedas_negociadas", "numero_trades",
                    "volume_ativo_base_compra", "volume_ativo_cotação", "-"]
    prices = prices[["fechamento", "tempo_fechamento"]]
    prices["tempo_fechamento"] = pd.to_datetime(prices["tempo_fechamento"], unit = "ms").dt.tz_localize("UTC")
    prices["tempo_fechamento"] = prices["tempo_fechamento"].dt.tz_convert("America/Sao_Paulo")
    return prices

def trading_strategy(client, data, trading_asset, individual_asset, quantity, position, rounding_factor = 1000):

    data["media_rapida"] = data["fechamento"].rolling(window = 7).mean()
    data["media_devagar"] = data["fechamento"].rolling(window = 40).mean()

    last_fast_mean = data["media_rapida"].iloc[-1]
    last_slow_mean = data["media_devagar"].iloc[-1]

    print(f"Última Média Rápida: {last_fast_mean} | Última Média Devagar: {last_slow_mean}")

    account = client.get_account()

    for asset in account["balances"]:

        if asset["asset"] == individual_asset:

            current_quantity = float(asset["free"])

    if last_fast_mean > last_slow_mean and position == False:

        # client.create_order(symbol = trading_asset,
        #     side = SIDE_BUY,
        #     type = ORDER_TYPE_MARKET,
        #     quantity = quantity
        # )
        
        print("COMPRAR O ATIVO")

        position = True

    elif last_fast_mean < last_slow_mean and position == True:

        # client.create_order(symbol = trading_asset,
        #     side = SIDE_SELL,
        #     type = ORDER_TYPE_MARKET,
        #     quantity = int(current_quantity * rounding_factor)/rounding_factor
        # )
        
        print("VENDER O ATIVO")

        position = False

    return position

client = Client(API_KEY, SECRET_KEY)

trading_asset = "FETUSDT"
individual_asset = "FET"
interval = Client.KLINE_INTERVAL_1HOUR
quantity = 0.1

rounding_factor = get_rounding_factor(client=client, asset=trading_asset)

current_position = False

while True:

    updated_data = get_prices(asset=trading_asset, interval=interval)
    current_position = trading_strategy(client=client, data=updated_data, trading_asset=trading_asset, 
                                        individual_asset=individual_asset, quantity=quantity, position=current_position,
                                        rounding_factor=rounding_factor)
    time.sleep(60 * 60)