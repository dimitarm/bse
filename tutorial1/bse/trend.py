'''
Created on Mar 20, 2014

@author: dimitar
'''


import math
import datetime as dt
import itertools
import sys
''' 3rd party imports '''
import numpy as np
import pandas as pand
from datetime import datetime
from datetime import timedelta
''' QSTK imports '''
from QSTK.qstkutil import DataAccess as da
import QSTK.qstkutil.tsutil as tsutil

from sklearn import preprocessing

import utils.bsedateutil as bsedateutil
import utils.equities as bseeq
import utils.data as datautil
import utils.tools as bsetools
import bse.utils as bseutils
import utils.data as bsedata

def get_prediction(dData, l_symbols, date, i_trainperiod, i_forwardlook, predicting_feat, l_features, d_FeatureParameters, fc_learnerfactory):
    result = {}
    index_of_date = dData[l_symbols[0]]
    for symbol in l_symbols:
        na_traindata = bsetools.calculateSymbolFeatures(dData, symbol, l_features, d_FeatureParameters)
        na_trainclass = bsetools.calculateSymbolFeatures(dData, symbol, (predicting_feat), d_FeatureParameters)
        #restrict data to train period
        na_traindata = na_traindata[-i_forwardlook - i_trainperiod:-i_forwardlook,:]
        na_trainclass = na_trainclass[-i_forwardlook - i_trainperiod:-i_forwardlook,:]
        #check data for correctness
        if bsedata.check_data_for_correctness(na_traindata):
            sys.stderr.write(symbol)
        #regularize
        scaler = preprocessing.StandardScaler().fit(na_traindata)
        na_traindata = scaler.transform(na_traindata)
        if bsedata.check_data_for_correctness(na_traindata):
            sys.stderr.write(symbol)        
        
        prediction = fc_learnerfactory(na_traindata, na_trainclass, na_mainData[i,:])
        result[symbol] = prediction
    
def prepare_data_for_prediction(dData):
    for key in dData.iterkeys():
        #fill forward
        tsutil.fillforward(dData[key].values)
        #fill backward
        tsutil.fillbackward(dData[key].values)
        
if __name__ == '__main__':
    
    i_trainPeriod = 60
    i_forwardlook = 5
    
    #get data
    dtEnd = dt.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    dtStart = dtEnd - dt.timedelta(days = i_trainPeriod * 1.5)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      

    #get train data
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16) )
    #get data
    dData = {
             'close': dataobj.get_data( ldtTimestamps, bseeq.get_all_equities(), 'close' ),
             'volume': dataobj.get_data( ldtTimestamps, bseeq.get_all_equities(), 'volume' ),
             'high': dataobj.get_data( ldtTimestamps, bseeq.get_all_equities(), 'high' ),
             'low': dataobj.get_data( ldtTimestamps, bseeq.get_all_equities(), 'low' ),
             'open': dataobj.get_data( ldtTimestamps, bseeq.get_all_equities(), 'open' )   
             }
    #get symbols to be predicted
    l_symbols = tsutil.stockFilter(dData['close'], dData['volume'], fNonNan = 0.95, fPriceVolume = 1)
    print "symbols to be predicted: " + str(l_symbols)
    
    prepare_data_for_prediction(dData)    
    
    
    
    
    
    
    
    
    