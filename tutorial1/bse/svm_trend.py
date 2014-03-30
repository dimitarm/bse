'''
Created on Aug 23, 2013

@author: I028663
'''

import math
import datetime as dt
import itertools

''' 3rd party imports '''
import numpy as np
import pandas as pand
import matplotlib.pyplot as plt

''' QSTK imports '''
from QSTK.qstkutil import DataAccess as da
from QSTK.qstkfeat.features import *
import QSTK.qstkfeat.featutil as ftu

import bse.utils.dateutil as bsedateutil
import bse.utils.data as datautil
import bse.utils.tools as bsetools
from utils.features import *
from utils.classes import featTrend

from sklearn import preprocessing
from sklearn import svm
from sklearn import metrics 
from sklearn import cross_validation
from sklearn import datasets
from sklearn import neighbors

def findBestFeatCobination(d_dfData, lfc_featCombinationSet, t_fcTestFeatures, fc_ClassificationFeature, ld_FeatureParameters, b_Plot = False):
    maxSuccess = -1
    combinations = 0
    l_fcFeatures = list(t_fcTestFeatures)
    l_fcFeatures.append(fc_ClassificationFeature)
    na_featuresData = bsetools.calculateFeaturesNA(d_dfData, 'SOFIX', l_fcFeatures, ld_FeatureParameters)
    #test each combination
    maxSuccess = -1
    combinations = 0
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
    
    lsSym = np.array(['SOFIX', '3JR'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2011,8,1)
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
    
    #lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featAroonDown, featVolumeDelta, featStochastic, featVolume, featBollinger)
    lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featVolumeDelta, featStochastic, featVolume)
    
    #default parameters
    ld_FeatureParameters = {}
    for fc_feat in lfc_TestFeatures:
        ld_FeatureParameters[fc_feat] = {}
        
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
    ld_FeatureParameters[featTrend] = {'lForwardlook':5}
         

    t1 = dt.datetime.now()
    
    findBestFeatCobination(dData, bsetools.getAllFeaturesCombinationsList(lfc_TestFeatures), lfc_TestFeatures, featTrend, ld_FeatureParameters)
    #findBestCombination(dData, itertools.combinations(lfc_TestFeatures, 1), lfc_TestFeatures, featTrend, ld_FeatureParameters, b_Plot = False)
    t2 = dt.datetime.now()
    tdelta = t2 - t1
    print "findBestCombination " + str(tdelta) + " seconds"
    #todo test data to be chosen randomly
    #feature normalization to be optimized






