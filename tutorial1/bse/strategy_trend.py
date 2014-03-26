'''
Created on Oct 31, 2013

@author: dimitar
'''

import math
import datetime as dt
import itertools
import sys

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
import utils.bsedateutil as bsedateutil
import utils.data as datautil
import utils.features.feats as bsefeats

from utils.classes import *
from utils import tools as bsetools
import utils.tools as bsetools
import utils.data as bsedata
from sklearn import preprocessing
from sklearn import svm
from sklearn import metrics 
from sklearn import cross_validation
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier


def testLearner(d_dfData, s_symbol, t_fcTestFeatures, fc_ClassificationFeature, ld_FeatureParameters, fc_learnerFactory, i_trainPeriod, i_forwardlook, b_Plot = False):
    l_fcFeatures = list(t_fcTestFeatures)
    l_fcFeatures.append(fc_ClassificationFeature)

    for key in d_dfData.iterkeys():
        #fill forward
        tsutil.fillforward(d_dfData[key].values)
        #fillbackward
        tsutil.fillbackward(d_dfData[key].values)
        if np.isnan(d_dfData[key].values.min()):
            print "serious error"
            return

    t1 = datetime.now()
    na_data = bsetools.calculateFeaturesNA(d_dfData, s_symbol, l_fcFeatures, ld_FeatureParameters)
    #print "features calculated in " + str(datetime.now() - t1) + " seconds"
    
    #get lookbacks list without trend feature!
    na_lookbacks = bsedata.get_highest_lookback(na_data[:,:-1])
    #remove NaNs at beginning and at end of period
    na_data = na_data[na_lookbacks.max():-i_forwardlook,:]
    #check data for correctness
    for col in range(na_data.shape[1]):
        for row in range(0, na_data.shape[0]):
            if math.isnan(na_data[row, col]) or np.isinf(na_data[row, col]):
                print "nan in data " + s_symbol
                print "col: " + str(col) + " row: " + str(row) + " : " + str(na_data[row, col])
                return
    
    #test each combination
    success = float(0)
    success_up = float(0)
    success_down = float(0)
    scaler = preprocessing.StandardScaler().fit(na_data[:,:-1])
    
    na_mainData = scaler.transform(na_data[:,:-1])
    na_classData = na_data[:,-1]#.reshape(na_data.shape[0], 1)
    count = 0
    all_count = na_data.shape[0] - i_forwardlook + 1 - i_trainPeriod
    for i in range(i_trainPeriod, na_data.shape[0] - i_forwardlook + 1):
        i_prediction = fc_learnerFactory(na_mainData[i - i_trainPeriod:i,:], na_classData[i - i_trainPeriod:i], na_mainData[i,:])
        if (i_prediction == na_classData[i]):
            success += 1
            if (i_prediction == 1):
                success_up += 1
            else:
                success_down += 1
        count += 1
        #sys.stdout.write(str(all_count - count) + " to go\r")
    print s_symbol + " success rate: " + str(success/count) + " up: " + str(success_up/count) + " down: " + str(success_down/count)

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
    clf = AdaBoostClassifier(n_estimators=20)
    clf.fit(na_train[:, l_featInd], na_class)
    return clf.predict(na_data[:, l_featInd])
    
def svmBestFeatCombinationLearner(na_train, na_class, na_data):
    clf, l_featInd = findBestFeatCombinationLearner(na_train, na_class, lambda : svm.SVC())
    clf = svm.SVC()
    clf.fit(na_train[:, l_featInd], na_class)
    return clf.predict(na_data[:, l_featInd])

def findBestFeatCombinationLearner(na_train, na_class, fc_learnerFactory):
    return bsetools.getBestFeaturesCombinationForwardSearch(na_train, na_class, fc_learnerFactory)

if __name__ == '__main__':
    i_forwardlook = 5
    lsSym = np.array(['3JR', '4CF', '6A6', '6C4', 'E4A', 'SOFIX', 'T57'])
    #lsSym = np.array(['SOFIX'])
    
    ''' Get data '''
    dtEnd = dt.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    dtStart = dtEnd - dt.timedelta(days = 365)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      
    lsKeys = ['open', 'high', 'low', 'close', 'volume']

    #get train data
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16))
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=False )
    dData = dict(zip(lsKeys, ldfData))
    lfc_TestFeatures, ld_FeatureParameters = bsefeats.get_feats()
    #default parameters
    ld_FeatureParameters = {}
    for fc_feat in lfc_TestFeatures:
        ld_FeatureParameters[fc_feat] = {}
    ld_FeatureParameters[featTrend] = {'lForwardlook':i_forwardlook}

    t1 = datetime.now()
    
    for symbol in lsSym:
        testLearner(dData, symbol, lfc_TestFeatures, featTrend, ld_FeatureParameters, svmLearner, i_trainPeriod = 60, i_forwardlook = i_forwardlook)
    t2 = datetime.now()
    tdelta = t2 - t1
    print str(tdelta) + " seconds"






