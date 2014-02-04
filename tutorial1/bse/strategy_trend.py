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

from utils.classes import *
from utils import tools as bsetools
import utils.tools as bsetools
from sklearn import preprocessing
from sklearn import svm
from sklearn import metrics 
from sklearn import cross_validation
from sklearn import datasets
from sklearn import neighbors
from sklearn.ensemble import AdaBoostClassifier


def testLearner(d_dfData, t_fcTestFeatures, fc_ClassificationFeature, ld_FeatureParameters, fc_learnerFactory, i_lookback, i_trainPeriod, i_forwardlook, b_Plot = False):
    l_fcFeatures = list(t_fcTestFeatures)
    l_fcFeatures.append(fc_ClassificationFeature)
    na_data = bsetools.calculateFeaturesNA(d_dfData, 'SOFIX', l_fcFeatures, ld_FeatureParameters)
    na_data = na_data[i_lookback:-i_forwardlook,:]
    #test each combination
    success = float(0)
    scaler = preprocessing.StandardScaler().fit(na_data[:,:-1])
    
    na_mainData = scaler.transform(na_data[:,:-1])
    na_classData = na_data[:,-1]
    for i in range(i_trainPeriod, na_data.shape[0] - i_forwardlook + 1):
        clf = fc_learnerFactory(na_mainData[i - i_trainPeriod:i,:], na_classData[i - i_trainPeriod:i])
        i_prediction = clf.predict(na_mainData[i,:])
        if (i_prediction == na_classData[i]):
            success += 1
    print "success rate: " + str(success/(na_data.shape[0] - i_forwardlook - i_trainPeriod))

def svmLearner(na_data, na_class):
    clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001, verbose=False)
    clf.fit(na_data, na_class)
    return clf

def adaBoostLearner(na_data, na_class):
    baseClf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=True, shrinking=True, tol=0.001, verbose=False)
    clf = AdaBoostClassifier(base_estimator = baseClf, n_estimators=50)
    clf.fit(na_data, na_class)    
    return clf

def findBestFeatCobination(na_data, b_Plot = False):
    maxSuccess = -1
    combinations = 0
    #test each combination
    maxSuccess = -1
    combinations = 0
    
    l_featCombinations = ()
    for i in range(1, na_data.shape[1] + 1):
        l_featCombinations.apend(itertools.combinations(range(0, na_data.shape[1]), i))
    for lfc_combination in lfc_featCombinationSet:
        na_data = np.empty((na_featuresData.shape[0], 0))
        #stack feat data from combination
        for fcFeat in lfc_combination:
            i_featIndex = l_fcFeatures.index(fcFeat)
            na_data = np.hstack((na_data, na_featuresData[:, i_featIndex].reshape(na_featuresData.shape[0], 1)))
        #stack classification data
        na_data = np.hstack((na_data, na_featuresData[:, -1].reshape(na_featuresData.shape[0], 1)))
        scaler = preprocessing.StandardScaler().fit(na_data[:,:-1])
        
        na_TrainSet, na_TestSet = cross_validation.train_test_split(na_data, test_size=0.3, random_state=1)
        
        na_TrainClass = na_TrainSet[:,-1]
        na_TrainSet = na_TrainSet[:,:-1]
        na_TrainSet = scaler.transform(na_TrainSet)
    
        na_TestClass = na_TestSet[:,-1]
        na_TestSet = na_TestSet[:,:-1]
        na_TestSet = scaler.transform(na_TestSet)
        
        clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001, verbose=False)
        #clf = neighbors.KNeighborsClassifier(n_neighbors = 20)
        clf.fit(na_TrainSet, na_TrainClass)
 
        na_Prediction = clf.predict(na_TestSet)
        
        success = metrics.metrics.accuracy_score(na_TestClass, na_Prediction)
        if success > maxSuccess:
            maxSuccess = success
            maxClf = clf
            l_maxFeatSet = list()
            for feat in lfc_combination:
                l_maxFeatSet.append(feat.func_name)
            l_maxFeatSet.sort()
            metric = "None"
            print "Test:" + str(success) + " combination: " + str(l_maxFeatSet) + " " + "-1" + ": " + str(metrics.metrics.f1_score(na_TestClass, na_Prediction, pos_label = -1))  + " " + "1" + ": " + str(metrics.metrics.f1_score(na_TestClass, na_Prediction, pos_label = 1))
            clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001, verbose=False)
            scores = cross_validation.cross_val_score(clf, na_data[:,:-1], na_data[:,-1], cv=5)            
            print str(scores)
            print "test data: " + str(np.histogram(na_TestClass, 2))
            print ""
            if b_Plot == True:
                plt.clf()
                for i in range(0, na_TrainClass.shape[0]):
                    if na_TrainClass[i] == 1:
                        plt.plot( na_TrainSet[i][0], na_TrainSet[i][1], 'g+' )
                    elif na_TrainClass[i] == -1:
                        plt.plot( na_TrainSet[i][0], na_TrainSet[i][1], 'ro' )
                    else:
                        plt.plot( na_TrainSet[i][0], na_TrainSet[i][1], 'kx' )
                plt.ylabel(lfc_combination[0].func_name)
                plt.xlabel(lfc_combination[1].func_name)
                plt.show()            
        combinations += 1
    print str(combinations) + " combinations tested"
    return l_maxFeatSet, maxSuccess


if __name__ == '__main__':
    i_forwardlook = 1
    i_lookback = 20
    lsSym = np.array(['SOFIX', '3JR'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2012,1,1)
    dtEnd = dt.datetime(2013,1,1)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      
    lsKeys = ['open', 'high', 'low', 'close', 'volume']

    #get train data
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16) )
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=True )
    
    dData = dict(zip(lsKeys, ldfData))
    
    
    lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featAroonDown, featVolumeDelta, featStochastic, featVolume, featBollinger)
#    lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featRSI)
    
    #default parameters
    ld_FeatureParameters = {}
    for fc_feat in lfc_TestFeatures:
        ld_FeatureParameters[fc_feat] = {}
        
    ld_FeatureParameters[featTrend] = {'lForwardlook':i_forwardlook}
    ld_FeatureParameters[featMomentum] = {'lLookback':i_lookback}  
    ld_FeatureParameters[featHiLow] = {'lLookback':i_lookback}
    ld_FeatureParameters[featMA] = {'lLookback':i_lookback}
    ld_FeatureParameters[featEMA] = {'lLookback':i_lookback}
    ld_FeatureParameters[featSTD] = {'lLookback':i_lookback}
    ld_FeatureParameters[featRSI] = {'lLookback':i_lookback}
    ld_FeatureParameters[featDrawDown] = {'lLookback':i_lookback}
    ld_FeatureParameters[featRunUp] = {'lLookback':i_lookback}
    ld_FeatureParameters[featAroon] = {'lLookback':i_lookback}
    ld_FeatureParameters[featAroonDown] = {'lLookback':i_lookback}
    ld_FeatureParameters[featVolumeDelta] = {'lLookback':i_lookback}
    ld_FeatureParameters[featStochastic] = {'lLookback':i_lookback}
    ld_FeatureParameters[featBollinger] = {'lLookback':i_lookback}
    ld_FeatureParameters[featVolume] = {}
         

    t1 = datetime.now()
    
    testLearner(dData, lfc_TestFeatures, featTrend, ld_FeatureParameters, adaBoostLearner, i_lookback = i_lookback, i_trainPeriod = 60, i_forwardlook = i_forwardlook)
    t2 = datetime.now()
    tdelta = t2 - t1
    print "testLearner " + str(tdelta) + " seconds"






