"""MLT: Utility code."""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data

#rule-based trading strategy
def strategy(indicator_file = "trainX.csv",verbose=False):
    #t1~t6: threshold
    t1=0.7;
    t2=0.1;
    t3=0.725;
    t4=-0.725;
    t5=0.016;
    t6=-0.02;
    x=pd.read_csv(indicator_file,index_col=0);

    rsibuy=1*(x['ind3']<t2);
    rsisell=(-1)*(x['ind3']>t1);
    norsi=(x['ind3']<=t1)*(x['ind3']>=t2);

    bbbuy=1*(x['ind2']<t4);
    bbsell=(-1)*(x['ind2']>t3);
    nobb=(x['ind2']>=t4)*(x['ind2']<=t3);

    mombuy=(-1)*(x['ind1']>t5);
    momsell=(1)*(x['ind1']<t6);
    suggest=rsibuy+rsisell+norsi*(bbbuy+bbsell)+norsi*nobb*(mombuy+momsell)

    suggest.iloc[0] = 1;

    if verbose==True:
        with open('a.csv', 'w') as f:
            suggest.to_csv(f, header=True, index=True)

    return suggest


def trade(file = "trainX.csv",verbose=True,draw=True):
    suggest=strategy(indicator_file = file,verbose=True).to_frame();
    start = suggest.index[0]
    end = suggest.index[-1]
    suggest.reset_index(level=0, inplace=True)
    suggest.reset_index(level=0, inplace=True)
    suggest.columns = ['no', 'Date', 'Order'];
    maxnum = suggest['no'].size
    # print suggest
    list = [];
    i = 0;
    while i < maxnum:
        if suggest['Order'].iloc[i] != 0:
            list.append(i);
            i = i + 9;
        i = i + 1;
        pass;
    order = suggest.iloc[list]
    exit = order.copy();
    list = exit['no'].values + 10;
    list = list[np.where(list < maxnum)]
    all = pd.read_csv(file, index_col=0).copy();
    out = all.iloc[list]
    out.reset_index(level=0, inplace=True)
    out['ind1'] = (-1) * order['Order'].iloc[out.index].values
    order = order.set_index(['Date']);
    order = order.drop('no', 1)
    out.columns = ['Date', 'Order', 'a', 'aa'];
    out = out.set_index(['Date']);
    out = out.drop('a', 1).drop('aa', 1);
    res1=order.copy();
    res2=out.copy();
    result = order.append(out);
    result['Symbol'] = result['Order'].values;
    result['Shares'] = result['Order'].values;
    result['Symbol'] = 'IBM';
    result['Shares'] = 500;
    # result['Order']=100*(result['Order']!=1).values+200*(result['Order']==1).values
    result = result.replace([-1, 1], ['SELL', 'BUY']);
    result = result[['Symbol', 'Order', 'Shares']];

    with open("order_" + file, 'w') as f:
        result.to_csv(f, header=True, index=True)
    benchmark=result.iloc[0:2];
    benchmark.reset_index(level=0, inplace=True)
    benchmark['Date']=[start,end]
    benchmark=benchmark.set_index(['Date']);
    benchmark['Order']=['BUY','SELL'];
    with open("benchmark_" + file, 'w') as f:
        benchmark.to_csv(f, header=True, index=True)

    #print suggest.where(suggest!=0);
    #suggest.set_index(suggest.iloc)
    #print suggest
    return res1,res2


if __name__=="__main__":
    [res1,res2]=trade(file="trainX.csv")
    [res1,res2]=trade(file="testX.csv")
