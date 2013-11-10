'''
Created on Nov 4, 2013

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

import utils.classes as bseclasses
import utils.tools as bsetools
from sklearn import preprocessing
from sklearn import metrics 
from sklearn import svm
from sklearn import cross_validation
from sklearn.ensemble import AdaBoostClassifier
from bse.utils import tools

def executePredictionAlgorithm():
    pass

def findBestCombination (d_dfData, li_param, lfc_TestFeatures, fc_ClassificationFeature, ld_FeatureParameters, b_Plot = True):
    l_fcFeatures = list(lfc_TestFeatures)
    l_fcFeatures.append(fc_ClassificationFeature)
    
    na_featuresData = bsetools.calculateFeaturesNA(d_dfData, 'SOFIX', l_fcFeatures, ld_FeatureParameters)
    na_featuresData = tools.removeNans(na_featuresData)
    scaler = preprocessing.StandardScaler().fit(na_featuresData[:,:-1])
    na_TestSet, na_TrainSet = cross_validation.train_test_split(na_featuresData, test_size=0.3, random_state=1)
    
    na_TrainClass = na_TrainSet[:,-1]
    na_TrainSet = na_TrainSet[:,:-1]
    na_TrainSet = scaler.transform(na_TrainSet)
    na_TestClass = na_TestSet[:,-1]
    na_TestSet = na_TestSet[:,:-1]
    na_TestSet = scaler.transform(na_TestSet)

    #test each combination
    na_errRate = np.empty((0, 2))
    for i_C in li_param:
        clf = AdaBoostClassifier(n_estimators=i_C)
        clf.fit(na_TrainSet, na_TrainClass)
        
        na_Prediction = clf.predict(na_TrainSet)
        trainRate = metrics.metrics.accuracy_score(na_TrainClass, na_Prediction)
        
        na_Prediction = clf.predict(na_TestSet)
        genericRate = metrics.metrics.accuracy_score(na_TestClass, na_Prediction) 
        
        na_errRate = np.append(na_errRate, [[trainRate, genericRate]], axis = 0)
        
    if b_Plot == True:
        plt.clf()
        plt.plot(li_param, na_errRate)
        plt.legend(('train', 'generic'))
        plt.ylabel('success')
        plt.xlabel('n estimators')
        plt.show()


if __name__ == '__main__':
    
    lsSym = np.array(['SOFIX', '3JR'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2011,1,1)
    dtEnd = dt.datetime(2013,1,1)
    
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      
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
        
    ld_FeatureParameters[bseclasses.featTrend] = {'lForwardlook':1}
    ld_FeatureParameters[featMomentum] = {'lLookback':20}
    ld_FeatureParameters[featHiLow] = {'lLookback':20}
    ld_FeatureParameters[featMA] = {'lLookback':20}
    ld_FeatureParameters[featEMA] = {'lLookback':20}
    ld_FeatureParameters[featSTD] = {'lLookback':20}
    ld_FeatureParameters[featRSI] = {'lLookback':20}
    ld_FeatureParameters[featDrawDown] = {'lLookback':20}
    ld_FeatureParameters[featRunUp] = {'lLookback':20}
    ld_FeatureParameters[featAroon] = {'lLookback':20}
    ld_FeatureParameters[featVolumeDelta] = {'lLookback':20}
    ld_FeatureParameters[featStochastic] = {'lLookback':20}
    ld_FeatureParameters[featBollinger] = {'lLookback':20}
    ld_FeatureParameters[featVolume] = {}
         

    t1 = datetime.now()
    findBestCombination(dData, np.arange(1, 100, 1), lfc_TestFeatures, bseclasses.featTrend, ld_FeatureParameters)
    t2 = datetime.now()
    tdelta = t2 - t1
    print "ready " + str(tdelta) + " seconds"
    #todo test data to be chosen randomly
    #feature normalization to be optimized









if __name__ == '__main__':
    pass