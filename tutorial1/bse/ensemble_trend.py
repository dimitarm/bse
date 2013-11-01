'''
Created on Oct 31, 2013

@author: dimitar
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
import QSTK.qstkfeat.featutil as ftu

import utils.dateutil as bsedateutil
import utils.data as datautil

from utils.features import *
import utils.tools as bsetools
from sklearn import preprocessing
from sklearn import svm
from sklearn import metrics 
from sklearn import cross_validation
from sklearn import datasets
from sklearn import neighbors
from sklearn.ensemble import AdaBoostClassifier


def findBestFeatCobination(d_dfData, lfc_featCombinationSet, t_fcTestFeatures, fc_ClassificationFeature, ld_FeatureParameters, b_Plot = False):
    maxSuccess = -1
    combinations = 0
    l_fcFeatures = list(t_fcTestFeatures)
    l_fcFeatures.append(fc_ClassificationFeature)
    na_data = bsetools.calculateFeaturesNA(d_dfData, 'SOFIX', l_fcFeatures, ld_FeatureParameters)
    #test each combination
    maxSuccess = -1
    combinations = 0
    
    scaler = preprocessing.StandardScaler().fit(na_data[:,:-1])
    
    na_TrainSet, na_TestSet = cross_validation.train_test_split(na_data, test_size=0.3, random_state=1)
    
    na_TrainClass = na_TrainSet[:,-1]
    na_TrainSet = na_TrainSet[:,:-1]
    na_TrainSet = scaler.transform(na_TrainSet)

    na_TestClass = na_TestSet[:,-1]
    na_TestSet = na_TestSet[:,:-1]
    na_TestSet = scaler.transform(na_TestSet)
    
    na_learnerResults = np.empty((0, 2))
    for i in range(4, 200, 4):
        baseclf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=True, shrinking=True, tol=0.001, verbose=False)
        clf = AdaBoostClassifier(n_estimators=i, base_estimator = baseclf)
        #clf = AdaBoostClassifier(n_estimators=i)
        clf.fit(na_TrainSet, na_TrainClass)
        na_Prediction = clf.predict(na_TestSet)
        success = metrics.metrics.accuracy_score(na_TestClass, na_Prediction)
        na_learnerResults = np.append(na_learnerResults, [[i, success]], axis = 0)

    plt.clf()
    plt.plot(na_learnerResults[:, 0], na_learnerResults[:, 1])
    plt.ylabel('acuracy score')
    plt.xlabel('n estimators')
    plt.show()            
#    print "Test:" + str(success) + " -1: " + str(metrics.metrics.f1_score(na_TestClass, na_Prediction, pos_label = -1))  + " 1: " + str(metrics.metrics.f1_score(na_TestClass, na_Prediction, pos_label = 1))
#    clf = AdaBoostClassifier(n_estimators=28)
#    scores = cross_validation.cross_val_score(clf, na_data[:,:-1], na_data[:,-1], cv=5)            
#    print str(scores)
#    print "test data: " + str(np.histogram(na_TestClass, 2))

if __name__ == '__main__':
    
    lsSym = np.array(['SOFIX', '3JR'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2010,6,1)
    dtEnd = dt.datetime(2012,5,30)
    testPeriodLength = dt.timedelta(days = 7)
    dtValEnd = dtEnd + testPeriodLength
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      
    lsKeys = ['open', 'high', 'low', 'close', 'volume']

    #get train data
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16) )
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=True )
    #get test data
#    ldtTimestamps = bsedateutil.getBSEdays( dtEnd, dtValEnd, dt.timedelta(hours=16) )
#    l_dfValidationData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=True )
    
    dData = dict(zip(lsKeys, ldfData))
#    d_dfValidationData = dict(zip(lsKeys, l_dfValidationData))
    
    #dData = datautil.get_random_data(l_keys = lsKeys, l_index = ldtTimestamps, l_symbols = lsSym)
#    plt.clf()
#    plt.plot(ldtTimestamps, dData['close'])
#    plt.show()     
    
    lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featAroonDown, featVolumeDelta, featStochastic, featVolume, featBollinger)
    #lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featVolumeDelta, featStochastic, featVolume)
    
    #default parameters
    ld_FeatureParameters = {}
    for fc_feat in lfc_TestFeatures:
        ld_FeatureParameters[fc_feat] = {}
        
    ld_FeatureParameters[featTrend] = {'lForwardlook':20}
    ld_FeatureParameters[featMomentum] = {'lLookback':20}  
    ld_FeatureParameters[featHiLow] = {'lLookback':20}
    ld_FeatureParameters[featMA] = {'lLookback':20}
    ld_FeatureParameters[featEMA] = {'lLookback':20}
    ld_FeatureParameters[featSTD] = {'lLookback':20}
    ld_FeatureParameters[featRSI] = {'lLookback':20}
    ld_FeatureParameters[featDrawDown] = {'lLookback':20}
    ld_FeatureParameters[featRunUp] = {'lLookback':20}
    ld_FeatureParameters[featAroon] = {'lLookback':20}
    ld_FeatureParameters[featAroonDown] = {'lLookback':20}
    ld_FeatureParameters[featVolumeDelta] = {'lLookback':20}
    ld_FeatureParameters[featStochastic] = {'lLookback':20}
    ld_FeatureParameters[featBollinger] = {'lLookback':20}
    ld_FeatureParameters[featVolume] = {}
         

    t1 = datetime.now()
    
    findBestFeatCobination(dData, bsetools.getAllFeaturesCombinationsList(lfc_TestFeatures), lfc_TestFeatures, featTrend, ld_FeatureParameters)
    #findBestCombination(dData, itertools.combinations(lfc_TestFeatures, 1), lfc_TestFeatures, featTrend, ld_FeatureParameters, b_Plot = False)
    t2 = datetime.now()
    tdelta = t2 - t1
    print "findBestCombination " + str(tdelta) + " seconds"
    #todo test data to be chosen randomly
    #feature normalization to be optimized






