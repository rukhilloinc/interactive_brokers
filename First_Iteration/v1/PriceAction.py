# Import libraries
from datetime import datetime, timedelta
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import threading
import json
import time
from First_Iteration.logger import log
from First_Iteration.telegram import send_telegram
from First_Iteration.v1.const import LOG_PATH

bull_engulf = f'Bullish Engulfing'
bear_engulf = f'Bearish Engulfing'
hammer = f'Bullish Hammer'
shooting_star = f'Bearish Shooting star'


class PriceAction(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}
        log('Connection is being established with IB', LOG_PATH)

    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = [
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume}]

        else:
            self.data[reqId].append(
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume})
        # print(f" historicalData:reqID:{reqId}, date:{bar.date}, open:{bar.open}, high:{bar.high}, low:{bar.low}")
        # close:{bar.close}, volume:{bar.volume}")


def websocket_con():
    app.run()


app = PriceAction()
app.connect("127.0.0.1", 7496, clientId=1)

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


def get_last_5_min_data(period, timeframe):
    histData(futures(), f'{period} D', f'{timeframe} mins')
    time.sleep(2)
    data = pd.DataFrame(app.data)
    l = data.tail(3)
    h = l.tail(2)
    # log(f'h {h}', LOG_PATH)
    # log(f'l {l}', LOG_PATH)
    dataFrame = pd.DataFrame(h)
    jso = dataFrame.to_json()
    js = json.loads(jso)
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
    return v


def price_action(period, timeframe):
    data = get_last_5_min_data(period, timeframe)
    log(data, LOG_PATH)
    prev_h = data[0]['previous']['High']
    prev_l = data[0]['previous']['Low']
    volume_prev = data[0]['previous']['Volume']
    volume_cur = data[1]['latest']['Volume']
    cur_d = data[1]['latest']['Date']
    cur_h = data[1]['latest']['High']
    cur_l = data[1]['latest']['Low']
    cur_o = data[1]['latest']['Open']
    cur_c = data[1]['latest']['Close']

    if len(cur_d) > 0:
        if volume_cur > volume_prev:
            if cur_c > cur_o:
                if (cur_h - cur_l) > (abs(cur_h - cur_o) * 3):
                    log(f'{hammer}', LOG_PATH)
                    send_telegram(hammer)
                    return {'datetime': cur_d, 'high': cur_h, 'price_action': 'hammer'}
                else:
                    pass
            elif cur_c < cur_o:
                if (cur_h - cur_l) > (abs(cur_h - cur_c) * 3):
                    log(f'{hammer}', LOG_PATH)
                    send_telegram(hammer)
                    return {'datetime': cur_d, 'high': cur_h, 'price_action': 'hammer'}
                else:
                    pass
        else:
            pass
    else:
        pass

    if len(cur_d) > 0:
        if volume_cur > volume_prev:
            if cur_c > cur_o:
                if (cur_h - cur_l) > (abs(cur_l - cur_c) * 3):
                    log(f'{shooting_star}', LOG_PATH)
                    send_telegram(shooting_star)
                    return {'datetime': cur_d, 'high': cur_l, 'price_action': 'shooting_star'}
                else:
                    pass
            elif cur_c < cur_o:
                if (cur_h - cur_l) > (abs(cur_l - cur_o) * 3):
                    log(f'{shooting_star}', LOG_PATH)
                    send_telegram(shooting_star)
                    return {'datetime': cur_d, 'high': cur_l, 'price_action': 'shooting_star'}
                else:
                    pass
        else:
            pass
    else:
        pass

    if len(cur_d) > 0:
        if volume_prev < volume_cur:
            if cur_h > prev_h and cur_l < prev_l:
                if cur_o < cur_c:
                    log(f'{bull_engulf}', LOG_PATH)
                    send_telegram(bull_engulf)
                    return {'datetime': cur_d, 'high': cur_h, 'price_action': 'bull_engulf'}
                elif cur_o > cur_c:
                    log(f'{bear_engulf}', LOG_PATH)
                    send_telegram(bear_engulf)
                    return {'datetime': cur_d, 'low': cur_l, 'price_action': 'bear_engulf'}
                elif cur_o == cur_c:
                    log(f'indecision engulfing', LOG_PATH)
                    send_telegram('indecision engulfing')
            else:
                pass
    else:
        pass


try:
    time_now = datetime.utcnow()
    prev_minute = time_now.minute - (time_now.minute % 5)
    time_rounded = time_now.replace(minute=prev_minute, second=0, microsecond=0)

    while True:
        time_rounded += timedelta(minutes=5)
        time_to_wait = (time_rounded - datetime.utcnow()).total_seconds()
        time.sleep(time_to_wait)
        price_action(1, 5)
except:
    log(KeyError, LOG_PATH)
    pass
