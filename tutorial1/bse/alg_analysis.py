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
from qstkutil import DataAccess as da

from qstkfeat.features import *
import qstkfeat.featutil as ftu

import utils.dateutil as bsedateutil

from utils.features import *
import utils.tools as bsetools
from sklearn import preprocessing

from sklearn import svm

def dataAnalysis (d_dfTrainData, d_dfTestData, b_Plot = True):
    na_trainData = bsetools.calculateFeaturesNA(d_dfTrainData, 'SOFIX', lfc_algFeatures, ld_FeatureParameters)
    na_testData = bsetools.calculateFeaturesNA(d_dfTestData, 'SOFIX', lfc_algFeatures, ld_FeatureParameters)
    
    l_featPerf = []
    for i_percent in range(0.05, 1, 0.05):

        scaler = preprocessing.StandardScaler().fit(na_trainData[:,:-1])

        na_TrainClass = na_trainData[:,-1]
        na_trainData = na_trainData[:,:-1]
        na_trainData = scaler.transform(na_trainData)
        na_TestClass = na_testData[:,-1]
        na_testData = na_testData[:,:-1]
        na_testData = scaler.transform(na_testData)
        
        i_splitPt = na_trainData.shape[0] - na_trainData.shape[0]*i_percent
        clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001, verbose=False)
        clf.fit(na_trainData[i_splitPt:-1,:], na_TrainClass) 
        na_Prediction = clf.predict(na_testData)
        testSuccess = float(na_TestClass.size - np.count_nonzero(na_TestClass - na_Prediction))/float(na_TestClass.size)
        l_featPerf.append(testSuccess)
        
    plt.clf()
    plt.plot(range(0.05, 1, 0.05), l_featPerf)
    plt.ylabel('success')
    plt.xlabel('% data')
    plt.show()    
     


if __name__ == '__main__':
    lsSym = np.array(['SOFIX', '3JR'])
    lsKeys = ['open', 'high', 'low', 'close', 'volume']
    dataobj = da.DataAccess('Investor')      
    lfc_algFeatures = [featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featVolumeDelta, featStochastic, featBollinger]
    valPeriodLength = dt.timedelta(months = 12) 
    testPeriodLength = dt.timedelta(days = 7)
    dtPOI = dt.datetime(2012,5,31)
    
    dtStart = dtPOI - testPeriodLength
    dtEnd = dt.POI + valPeriodLength 
    
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
        ld_FeatureParameters[feat] = {}
    ld_FeatureParameters[featTrend] = {'lForwardlook':5}
    ld_FeatureParameters[featMomentum] = {'lLookback':2}  #34
    ld_FeatureParameters[featHiLow] = {'lLookback':42}
    ld_FeatureParameters[featMA] = {'lLookback':50}
    ld_FeatureParameters[featEMA] = {'lLookback':44}
    ld_FeatureParameters[featSTD] = {'lLookback':35}
    ld_FeatureParameters[featRSI] = {'lLookback':46}
    ld_FeatureParameters[featDrawDown] = {'lLookback':2}
    ld_FeatureParameters[featRunUp] = {'lLookback':34}
    ld_FeatureParameters[featAroon] = {'lLookback':2}
    ld_FeatureParameters[featVolumeDelta] = {'lLookback':13}
    ld_FeatureParameters[featStochastic] = {'lLookback':7}
    ld_FeatureParameters[featBollinger] = {'lLookback':2}
    ld_FeatureParameters[featVolume] = {}
    
    dataAnalysis(d_dfTrainData, d_dfTestData)



