class Confirmation:
    def __init__(self, price_action_data, real_time_data):
        self.price_action_data = price_action_data
        self.real_time_data = real_time_data

    def price_action_confirmation(self):
        if self.price_action_data is not None:
            if 'price_action' in self.price_action_data:
                if self.real_time_data is not None:
                    if self.price_action_data['price_action'] == 'hammer' or self.price_action_data['price_action']=='bullish_engulfing':
                        if self.real_time_data['High'] > self.price_action_data['High']:
                            return f"Buy {self.price_action_data['price_action']} Higher High"
                        else:
                            pass
                    elif self.price_action_data['price_action'] == 'shooting_star' or self.price_action_data['price_action']=='bearish_engulfing':
                        if self.real_time_data['Low'] < self.price_action_data['Low']:
                            return f"Sell {self.price_action_data['price_action']} Lower Low"

                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass
