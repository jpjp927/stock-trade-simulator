import argparse
import yfinance as yf
import strategy
from datetime import datetime

class StockTradeSimulator:
    def __init__(self, args):
        self.symbol = args.symbol
        self.start_date = args.start_date
        self.end_date = args.end_date
        self.initial_capital = args.initial_capital
        try:
            self.strategy = getattr(strategy, args.strategy)()
        except:
            print("[Error] The strategy is not implemented yet")
            exit()

        self.capital = self.initial_capital
        self.shares  = 0
        # Download data
        self.stock_data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--symbol", help="stock ticker", default="0050.tw")
    parser.add_argument("-b", "--start_date", help="start date of simulation", default="2001-01-01")
    parser.add_argument("-e", "--end_date", help="end date of simulation", default="2022-03-02")
    parser.add_argument("-i", "--initial_capital", help="cappital before on simulatoin", default=10000)
    parser.add_argument("-s", "--strategy", help="trading strategy", default="Pullback")
    args = parser.parse_args()

    # Initialize Simulator
    simulator = StockTradeSimulator(args)
    # Start simulation
    final_capital, final_shares, net, irr = simulator.simulate()

    print("===================")
    print(f'Final Capital: {final_capital:.2f}')
    print(f'Shares: {final_shares:.2f}')
    print(f'Net: {net:.2f}')
    print(f'IRR: {irr:.2f}%')
    print("===================")
