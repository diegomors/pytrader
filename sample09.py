from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import MetaTrader5 as mt5

# conecte-se ao MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# consultamos o estado e os parâmetros de conexão
print(mt5.terminal_info())
# obtemos informações sobre a versão do MetaTrader 5
print(mt5.version())

# solicitamos 1 000 ticks de WDOK21
WDOK21_ticks = mt5.copy_ticks_from("WDOK21", datetime(2021,4,1), 1000, mt5.COPY_TICKS_ALL)

print('WDOK21_ticks(', len(WDOK21_ticks), ')')
for val in WDOK21_ticks[:10]: print(val)

#PLOT
# a partir dos dados recebidos criamos o DataFrame
ticks_frame = pd.DataFrame(WDOK21_ticks)

# plotamos os ticks no gráfico
plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')

# exibimos rótulos
plt.legend(loc='upper left')

# adicionamos cabeçalho
plt.title('WDOK21 ticks')

# mostramos o gráfico
plt.show()
