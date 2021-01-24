from datetime import datetime, timedelta

from logger import log
from orders import market_order
from telegram import send_telegram
from v1.PriceAction import price_action
from v1.const import LOG_PATH
from v1.rtmd import price_action_confirmation


def trade():
    p_act = price_action(1, 5)
    if len(p_act)>0:
        now = datetime.now()
        now_plus_10 = now + timedelta(minutes=10)
        req_id = 0
        while datetime.now() < now_plus_10:
            req_id = req_id + 1
            if price_action_confirmation(req_id, p_act) == 'BUY':
                market_order('BUY', 1)
                log(f'Market Buy sent', LOG_PATH)
                send_telegram(f'Market Buy sent')
                return 'BUY'
            elif price_action_confirmation(req_id, p_act) == 'SELL':
                market_order('SELL', 1)
                log(f'Market Sell sent', LOG_PATH)
                send_telegram(f'Market Sell sent')
                return 'SELL'
            else:
                pass
