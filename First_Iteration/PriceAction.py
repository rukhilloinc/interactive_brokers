# Import libraries
import datetime
from datetime import datetime
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import threading
import json
import time
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


import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_last_5_min_data():
    histData(generalStk(), '1 D', '5 mins')
    time.sleep(5)
    data = pd.DataFrame(app.data)
    l = data.tail(3)
    h = l.head(2)
    dataFrame = pd.DataFrame(h)
    jso = dataFrame.to_json()
    js = json.loads(jso)
    log(f"last 5 mins data: {js['1']}")
    js = js['1']
    date_time_obj = []
    for i in js.values():
        t = i['Date'].split()[1]
        date_time_obj.append(datetime.strptime(t, '%H:%M:%S').time())
    d = {'earliest': min(date_time_obj), 'latest': max(date_time_obj)}
    v = []
    for i in js.values():
        ti = i['Date'].split()[1]
        if str(d['earliest']) == ti:
            v.append({'previous': i})
        if str(d['latest']) == ti:
            v.append({'latest': i})
    log(f"Manipulated data {v}")
    return v


def engulfing():
    data = get_last_5_min_data()
    prev_h = data[0]['previous']['High']
    cur_h = data[1]['latest']['High']
    prev_l = data[0]['previous']['Low']
    cur_l = data[1]['latest']['Low']
    cur_o = data[1]['latest']['Open']
    cur_c = data[1]['latest']['Close']
    volume_prev = data[0]['previous']['Volume']
    volume_cur = data[1]['latest']['Volume']
    if volume_prev < volume_cur:
        if cur_h > prev_h and cur_l < prev_l:
            if cur_o < cur_c:
                log('bullish engulfing')
            elif cur_o > cur_c:
                log('bearish engulfing')
            elif cur_o == cur_c:
                log('indecision engulfing')
        else:
            pass


def hammer():
    data = get_last_5_min_data()
    volume_prev = data[0]['previous']['Volume']
    volume_cur = data[1]['latest']['Volume']
    cur_h = data[1]['latest']['High']
    cur_l = data[1]['latest']['Low']
    cur_o = data[1]['latest']['Open']
    cur_c = data[1]['latest']['Close']
    if cur_o > cur_c:
        candle_color = 'red'
        candle_range = cur_h - cur_l
        body_range = cur_o - cur_c
        top_wick = cur_h - cur_o
        bottom_wick = cur_c - cur_l
        dic = {'candle_color': candle_color, 'candle_range': candle_range, 'body_range': body_range,
               'top_wick': top_wick, 'bottom_wick': bottom_wick, 'volume_prev': volume_prev,
               'volume_cur': volume_cur}
        log({'candle_color': candle_color, 'candle_range': candle_range, 'body_range': body_range,
             'top_wick': top_wick, 'bottom_wick': bottom_wick, 'volume_prev': volume_prev,
             'volume_cur': volume_cur})
    elif cur_c > cur_o:
        candle_color = 'grn'
        candle_range = cur_h - cur_l
        body_range = cur_c - cur_o
        top_wick = cur_h - cur_c
        bottom_wick = cur_o - cur_l
        dic = {'candle_color': candle_color, 'candle_range': candle_range, 'body_range': body_range,
               'top_wick': top_wick, 'bottom_wick': bottom_wick, 'volume_prev': volume_prev,
               'volume_cur': volume_cur}
        log({'candle_color': candle_color, 'candle_range': candle_range, 'body_range': body_range,
             'top_wick': top_wick, 'bottom_wick': bottom_wick, 'volume_prev': volume_prev,
             'volume_cur': volume_cur})
    else:
        dic = {'candle': 'indecision'}

    if 'bottom_wick' in dic.keys():
        if dic['volume_prev'] < dic['volume_cur']:
            if dic['bottom_wick'] > dic['top_wick'] and dic['candle_range'] > dic['body_range'] * 3:
                log(f'bullish hammer {dic}')
            elif dic['bottom_wick'] < dic['top_wick'] and dic['candle_range'] > dic['body_range'] * 3:
                log(f'shooting star {dic}')
    else:
        log('Indecision')
    return dic

