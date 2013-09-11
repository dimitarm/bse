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

def findBestFeatureParamValue (d_dfTrainData, d_dfTestData, fc_feature, fc_ClassificationFeature, s_paramName, l_paramValues, d_basicFeatParameters, b_Plot = True):
    l_fcFeatures = (fc_feature, fc_ClassificationFeature)
    ld_FeatureParameters = dict(d_basicFeatParameters)
    na_featPerf = ()
    for paramVal in l_paramValues:
        ld_FeatureParameters[fc_feature][s_paramName] = paramVal
        na_trainData = bsetools.calculateFeaturesNA(d_dfTrainData, 'SOFIX', l_fcFeatures, ld_FeatureParameters)
        na_testData = bsetools.calculateFeaturesNA(d_dfTestData, 'SOFIX', l_fcFeatures, ld_FeatureParameters)
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
        na_featPerf.append(testSuccess)
        
    i_maxValSetValue = na_featPerf[:, 0].argmax()
    print fc_feature.func_name + ': ' + 'param: ' + str(l_paramValues[i_maxValSetValue]) + ' validationSet: ' + str(na_featPerf[i_maxValSetValue][0]) + ' testSet: ' + str(na_featPerf[i_maxValSetValue][1])
    plt.clf()
    plt.plot(l_paramValues, na_featPerf)
    plt.legend(('validationSet', 'testSet'))
    plt.ylabel(fc_feature.func_name)
    plt.xlabel(s_paramName)
    plt.show()    
     


if __name__ == '__main__':
    lsSym = np.array(['SOFIX', '3JR'])
    lsKeys = ['open', 'high', 'low', 'close', 'volume']
    dataobj = da.DataAccess('Investor')      
    lfc_Features2Test = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featVolumeDelta, featStochastic, featBollinger)
    valPeriodLength = dt.timedelta(days = 7) 
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
    
    #default parameters
    d_basicFeatParameters = {}
    for feat in lfc_Features2Test:
        d_basicFeatParameters[feat] = {}
    d_basicFeatParameters[featTrend] = {'lForwardlook':1}

    for fc_feature in lfc_Features2Test:
        findBestFeatureParamValue (d_dfTrainData, d_dfTestData, fc_feature, featTrend, 'lLookback', range(2, testPeriodLength.days, 1), d_basicFeatParameters)











    findBestFeatureParamValue (dData, lfc_TestFeatures, featTrend, 'lLookback', [20], d_FeatureParameters, b_Plot = True)    
    

