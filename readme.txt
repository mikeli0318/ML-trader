Before you run:
please make sure all the data file (price data) are in the ../data
that is:
/some folder
     /data
          /(all the data files)
     /mc3_p3
          /(all my files here)

THANKS A LOT
—————————————————————————————————————————————————————————————————————————————

If you want to run the whole project, here’s what you need to do:
step 1. "python test.py"
step 2. "python evaluate.py"
step 3. "python plotTrade.py"


If you are using your own market simulator, here’s what you need to do:
—>only run "python test.py"

This will generate the indicator file, the indicator plots and 6 order files for benchmark, manual strategy and ML trader for in-sample and out-sample test.
the 6 order files are:
-benchmark_trainX.csv: 
	benchmark order file, in-sample
-benchmark_testX.csv: 
	benchmark order file, out-sample
-order_trainX.csv:
	manual strategy order, in-sample
-order_testX.csv:
	manual strategy order, out-sample
-ML_order_trainX.csv:
	ML trader order, in-sample
-ML_order_testX.csv:
	ML trader order, out-sample

You can use them for your own market simulator.

===================================

here’s what the 3 files mentioned above will do:
1.test.py:
It will run the indicators.py and my trading strategies. If the data files are put in the correct position, then it can generate the indicator matrix correctly, as well as the Y_train for the machine learning trader. Then it will perform all the 2 methods in both in-sample period and out-sample period.
Finally there will be 6 order files, including 2 for benchmark.

2.evaluate.py:
it will evaluate the 2 traders VS benchmark for in-sample and out-sample period. IF YOU ARE USING YOUR OWN MARKET SIMULATOR, THEN DO NOT RUN THIS FILE.

3.plotTrade.py:
this will draw the plot for part 2,3,4.
IF YOU ARE USING YOUR OWN MARKET SIMULATOR, THEN DO NOT RUN THIS FILE.


———————appendix: other files—————
RTLearner.py:
Random forest, which will be used by bag learner.

BagLearner.py:
Bag learner. Use this build random forest.
indicators.py:
read in the data of IBM, and generate the 3 indicators. No need to run this file separately, it is already run by test.py.
marketsim.py:
my own market simulator, you can replace since test.py will generate all the order files necessary. If you replace this, don’t run evaluate.py and plotTrade.py.
ml_based.py:
a file which uses the data to train random forest and get order files for in-sample and out-sample test. If you want to modify the leaf size and bags, you can modify it in this file. No need to run this file separately, it is already run by test.py.
rule_based.py:
My manual strategy.
util.py:
You can replace it, I only use it for reading data.
