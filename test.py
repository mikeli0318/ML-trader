import rule_based as rule
import numpy as np
import pandas as pd
import datetime as dt
import RTLearner as rt
import BagLearner as bl
import ml_based as ml
import indicators as ind
from util import get_data, plot_data

if __name__=="__main__":
    ind.get_indicators(draw=True);
    rule.trade(file="trainX.csv");
    rule.trade(file="testX.csv");
    ml.TwoTrade();



