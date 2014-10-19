'''
Created on Oct 31, 2013

@author: dimitar
'''

import datetime as dt

''' 3rd party imports '''
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

''' QSTK imports '''

import QSTK.qstkutil.tsutil as tsutil
import utils.features.feats as bsefeats

from utils.classes import featTrend
import utils.tools as bsetools
import utils.data as bsedata
import bse.utils.reader.data as bsereader
import bse.utils.tradesimulator as tradesimulator
from sklearn.ensemble import AdaBoostClassifier


if __name__ == '__main__':
    i_forwardlook = 5
    i_trainPeriod = 60
    lsSym = np.array(['3JR', '4CF', '6A6', '6C4', 'E4A', 'SOFIX'])
    
    ''' Get data '''
    dtStart = dt.datetime(2013,1,11).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    dtEnd = dt.datetime(2014,1,1).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    dPrices = bsereader.get_data(dtStart, dtEnd, lsSym)
    #fill forward
    for sym in dPrices.iterkeys():
        dPrices[sym].fillna(method='ffill')
    
    #calculate features
    lfc_TestFeatures = bsefeats.get_feats()
    ldfFeatures = bsetools.calculateFeatures(dPrices, lfc_TestFeatures, {})
    ddfFeatures = bsetools.extractSymbolFeatures(ldfFeatures)
    #calculate class
    fcClassificationFeature = lambda (dFullData): featTrend(dFullData, lForwardlook = i_forwardlook), 
    ldfClass = bsetools.calculateFeatures(dPrices, (fcClassificationFeature), {})
    ddfClass = bsetools.extractSymbolFeatures(ldfClass)
    
    dAllocations = {}
    #get loopback
    loopback = bsedata.get_highest_lookback(ddfFeatures[lsSym[0]])
    
    for day_index in range(i_trainPeriod + i_forwardlook.max(), dPrices.index.size - i_forwardlook - 1, i_forwardlook):
        day = dPrices.index[day_index]
        lPortfolio = []
        #calculate new portfolio symbols
        for symbol in lsSym:
            predictor = AdaBoostClassifier(n_estimators=50)
            train_data = ddfFeatures[symbol][day_index - i_trainPeriod:day_index,:]
            class_data = ddfClass[symbol][day_index - i_trainPeriod:day_index]
            predictor.fit(train_data, class_data)
            if predictor.predict(ddfFeatures[symbol][day_index, :-1]) == 1:
                lPortfolio.append(symbol)
        #calclate portfolio structure
        dDayAllocation = {} 
        for symbol in lPortfolio:
            dDayAllocation[symbol] = 1/len(lPortfolio) #equal portfolio structure
        dAllocations[day] = dDayAllocation
    
    tradesimulator.simulate_trades(dAllocations, dPrices, 10000)
    
    






