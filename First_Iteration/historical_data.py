import json
import random
import uuid
import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time


class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def historicalData(self, reqId, bar):

        print( f"reqID:{reqId}, date:{bar.date}, open:{bar.open}, high:{bar.high}, low:{bar.low}, close:{bar.close}, volume:{bar.volume}")

    def headTimestamp(self, reqId: int, headTimestamp: str):
        print("HeadTimestamp. ReqId:", reqId, "HeadTimeStamp:", headTimestamp)


        # m = {'date_time': bar.date, 'open': bar.open,
        #      'high': bar.high, 'low': bar.low,
        #      'close': bar.close, 'volume': bar.volume}


    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)


def websocket_con():
    app.run()


app = TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)  # some latency added to ensure that the connection is established


# creating object of the Contract class - will be used as a parameter for other function calls
def contract(symbol="ES", secType="FUT", exchange="GLOBEX", lastTradeDateOrContractMonth="202103"):
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
    app.reqHistoricalData(reqId=1,
                          contract=cont,
                          endDateTime='',
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=0,
                          formatDate=1,
                          keepUpToDate=False,
                          chartOptions=[])  # EClient function to request contract details

def get_last_data():
    app.reqHeadTimeStamp(4101, contract(), 'ADJUSTED_LAST', 0, 1)

histData(contract(), '1 D', '5 mins')
# get_last_data()
# time.sleep(2)
