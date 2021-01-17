from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def historicalDataUpdate(self, reqId, bar):
        print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)



app = TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)
app.run()


def contracts(symbol="ES", secType="FUT", exchange="GLOBEX", lastTradeDateOrContractMonth="202103"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.currency = "USD"
    contract.exchange = exchange
    contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    print('Contract details are retrieved', contract)
    return contract


def histData(cont, duration, candle_size):
    print('Requesting historical data...')
    data = app.reqHistoricalData(reqId=1,
                                 contract=cont,
                                 endDateTime='',
                                 durationStr=duration,
                                 barSizeSetting=candle_size,
                                 whatToShow='ADJUSTED_LAST',
                                 useRTH=1,
                                 formatDate=1,
                                 keepUpToDate=0,
                                 chartOptions=[])
    print(dir(data))
    print(type(data))
    print(data.__str__)


histData(contracts(), '1 D', '5 mins')
