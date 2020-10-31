import MetaTrader5 as mt5
# exibimos dads sobre o pacote MetaTrader5
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# estabelecemos a conexão com o terminal MetaTrader 5 para a conta especificada
if not mt5.initialize(login=25115284, server="MetaQuotes-Demo",password="4zatlbqx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# imprimimos informações sobre o estado da conexão, o nome do servidor e a conta de negociação
print(mt5.terminal_info())
# imprimimos informações sobre a versão do MetaTrader 5
print(mt5.version())

# concluímos a conexão ao terminal MetaTrader 5
mt5.shutdown()