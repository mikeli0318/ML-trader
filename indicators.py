"""
Test a Strategy Learner.  (c) 2016 Tucker Balch
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
import matplotlib as plt

def get_indicators(draw=True):
    train_start_date = dt.datetime(2006, 1, 1);
    train_end_date = dt.datetime(2009, 12, 31);
    test_start_date = dt.datetime(2010, 1, 1);
    test_end_date = dt.datetime(2010, 12, 31);
    symbols=['IBM'];
    price_train_df = get_data(symbols, pd.date_range(train_start_date, train_end_date)).drop('SPY', 1);
    price_test_df = get_data(symbols, pd.date_range(test_start_date, test_end_date)).drop('SPY', 1);
    #price_train_df=price_train_df/price_train_df.iloc[0];
    #price_test_df=price_test_df/price_test_df.iloc[0];
    #print price_train
    #print price_test
    #t=price_test.values

    #gen train
    ind1=price_train_df/price_train_df.shift(10)-1;
    sma = pd.rolling_mean(price_train_df, 10);
    std= pd.rolling_std(price_train_df, 10);
    ind2=(price_train_df-sma)/(2*std);
    dif=price_train_df-price_train_df.shift(1);
    dif.iloc[0]=0;
    up=dif*(dif>0);
    down=dif*(dif<0);
    smaup=pd.rolling_mean(up, 9);
    smadown=pd.rolling_mean(down, 9);
    ind3=smaup/(smaup-smadown);
    indicators=pd.concat([ind1,ind2,ind3], axis=1);
    indicators.columns = ['ind1', 'ind2', 'ind3'];
    with open('trainX.csv', 'w') as f:
        indicators.to_csv(f, header=True, index=True)

    #plot 1
    col1=price_train_df/price_train_df.iloc[0];
    col1.columns=['price'];
    col2=ind1.copy();
    col2.columns=['indicator (window=10)'];
    df1 = pd.concat([col1, col2], axis=1)
    df1.colums = ['price', 'indicator (window=10)']
    plot1 = df1.plot(grid=True, title="Indicator 1", fontsize=12)
    plot1.set_xlabel("Date")
    plot1.set_ylabel("Values")
    fig = plot1.get_figure()
    fig.savefig("indicator_1.png")

    #plot 2
    col1 = price_train_df / price_train_df.iloc[0];
    col2 = pd.rolling_mean(col1, 10);
    col3 = pd.rolling_std(col1, 10);
    col4 =(col1-col2)/(2*col3);
    col1.columns = ['price'];
    col2.columns = ['SMA'];
    col3.columns = ['Stdev'];
    col4.columns = ['indicator (window=10)'];
    df1 = pd.concat([col1, col2,col3,col4], axis=1)
    df1.colums = ['price', 'SMA','Stdev','indicator (window=10)']
    plot1 = df1.plot(grid=True, title="Indicator 2", fontsize=12)
    plot1.set_xlabel("Date")
    plot1.set_ylabel("Values")
    fig = plot1.get_figure()
    fig.savefig("indicator_2.png")

    #plot 3
    col1 = price_train_df / price_train_df.iloc[0];
    col2 = smaup.copy();
    col3 = (-1)*smadown.copy();
    col4 = ind3.copy();
    col1.columns = ['price'];
    col2.columns = ['SMA of price rise'];
    col3.columns = ['SMA of price down'];
    col4.columns = ['indicator'];
    df1 = pd.concat([col1, col2, col3, col4], axis=1)
    df1.colums = ['price', 'SMA of price rise', 'SMA of price down', 'indicator']
    plot1 = df1.plot(grid=True, title="Indicator 3", fontsize=12)
    plot1.set_xlabel("Date")
    plot1.set_ylabel("Values")
    fig = plot1.get_figure()
    fig.savefig("indicator_3.png")

    #gen test
    ind1=price_test_df/price_test_df.shift(10)-1;
    sma = pd.rolling_mean(price_test_df, 10);
    std= pd.rolling_std(price_test_df, 10);
    ind2=(price_test_df-sma)/(2*std);
    dif=price_test_df-price_test_df.shift(1);
    dif.iloc[0]=0;
    up=dif*(dif>0);
    down=dif*(dif<0);
    smaup=pd.rolling_mean(up, 9);
    smadown=pd.rolling_mean(down, 9);
    ind3=smaup/(smaup-smadown);
    indicators=pd.concat([ind1,ind2,ind3], axis=1);
    indicators.columns = ['ind1', 'ind2', 'ind3'];
    with open('testX.csv', 'w') as f:
        indicators.to_csv(f, header=True, index=True)
    pass;

if __name__=="__main__":
    get_indicators(draw=True);
