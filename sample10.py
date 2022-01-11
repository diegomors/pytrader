from math import nan
from typing import List
import MetaTrader5 as mt5
from matplotlib.pyplot import hlines

import pandas as pd
import numpy as np
import mplfinance as fplt
from datetime import datetime
from datetime import timedelta

def isSupport(df: pd.DataFrame, i: int):
  support = df.iloc[i]['low'] < df.iloc[i-1]['low']  and df.iloc[i]['low'] < df.iloc[i+1]['low'] and df.iloc[i+1]['low'] < df.iloc[i+2]['low'] and df.iloc[i-1]['low'] < df.iloc[i-2]['low']
  return support

def isResistance(df: pd.DataFrame, i: int):
  resistance = df.iloc[i]['high'] > df.iloc[i-1]['high']  and df.iloc[i]['high'] > df.iloc[i+1]['high'] and df.iloc[i+1]['high'] > df.iloc[i+2]['high'] and df.iloc[i-1]['high'] > df.iloc[i-2]['high']
  return resistance

def isFarFromLevel(value: float, mean: float, levels: List[float]):
   return np.sum([abs(value-x) < mean  for x in levels]) == 0

stock = 'WING22'
timeframe_str = 'M15'
timeframe = mt5.TIMEFRAME_M15
dt_from = datetime(2022, 1, 3)
dt_to = datetime(2022, 1, 10)

period_str = dt_from.strftime('%d/%m/%y') + ' à ' + (dt_to - timedelta(days=1)).strftime('%d/%m/%y')
title = stock + ' | ' + timeframe_str + ' | ' + period_str

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

stock_rates = mt5.copy_rates_range(stock, timeframe, dt_from, dt_to)

mt5.shutdown()

df: pd.DataFrame = pd.DataFrame(stock_rates)
df = df.loc[:,['time','open','high','low','close']]
df['time'] = pd.to_datetime(df['time'], unit='s')
df = df.set_index('time')

mean: float =  np.mean(df['high'] - df['low'])

levels: List[float] = []
for i in range(2,df.shape[0]-2):
  if isSupport(df, i):
    v = df.iloc[i]['low']
    if isFarFromLevel(v, mean, levels):
      levels.append(v)
  elif isResistance(df, i):
    v = df.iloc[i]['high']
    if isFarFromLevel(v, mean, levels):
      levels.append(v)

levels.sort()

print(levels)

fplt.plot(
    df,
    title=title,
    hlines=levels,
    type='candle',
    ylabel='Preço (R$)'
)
