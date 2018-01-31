import marketsim as mar
import pandas as pd
from util import get_data, plot_data
import numpy as np
import rule_based as rule
import ml_based as ml
import datetime as dt

def compute_portvals(orders_file = "Order_for_trainX.csv", start_val = 100000,start_date=dt.datetime(2001,1,1),end_date=dt.datetime(2001,1,1)):
    # this is the function the autograder will call to test your code
    # TODO: Your code here

    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan']).sort_index(axis=0).drop(['2011-06-15'],axis=0,errors='ignore');

    symbols=list(orders_df["Symbol"].drop_duplicates());

    #start_date = orders_df.index[0];
    #end_date = orders_df.index[-1];
    price = get_data(symbols, pd.date_range(start_date, end_date));
    ###########SPYprice=price['SPY'];

    price=price.drop(['SPY'],axis=1);
    ##################
    #price['CASH']=pd.Series(np.ones(price.shape[0]),index=price.index)
    #################

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




if __name__=="__main__":
    train_start_date = dt.datetime(2006, 1, 1);
    train_end_date = dt.datetime(2009, 12, 31);
    test_start_date = dt.datetime(2010, 1, 1);
    test_end_date = dt.datetime(2010, 12, 31);

    sv = 100000;
    manualIn = compute_portvals(orders_file="order_trainX.csv", start_val=sv,start_date=train_start_date,end_date=train_end_date);
    mlIn = compute_portvals(orders_file="ML_order_trainX.csv", start_val=sv,start_date=train_start_date,end_date=train_end_date);
    benchIn = compute_portvals(orders_file="benchmark_trainX.csv", start_val=sv,start_date=train_start_date,end_date=train_end_date);
    manualOut = compute_portvals(orders_file="order_testX.csv", start_val=sv,start_date=test_start_date,end_date=test_end_date);
    mlOut = compute_portvals(orders_file="ML_order_testX.csv", start_val=sv,start_date=test_start_date,end_date=test_end_date);
    benchOut = compute_portvals(orders_file="benchmark_testX.csv", start_val=sv,start_date=test_start_date,end_date=test_end_date);
    manualIn=manualIn/manualIn.iloc[0];
    mlIn=mlIn/mlIn.iloc[0];
    benchIn=benchIn/benchIn.iloc[0];
    manualOut=manualOut/manualOut.iloc[0];
    mlOut=mlOut/mlOut.iloc[0];
    benchOut=benchOut/benchOut.iloc[0];

    [order1, exit1]=rule.trade(file="trainX.csv");
    learn = ml.genTrain();
    [order2, exit2] = ml.trade(file="trainX.csv", learner=learn);

    #plot 1 in
    col1 = benchIn.copy();
    col2 = manualIn.copy();
    col1.columns = ['benchmark'];
    col2.columns = ['manual'];
    df1 = pd.concat([col1, col2], axis=1)
    df1.colums = ['benchmark', 'manual']
    my_colors = ['black','blue'];
    plot1 = df1.plot(grid=True, title="Part 2", fontsize=12, color=my_colors)
    plot1.set_xlabel("Date")
    plot1.set_ylabel("Values")
    for date in order1.index.values:
        if order1.ix[date][0] == 1:
            plot1.axvline(x=date, color='green', linestyle='-')
        else:
            plot1.axvline(x=date, color='red', linestyle='-')
    for date in exit1.index.values:
        plot1.axvline(x=date, color='black', linestyle='--')
    fig = plot1.get_figure()
    fig.savefig("part_2.png")

    #plot 2 in
    col1 = benchIn.copy();
    col2 = manualIn.copy();
    col3=mlIn.copy();
    col1.columns = ['benchmark'];
    col2.columns = ['manual'];
    col3.columns = ['machine learning'];
    df1 = pd.concat([col1, col2, col3], axis=1)
    df1.colums = ['benchmark', 'manual', 'machine learning']
    my_colors = ['black', 'blue', 'green'];
    plot1 = df1.plot(grid=True, title="Part 3", fontsize=12, color=my_colors)
    plot1.set_xlabel("Date")
    plot1.set_ylabel("Values")
    for date in order2.index.values:
        if order2.ix[date][0] == 1:
            plot1.axvline(x=date, color='green', linestyle='-')
        else:
            plot1.axvline(x=date, color='red', linestyle='-')
    for date in exit2.index.values:
        plot1.axvline(x=date, color='black', linestyle='--')
    fig = plot1.get_figure()
    fig.savefig("part_3.png")

    #plot 3 out
    col1 = benchOut.copy();
    col2 = manualOut.copy();
    col3=mlOut.copy();
    col1.columns = ['benchmark'];
    col2.columns = ['manual'];
    col3.columns = ['machine learning'];
    df1 = pd.concat([col1, col2, col3], axis=1)
    df1.colums = ['benchmark', 'manual', 'machine learning']
    my_colors = ['black', 'blue', 'green'];
    plot1 = df1.plot(grid=True, title="Part 4", fontsize=12, color=my_colors)
    plot1.set_xlabel("Date")
    plot1.set_ylabel("Values")
    fig = plot1.get_figure()
    fig.savefig("part_4.png")


