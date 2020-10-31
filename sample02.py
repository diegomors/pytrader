from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5

# conecte-se ao MetaTrader 5
if not mt5.initialize(login=25115284, server="MetaQuotes-Demo",password="4zatlbqx"):
    print("initialize() failed")
    mt5.shutdown()

# consultamos o estado e os parâmetros de conexão
print(mt5.terminal_info())
# obtemos informações sobre a versão do MetaTrader 5
print(mt5.version())

# solicitamos 1 000 ticks de EURAUD
euraud_ticks = mt5.copy_ticks_from("EURAUD", datetime(2020,10,30,13), 1000, mt5.COPY_TICKS_ALL)
# solicitamos ticks de AUDUSD no intervalo 2019.10.29 13:00 - 2019.10.30 13:00
audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2020,10,29,13), datetime(2020,10,30,13), mt5.COPY_TICKS_ALL)

# obtemos barras de vários instrumentos de diferentes maneiras
eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(2020,10,30,13), 1000)
eurgbp_rates = mt5.copy_rates_from_pos("EURGBP", mt5.TIMEFRAME_M1, 0, 1000)
eurcad_rates = mt5.copy_rates_range("EURCAD", mt5.TIMEFRAME_M1, datetime(2020,10,29,13), datetime(2020,10,30,13))

# concluímos a conexão ao MetaTrader 5
mt5.shutdown()

#DATA
print('euraud_ticks(', len(euraud_ticks), ')')
for val in euraud_ticks[:10]: print(val)

print('audusd_ticks(', len(audusd_ticks), ')')
for val in audusd_ticks[:10]: print(val)

print('eurusd_rates(', len(eurusd_rates), ')')
for val in eurusd_rates[:10]: print(val)

print('eurgbp_rates(', len(eurgbp_rates), ')')
for val in eurgbp_rates[:10]: print(val)

print('eurcad_rates(', len(eurcad_rates), ')')
for val in eurcad_rates[:10]: print(val)

#PLOT
# a partir dos dados recebidos criamos o DataFrame
ticks_frame = pd.DataFrame(euraud_ticks)
# plotamos os ticks no gráfico
plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')

# exibimos rótulos
plt.legend(loc='upper left')

# adicionamos cabeçalho
plt.title('EURAUD ticks')

# mostramos o gráfico
plt.show()