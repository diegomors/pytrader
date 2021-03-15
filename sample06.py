import MetaTrader5 as mt5
import mplfinance as fplt
import pandas as pd
from datetime import datetime
from datetime import timedelta

stock = 'WDOG21'
timeframe_str = 'M15'
timeframe = mt5.TIMEFRAME_M15
dt_from = datetime(2021, 1, 15)
dt_to = datetime(2021, 1, 16)

period_str = dt_from.strftime('%d/%m/%y') + ' > ' + (dt_to - timedelta(days=1)).strftime('%d/%m/%y')
title = stock + ' ' + timeframe_str + ' [' + period_str + ']'

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

stock_rates = mt5.copy_rates_range(stock, timeframe, dt_from, dt_to)

mt5.shutdown()

print('WDOG21(', len(stock_rates), ')')
for val in stock_rates[:10]: print(val)

rates_frame = pd.DataFrame(stock_rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
rates_frame['time_formatted']=rates_frame['time'].dt.strftime('%d/%m %H:%M')
rates_frame = rates_frame.set_index('time')

fplt.plot(
            rates_frame,
            type='candle',
            title=title,
            ylabel='Preço (R$)'
        )