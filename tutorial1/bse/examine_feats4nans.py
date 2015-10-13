'''
Created on Oct 31, 2013

@author: dimitar
'''

import math
import datetime as dt
import itertools
import sys

''' 3rd party imports '''
import numpy as np
import pandas as pand
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta



import utils.dateutil as bsedateutil    
import utils.data as bsedatautil
import utils.features.feats as bsefeats
import bse.utils.reader.data as bsereader

from utils.classes import *
import utils.tools as bsetools
from sklearn import preprocessing
from sklearn import svm
from sklearn import decomposition
from sklearn.utils import assert_all_finite
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier


if __name__ == '__main__':
    i_forwardlook = 5
    #lsSym = np.array(['3JR', '4CF', '6C4', 'SOFIX'])
    lsSym = np.array(['3JR', 'SOFIX'])
    
    ''' Get data '''
    dtEnd = dt.datetime(2014,9,23). replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    dtStart = dtEnd - dt.timedelta(days = 365*2)
    lsKeys = ['open', 'high', 'low', 'close', 'volumes']
    #get train data
    dPrices = bsereader.get_data(dtStart, dtEnd, lsSym)

    #dPrices = bsedatautil.get_random_data(lsKeys, bsedateutil.getBSEdays(dtStart, dtEnd), lsSym)
    #fill forward values
    lfc_TestFeatures = bsefeats.get_uniques_feats()

    t1 = datetime.now()

    #calculate features
    ldfFeatures = bsetools.calculateFeatures(dPrices, lfc_TestFeatures, {})
    print "features calculated in {0} seconds".format(datetime.now() - t1)
    ddfFeatures = bsetools.extractSymbolFeatures(ldfFeatures)
    off = 0
    symbol = '3JR'
    plt.clf()
    plt.plot(dPrices['close'][symbol], label = symbol)
    plt.legend()
    plt.show()
    dfFeatures = ddfFeatures[symbol]
    for serie in dfFeatures:
        tsSerie = dfFeatures[serie]
        dfNans = tsSerie[tsSerie == np.NAN]
        plt.clf()
        plt.plot(tsSerie.index, tsSerie, label = serie)
        plt.legend()
        plt.show()
    #calculate class
    fcClassificationFeature = lambda (dFullData): featTrend(dFullData, lForwardlook = i_forwardlook), 
    ldfClass = bsetools.calculateFeatures(dPrices, (fcClassificationFeature), {})
    ddfClass = bsetools.extractSymbolFeatures(ldfClass) 
    
    for symbol in ddfClass.iterkeys():
        dfFeatures = ddfClass[symbol]
        print "{}: {} nans in class".format(symbol, np.count_nonzero(np.isnan(dfFeatures.values))) 
    






