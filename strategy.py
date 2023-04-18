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
    def __init__(self, threshold=0.01, window=20):
        super().__init__()
        # Safty zone
        self.threshold = threshold 
        self.window = window
        self.do_preprocessing = True

    def __call__(self, price_data):
        if price_data['Close'] < price_data['SMA'] * (1 - self.threshold):
            return 'buy'
        elif price_data['Close'] > price_data['SMA']:
            return 'sell'
        else:
            return 'hold'
            
    def preprocess_data(self, timeseris_data):
        # Calculate Simple Moving Average -- 20 days
        timeseris_data['SMA'] = timeseris_data['Close'].rolling(window=self.window).mean()
        return timeseris_data


   
"""
"buy" if the momentum is positive and the price is above the moving average,
"sell" if the momentum is negative and the price is below the moving average,
"hold" if the momentum is neutral.
"""
class Momentum(Strategy):
    def __init__(self, window=20):
        super().__init__()
        self.window = window
        self.do_preprocessing = True
        
    def preprocess_data(self, timeseris_data):
        timeseris_data['SMA'] = timeseris_data['Close'].rolling(window=self.window).mean()
        timeseris_data['Before'] = timeseris_data['Close'].shift(self.window)
        return timeseris_data
    
    def __call__(self, price_data):
        # Calculate momentum
        # momentum = (price_data["Close"] / price_data["Close"].shift(self.window)) - 1
        momentum = price_data["Close"] - price_data["Before"]
        if momentum > 0 and price_data["Close"] > price_data["SMA"]:
            return "buy"
        elif momentum < 0 and price_data["Close"] < price_data["SMA"]:
            return "sell"
        else:
            return "hold"
