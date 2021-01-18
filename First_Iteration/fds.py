import datetime
import json
d = {'date_time': '20210115  08:45:00', 'open': 3776.75, 'high': 3780.5, 'low': 3775.25, 'close': 3778.25, 'volume': 22536}


# end_time = (datetime.datetime.today()).strftime("%Y%m%d %H:%M:%S")
# start_time = (datetime.datetime.today()-datetime.timedelta(minutes=5, seconds=2)).strftime("%Y%m%d %H:%M:%S")
# print(start_time)


j = {"1":{"69":{"Date":"20210117  22:45:00","Open":3753.25,"High":3753.25,"Low":3752.75,"Close":3753.25,"Volume":98},
          "70":{"Date":"20210117  22:50:00","Open":3753.25,"High":3753.5,"Low":3753.0,"Close":3753.25,"Volume":108}}}

jo = j['1'].keys()
print(jo)