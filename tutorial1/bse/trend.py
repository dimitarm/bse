'''
Created on Mar 20, 2014

@author: dimitar
'''


import math
import datetime as dt
import itertools
import sys
from bse.utils.classes import featTrend
''' 3rd party imports '''
import numpy as np
import pandas as pand
from datetime import datetime
from datetime import timedelta
''' QSTK imports '''
from QSTK.qstkutil import DataAccess as da
import QSTK.qstkutil.tsutil as tsutil

import matplotlib.pyplot as plt
import matplotlib.axes as ax

from sklearn import preprocessing

import utils.bsedateutil as bsedateutil
import utils.equities as bseeq
import utils.data as datautil
import utils.tools as bsetools
import utils.data as bsedata
import utils.features.feats as bsefeats
import strategy_trend
import sys

def get_prediction(data, symbols, trainperiod, forwardlook, predicting_feat, features, feature_parameters, learner_factory):
    result = {}
    for symbol in symbols:
        na_full_data = bsetools.calculateSymbolFeatures(data, symbol, features, feature_parameters)
        na_full_class = bsetools.calculateSymbolFeatures(data, symbol, (predicting_feat,), feature_parameters)
        # restrict data to train period
        na_traindata = na_full_data[-i_forwardlook - trainperiod:-i_forwardlook, :]
        na_trainclass = na_full_class[-i_forwardlook - trainperiod:-i_forwardlook, :]
        # check data for correctness
        if bsedata.check_data_for_correctness(na_traindata):
            sys.stderr.write(symbol)
        # regularize
        scaler = preprocessing.StandardScaler().fit(na_traindata)
        na_traindata = scaler.transform(na_traindata)
        if bsedata.check_data_for_correctness(na_traindata):
            sys.stderr.write(symbol)        
        # make prediction for the last date in the data set
        prediction = learner_factory(na_traindata, na_trainclass, na_full_data[-1, :])
        result[symbol] = prediction
    return result

def get_feature_value(l_symbols, date, i_forwardlook, predictig_feat):
    # get data
    dtEnd = date + dt.timedelta(days=i_forwardlook)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      

    # get train data
    ldtTimestamps = bsedateutil.getBSEdays(dtStart, dtEnd, dt.timedelta(hours=16))
    # get data
    dataobj.get_data(ldtTimestamps, bseeq.get_all_equities(), 'close')
    
    
def prepare_data_for_prediction(dFullData):
    for key in dFullData.iterkeys():
        # fill forward
        tsutil.fillforward(dFullData[key].values)
        # fill backward
        tsutil.fillbackward(dFullData[key].values)
    
def show_data(dfData):
    plt.clf()
    count_symbols = len(dfData.columns)
    fig, axes = plt.subplots(nrows=count_symbols / 2 + count_symbols % 2, ncols=2)
    count = 0
    for symbol in dfData:
        dfData[symbol].plot(ax=axes[count / 2, count % 2], subplots=False, grid=False, sharex=True)
        axes[count / 2, count % 2].set_title(symbol)
        count += 1
    plt.show()
    
if __name__ == '__main__':
    
    i_trainPeriod = 60
    i_forwardlook = 5
    bShowdata = False
    
    # get data
    dtEnd = dt.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    dtStart = dtEnd - dt.timedelta(days=i_trainPeriod * 1.5)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      

    # get train data
    ldtTimestamps = bsedateutil.getBSEdays(dtStart, dtEnd, dt.timedelta(hours=16))
    # get data
    dFullData = {
             'close': dataobj.get_data(ldtTimestamps, bseeq.get_all_equities(), 'close'),
             'volume': dataobj.get_data(ldtTimestamps, bseeq.get_all_equities(), 'volume'),
             'high': dataobj.get_data(ldtTimestamps, bseeq.get_all_equities(), 'high'),
             'low': dataobj.get_data(ldtTimestamps, bseeq.get_all_equities(), 'low'),
             'open': dataobj.get_data(ldtTimestamps, bseeq.get_all_equities(), 'open')   
             }
    # get symbols to be predicted
    symbols = tsutil.stockFilter(dFullData['close'], dFullData['volume'], fNonNan=0.95, fPriceVolume=1)
    print "symbols to be predicted: " + str(symbols)
    # get only data for symbols we want to make prediction for
    dData = {}
    for serie in dFullData.iterkeys():
        dSerieData = {}
        for symbol in dFullData[serie]:
            if symbols.count(symbol) > 0:
                dSerieData[symbol] = dFullData[serie][symbol]
        dfSerie = pand.DataFrame(dSerieData)
        dData[serie] = dfSerie
    if bShowdata:
        show_data(dData['close'])    
    dt_last_date = dData['close'].index[-1].replace(hour=0, minute=0, second=0, microsecond=0)
    if dt_last_date != dtEnd:
        print "There is no data for: " + str(dtEnd)
        if raw_input("Would you like to make prediction for " + str(dt_last_date.isoweekday()) + " " + str(dt_last_date) + " (Y\N) ") != 'y':
            print "bye!"
            sys.exit(-1)
    prepare_data_for_prediction(dData)
    features, feature_parameters = bsefeats.get_feats()
    feature_parameters[featTrend] = {}
    dPredictions = get_prediction(data=dData, symbols=symbols, trainperiod=60, forwardlook=5, predicting_feat=featTrend, features=features, feature_parameters=feature_parameters, learner_factory=strategy_trend.adaBoostLearner) 

    
    
    
    
    
    
    
    
