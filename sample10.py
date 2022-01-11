from typing import List
import MetaTrader5 as mt5
from matplotlib.pyplot import hlines

import pandas as pd
import numpy as np
import mplfinance as fplt
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta, MO


def copyRatesFrom(stock, timeframe, dt_from: datetime, dt_to: datetime) -> pd.DataFrame:
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    stock_rates = mt5.copy_rates_range(stock, timeframe, dt_from, dt_to)
    mt5.shutdown()
    df: pd.DataFrame = pd.DataFrame(stock_rates)
    df = df.loc[:, ['time', 'open', 'high', 'low', 'close']]
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df.set_index('time')
    return df


def mean(df: pd.DataFrame) -> float:
    return np.mean(df['high'] - df['low'])


def isSupport(df: pd.DataFrame, i: int) -> bool:
    support = df.iloc[i]['low'] < df.iloc[i-1]['low'] and df.iloc[i]['low'] < df.iloc[i +
                                                                                      1]['low'] and df.iloc[i+1]['low'] < df.iloc[i+2]['low'] and df.iloc[i-1]['low'] < df.iloc[i-2]['low']
    return support


def isResistance(df: pd.DataFrame, i: int) -> bool:
    resistance = df.iloc[i]['high'] > df.iloc[i-1]['high'] and df.iloc[i]['high'] > df.iloc[i +
                                                                                            1]['high'] and df.iloc[i+1]['high'] > df.iloc[i+2]['high'] and df.iloc[i-1]['high'] > df.iloc[i-2]['high']
    return resistance


def isFarFromLevel(value: float, mean: float, levels: List[float]) -> bool:
    return np.sum([abs(value-x) < mean for x in levels]) == 0


def filterLevels(levels: List[float], df: pd.DataFrame, mean: float) -> List[float]:
    l: List[float] = []
    for i in range(2, df.shape[0]-2):
        if isSupport(df, i):
            v = df.iloc[i]['low']
            if isFarFromLevel(v, mean, levels):
                levels.append(v)
            if isFarFromLevel(v, mean, l):
                l.append(v)
        elif isResistance(df, i):
            v = df.iloc[i]['high']
            if isFarFromLevel(v, mean, levels):
                levels.append(v)
            if isFarFromLevel(v, mean, l):
                l.append(v)
    return l


stock = input('Código do Ativo: ')
dt_now = datetime.now()
dt_from = dt_now + relativedelta(weekday=MO(-2))
period_str = dt_from.strftime('%d/%m/%y') + ' à ' + \
    (dt_now).strftime('%d/%m/%y')

df_M15 = copyRatesFrom(stock, mt5.TIMEFRAME_M15, dt_from, dt_now)
mean_M15 = mean(df_M15)

df_M5 = copyRatesFrom(stock, mt5.TIMEFRAME_M5, dt_from, dt_now)
mean_M5 = mean(df_M5)

levels: List[float] = []

levels_M15 = filterLevels(levels, df_M15, mean_M15)
levels_M5 = filterLevels(levels, df_M5, mean_M5)

levels.sort()
print(levels)

plot = fplt.plot(
    df_M15,
    title=stock + ' | ' + period_str + ' | M15',
    hlines=levels_M15,
    type='candle',
    ylabel='Preço (R$)'
)

plot = fplt.plot(
    df_M5,
    title=stock + ' | ' + period_str + ' | M5',
    hlines=levels_M5,
    type='candle',
    ylabel='Preço (R$)'
)

plot = fplt.plot(
    df_M5,
    title=stock + ' | ' + period_str + ' | M15 + (M5)',
    hlines=levels,
    type='candle',
    ylabel='Preço (R$)'
)
