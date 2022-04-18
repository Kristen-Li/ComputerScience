"""experiment1
Python 3.6
CS7646 Project 8 - Strategy Learner

"""
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import marketsimcode

import StrategyLearner as sl
import ManualStrategy as ms

"""This code compares the performance of the strategy learner to the project 6 manual strategy, as well as the 
respective benchmark (buy and hold 1000 shares).

The code will print a plot of the normalized gain, as well as a dataframe with the respective values"""
def author():
    return('wli626')
    
if __name__ == "__main__":
    print('Project 8 Experiment1: mtong31')
    sym = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sd2 = dt.datetime(2011,1,1)
    ed2 = dt.datetime(2011,12,31)
    sv = 100000
    learner = sl.StrategyLearner(verbose=False, impact=0.00)
    learner.addEvidence(sym, sd, ed, 100000)
    
    strategy = learner.testPolicy(sym, sd, ed)
    manual = ms.testPolicy(sym, sd, ed)
    benchmark = pd.DataFrame(index=strategy.index)
    benchmark[sym] = 0
    benchmark.iloc[0,0] = 1000    
    
    values = marketsimcode.compute_portvals(strategy)
    values_bench = marketsimcode.compute_portvals(benchmark)

    values_manual = marketsimcode.compute_portvals(manual)
    
    # below normalizes gains to the sv
    values /= sv
    values_bench /= sv
    values_manual /= sv
    
    fig = plt.figure(figsize=(10,5), dpi=80)
    df_trades_ms = ms.testPolicy(symbol=sym, sd=sd, ed=ed, sv = 100000)
    for index, marks in df_trades_ms.iterrows():
        if marks[0] > 0:
            plt.axvline(x=index, color='blue', linestyle='dashed', alpha=.9)
        elif marks[0] < 0:
            plt.axvline(x=index, color='black', linestyle='dashed', alpha=.9)
        else:
            pass
    plt.plot(values, color='b', label='Strategy')
    plt.plot(values_bench, color='purple', linestyle=':', linewidth=2, label='Benchmark')
    plt.plot(values_manual, color='red', label='Manual')
    plt.xlabel('Dates', fontsize=14)
    plt.ylabel('Portfolio value', fontsize=14)
    
    fig.suptitle('In Sample Comparison: Benchmark vs Manual vs Strategy', fontsize=18)
    fig.legend(loc=3, bbox_to_anchor=(0.08, 0.7))
    plt.show()


    
    columns = len(learner.xTrain.columns)
    result_df = pd.concat([values, values_bench, values_manual],axis=1)
    result_df.rename(columns={0 : 'Strategy_Learner', 1 : 'Benchmark', 2 : 'Manual_Strategy'}, inplace=True)
    # print('Performance comparison: ')
    # print(result_df)

    plt.savefig('exp1.png')

    plt.close()

    port_cr_sl, port_adr_sl, port_stddr_sl, port_sr_sl =marketsimcode.get_portfolio_stats(values)
    port_cr_ms, port_adr_ms, port_stddr_ms, port_sr_ms = marketsimcode.get_portfolio_stats(values_manual)
    bench_cr, bench_adr, bench_stddr, bench_sr = marketsimcode.get_portfolio_stats(values_bench)

    # Compare portfolio against benchmark
    print("=== Machine Learning Strategy (MLS) V.S. Manual Strategy (MS) In Sample ===")
    print("Date Range: {} to {}".format(sd, ed))
    print()
    print("Sharpe Ratio of MLS: {}".format(port_sr_sl))
    print("Sharpe Ratio of MS: {}".format(port_sr_ms))
    print("Sharpe Ratio of BenchMark : {}".format(bench_sr))
    print()
    print("Cumulative Return of MLS: {}".format(port_cr_sl))
    print("Cumulative Return of MS: {}".format(port_cr_ms))
    print("Cumulative Return of Benchmark : {}".format(bench_cr))
    print()
    print("Standard Deviation of MLS: {}".format(port_stddr_sl))
    print("Standard Deviation of MS: {}".format(port_stddr_ms))
    print("Standard Deviation of Benchmark : {}".format(bench_stddr))
    print()
    print("Average Daily Return of MLS: {}".format(port_adr_sl))
    print("Average Daily Return of MS: {}".format(port_adr_ms))
    print("Average Daily Return of BenchMark : {}".format(bench_adr))
    print()
    print("Final MLS Portfolio Value: {}".format(values[-1]))
    print("Final MS Portfolio Value: {}".format(values_manual[-1]))
    print("Final Benchmark Portfolio Value: {}".format(values_bench[-1]))
    print()