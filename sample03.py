from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
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

rates_frame = pd.DataFrame(winz20_rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
rates_frame['time_formatted']=rates_frame['time'].dt.strftime('%d/%m %H:%M')

print(rates_frame.tail(10))

plt.plot(rates_frame['time_formatted'], rates_frame['low'], 'r-', label='low')
plt.plot(rates_frame['time_formatted'], rates_frame['high'], 'b-', label='high')

plt.xticks(rotation=45, size = 8)

plt.legend(loc='upper left')

plt.title(title)

plt.show()