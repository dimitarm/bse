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
import QSTK.qstkutil.tsutil as tsutil
import utils.dateutil as bsedateutil
import utils.data as datautil
import utils.features.feats as bsefeats

from utils.classes import *
from utils import tools as bsetools
import utils.tools as bsetools
from sklearn import preprocessing
from sklearn import svm
from sklearn import metrics 
from sklearn import cross_validation
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier


def testLearner(d_dfData, t_fcTestFeatures, fc_ClassificationFeature, ld_FeatureParameters, fc_learnerFactory, i_lookback, i_trainPeriod, i_forwardlook, b_Plot = False):
    l_fcFeatures = list(t_fcTestFeatures)
    l_fcFeatures.append(fc_ClassificationFeature)
    na_data = bsetools.calculateFeaturesNA(d_dfData, '3JR', l_fcFeatures, ld_FeatureParameters)
    #fill forward
    tsutil.fillforward(na_data)
    #fillbackward
    tsutil.fillbackward(na_data)
    
    na_data = na_data[i_lookback:-i_forwardlook,:]
    #test each combination
    success = float(0)
    scaler = preprocessing.StandardScaler().fit(na_data[:,:-1])
    
    na_mainData = scaler.transform(na_data[:,:-1])
    na_classData = na_data[:,-1]#.reshape(na_data.shape[0], 1)
    count = 0
    for i in range(i_trainPeriod, na_data.shape[0] - i_forwardlook + 1):
        hit = 0
        i_prediction = fc_learnerFactory(na_mainData[i - i_trainPeriod:i,:], na_classData[i - i_trainPeriod:i], na_mainData[i,:])
        if (i_prediction == na_classData[i]):
            success += 1
            hit = 1
        count += 1
    print "success rate: " + str(success/count)

def svmLearner(na_train, na_class, na_data):
    clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001, verbose=False)
    clf.fit(na_train, na_class)
    return clf.predict(na_data)

def adaBoostLearner(na_train, na_class, na_data):
    #baseClf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='rbf', probability=True, shrinking=True, tol=0.001, verbose=False)
    #clf = AdaBoostClassifier(base_estimator = baseClf, n_estimators=50)
    clf = AdaBoostClassifier(n_estimators=50)
    clf.fit(na_train, na_class)    
    return clf.predict(na_data)

def knnLearner(na_train, na_class, na_data):
    clf = KNeighborsClassifier(n_neighbors = 5)
    clf.fit(na_train, na_class)    
    return clf.predict(na_data)

def knnBestFeatCombinationLearner(na_train, na_class, na_data):
    clf, l_featInd = findBestFeatCombinationLearner(na_train, na_class, lambda : KNeighborsClassifier(n_neighbors = 5))
    return clf.predict(na_data[:, l_featInd])

def adaBoostBestFeatCombinationLearner(na_train, na_class, na_data):
    clf, l_featInd = findBestFeatCombinationLearner(na_train, na_class, lambda : AdaBoostClassifier(n_estimators=20))
    return clf.predict(na_data[:, l_featInd])
    
def svmBestFeatCombinationLearner(na_train, na_class, na_data):
    clf, l_featInd = findBestFeatCombinationLearner(na_train, na_class, lambda : svm.SVC())
    clf = svm.SVC()
    clf.fit(na_train[:, l_featInd], na_class)
    return clf.predict(na_data[:, l_featInd])

def findBestFeatCombinationLearner(na_train, na_class, fc_learnerFactory):
    return bsetools.getBestFeaturesCombinationForwardSearch(na_train, na_class, fc_learnerFactory)

if __name__ == '__main__':
    i_forwardlook = 1
    i_lookback = 26
    lsSym = np.array(['3JR'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2012,2,18)
    dtEnd = dt.datetime(2013,2,17)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      
    lsKeys = ['open', 'high', 'low', 'close', 'volume']

    #get train data
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd)
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=False )
    
    dData = dict(zip(lsKeys, ldfData))
    
    
    lfc_TestFeatures = (featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featAroonDown, featVolumeDelta, featStochastic, featVolume, featBollinger)
    
    #default parameters
    ld_FeatureParameters = {}
    for fc_feat in lfc_TestFeatures:
        ld_FeatureParameters[fc_feat] = {}
        
    lfc_TestFeatures, ld_FeatureParameters = bsefeats.get_feats()
    ld_FeatureParameters[featTrend] = {'lForwardlook':i_forwardlook}

    t1 = datetime.now()
    
    testLearner(dData, lfc_TestFeatures, featTrend, ld_FeatureParameters, svmBestFeatCombinationLearner, i_lookback = i_lookback, i_trainPeriod = 60, i_forwardlook = i_forwardlook)
    t2 = datetime.now()
    tdelta = t2 - t1
    print str(tdelta) + " seconds"






