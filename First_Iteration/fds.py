# import json
# d = {'date_time': '20210115  08:45:00', 'open': 3776.75, 'high': 3780.5, 'low': 3775.25, 'close': 3778.25, 'volume': 22536}


# end_time = (datetime.datetime.today()).strftime("%Y%m%d %H:%M:%S")
# start_time = (datetime.datetime.today()-datetime.timedelta(minutes=5, seconds=2)).strftime("%Y%m%d %H:%M:%S")
# print(start_time)
#
#
# j = {"1":{"69":{"Date":"20210117  22:45:00","Open":3753.25,"High":3753.25,"Low":3752.75,"Close":3753.25,"Volume":98},
#           "70":{"Date":"20210117  22:50:00","Open":3753.25,"High":3753.5,"Low":3753.0,"Close":3753.25,"Volume":108}}}
#
# jo = j['1'].keys()
# print(jo)


# import datetime
# #
# # while True:
# #     current_time = datetime.datetime.now()
# #     if current_time.second % 60 == 0 and current_time.minute % 1 == 0 and current_time.microsecond == 0:
# #
# #         print(current_time)

# import time


#
# def get_engulfing_candle():
#     date_time_obj = []
#     data = {'182': {'Date': '20210119  08:10:00', 'Open': 3787.75, 'High': 3788.5, 'Low': 3786.25, 'Close': 3788.0,
#                     'Volume': 1667},
#             '183': {'Date': '20210119  08:15:00', 'Open': 3788.25, 'High': 3789.5, 'Low': 3788.0, 'Close': 3789.5,
#                     'Volume': 2621}}
#     for i in data.values():
#         time = i['Date'].split()[1]
#         date_time_obj.append(datetime.strptime(time, '%H:%M:%S').time())
#     d = {'earliest': min(date_time_obj), 'latest': max(date_time_obj)}
#     l = []
#     for i in data.values():
#         time = i['Date'].split()[1]
#         if str(d['earliest']) == time:
#             l.append({'previous': i})
#         if str(d['latest']) == time:
#             l.append({'latest': i})
#
#     print(l)
#     return l
#

# get_engulfing_candle()
#
# while True:
#     print('book')
#     time.sleep(300)


# #extract and store historical data in dataframe repetitively
# # tickers = ["FB","AMZN","INTC"]
# starttime = time.time()
# timeout = time.time() + 60*5
# while time.time() <= timeout:
#     for ticker in tickers:
#         histData(tickers.index(ticker),usTechStk(ticker),'3600 S', '30 secs')
#         time.sleep(4)
#     historicalData = dataDataframe(app,tickers)
# #     time.sleep(30 - ((time.time() - starttime) % 30.0))
# import datetime
#
# while True:
#     if datetime.datetime.now().second % 5 == 0:
#         print("Time now is ", datetime.datetime.now().minute)
import json

from logger import log

data = [{'previous': {'Date': '20210119  13:50:00', 'Open': 3793.25, 'High': 3794.0, 'Low': 3792.0, 'Close': 3793.0,
                      'Volume': 6059}}, {
            'latest': {'Date': '20210119  13:55:00', 'Open': 3787.75, 'High': 3788.50, 'Low': 3786.25, 'Close': 3788,
                       'Volume': 9759}}]

volume_prev = data[0]['previous']['Volume']
volume_cur = data[1]['latest']['Volume']
cur_h = data[1]['latest']['High']
cur_l = data[1]['latest']['Low']
cur_o = data[1]['latest']['Open']
cur_c = data[1]['latest']['Close']
dic = {}
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
