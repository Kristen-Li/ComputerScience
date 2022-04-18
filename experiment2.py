"""
 experiment2
 this code will experiment of different impact and see the effect on trading behavior for the in-sample data
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import marketsimcode
import StrategyLearner as sl

def author():
    return 'wli626'
    
if __name__ == "__main__":  
    sym = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000
    
    learner  = sl.StrategyLearner(verbose=False, impact=0.0005)
    learner2 = sl.StrategyLearner(verbose=False, impact=0.005)
    learner3 = sl.StrategyLearner(verbose=False, impact=0.05)


    # Training phase
    learner.addEvidence(sym, sd, ed, 100000)
    learner2.addEvidence(sym, sd, ed, 100000)
    learner3.addEvidence(sym, sd, ed, 100000)
   
    
    # Test Phase
    strategy  = learner.testPolicy(sym, sd, ed)
    strategy2 = learner2.testPolicy(sym, sd, ed)
    strategy3 = learner3.testPolicy(sym, sd, ed)
   
    
    # Performance Metrics
    values  = marketsimcode.compute_portvals(strategy)
    values2 = marketsimcode.compute_portvals(strategy2)
    values3 = marketsimcode.compute_portvals(strategy3)


    # Normalize gains to the sv
    values  /= sv
    values2 /= sv
    values3 /= sv

    
    fig = plt.figure(figsize=(12,6), dpi=80)
    plt.plot(values,  label='impact: 0.00')
    plt.plot(values2, label='impact: 0.0005')
    plt.plot(values3, label='impact: 0.005')
   
    
    plt.xlabel('Dates', fontsize=13)
    plt.ylabel('Portfolio value', fontsize=13)
    fig.suptitle('Porfolio Values for different Impact Values', fontsize=17)
    fig.legend(loc=3, bbox_to_anchor=(0.08, 0.6))
    plt.show()
    
    columns = len(learner.xTrain.columns)
    result_df = pd.concat([values, values2, values3, values4, values5],axis=1)
    result_df.rename(columns={0 : 'impact: 0.0005',\
                              1 : 'impact: 0.005',\
                              2 : 'impact: 0.05'
                           }, inplace=True)
    
    print('Performance comparison: ')
    print(result_df)
    port_cr_1, port_adr_1, port_stddr_1, port_sr_1 =marketsimcode.get_portfolio_stats(values)
    port_cr_2, port_adr_2, port_stddr_2, port_sr_2 =marketsimcode.get_portfolio_stats(values2)
    port_cr_3, port_adr_3, port_stddr_3, port_sr_3 =marketsimcode.get_portfolio_stats(values3)
   

    # Compare portfolio against benchmark
    print("=== Strategy  V.S. Manual Strategy  In Sample ===")
    print("Date Range: {} to {}".format(sd, ed))
    print()
    print("Sharpe Ratio of 1: {}".format(port_sr_1))
    print("Sharpe Ratio of 2: {}".format(port_sr_2))
    print("Sharpe Ratio of 3: {}".format(port_sr_3))
    print()
    print("Cumulative Return of 1: {}".format(port_cr_1))
    print("Cumulative Return of 2: {}".format(port_cr_2))
    print("Cumulative Return of 3 : {}".format(port_cr_3))
    print()
    print("Average Daily Return of 1: {}".format(port_adr_1))
    print("Average Daily Return of 2: {}".format(port_adr_2))
    print("Average Daily Return of 3 : {}".format(port_adr_3))
    print()
    print("Standard Deviation of 1: {}".format(port_stddr_1))
    print("Standard Deviation of 2: {}".format(port_stddr_2))
    print("Standard Deviation of 3 : {}".format(port_stddr_3))
    print()
    print("Final Portfolio Value 1: {}".format(values[-1]))
    print("Final  Portfolio Value 2: {}".format(values2[-1]))
    print("Final Portfolio Value 3: {}".format(values3[-1]))
    print()
