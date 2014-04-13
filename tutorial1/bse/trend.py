'''
Created on Mar 20, 2014

@author: dimitar
'''
import datetime as dt
import sys
from bse.utils.classes import featTrend
''' QSTK imports '''
import QSTK.qstkutil.tsutil as tsutil

import matplotlib.pyplot as plt

from sklearn import preprocessing

import utils.equities as bseeq
import utils.data as datautil
import utils.tools as bsetools
import utils.data as bsedata
import utils.features.feats as bsefeats
import bse.utils.reader.data as bsereader
import strategy_trend

def get_prediction(data, symbols, trainperiod, forwardlook, predicting_feat, features, feature_parameters, learner_factory):
    result = {}
    for symbol in symbols:
        na_full_data = bsetools.calculateSymbolFeatures(data, symbol, features, feature_parameters)
        na_full_class = bsetools.calculateSymbolFeatures(data, symbol, (predicting_feat,), feature_parameters)
        
        #remove NaNs at beginning and at end of period
        #so that we have exactly trainperiod data to learn from
        lookbacks = bsedata.get_highest_lookback(na_full_data)
        na_traindata = na_full_data[-forwardlook - trainperiod:-forwardlook, :]
        na_trainclass = na_full_class[-forwardlook - trainperiod:-forwardlook, :].reshape((trainperiod,))
        # check data for correctness
        if bsedata.is_data_correct(na_traindata) == False:
            sys.stderr.write(symbol + " has incorrect data")
            sys.exit(-1)
        # regularize
        scaler = preprocessing.StandardScaler().fit(na_traindata)
        na_traindata = scaler.transform(na_traindata)
        if bsedata.is_data_correct(na_traindata) == False:
            print symbol + " has incorrect data after regularization" >> sys.stderr
            sys.exit(-1)       
        # make prediction for the last date in the data set
        prediction = learner_factory(na_traindata, na_trainclass, na_full_data[-1, :])
        result[symbol] = prediction
    return result

def get_symbols_for_prediction(date_end = dt.date.today(), days_period = 90):
    # calculate limit dates
    date_start = date_end - dt.timedelta(days=days_period) #fixed number of days which cover the biggest lookback period in all features + some coefficient for non working days
    #get data
    full_data = bsereader.get_data(date_start, date_end, symbols = bseeq.get_all_equities())
    # get symbols to be predicted
    return tsutil.stockFilter(full_data['close'], full_data['volumes'], fNonNan=0.95, fPriceVolume=1)

def show_data(dfData):
    plt.clf()
    count_symbols = len(dfData.columns)
    fig, axes = plt.subplots(nrows=count_symbols / 2 + count_symbols % 2, ncols=2)
    count = 0
    for symbol in dfData:
        dfData[symbol].plot(ax=axes[count / 2, count % 2], subplots=False, grid=False, sharex=True)
        dfData[symbol].plot()
        axes[count / 2, count % 2].set_title(symbol)
        count += 1
    plt.show()


    
if __name__ == '__main__':
 
    i_trainPeriod = 60
    forwardlook_days = 5
    bShowdata = True
    
    date_prediction = dt.date.today() 
    
    symbols = get_symbols_for_prediction(date_end = date_prediction, days_period = (i_trainPeriod + 40)*1.5)#fixed number of days which cover the biggest lookback period in all features + some coefficient for non working days
    print "symbols to be predicted: " + str(symbols)
    
    #read data
    data = bsereader.get_data(date_prediction - dt.timedelta(days = (i_trainPeriod + 40)*1.5), date_prediction, symbols)
    if bShowdata:
        show_data(data['close'])
    datautil.prepare_data_for_prediction(data)
    features = bsefeats.get_feats()
    
    predictions = get_prediction(
                                 data=data, 
                                 symbols=symbols, 
                                 trainperiod=60, 
                                 forwardlook=forwardlook_days, 
                                 predicting_feat=lambda (dFullData): featTrend(dFullData, lForwardlook = forwardlook_days), 
                                 features=features, 
                                 feature_parameters={}, 
                                 learner_factory=strategy_trend.adaBoostLearner) 
    print predictions
