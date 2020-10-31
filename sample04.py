from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

print(mt5.terminal_info())
print(mt5.version())

# inputs
stock = 'WINZ20'
timeframe_str = 'H1'
timeframe = mt5.TIMEFRAME_H1
dt_from = datetime(2020, 10, 26)
dt_to = datetime(2020, 10, 31)

period_str = dt_from.strftime('%d/%m/%y') + ' > ' + (dt_to - timedelta(days=1)).strftime('%d/%m/%y')
title = stock + ' ' + timeframe_str + '\n' + period_str

winz20_rates = mt5.copy_rates_range(stock, timeframe, dt_from, dt_to)

mt5.shutdown()

df = pd.DataFrame(winz20_rates)
df['time']=pd.to_datetime(df['time'], unit='s')

fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.show()