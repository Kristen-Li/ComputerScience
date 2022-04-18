"""Strategy Learner
Python 3.6
CS7646 Project 8 - Strategy Learner
Mike Tong (mtong31)

This program returns a trades dataframe based on a random forest classifier
"""

import pandas as pd
import datetime as dt
import numpy as np
import RTLearner as rt
import BagLearner as bl
import indicators as ind
import util 

# below is for local file operation
import os
os.chdir('/home/shinee/GitRepos/ml4tsp22/strategy_evaluation/')
#####

class StrategyLearner(object):
    def __init__(self, verbose=False, impact=0.0):
        self.verbose = verbose # aids in debugging
        self.impact = impact
        self.learner = None
        self.indicator_window = 10 # adjusts window size for rolling indicators
    
    def author(self):
        return('wli626')

    def getCol(self,symbols, start_date, end_date, colname, normed=True):
        col = util.get_data([symbols], pd.date_range(start_date, end_date), colname)
        if 'SPY' not in symbols:
            col.drop(columns='SPY', inplace=True)

        col = col.fillna(method='ffill')
        col = col.fillna(method='bfill')
        if normed:
            col = col / col.iloc[0]

        return col

    # if specific conditions for the learner want to be modified, use the function below prior to training
    def get_tree(self, learner=rt.RTLearner, leaf_size=6, bags=18): # 6 , 20
        """Initalizes the learner parameters, does not return anything, but primes the learner for training"""
        self.learner = bl.BagLearner(learner, kwargs={'leaf_size' : leaf_size}, bags=bags, boost=False)
        
    def signage(self, value):
        """Accepts a value, returns the normalized value as -1 or 1"""
        return(value/abs(value))


        
    def feature_balance(self, trees):
        """Function to check the overall balance of the formed trees by counting the number of features used for split values"""
        num_columns = len(self.xTrain.columns)
        feature_count = dict(enumerate([0]*num_columns))
        
        for tree in trees:
            for branch in tree:
                if branch[0] > -1:
                    feature_count[branch[0]] += 1
                    
        for i in range(num_columns):
            feature_count[self.xTrain.columns[i]] = feature_count.pop(i)
        return(feature_count)
    
    def df_yTrain(self, symbol, sd, ed):
        """Creates buy/hold/sell signals based on price history. Impact affects trading thresholds. Returns a trades dataframe"""
        df_prices = self.getCol(symbol, sd, ed, 'Adj Price', normed=True)

        df_trades = pd.DataFrame(data=0, index=df_prices.index, columns={symbol})
        df_prices['diff'] = df_prices.diff(-1)

        prev_pos = df_prices.iloc[0,-1]
        df_trades[symbol] = prev_pos
        
        for i,j in df_prices[1:].iterrows():
            if j['diff'] == prev_pos:
                df_trades.loc[i] = 0
            elif j['diff'] < 0 and j['diff'] > -self.impact*df_prices.loc[i,symbol]:
                df_trades.loc[i] = 0
            elif j['diff'] > 0 and j['diff'] < self.impact*df_prices.loc[i,symbol]:
                df_trades.loc[i] = 0
            else:
                prev_pos = j['diff']
                df_trades.loc[i] = prev_pos * -1
        
        df_trades = self.signage(df_trades.iloc[:,0])
        df_trades.fillna(0, inplace=True)
        df_trades[-1] = 0 # last day cannot see into the future
        
        if self.verbose:
            print(pd.concat([df_prices, df_trades],axis=1))
            
        return(df_trades)
        
    # indicator_values is used to generate the input data for the model
    def indicator_values(self, df_prices, df_volumes):
        """Function is used to generate X inputs based on indicator performance
        Accepts a prices df from util.get_data, returns a df of indicator performance"""
        window = 20

        sma, sma_over_price, sma60 = ind.ind_sma(df_prices,window)
        OBV, OBV_ema = ind.ind_OBV(df_prices, df_volumes,window)
        bbp, ub, lb = ind.ind_bbp(df_prices, window)
        MMT = ind.ind_momentum(df_prices, window=5)

        macd, macd_s = ind.ind_MACD(df_prices, ema1_days=12, ema2_days=24, macd_signal_days=9)

        md = (macd['macd'] - macd_s['macd_signal']).rename('m-d')
        md = md.to_frame()
        md_diff = (md.shift(1) / md) / abs(md.shift(1) / md)  # checks if MACD crosses its signal (-1 if it does)

        sma2, upper, lower = ind.simple_ma(df_prices, window=19, bollinger=True, threshold=1.45)

        df_ind = pd.concat([sma_over_price,sma60,  OBV, OBV_ema,bbp, MMT,sma2], axis=1)
        df_ind.set_axis(['sma_over_price', 'sma60', 'OBV', 'OBV_ema', 'bbp', 'MMT','sma2'], axis=1, inplace=True)

        self.window = df_ind.isnull().any(1).nonzero()[
                          0].max() + 1  # highest index is mainteined to prevent training during this period
        if self.verbose:
            self.ind = df_ind

        return (df_ind.iloc[self.window:, :])

    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 
        "Accepts a symbol, start date (sd), end date(ed) and start value (sv), creates an optimized decision tree"""
        df_prices = self.getCol(symbol, sd, ed, 'Adj Price')
        df_volumes = self.getCol(symbol, sd, ed, 'Volume')

        xTrain = self.indicator_values(df_prices, df_volumes)
        self.yTrain = self.df_yTrain(symbol, sd, ed)[self.window:]
        
        if len(self.yTrain.nonzero()[0]) != 0:
            if self.learner == None:
                self.get_tree()
            self.learner.add_evidence(xTrain.values, self.yTrain.values.astype('int8'))
        else:
            if self.verbose: print('Impact is probably too high')

        self.xTrain = xTrain
        
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        """Creates a trading dataframe based on queried indicator values for the out of sample data using a random forest"""
        df_prices = self.getCol(symbol, sd, ed, 'Adj Price')
        df_volumes = self.getCol(symbol, sd, ed, 'Volume')
        
        if len(self.yTrain.nonzero()[0]) == 0:
            return(pd.DataFrame(data=0, index=df_prices.index,columns=[symbol]))
            
        xTest = self.indicator_values(df_prices, df_volumes)
        
        query = self.learner.query(xTest.values)
        
        query[query <= -0.5] = -2000
        query[query >= 0.5] = 2000
        query[abs(query) != 2000] = 0       
        
        query = np.insert(query, 0, np.zeros(self.window)) # replaces rolling window values with zero to prevent querying
        
        if len(query.nonzero()[0]) == 0:
            if self.verbose: print('Impact is definitely too high')
            return(pd.DataFrame(data=0, index=df_prices.index,columns=[symbol]))

        first_trade = query.nonzero()[0][0]
        if first_trade > 0:
            query[first_trade] = 1000
        else:
            query[first_trade] = -1000

        current_pos = self.signage(query[first_trade])
        
        for pos in range(first_trade+1, len(query)):
            if query[pos] == 0:
                continue
            elif self.signage(query[pos]) == current_pos:
                query[pos] = 0
            else:
                query[pos] = self.signage(query[pos]) * 2000
                current_pos = self.signage(query[pos])

        df_trades = pd.DataFrame(index=df_prices.index)
        df_trades[symbol] = query
        
        if self.verbose:
            self.query=query
            self.xTest = xTest

        return(df_trades)
    
