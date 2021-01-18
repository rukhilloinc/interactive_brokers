# Import libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import threading
import time
import json

from logger import log


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = [
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume}]

        else:
            self.data[reqId].append(
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume})
        # log(f" historicalData:reqID:{reqId}, date:{bar.date}, open:{bar.open}, high:{bar.high}, low:{bar.low}, close:{bar.close}, volume:{bar.volume}")


def websocket_con():
    app.run()


app = TradeApp()
app.connect("127.0.0.1", 7497, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)  # some latency added to ensure that the connection is established


# creating object of the Contract class - will be used as a parameter for other function calls
def generalStk(symbol="ES", sec_type="FUT", currency="USD", exchange="GLOBEX", lastTradeDateOrContractMonth="202103"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    log(f'Contract details extracted {contract}')
    return contract


def histData(contract, duration, candle_size):
    app.reqHistoricalData(reqId=1,
                          contract=contract,
                          endDateTime='',
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=0,
                          formatDate=1,
                          keepUpToDate=False,
                          chartOptions=[])  # EClient function to request contract details


def get_last_5_min_data():
    histData(generalStk(), '1 D', '5 mins')
    time.sleep(5)
    data = pd.DataFrame(app.data)
    l = data.tail(1)
    dataFrame = pd.DataFrame(l)
    jso = dataFrame.to_json()
    js = json.loads(jso)
    g = list(js['1'].keys())
    g1 = str(g)[2:-2]
    data = js['1'][g1]
    log(f'last 5 mins data: {data}')
    return data


while True:
    get_last_5_min_data()
    time.sleep(300)



