"""experiment1

"""
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import StrategyLearner as sl
import ManualStrategy as ms
import marketsimcode



"""
This file will generate a graph of normalized portfolio values for manual, strategy learner and baseline model. The portfolio statistics will also be generated."""
def author():
    return'wli626'
    
if __name__ == "__main__":
    print(' Start Experiment 1 wli626')
    sym = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)

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
    
    fig = plt.figure(figsize=(12,6), dpi=80)
    df_trades_ms = ms.testPolicy(symbol=sym, sd=sd, ed=ed, sv = 100000)
    for index, marks in df_trades_ms.iterrows():
        if marks[0] > 0:
            plt.axvline(x=index, color='blue', linestyle='dashed', alpha=.9)
        elif marks[0] < 0:
            plt.axvline(x=index, color='black', linestyle='dashed', alpha=.9)
        else:
            pass
    plt.plot(values, color='b', label='Strategy')
    plt.plot(values_bench, color='purple', linestyle=':', linewidth=2.1, label='Benchmark')
    plt.plot(values_manual, color='red', label='Manual')
    plt.xlabel('Dates', fontsize=13)
    plt.ylabel('Portfolio value', fontsize=13)
    
    fig.suptitle('In Sample Comparison: Manual vs Strategy vs Benchmark', fontsize=17)
    fig.legend(loc=3, bbox_to_anchor=(0.08, 0.7))
    plt.show()

    plt.savefig('exp1.png')

    plt.close()

    port_cr_sl, port_adr_sl, port_stddr_sl, port_sr_sl =marketsimcode.get_portfolio_stats(values)
    port_cr_ms, port_adr_ms, port_stddr_ms, port_sr_ms = marketsimcode.get_portfolio_stats(values_manual)
    bench_cr, bench_adr, bench_stddr, bench_sr = marketsimcode.get_portfolio_stats(values_bench)

    # Compare portfolio against benchmark
    print("=== Machine Learning Strategy  V.S. Manual Strategy  In Sample ===")
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
    
#     Out of sample comparisons
    sd2 = dt.datetime(2010,1,1)
    ed2 = dt.datetime(2011,12,31)
    learner.addEvidence(sym, sd2, ed2, 100000)
    
    strategy = learner.testPolicy(sym, sd2, ed2)
    manual = ms.testPolicy(sym, sd2, ed2)
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
    
    fig = plt.figure(figsize=(12,6), dpi=80)
    df_trades_ms = ms.testPolicy(symbol=sym, sd=sd2, ed=ed2, sv = 100000)
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
    plt.xlabel('Dates', fontsize=13)
    plt.ylabel('Portfolio value', fontsize=13)
    
    fig.suptitle('Out-of Sample Comparison: Manual vs Strategy vs Benchmark', fontsize=17)
    fig.legend(loc=3, bbox_to_anchor=(0.08, 0.7))
    plt.show()


    plt.savefig('exp1out.png')

    plt.close()

    port_cr_sl, port_adr_sl, port_stddr_sl, port_sr_sl =marketsimcode.get_portfolio_stats(values)
    port_cr_ms, port_adr_ms, port_stddr_ms, port_sr_ms = marketsimcode.get_portfolio_stats(values_manual)
    bench_cr, bench_adr, bench_stddr, bench_sr = marketsimcode.get_portfolio_stats(values_bench)

    # Compare portfolio against benchmark
    print("=== Machine Learning Strategy (MLS) V.S. Manual Strategy (MS) Out-of Sample ===")
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
