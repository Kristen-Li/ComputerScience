"""
this file returns the trades 
"""

import pandas as pd
import datetime as dt

from util import get_data, plot_data

def testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    df_prices = get_data([symbol], pd.date_range(sd, ed))
    
    if symbol != 'SPY': 
        df_prices = df_prices.drop(['SPY'], axis=1)
        
    df_prices['diff'] = df_prices.shift(-1)-df_prices
    
    df_prices['diff'] = df_prices['diff']/abs(df_prices['diff']) 
    
    df_prices.fillna(method='bfill',inplace=True) 
    
    df_trades = pd.DataFrame(data=0, index=df_prices.index, columns={symbol})
    
    prev_pos = df_prices.ix[0,-1]
    df_trades[symbol] = prev_pos * 1000
    
    for i,j in df_prices[1:].iterrows():
        if j['diff'] == prev_pos:
            df_trades.loc[i] = 0
        else:
            df_trades.loc[i] = prev_pos*-2000
            prev_pos = j['diff']
    
    df_trades.ix[-1] = 0 # last day cannot see into the future
    return(df_trades)

