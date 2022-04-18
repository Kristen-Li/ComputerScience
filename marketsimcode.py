import numpy as np

from util import get_data, plot_data


def compute_portvals(orders_file, start_val=100000, commission=9.95, impact=0.005):
    """This will compute the portfolio values in each periods"
    if len(orders_file.any(1).nonzero()[0]) == 0:
        return (pd.DataFrame(data=100000, index=orders_file.index, columns=[orders_file.columns[0]]))

    dates = orders_file.index
    symbol = orders_file.columns[0]

    input_prices = get_data([symbol], pd.date_range(dates[0], dates[-1]))     # use Adj close for input_prices

    # remove SPY if the symbol doesn’t contain it
    if symbol != 'SPY':
        input_prices = input_prices.drop('SPY', axis=1)
    
    df_prices = pd.DataFrame(input_prices) # add cash 
    df_prices['cash'] = 1

    # df_trades saves the holdings of stock and cash on the trading days
    df_trades = orders_file.copy()

    
    df_holdings = df_trades.copy()

    for i in orders_file.index:
        if orders_file.ix[i, symbol] != 0:  
            total_cost = orders_file.loc[i, symbol] * df_prices.loc[i, symbol]  
            df_trades.loc[i, 'cash'] = -total_cost - abs(commission + total_cost * impact) # transaction cost and impact
    df_trades.fillna(0, inplace=True) #if no trade, then use 0

    df_holdings.loc[dates[0], 'cash'] = start_val + df_trades.loc[dates[0], 'cash']
    df_holdings.iloc[0, :-1] = df_trades.iloc[0, :-1]

    for i in range(1, df_holdings.shape[0]):
        df_holdings.iloc[i, :] = df_trades.iloc[i, :] + df_holdings.iloc[i - 1, :]

    # df_values 
    df_values = df_holdings.multiply(df_prices)

    df_portval = df_values.sum(axis=1)
    return (df_portval)


def get_portfolio_stats(port_val, rfr=0, sf=252):
    # this will generate necessary stats to use. 
    daily_rets = (port_val / port_val.shift(1)) - 1
    daily_rets = daily_rets[1:]    
    cr = (port_val[-1] / port_val[0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = np.sqrt(sf) * np.mean(adr - rfr) / sddr
    return cr, adr, sddr, sr

def author():
    return 'wli626'

