"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "Order_for_trainX.csv", start_val = 100000):
    # this is the function the autograder will call to test your code
    # TODO: Your code here
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan']).sort_index(axis=0).drop(['2011-06-15'],axis=0,errors='ignore');
    symbols=list(orders_df["Symbol"].drop_duplicates());
    start_date = orders_df.index[0];
    end_date = orders_df.index[-1];
    price = get_data(symbols, pd.date_range(start_date, end_date));
    price=price.drop(['SPY'],axis=1);
    holdings=price.copy();
    holdings.ix[:,:]=0;
    holdings['CASH']=pd.Series(np.zeros(holdings.shape[0]),index=holdings.index);
    holdings['CASH']=np.nan;
    temphold=holdings.ix[0].copy();
    temphold['CASH']=start_val;
    templasthold=temphold.copy();#will not be used in the following loop
    for i in range(0,orders_df.shape[0]):
        todayprice = price.ix[orders_df.index[i], :];
        prevhold=temphold.copy();
        previnvest=temphold.drop(['CASH'])*todayprice;
        prevleverage=sum(abs(previnvest))/(sum(previnvest)+temphold['CASH']);
        #print orders_df.ix[i,'Symbol'];
        #print orders_df.ix[i,'Shares'];
        #print orders_df.ix[i,'Order'];
        #print orders_df.index[i];
        if orders_df.ix[i,'Order']=='SELL':
            temphold[orders_df.ix[i,'Symbol']]-=orders_df.ix[i,'Shares'];
            temphold['CASH']+=orders_df.ix[i,'Shares']*todayprice[orders_df.ix[i,'Symbol']];
        else:
            temphold[orders_df.ix[i, 'Symbol']] +=orders_df.ix[i, 'Shares'];
            temphold['CASH'] -=orders_df.ix[i,'Shares']*todayprice[orders_df.ix[i,'Symbol']];
        #now calculate leverage
        invest = temphold.drop(['CASH'])*todayprice;
        leverage=sum(abs(invest))/(sum(invest)+temphold['CASH']);
        if(leverage<=3.0 or leverage<prevleverage):
            holdings.ix[orders_df.index[i]]=temphold.copy();
            #print holdings.ix[orders_df.index[i]];
        else:
            temphold=prevhold.copy();
    #end for
    for index, row in holdings.iterrows():
        if row.isnull()[-1]:
            row[:]=templasthold[:].copy();
        #print row.isnull()[-1];
        else:
            templasthold[:]=row[:].copy();
    price['CASH'] = pd.Series(np.ones(price.shape[0]), index=price.index);
    values= holdings*price;
    portvals=pd.DataFrame(values.sum(axis=1),columns=['portvalue']);
    return portvals

def test_code(of = "Order_for_trainX.csv"):
    sv = 100000
    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
#    if isinstance(portvals, pd.DataFrame):
#        portvals = portvals[portvals.columns[0]] # just get the first column
#    else:
#        "warning, code did not return a DataFrame"
    start_date=portvals.index[0];
    end_date = portvals.index[-1];
    SPYvalues = get_data([], pd.date_range(start_date, end_date));
    [cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY, daily_port_SPY]=compute_portfolio(prices = SPYvalues, \
    allocs=[1],\
    sv=sv, rfr=0.0, sf=252.0);
    [cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio, daily_port] = compute_portfolio(
        prices=portvals, \
        allocs=[1], \
        sv=sv, rfr=0.0, sf=252.0);
    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    #print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    #print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    #print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    #print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals.ix[-1,0])
    return cum_ret

def compute_portfolio(prices = pd.DataFrame, \
    allocs=[0.1,0.2,0.3,0.4],\
    sv=1000000, rfr=0.0, sf=252.0):
    #this function is REALLY GREAT
    #prices: DataFrame/ndarray, it should be already selected via symbols (like ['GOOG''AAPL'], etc)
    #allocs: allocation for each company
    #sv: start value, the amount of $ you put for your portfolio at first
    #rfr: risk free return
    #sf: sampling frequency
    prices=prices/prices.ix[0] # normalize by the 1st day
    prices=sv*prices*allocs # multiple by allocation and start value
    daily_port=prices.sum(axis=1) # daily protfolio
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    daily_return=daily_port.copy()
    daily_return=(daily_port/daily_port.shift(1))-1
    daily_return=daily_return[1:]
    cr=(daily_port[-1]/daily_port[0])-1
    adr=daily_return.mean()
    sddr=daily_return.std()
    aux_sr=daily_return-rfr # auxiliary dataframe, whose mean value will be used for sharp ratio
    sr=np.sqrt(252)*aux_sr.mean()/sddr
    #here's output
    #cr: cumulative return
    #adr: average daily return
    #sddr: standard deviation of daily return
    #sr: sharpe ratio
    #daily_port: the worth of your portfolio everyday, so your final worth of portfolio should be daily_port[-1]
    return cr, adr, sddr, sr, daily_port#I return daily_report because we dont need to compute again if plot is needed

if __name__ == "__main__":
    test_code(of="ML_order_trainX.csv")
    #test_code(of="benchmark_trainX.csv")
