import yfinance as yf
from strategy import *
from datetime import datetime

class StockTradeSimulator:
    def __init__(self, symbol, start_date, end_date, initial_capital):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.shares  = 0
        # Download data
        self.stock_data = yf.download(symbol, start=start_date, end=end_date)

    def buy(self, share, price):
        cost = share * price
        if cost > self.capital:
            return False
        self.capital -= cost
        self.shares += share
        return True

    def sell(self, share, price):
        if share == 0:
            return False
        earnings = share * price
        self.capital += earnings
        self.shares -= share
        return True

    def cal_irr(self):
        d1 = datetime.strptime(self.start_date, "%Y-%m-%d")
        d2 = datetime.strptime(self.end_date, "%Y-%m-%d")
        years = (d2 - d1).days/365   
        return ((self.capital / self.initial_capital)**(1/years))-1
    
    def simulate(self, strategy):
        pre_buy_price = 0

        # Sweep everyday
        for date, row in self.stock_data.iterrows():
            # The strategy should tell us buy, sell or hold
            action = strategy(row)
            
            # Buy
            if action == 'buy':
                share = self.capital // row['Close']
                if self.buy(share, row['Close']):
                    pre_buy_price = row['Close']
            
            # Sell
            elif action == 'sell':
                if self.sell(self.shares, row['Close']):
                    print('Gain: ', row['Close']-pre_buy_price)
            # Hold
            else:
                continue
        
        final_capital = self.capital
        final_shares = self.shares
        # Get current holdings value
        self.sell(self.shares, row['Close'])
        # Calculate Internal Rate of Return (IRR)
        irr = self.cal_irr() * 100
    
        return final_capital, final_shares, self.capital, irr

# def pullback_strategy(row, threshold):
#     if row['Close'] < row['SMA20'] * (1 - threshold):
#         return 'buy'
#     elif row['Close'] > row['SMA20']:
#         return 'sell'
#     else:
#         return 'hold'

if __name__ == '__main__':
    symbol = '0050.tw'          # Stock Name
    start_date = '2001-01-01'   # Start Date
    end_date = '2022-03-02'     # End Date
    initial_capital = 10000     # Budget
    threshold = 0.01            # Safty zone

    # Initialize Simulator
    simulator = StockTradeSimulator(symbol, start_date, end_date, initial_capital)
    # Calculate Simple Moving Average -- 20 days
    simulator.stock_data['SMA20'] = simulator.stock_data['Close'].rolling(window=20).mean()

    # Start simulation
    final_capital, final_shares, net, irr = simulator.simulate(lambda row: pullback_strategy(row, threshold))


    print(f'Final Capital: {final_capital:.2f}')
    print(f'Shares: {final_shares:.2f}')
    print(f'Net: {net:.2f}')
    print(f'IRR: {irr:.2f}%')
