import plotly.graph_objects as go
import pandas as pd

columns = ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']
df = pd.read_csv('WINZ20M5.csv', names=columns)
df['time']=pd.to_datetime(df['time'], format='%Y.%m.%d %H:%M' , errors='coerce')

fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

fig.show()