"""
CS7646 ML For Trading
Project 6: Manual Strategy
Manual Strategy Function
Wanjun Li

This script implements indicators and generates a trading dataframe. Indicator usage is hardcoded and optimized for 
JPM from 2008 to the end of 2009.
"""

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import warnings

from indicators import ind_sma, ind_OBV, ind_bbp, ind_momentum, ind_MACD,simple_ma
from marketsimcode import compute_portvals,  get_portfolio_stats
from BestPossibleStrategy import testPolicy as bps
from util import get_data, plot_data


def getCol(symbols, start_date, end_date, colname, normed=True):
    col = get_data([symbols], pd.date_range(start_date, end_date), colname)
    if 'SPY' not in symbols:
        col.drop(columns='SPY', inplace=True)

    col = col.fillna(method='ffill')
    col = col.fillna(method='bfill')
    if normed:
        col = col / col.iloc[0]
    return col


def testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    """Accepts a prices df, returns a trade dataframe based on BB, MACD, and Stoch Osc"""

    prices = getCol(symbol, sd, ed, 'Adj Price', normed=True)
    volumes = getCol(symbol, sd, ed, 'Volume', normed=True)
    # BB was implemented into the SMA, the threshold value had been iteratively optimized
    window = 20
    sma, sma_over_price, sma60 = ind_sma(prices,window)
    OBV, OBV_ema = ind_OBV(prices, volumes,window)
    bbp, ub, lb = ind_bbp(prices, window)
    MMT = ind_momentum(prices, window=5)

    macd, macd_s = ind_MACD(prices, ema1_days=12, ema2_days=24, macd_signal_days=9)


    md = (macd['macd'] - macd_s['macd_signal']).rename('m-d')
    md = md.to_frame()
    md_diff = (md.shift(1) / md) / abs(md.shift(1) / md)  # checks if MACD crosses its signal (-1 if it does)

    sma, upper, lower = simple_ma(prices, window=19, bollinger=True, threshold=1.45)

    # df2 is a dashboard of indicator values
    df2 = pd.concat([prices, sma, sma_over_price, upper, lower, sma60, OBV, OBV_ema, bbp,  MMT, md_diff], axis=1)
    df2.set_axis([symbol, 'sma','sma_over_price', 'sma60','upper', 'lower', 'OBV', 'OBV_ema', 'bbp', 'MMT', 'MACD'], axis=1, inplace=True)

    # generating a long/short df marked with 1's or 0's, 1's meaning perform the action
    df_buy = pd.DataFrame(index=df2.index)
    df_sell = df_buy.copy()



    df_buy['SMA'] = np.where(df2.ix[:, 'sma'] > 1, 1, 0)
    df_buy['BB'] = np.where(df2.ix[:,0] < df2.ix[:,'lower'], 1, 0)
    df_buy['BBP'] = np.where(df2.ix[:, 'bbp'] < 0, 1, 0)
    df_buy['OBV'] = np.where(df2.ix[:, 'OBV'] > df2.ix[:, 'OBV_ema'], 1, 0)
    df_buy['MMT'] = np.where(df2.ix[:,'MMT'] > 0.05, 1, 0)
    df_buy['MACD'] = np.where(md_diff.ix[:,0] == -1, 1, 0)

    df_sell['SMA'] = np.where(df2.ix[:, 'sma'] < 1, 1, 0)
    df_sell['BB'] = np.where((df2.ix[:,0] > df2.ix[:,'upper']), 1, 0)
    df_sell['BBP'] = np.where(df2.ix[:, 'bbp'] > 1, 1, 0)
    df_sell['OBV'] = np.where(df2.ix[:, 'OBV'] < df2.ix[:, 'OBV_ema'], 1, 0)
    df_sell['MMT'] = np.where(df2.ix[:,'MMT'] < -0.05, 1, 0)
    df_sell['MACD'] = np.where(md_diff.ix[:,0] == -1, 1, 0)


    df_trades = pd.DataFrame(index=prices.index)
    df_trades[prices.columns[0]] = 0
    holding = 0
    print(df_buy.head(20))

    # Trading Scheme is to long/short primarily off BB crossings. The second criteria is off the strength of the momentum indicators
    for i in df_buy.index:

        if holding== 0:
            # if df_buy.ix[i, 'SMA']  + df_buy.ix[i, 'BBP'] + df_buy.ix[i, 'OBV'] + df_buy.ix[i, 'MMT'] >=3:

            if df_buy.ix[i, 'BB']==1 or df_buy.ix[i,'SMA'] ==1 and   df_buy.ix[i,'MMT']==1 and   df_buy.ix[i,'MACD']==1 :
                df_trades.ix[i, 0] = 1000
                holding = 1000
            elif  df_sell.ix[i, 'BB']==1 or df_sell.ix[i,'SMA']==1 and   df_sell.ix[i,'MMT']==1  and   df_sell.ix[i,'MACD']==1 :
                df_trades.ix[i, 0] = -1000
                holding = -1000
        elif holding == 1000:
            if df_sell.ix[i, 'BB']==1  or df_sell.ix[i,'SMA']==1 and   df_sell.ix[i,'MMT']==1 and   df_sell.ix[i,'MACD']==1 :
                df_trades.ix[i, 0] = -2000
                holding = -1000

        elif holding == -1000:
            if df_buy.ix[i, 'BB'] ==1 or df_buy.ix[i,'SMA'] ==1  and    df_buy.ix[i,'MMT']==1 and   df_buy.ix[i,'MACD']==1  :
                df_trades.ix[i, 0] = 2000
                holding = 1000
    print(df_trades.head(20))
    return df_trades


def plot_indicators(df, *args):
    """Accepts a df and indicator df's, returns a plot of the df with indicators"""
    fig = plt.figure(figsize=(10, 5), dpi=120)
    plt.plot(df, color='k', label='JPM')
    plt.rcParams.update({'font.size': 16})
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Share Price', fontsize=18)
    plt.xticks(rotation=45)
    fig.suptitle('Bollinger Bands')

    if len(args) > 0:
        for i in args:
            plt.plot(i)  # , label=i.name)

    fig.legend(loc=4, bbox_to_anchor=(0.85, 0.25))
    plt.show()


def plot_oscillator(df1, df2, title):
    """Function that accepts two df's and a plot title, returns a plot of the oscillators"""
    fig = plt.figure(figsize=(10, 5), dpi=120)
    plt.plot(df1, color='y', label=df1.name)
    plt.plot(df2, color='b', label=df2.name)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Arbitrary Price Percentage', fontsize=18)
    plt.xticks(rotation=45)
    fig.suptitle(title, fontsize=24)

    fig.legend(loc=4, bbox_to_anchor=(0.85, 0.25))
    plt.show()




def print_stats(df):
    """Accepts a df of portfolio values and returns basic metrics of the portfolio, sharpe ratio, cumulative returns, 
    volatility, average daily return, and final portfolio value"""
    port_value = df
    d_returns = port_value.copy()
    d_returns = (port_value[1:] / port_value.shift(1) - 1)
    d_returns.iloc[0] = 0
    d_returns = d_returns[1:]

    # Below are desired output values   
    # Cumulative return (final - initial) - 1
    cr = port_value[-1] / port_value[0] - 1
    # Average daily return
    adr = d_returns.mean()
    # Standard deviation of daily return
    sddr = d_returns.std()
    # Sharpe ratio ((Mean - Risk free rate)/Std_dev)
    daily_rfr = (1.0) ** (1 / 252) - 1  # Should this be sampling freq instead of 252?
    sr = (d_returns - daily_rfr).mean() / sddr
    sr_annualized = sr * (252 ** 0.5)

    print("\nDate Range: {} to {}".format(port_value.index[0], port_value.index[-1], end='\n'))
    print("Sharpe Ratio of Fund: {}".format(sr_annualized))
    print("Cumulative Return of Fund: {}".format(cr))
    print("Standard Deviation of Fund: {}".format(sddr))
    print("Average Daily Return of Fund: {}".format(adr))
    print("\nFinal Portfolio Value: {}\n".format(port_value[-1]))


def author():
    return ('wli626')
