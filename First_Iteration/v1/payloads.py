import uuid


def market_structure(strategy, low_range, high_range, times_tested, time_frame):
    js = {
        'id' : str(uuid.uuid4())[:6],
        'strategy': strategy,
        'low_range': low_range,
        'high_range': high_range,
        'times_tested': times_tested,
        'time_frame': time_frame
    }
    return js


def abcd_trend(trend, a, b, c, a_low, a_high, b_low, b_high, time_frame):
    js = {
        'id' : str(uuid.uuid4())[:6],
        'trend': trend,
        'a': a,
        'b': b,
        'c': c,
        'a_low': a_low,
        'a_high': a_high,
        'b_low': b_low,
        'b_high': b_high,
        'time_frame': time_frame
    }
    return js
