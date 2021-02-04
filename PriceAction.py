class Price_Action:
    def __init__(self, data):
        self.prev_h = data[0]['previous']['High']
        self.prev_l = data[0]['previous']['Low']
        self.volume_prev = data[0]['previous']['Volume']
        self.volume_cur = data[1]['latest']['Volume']
        self.cur_d = data[1]['latest']['Date']
        self.cur_h = data[1]['latest']['High']
        self.cur_l = data[1]['latest']['Low']
        self.cur_o = data[1]['latest']['Open']
        self.cur_c = data[1]['latest']['Close']

    # Hammer
    def hammer(self):
        if len(self.cur_d) > 0:
            if self.volume_cur >= self.volume_prev:
                if self.cur_c > self.cur_o:
                    if (self.cur_h - self.cur_l) > (abs(self.cur_h - self.cur_o) * 2.5):
                        return {'datetime': self.cur_d, 'high': self.cur_h, 'price_action': 'hammer'}
                    else:
                        pass
                elif self.cur_c < self.cur_o:
                    if (self.cur_h - self.cur_l) > (abs(self.cur_h - self.cur_c) * 2.5):
                        return {'datetime': self.cur_d, 'high': self.cur_h, 'price_action': 'hammer'}
                    else:
                        pass
                elif self.cur_c == self.cur_o:
                    if (self.cur_h - self.cur_l) > (abs(self.cur_h - self.cur_c) * 2.5):
                        return {'datetime': self.cur_d, 'high': self.cur_h, 'price_action': 'hammer'}
                    else:
                        pass
            else:
                pass
        else:
            pass

    # Shooting star
    def shooting_star(self):
        if len(self.cur_d) > 0:
            if self.volume_cur >= self.volume_prev:
                if self.cur_c > self.cur_o:
                    if (self.cur_h - self.cur_l) > (abs(self.cur_l - self.cur_c) * 2.5):
                        return {'datetime': self.cur_d, 'high': self.cur_l, 'price_action': 'shooting_star'}
                    else:
                        pass
                elif self.cur_c < self.cur_o:
                    if (self.cur_h - self.cur_l) > (abs(self.cur_l - self.cur_o) * 2.5):
                        return {'datetime': self.cur_d, 'high': self.cur_l, 'price_action': 'shooting_star'}
                    else:
                        pass
                elif self.cur_c == self.cur_o:
                    if (self.cur_h - self.cur_l) > (abs(self.cur_l - self.cur_o) * 2.5):
                        return {'datetime': self.cur_d, 'high': self.cur_l, 'price_action': 'shooting_star'}
                    else:
                        pass
            else:
                pass
        else:
            pass

    # Bearish/Bullish Engulfing
    def engulfing(self):
        if len(self.cur_d) > 0:
            if self.volume_prev <= self.volume_cur:
                if self.cur_h > self.prev_h and self.cur_l < self.prev_l:
                    if self.cur_o < self.cur_c:
                        return {'datetime': self.cur_d, 'high': self.cur_h, 'price_action': 'bullish_engulfing'}
                    elif self.cur_o > self.cur_c:
                        return {'datetime': self.cur_d, 'low': self.cur_l, 'price_action': 'bearish_engulfing'}
                    else:
                        pass
                else:
                    pass
        else:
            pass


