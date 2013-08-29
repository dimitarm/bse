'''
Created on Aug 29, 2013

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

def executePredictionAlgorithm():
    pass

def findBestFeatureParamValue (d_dfData, fc_feature, fc_ClassificationFeature, s_paramName, l_paramValues, d_basicFeatParameters, b_Plot = True):
    l_fcFeatures = list()
    l_fcFeatures.append(fc_feature)
    l_fcFeatures.append(fc_ClassificationFeature)
    ld_FeatureParameters = dict(d_basicFeatParameters)
    print 'feature: ' + fc_feature.func_name
    for paramVal in l_paramValues:
        #d_featParams = dict(d_basicFeatParameters[fc_feature])
        #d_featParams[s_paramName] = paramVal
        ld_FeatureParameters[fc_feature][s_paramName] = paramVal
        
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
    
        clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001, verbose=False)
        clf.fit(na_TrainSet, na_TrainClass) 
        na_Prediction = clf.predict(na_ValSet)
        valSuccess = float(na_ValClass.size - np.count_nonzero(na_ValClass - na_Prediction))/float(na_ValClass.size)
        na_Prediction = clf.predict(na_TestSet)
        testSuccess = float(na_TestClass.size - np.count_nonzero(na_TestClass - na_Prediction))/float(na_TestClass.size)
        print '    ' + 'param: ' + str(paramVal) + ' validationSet: ' + str(valSuccess) + ' testSet: ' + str(testSuccess) 


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
    #lfc_TestFeatures = [featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featBollinger]
    lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featVolumeDelta, featStochastic, featVolume, featBollinger)
    #default parameters
    d_FeatureParameters = {}
    for feat in lfc_TestFeatures:
        d_FeatureParameters[feat] = {}
    d_FeatureParameters[featTrend] = {'lForwardlook':1}
#    ldArgs = [ {'lLookback':30, 'bRel':True},\
#               {},\
#               {}]             
         

    findBestFeatureParamValue (dData, featAroon, featTrend, 'lLookback', range(2, 100, 1), d_FeatureParameters, b_Plot = True)    
    






