import time
from datetime import datetime, timedelta

from First_Iteration.v2.telegram import send_telegram
from First_Iteration.v2.PriceAction import Price_Action
from First_Iteration.v2.get_data import get_data
from First_Iteration.v2.const import LOG_PATH
from First_Iteration.v2.logger import log
from First_Iteration.v2.price_action_confirmation import Confirmation
from First_Iteration.v2.get_real_time_data import get_real_time_data


def runner():
    historical_data = get_data('1 D', '1 min')
    log(historical_data, LOG_PATH)
    p = Price_Action(historical_data)
    shooting_star = p.shooting_star()
    engulfing = p.engulfing()
    hammer = p.hammer()
    if engulfing is not None:
        if 'price_action' in engulfing:
            log(f"{engulfing['price_action']} on 5 mins timeframe", LOG_PATH)
            send_telegram(f"{engulfing['price_action']} on 5 mins timeframe")
            now = datetime.now()
            now_plus_5 = now + timedelta(seconds=55)
            while datetime.now() < now_plus_5:
                if len(get_real_time_data('60 S', '10 secs')) > 0 or get_real_time_data('60 S', '10 secs') is not None:
                    if Confirmation(engulfing, get_real_time_data('60 S', '10 secs')).price_action_confirmation() is not None:
                        log(Confirmation(engulfing, get_real_time_data('60 S', '10 secs')).price_action_confirmation(), LOG_PATH)
                        send_telegram(f"{Confirmation(engulfing, get_real_time_data('60 S', '10 secs')).price_action_confirmation()}")
                        break
                    else:
                        pass
                else:
                    pass
                time.sleep(5)
        else:
            pass
    else:
        pass

    if hammer is not None:
        if 'price_action' in hammer:
            log(f"{hammer['price_action']} on 5 mins timeframe", LOG_PATH)
            send_telegram(f"{hammer['price_action']} on 5 mins timeframe")
            now = datetime.now()
            now_plus_5 = now + timedelta(seconds=55)
            while datetime.now() < now_plus_5:
                if len(get_real_time_data('60 S', '10 secs')) > 0 or  get_real_time_data('60 S', '10 secs') is not None:
                    if Confirmation(hammer, get_real_time_data('60 S', '10 secs')).price_action_confirmation() is not None:
                        log(Confirmation(hammer, get_real_time_data('60 S', '10 secs')).price_action_confirmation(), LOG_PATH)
                        send_telegram(f"{Confirmation(hammer, get_real_time_data('60 S', '10 secs')).price_action_confirmation()}")
                        break
                    else:
                        pass
                else:
                    pass
                time.sleep(5)

        else:
            pass
    else:
        pass

    if shooting_star is not None:
        if 'price_action' in shooting_star:
            log(f"{shooting_star['price_action']} on 5 mins timeframe", LOG_PATH)
            send_telegram(f"{shooting_star['price_action']} on 5 mins timeframe")
            now = datetime.now()
            now_plus_5 = now + timedelta(seconds=55)
            while datetime.now() < now_plus_5:
                if len(get_real_time_data('60 S', '10 secs')) > 0 or get_real_time_data('60 S', '10 secs') is not None:
                    if Confirmation(shooting_star, get_real_time_data('60 S', '10 secs')).price_action_confirmation() is not None:
                        log(Confirmation(shooting_star, get_real_time_data('60 S', '10 secs')).price_action_confirmation(), LOG_PATH)
                        send_telegram(f"{Confirmation(shooting_star, get_real_time_data('60 S', '10 secs')).price_action_confirmation()}")
                        break
                    else:
                        pass
                else:
                    pass
                time.sleep(5)
        else:
            pass
    else:
        pass


try:
    time_now = datetime.utcnow()
    prev_minute = time_now.minute - (time_now.minute % 1)
    time_rounded = time_now.replace(minute=prev_minute, second=0, microsecond=0)

    while True:
        time_rounded += timedelta(minutes=1)
        time_to_wait = abs((time_rounded - datetime.utcnow()).total_seconds())
        time.sleep(time_to_wait)
        runner()
except KeyError:
    log(f"K {KeyError}", LOG_PATH)
    pass
