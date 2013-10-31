'''
Created on Sep 11, 2013

@author: I028663
'''

import math
import datetime as dt
import itertools

''' 3rd party imports '''
import numpy as np
import pandas as pand
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

''' QSTK imports '''
from QSTK.qstkutil import DataAccess as da

from QSTK.qstkfeat.features import *
from QSTK.qstkfeat.features import *

import utils.dateutil as bsedateutil

from utils.features import *
import utils.tools as bsetools
from sklearn import preprocessing

from sklearn import svm

def dataAnalysis (d_dfData, dtPOI, b_Plot = True):
    na_allTrainData = bsetools.calculateFeaturesNA(d_dfTrainData, 'SOFIX', lfc_algFeatures, ld_FeatureParameters)
    na_testData = bsetools.calculateFeaturesNA(d_dfTestData, 'SOFIX', lfc_algFeatures, ld_FeatureParameters)
    
    l_featPerf = []
    l_percents = range(5, 100, 5)
    for i_percent in l_percents:
        i_intPart = na_allTrainData.shape[0] - na_allTrainData.shape[0] * i_percent / 100
        na_trainData = na_allTrainData[i_intPart:-1,:]
        scaler = preprocessing.StandardScaler().fit(na_trainData[:,:-1])

        na_TrainClass = na_trainData[:,-1]
        na_trainData = na_trainData[:,:-1]
        na_trainData = scaler.transform(na_trainData)
        na_TestClass = na_testData[:,-1]
        na_testData = na_testData[:,:-1]
        na_testData = scaler.transform(na_testData)
        
        clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001, verbose=False)
        clf.fit(na_trainData, na_TrainClass) 
        na_Prediction = clf.predict(na_testData)
        testSuccess = float(na_TestClass.size - np.count_nonzero(na_TestClass - na_Prediction))/float(na_TestClass.size)
        l_featPerf.append(testSuccess)
        
    plt.clf()
    plt.plot(l_percents, l_featPerf)
    plt.ylabel('success')
    plt.xlabel('% data')
    plt.show()    
     


if __name__ == '__main__':
    i_ForwardLook = 1
    i_lookback = 20
    lsSym = np.array(['SOFIX', '3JR'])
    lsKeys = ['open', 'high', 'low', 'close', 'volume']
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      
    lfc_algFeatures = [featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featVolumeDelta, featStochastic, featBollinger]
    valPeriodLength = dt.timedelta(days = 7) 
    trainPeriodLength = dt.timedelta(days = 365)
    dtPOI = dt.datetime(2012,5,31)
    
    dtStart = dtPOI - trainPeriodLength
    dtEnd = dtPOI + valPeriodLength 
    
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtPOI, dt.timedelta(hours=16) )
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=True )
    d_dfTrainData = dict(zip(lsKeys, ldfData))
    
    ldtTimestamps = bsedateutil.getBSEdays( dtPOI, dtEnd, dt.timedelta(hours=16) )
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=True )
    d_dfTestData = dict(zip(lsKeys, ldfData))
    #add classification feature
    lfc_algFeatures.append(featTrend)
    #default parameters
    ld_FeatureParameters = {}
    for feat in lfc_algFeatures:
        ld_FeatureParameters[feat] = {'lLookback':i_lookback}
    ld_FeatureParameters[featTrend] = {'lForwardlook':i_ForwardLook}
    ld_FeatureParameters[featVolume] = {}
    
    dataAnalysis(d_dfTrainData, d_dfTestData)



