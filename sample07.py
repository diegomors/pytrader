from math import nan
import MetaTrader5 as mt5
from matplotlib.pyplot import hlines

import pandas as pd
import numpy as np
import mplfinance as fplt
from datetime import datetime
from datetime import timedelta

def isSupport(i):
  support = df.iloc[i]['low'] < df.iloc[i-1]['low']  and df.iloc[i]['low'] < df.iloc[i+1]['low'] and df.iloc[i+1]['low'] < df.iloc[i+2]['low'] and df.iloc[i-1]['low'] < df.iloc[i-2]['low']
  return support

def isResistance(i):
  resistance = df.iloc[i]['high'] > df.iloc[i-1]['high']  and df.iloc[i]['high'] > df.iloc[i+1]['high'] and df.iloc[i+1]['high'] > df.iloc[i+2]['high'] and df.iloc[i-1]['high'] > df.iloc[i-2]['high']
  return resistance

def isFarFromLevel(l):
   return np.sum([abs(l-x) < s  for x in levels]) == 0

stock = 'WDOJ21'
timeframe_str = 'M15'
timeframe = mt5.TIMEFRAME_M15
dt_from = datetime(2021, 3, 1)
dt_to = datetime(2021, 3, 5)

period_str = dt_from.strftime('%d/%m/%y') + ' à ' + (dt_to - timedelta(days=1)).strftime('%d/%m/%y')
title = stock + ' | ' + timeframe_str + ' | ' + period_str

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

stock_rates = mt5.copy_rates_range(stock, timeframe, dt_from, dt_to)

mt5.shutdown()

df = pd.DataFrame(stock_rates)
df = df.loc[:,['time','open','high','low','close']]
df['time'] = pd.to_datetime(df['time'], unit='s')
df = df.set_index('time')

s =  np.mean(df['high'] - df['low'])

levels = []
for i in range(2,df.shape[0]-2):
  if isSupport(i):
    l = df.iloc[i]['low']
    if isFarFromLevel(l):
      levels.append(l)
  elif isResistance(i):
    l = df.iloc[i]['high']
    if isFarFromLevel(l):
      levels.append(l)

print(levels)

fplt.plot(
    df,
    title=title,
    hlines=levels,
    type='candle',
    ylabel='Preço (R$)'
)
