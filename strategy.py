#####################################
# This file contains strategies
# A strategy should return buy, sell or hold
#####################################


def pullback_strategy(row, threshold):
    if row['Close'] < row['SMA20'] * (1 - threshold):
        return 'buy'
    elif row['Close'] > row['SMA20']:
        return 'sell'
    else:
        return 'hold'