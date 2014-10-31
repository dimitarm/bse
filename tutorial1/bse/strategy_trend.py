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



import utils.dateutil as bsedateutil
import utils.features.feats as bsefeats
import bse.utils.reader.data as bsereader

from utils.classes import *
import utils.tools as bsetools
from sklearn import preprocessing
from sklearn import svm
from sklearn import decomposition
from sklearn.utils import assert_all_finite
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier


def print_full(data):
    for row in range(0, data.shape[0]):
        for col in range(data.shape[1]):
            sys.stdout.write(str(data[row, col]) + " ")
        sys.stdout.write("\r\n")

def testLearner(d_dfData, s_symbol, d_dfFeatures, d_dfClass, b_scaling, b_pca, fc_learnerFactory, i_trainPeriod, b_Plot = False):
    print s_symbol
    t1 = datetime.now()
    
    df_data = d_dfFeatures[s_symbol]
    df_classData = d_dfClass[s_symbol]
    #test each combination
    success = float(0)
    success_up = float(0)
    success_down = float(0)
    
    count = 0
    #all_count = na_data.shape[0] - i_forwardlook + 1 - i_trainPeriod
    for i in range(i_trainPeriod, df_data.index.size - i_forwardlook + 1):
        day = df_data.index[i]
        na_data = df_data.iloc[i - i_trainPeriod:i].values
        y_train = df_classData.iloc[i - i_trainPeriod:i].values.ravel()
        x_predict = df_data.iloc[i].values
        try:
            assert_all_finite(na_data)
            assert_all_finite(y_train)
            assert_all_finite(x_predict)
        except ValueError:
            continue
        if b_scaling == True:
            scaler = preprocessing.StandardScaler().fit(na_data)
            x_train = scaler.transform(na_data)
        else:
            x_train = na_data
        
        
        if b_pca == True:
            pca = decomposition.PCA(n_components = 40)
            pca.fit(x_train)
            x_train = pca.transform(x_train)
            x_predict = pca.transform(x_predict)
        
        i_prediction = fc_learnerFactory(x_train, y_train, x_predict)
        if (i_prediction == df_classData.iloc[i][0]):
            success += 1
            if (i_prediction == 1):
                success_up += 1
            else:
                success_down += 1
        count += 1
        #sys.stdout.write(str(all_count - count) + " to go\r")
    if count == 0:
        print "no prediction"
    else:
        print "success rate: " + str(success/count) + " up: " + str(success_up/count) + " down: " + str(success_down/count) + " count: " + str(count)

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
    return clf.predict(na_data[l_featInd])

def adaBoostBestFeatCombinationLearner(na_train, na_class, na_data):
    clf, l_featInd = findBestFeatCombinationLearner(na_train, na_class, lambda : AdaBoostClassifier(n_estimators=20))
    clf = AdaBoostClassifier(n_estimators=20)
    clf.fit(na_train[:, l_featInd], na_class)
    return clf.predict(na_data[l_featInd])
    
def svmBestFeatCombinationLearner(na_train, na_class, na_data):
    clf, l_featInd = findBestFeatCombinationLearner(na_train, na_class, lambda : svm.SVC())
    clf = svm.SVC()
    clf.fit(na_train[:, l_featInd], na_class)
    return clf.predict(na_data[l_featInd])

def findBestFeatCombinationLearner(na_train, na_class, fc_learnerFactory):
    return bsetools.getBestFeaturesCombinationForwardSearch(na_train, na_class, fc_learnerFactory)

if __name__ == '__main__':
    i_forwardlook = 5
    lsSym = np.array(['3JR', '4CF', '6A6', '6C4', 'E4A', 'SOFIX'])
    
    ''' Get data '''
    dtEnd = dt.datetime(2014,9,23). replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    dtStart = dtEnd - dt.timedelta(days = 365*2)
    lsKeys = ['open', 'high', 'low', 'close', 'volumes']

    #get train data
    dPrices = bsereader.get_data(dtStart, dtEnd, lsSym)

    lfc_TestFeatures = bsefeats.get_feats()

    t1 = datetime.now()

    #calculate features
    ldfFeatures = bsetools.calculateFeatures(dPrices, lfc_TestFeatures, {})
    print "features calculated in {0} seconds".format(datetime.now() - t1)
    ddfFeatures = bsetools.extractSymbolFeatures(ldfFeatures)
    #calculate class
    fcClassificationFeature = lambda (dFullData): featTrend(dFullData, lForwardlook = i_forwardlook), 
    ldfClass = bsetools.calculateFeatures(dPrices, (fcClassificationFeature), {})
    ddfClass = bsetools.extractSymbolFeatures(ldfClass) 
    
    for symbol in lsSym:
        testLearner(
                    dPrices, 
                    symbol, 
                    ddfFeatures, 
                    ddfClass, 
                    False,   #scaling
                    False,  #pca
                    adaBoostLearner, 
                    i_trainPeriod = 60)
    t2 = datetime.now()
    tdelta = t2 - t1
    print str(tdelta) + " seconds"






