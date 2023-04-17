import yfinance as yf
from strategy import Pullback
from datetime import datetime

class StockTradeSimulator:
    def __init__(self, symbol, start_date, end_date, initial_capital, strategy):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.shares  = 0
        # Download data
        self.stock_data = yf.download(symbol, start=start_date, end=end_date)
        self.strategy = strategy
        if self.strategy.do_preprocessing:
            self.stock_data = self.strategy.preprocess_data(self.stock_data)

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
    
    def simulate(self):
        pre_buy_price = 0
        # Sweep everyday
        for date, row in self.stock_data.iterrows():
            # The strategy should tell us buy, sell or hold
            action = self.strategy(row)
            
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

if __name__ == '__main__':
    symbol = '0050.tw'          # Stock Name
    start_date = '2001-01-01'   # Start Date
    end_date = '2022-03-02'     # End Date
    initial_capital = 10000     # Budget
    
    strategy = "pullback"
    if strategy == "pullback":
        trading_strategy = Pullback()
    else:
        raise Exception("The strategy is not implemented yet")

    # Initialize Simulator
    simulator = StockTradeSimulator(symbol, start_date, end_date, initial_capital, trading_strategy)
    # Start simulation
    final_capital, final_shares, net, irr = simulator.simulate()


    print(f'Final Capital: {final_capital:.2f}')
    print(f'Shares: {final_shares:.2f}')
    print(f'Net: {net:.2f}')
    print(f'IRR: {irr:.2f}%')
