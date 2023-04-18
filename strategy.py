#####################################
# This file contains strategies
# A strategy should return buy, sell or hold
#####################################

class Strategy():
    # parent class of strategy
    def __init__(self):
        self.do_preprocessing = False
        
    def __call__(self):
        pass

class Pullback(Strategy):
    # Pullback strategy, inherited from Strategy
    def __init__(self, threshold=0.01):
        super().__init__()
        # Safty zone
        self.threshold = threshold 
        self.do_preprocessing = True

    def __call__(self, price_data):
        if price_data['Close'] < price_data['SMA20'] * (1 - self.threshold):
            return 'buy'
        elif price_data['Close'] > price_data['SMA20']:
            return 'sell'
        else:
            return 'hold'
            
    def preprocess_data(self, timeseris_data):
        # Calculate Simple Moving Average -- 20 days
        timeseris_data['SMA20'] = timeseris_data['Close'].rolling(window=20).mean()
        return timeseris_data
