import time

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import datetime
import threading

from logger import log
from telegram import send_telegram
from v1.const import LOG_PATH


class RTMD(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}

    def tickByTickAllLast(self, reqId, tickType, time, price, size, tickAtrribLast, exchange, specialConditions):
        super().tickByTickAllLast(reqId, tickType, time, price, size, tickAtrribLast, exchange, specialConditions)
        if tickType == 1:
            pass
        else:
            self.data = {'Time': datetime.datetime.fromtimestamp(time).strftime('%Y%m%d %H:%M:%S'),
                         'Price': price, 'Size': size}
            # log({f" 'ReqId:', {reqId}, 'Time:', {datetime.datetime.fromtimestamp(time).strftime('%Y%m%d
            # %H:%M:%S')},'Price:', {price}, 'Size:', {size}"})


def futures(symbol="ES", sec_type="FUT", currency="USD", exchange="GLOBEX", lastTradeDateOrContractMonth="202103"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    return contract


def streamData(r, contract):
    """stream tick leve data"""
    app.reqTickByTickData(reqId=r,
                          contract=contract,
                          tickType="AllLast",
                          numberOfTicks=0,
                          ignoreSize=False)


def cancel_real_time_md(reqId):
    app.cancelTickByTickData(reqId)


def websocket_con():
    app.run()


app = RTMD()
app.connect(host='127.0.0.1', port=7496, clientId=3)
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()


def price_action_confirmation(req_id, data):
    streamData(req_id, futures())
    rtmd = app.data
    if len(rtmd.values()) != 0:
        if data['price_action'] == 'hammer' or data['price_action'] == 'bull_engulf':
            if rtmd['Price'] > data['high']:
                log(f"Buy signal bc {data['price_action']} higher high", LOG_PATH)
                send_telegram(f"Buy signal bc {data['price_action']} higher high")
                return 'BUY'
            else:
                pass
        elif data['price_action'] == 'shooting_star' or data['price_action'] == 'bear_engulf':
            if rtmd['Price'] < data['low']:
                log(f"Sell signal bc {data['price_action']} lower low", LOG_PATH)
                send_telegram(f"Sell signal bc {data['price_action']} lower low")
                return 'SELL'
            else:
                pass
        else:
            pass
    else:
        pass


# d = {'Time': '20210121 18:48:57', 'Price': 3844.0, 'Size': 1}
# data_h = {'price_action': 'hammer', 'high': 3838}


# while True:
#     try:
#         price_action_confirmation(capture_rt_md(), data_h)
#     except KeyError:
#         continue
#     break

# count = 1
# while count < 5000000000:
#     dd = price_action_confirmation(capture_rt_md(count), price_action())
#     count += 1
#     if dd:
#         break