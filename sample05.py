import mplfinance as fplt
import pandas as pd

columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Ticks', 'Volume']
only_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
df = pd.read_csv('WINZ20M5.csv', names=columns, usecols=only_columns)
df['Date']=pd.to_datetime(df['Date'], format='%Y.%m.%d %H:%M' , errors='coerce')
df = df.set_index('Date')

df_subset = df.loc[(df.index >= '2020-10-30') & (df.index < '2020-10-31')]

fplt.plot(
            df_subset,
            type='candle',
            title='WINZ20 M5',
            ylabel='Preço (R$)'
        )