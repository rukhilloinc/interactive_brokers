# Import libraries
import threading
import time

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

from First_Iteration.v2.const import LOG_PATH
from First_Iteration.v2.logger import log


class Historical_Data(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []
        log('Historical data connection is being established with IB', LOG_PATH)

    def error(self, reqId, errorCode, errorString):
        log("Error {} {} {}".format(reqId, errorCode, errorString), LOG_PATH)

    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data.append({"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume})
        else:
            self.data.append({"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                         "Volume": bar.volume})


def websocket_con():
    app.run()


app = Historical_Data()
app.connect("127.0.0.1", 7497, clientId=2)

con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)


def futures(symbol="ES", sec_type="FUT", currency="USD", exchange="GLOBEX", lastTradeDateOrContractMonth="202103"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    return contract


def histData(contract, duration, candle_size):
    app.reqHistoricalData(reqId=2,
                          contract=contract,
                          endDateTime='',
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=0,
                          formatDate=1,
                          keepUpToDate=False,
                          chartOptions=[])  # EClient function to request contract details


def get_data(period, timeframe):
    histData(futures(), period, timeframe)
    time.sleep(2)
    d = app.data
    if d is not None:
        v = [{'previous': d[-2]}, {'latest': d[-1]}]
        return v
    else:
        pass