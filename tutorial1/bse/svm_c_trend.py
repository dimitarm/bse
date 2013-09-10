'''
Created on Sep 6, 2013

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
from qstkutil import DataAccess as da

from qstkfeat.features import *
import qstkfeat.featutil as ftu

import utils.dateutil as bsedateutil

from utils.features import *
import utils.tools as bsetools
from sklearn import preprocessing

from sklearn import svm

def executePredictionAlgorithm():
    pass

def findBestCombination (d_dfData, li_param, lfc_TestFeatures, fc_ClassificationFeature, ld_FeatureParameters, b_Plot = True):
    maxSuccess = -1
    combinations = 0

    l_fcFeatures = list(lfc_TestFeatures)
    l_fcFeatures.append(fc_ClassificationFeature)
    
    na_featuresData = bsetools.calculateFeaturesNA(d_dfData, 'SOFIX', l_fcFeatures, ld_FeatureParameters)
    scaler = preprocessing.StandardScaler().fit(na_featuresData[:,:-1])
    
    (na_TrainSet, na_ValSet, na_TestSet) = bsetools.getTrainTestValidationSets(na_featuresData, bsetools.defaultTrainTestValidationFunc)
    na_TrainClass = na_TrainSet[:,-1]
    na_TrainSet = na_TrainSet[:,:-1]
    na_TrainSet = scaler.transform(na_TrainSet)

    na_ValClass = na_ValSet[:,-1]
    na_ValSet = na_ValSet[:,:-1]
    na_ValSet = scaler.transform(na_ValSet)
    
    na_TestClass = na_TestSet[:,-1]
    na_TestSet = na_TestSet[:,:-1]
    na_TestSet = scaler.transform(na_TestSet)

    #test each combination
    maxSuccess = -1
    combinations = 0
    l_perfRes = list()
    for i_C in li_param:
        clf = svm.SVC(i_C, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001, verbose=False)
        clf.fit(na_TrainSet, na_TrainClass)
        
        na_Prediction = clf.predict(na_TestSet)
        testSuccess = float(na_TestClass.size - np.count_nonzero(na_TestClass - na_Prediction))/float(na_TestClass.size)
        na_Prediction = clf.predict(na_ValSet)
        success = float(na_ValClass.size - np.count_nonzero(na_ValClass - na_Prediction))/float(na_ValClass.size)
        l_perfRes.append(success)
        if success > maxSuccess:
            maxSuccess = success
            maxClf = clf
            print "CV: " + str(success) + " Test:" + str(testSuccess) + " C: " + str(i_C)
        elif success == maxSuccess:
            print "CV: " + str(success) + " Test:" + str(testSuccess) + " C: " + str(i_C)
        combinations += 1
        
    if b_Plot == True:
        plt.clf()
        plt.plot(li_param, l_perfRes)
        plt.legend(('rbf'))
        plt.ylabel('success')
        plt.xlabel('param value')
        plt.show()
    print str(combinations) + " combinations tested"


if __name__ == '__main__':
    
    lsSym = np.array(['SOFIX', '3JR'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2011,1,1)
    dtEnd = dt.datetime(2013,5,30)
    
    dataobj = da.DataAccess('Investor')      
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16) )
    
    lsKeys = ['open', 'high', 'low', 'close', 'volume']
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=True )
    
    dData = dict(zip(lsKeys, ldfData))

    ldArgs = list()
    lfc_TestFeatures = (featBollinger, featEMA, featMA, featStochastic)
    #default parameters
    ld_FeatureParameters = {}
    for fc_feat in lfc_TestFeatures:
        ld_FeatureParameters[fc_feat] = {}
        
    ld_FeatureParameters[featTrend] = {'lForwardlook':1}
    ld_FeatureParameters[featMomentum] = {'lLookback':34}
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
         

    t1 = datetime.now()
    findBestCombination(dData, np.arange(0.5, 5, 0.01), lfc_TestFeatures, featTrend, ld_FeatureParameters)
    t2 = datetime.now()
    tdelta = t2 - t1
    print "ready " + str(tdelta) + " seconds"
    #todo test data to be chosen randomly
    #feature normalization to be optimized









if __name__ == '__main__':
    pass