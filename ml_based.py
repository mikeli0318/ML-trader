"""MLT: Utility code."""

import pandas as pd
import numpy as np
import datetime as dt
import RTLearner as rt
import BagLearner as bl
from util import get_data, plot_data

def genTrain():
    ybuy=1;
    ysell=-1;
    train_file = "trainX.csv";
    train = pd.read_csv(train_file, index_col=0);
    x=np.array(train.values);
    train_start_date = dt.datetime(2006, 1, 1);
    train_end_date = dt.datetime(2009, 12, 31);
    symbols = ['IBM'];
    price_train_df = get_data(symbols, pd.date_range(train_start_date, train_end_date)).drop('SPY', 1);
    ret=price_train_df.shift(-10).values-price_train_df.values;
    y=1*(ret>ybuy)+(-1)*(ret<ysell);
    y=y[10:-10]
    x=x[10:-10]

    #training
    learner = bl.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": 5}, bags=7, boost=False, verbose=False)
    learner.addEvidence(x, y)
    return learner

def strategy(indicator_file = "trainX.csv",learner = bl.BagLearner):
    data = pd.read_csv(indicator_file, index_col=0);
    x = np.array(data.values);
    predY = learner.query(x)
    res=data.copy().drop('ind3', 1).drop('ind2', 1);
    res['ind1']=predY;
    return res;

def trade(file = "trainX.csv",learner = bl.BagLearner,draw=True):
    suggest=strategy(indicator_file = file,learner=learner);
    start=suggest.index[0]
    end=suggest.index[-1]
    suggest.reset_index(level=0, inplace=True)
    suggest.reset_index(level=0, inplace=True)
    suggest.columns=['no','Date','Order'];
    maxnum=suggest['no'].size
    #print suggest
    list=[];
    i=0;
    while i<maxnum:
        if suggest['Order'].iloc[i]!=0:
            list.append(i);
            i=i+9;
        i=i+1;
        pass;
    order=suggest.iloc[list]
    exit=order.copy();
    list=exit['no'].values+10;
    list=list[np.where(list<maxnum)]
    all=pd.read_csv(file, index_col=0).copy();
    out=all.iloc[list]
    out.reset_index(level=0, inplace=True)
    out['ind1']=(-1)*order['Order'].iloc[out.index].values
    order=order.set_index(['Date']);
    order=order.drop('no', 1)
    out.columns=['Date','Order','a','aa'];
    out=out.set_index(['Date']);
    out=out.drop('a', 1).drop('aa', 1);
    res1 = order.copy();
    res2 = out.copy();
    result=order.append(out);
    result['Symbol']=result['Order'].values;
    result['Shares'] = result['Order'].values;
    result['Symbol']='IBM';
    result['Shares'] =500;
    #result['Order']=100*(result['Order']!=1).values+200*(result['Order']==1).values
    result=result.replace([-1,1],['SELL','BUY']);
    result=result[['Symbol','Order','Shares']];
    with open("ML_order_"+file, 'w') as f:
        result.to_csv(f, header=True, index=True)
    return res1,res2;

def TwoTrade():
    learn = genTrain();
    [res1,res2]=trade(file="trainX.csv", learner=learn);
    [res1,res2]=trade(file="testX.csv", learner=learn);

if __name__=="__main__":
    pass;
