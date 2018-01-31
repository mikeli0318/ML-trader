import marketsim as mar


if __name__=="__main__":
    print
    print "-------------------"
    print "manual strategy - in sample"
    print
    mar.test_code(of="order_trainX.csv");
    print
    print "-------------------"
    print "ML strategy - in sample"
    print
    print
    mar.test_code(of="ML_order_trainX.csv");
    print
    print "-------------------"
    print "benchmark - in sample"
    print
    print
    mar.test_code(of="benchmark_trainX.csv");
    print
    print "-------------------"
    print "manual strategy - out sample"
    print
    print
    mar.test_code(of="order_testX.csv");
    print
    print "-------------------"
    print "ML strategy - out sample"
    print
    print
    mar.test_code(of="ML_order_testX.csv");
    print
    print "-------------------"
    print "benchmark - out sample"
    print
    print
    mar.test_code(of="benchmark_testX.csv");



