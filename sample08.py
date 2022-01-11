import mplfinance as fplt
import pandas as pd

# Load data
columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Ticks', 'Volume']
only_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
df = pd.read_csv('WDOJ21M5.csv', names=columns, usecols=only_columns)
df['Date'] = pd.to_datetime(
    df['Date'], format='%Y.%m.%d %H:%M', errors='coerce')
df = df.set_index('Date')

# Calculate exponential moving average
df['EMA_9'] = df.loc[:, 'Close'].ewm(span=9, adjust=False).mean()

# Select intraday period
df_subset = df.loc[(df.index >= '2021-03-22') & (df.index < '2021-03-23')]

# Create a subplot to EMA_9
ema9 = [fplt.make_addplot(df_subset['EMA_9'], color='fuchsia')]

# Plot candlestick graphic
fplt.plot(
    df_subset,
    type='candle',
    title='WDOJ21 M5',
    ylabel='Preço (R$)',
    addplot=ema9
)
