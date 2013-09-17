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
from QSTK.qstkutil import DataAccess as da

from QSTK.qstkfeat.features import *
import QSTK.qstkfeat.featutil as ftu

import utils.dateutil as bsedateutil

from utils.features import *
import utils.tools as bsetools
from sklearn import preprocessing

from sklearn import svm

def executePredictionAlgorithm():
    pass

def findBestParamValue(d_dfData, lfc_testFeatures, fc_ClassificationFeature, s_paramName, l_paramValues, d_basicFeatParameters, b_Plot = True):
    for fc_feature in lfc_testFeatures:
        l_fcFeatures = list()
        l_fcFeatures.append(fc_feature)
        l_fcFeatures.append(fc_ClassificationFeature)
        ld_FeatureParameters = dict(d_basicFeatParameters)
        na_featPerf = np.empty((0, 2))
        for paramVal in l_paramValues:
            #d_featParams = dict(d_basicFeatParameters[fc_feature])
            #d_featParams[s_paramName] = paramVal
            ld_FeatureParameters[fc_feature][s_paramName] = paramVal
            
            na_featuresData = bsetools.calculateFeaturesNA(d_dfData, '3JR', l_fcFeatures, ld_FeatureParameters)
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
            na_Prediction = clf.predict(na_TestSet)
            testSuccess = float(na_TestClass.size - np.count_nonzero(na_TestClass - na_Prediction))/float(na_TestClass.size)
            na_Prediction = clf.predict(na_ValSet)
            valSuccess = float(na_ValClass.size - np.count_nonzero(na_ValClass - na_Prediction))/float(na_ValClass.size)
            #print '    ' + 'param: ' + str(paramVal) + ' validationSet: ' + str(valSuccess) + ' testSet: ' + str(testSuccess)
            na_featPerf = np.append(na_featPerf, [[valSuccess, testSuccess]], axis = 0)
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
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2012,5,31)
    dtEnd = dt.datetime(2013,5,30)
    
    dataobj = da.DataAccess(sourcein = da.DataSource.CUSTOM, verbose=True)
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16) )
    
    lsKeys = ['open', 'high', 'low', 'close', 'volume']
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=True )
    
    dData = dict(zip(lsKeys, ldfData))

    ldArgs = list()
    lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featVolumeDelta, featStochastic, featBollinger)
    #default parameters
    d_FeatureParameters = {}
    for feat in lfc_TestFeatures:
        d_FeatureParameters[feat] = {}
    d_FeatureParameters[featTrend] = {'lForwardlook':1}

    findBestParamValue(dData, lfc_TestFeatures, featTrend, 'lLookback', range(2, 80, 1), d_FeatureParameters, b_Plot = True)    
    






