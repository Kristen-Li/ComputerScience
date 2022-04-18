import pandas as pd
import numpy as np
import  os
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data


def author():
    return "wli626"


def getCol(symbols, start_date, end_date, colname,normed=True):
    col = get_data([symbols], pd.date_range(start_date, end_date), colname)
    if 'SPY' not in symbols:
        col.drop(columns='SPY', inplace=True)

    col = col.fillna(method='ffill')
    col = col.fillna(method='bfill')
    if normed:
        col = col / col.iloc[0]
    return col

# Simple Moving Average

def ind_sma(prices, window):
    sma = prices.rolling(window=window).mean()
    sma_over_price = sma/prices
    sma_60= prices.rolling(window=30).mean()
    return sma, sma_over_price, sma_60


def simple_ma(prices, window=5, bollinger=False, threshold=2):
    """Takes a dataframe and returns a df with simple moving average values for the given window
    Optionally adds Bollinger Bands as a tuple (mean, upper-band, lower-band)
    """
    mean = prices.rolling(window, center=False).mean()

    if bollinger:
        std = prices.rolling(window, center=False).std()
        upper = mean + threshold * std
        upper.rename(columns={mean.columns[0]: 'upper_band'}, inplace=True)

        lower = mean - threshold * std
        lower.rename(columns={mean.columns[0]: 'lower_band'}, inplace=True)

        mean.rename(columns={mean.columns[0]: 'mean'}, inplace=True)
        return ((mean, upper, lower))

    mean.rename(columns={mean.columns[0]: 'mean'}, inplace=True)
    return (mean)

# On Balance Volume
def ind_OBV(prices,volumes, window):
    OBV = volumes.copy()
    OBV[:]=0
    # boolean variable: if price has increased
    price_changes = (prices[1:] > prices[:-1].values).replace({True:1, False: -1})
    OBV[1:] = volumes[1:]*price_changes
    OBV=OBV.cumsum()

    # the ema of OBV for trading signal
    OBV_ema = OBV.rolling(window=20).mean()

    return OBV, OBV_ema

# Bolllinger Bands %

def ind_bbp(prices, window):
    mean_rolling = prices.rolling(window= window).mean()
    std_rolling = prices.rolling(window=window).std()
    ub = mean_rolling + 2*std_rolling
    lb = mean_rolling - 2*std_rolling
    bbp = (prices-lb) / (ub-lb)
    return bbp, ub, lb

# Volatility

def ind_volatility(prices, window):
    daily_rets= prices.copy()
    daily_rets = (prices[1:]/prices[:-1].values) -1
    daily_rets=daily_rets[1:]
    volatility = daily_rets.rolling(window).std()
    return volatility

# MACD
def exp_ma(df, days=12):
    """Takes a df and number of days and returns an exponential moving average"""
    ema = df.ewm(com=((days-1)/2)).mean()
    ema.rename(columns={ema.columns[0] : 'exp_ma'}, inplace=True)
    return(ema)

def ind_MACD(df, ema1_days=10, ema2_days=20, macd_signal_days=9):
    """Accepts a df, returns a df with MACD - MACD_singal, where MACD is (ema1-ema2) and MACD_signal is the EMA of MACD"""
    ema1 = exp_ma(df, ema1_days)
    ema2 = exp_ma(df, ema2_days)

    macd = ema1 - ema2
    macd_signal = exp_ma(macd, macd_signal_days)

    macd_signal.rename(columns={macd.columns[0]: 'macd_signal'}, inplace=True)
    macd.rename(columns={macd.columns[0]: 'macd'}, inplace=True)
    return (macd, macd_signal)


# momentum


def ind_momentum(prices, window):
    return prices/prices.shift(window) -1


def charts(symbol = ['JPM'], sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):
    window = 10
    prices = getCol(symbol, sd, ed, 'Adj Price',normed=True)
    volumes = getCol(symbol, sd, ed,'Volume',normed=False)

    #  prices

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set(xlabel="Date", ylabel="Price (Normalized)", title="Price (Normalized)")
    ax.plot(prices, "green", label="Price (Normalized)")
    ax.legend()
    fig.savefig('price.png')
    plt.close()

    #  OBV
    OBV, OBV_ema = ind_OBV(prices, volumes, window)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set(xlabel="Date", ylabel="Price (Normalized)", title="On Balanced Volume")
    ax.plot(OBV, "blue", label=f"OBV")
    ax.plot(OBV_ema, "purple", label=f"OBV  Exponential Moving Average 60 Days")
    # ax.plot(prices, "green", label="Price (Normalized)")
    ax.legend()
    fig.savefig('OBV.png')
    plt.close()

    # SMA and SMA - 60
    sma, sma_over_price, sma_60=ind_sma(prices, window)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set(xlabel="Date", ylabel="Price (Normalized)", title="Simple Moving Average")
    ax.plot(sma, "blue", label=f"SMA {window} days")
    ax.plot(sma_60, "purple", label="SMA 60 days")
    ax.plot(prices, "green", label="Price Normalized")
    ax.legend()
    fig.savefig('sma.png')
    plt.close()

    # Bollinger Bands
    bbp, up, lb=ind_bbp(prices, window)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set(xlabel="Date", ylabel="Price (Normalized)", title="Bollinger Bands")
    ax.plot(up, "blue", label=f"Bollinger Upper Band")
    ax.plot(lb, "purple", label=f"Bollinger Lower Band")
    ax.plot(prices,"green", label="Price (Normalized)")
    ax.legend()
    fig.savefig('bb.png')
    plt.close()


    #  Momentum
    momentum = ind_momentum(prices, window)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set(xlabel="Date", ylabel="Price (Normalized)", title="Momentum")
    ax.plot(momentum, "purple", label=f"Momentum")
    ax.plot(prices, "green", label="Price (Normalized)")
    ax.legend()
    fig.savefig('momentum.png')
    plt.close()

    # Bollinger Bands %
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set(xlabel="Date", ylabel="Price (Normalized)", title="Bollinger Bands Percentage")
    ax.plot(bbp, "purple", label=f"Bollinger Bands Percentage")
    ax.plot(prices, "green", label="Price (Normalized)")
    ax.legend()
    fig.savefig('bbp.png')
    plt.close()


    # Volatility

    volatility = ind_volatility(prices, window)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set(xlabel="Date", ylabel="Price (Normalized)", title="Volatility")
    ax.plot(volatility, "purple", label=f"Volatility")
    ax.plot(prices, "green", label="Price (Normalized)")
    ax.legend()
    fig.savefig('volatility.png')
    plt.close()
