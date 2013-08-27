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

def findBestFeaturesSetAmongCombinationsSet (d_dfData, lfc_featCombinationSet, t_fcTestFeatures, fc_ClassificationFeature, ld_FeatureParameters, b_Plot = False):
    maxSuccess = -1
    combinations = 0

    l_fcFeatures = list(t_fcTestFeatures)
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
    for lfc_combination in lfc_featCombinationSet:
        na_trainData = np.empty((na_TrainSet.shape[0], 0))
        na_valData = np.empty((na_ValSet.shape[0], 0))
        na_testData = np.empty((na_TestSet.shape[0], 0))
        for fcFeat in lfc_combination:
            i_featIndex = l_fcFeatures.index(fcFeat)
            na_trainData = np.hstack((na_trainData, na_TrainSet[:, i_featIndex].reshape(na_TrainSet[:, i_featIndex].size, 1)))
            na_valData = np.hstack((na_valData, na_ValSet[:, i_featIndex].reshape(na_ValSet[:, i_featIndex].size, 1)))
            na_testData = np.hstack((na_testData, na_TestSet[:, i_featIndex].reshape(na_TestSet[:, i_featIndex].size, 1)))
        
        clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=8, gamma=0.0, kernel='poly', probability=False, shrinking=True, tol=0.001, verbose=False)
        clf.fit(na_trainData, na_TrainClass) 
        na_Prediction = clf.predict(na_testData)
        testSuccess = float(na_TestClass.size - np.count_nonzero(na_TestClass - na_Prediction))/float(na_TestClass.size)
        na_Prediction = clf.predict(na_valData)
        success = float(na_ValClass.size - np.count_nonzero(na_ValClass - na_Prediction))/float(na_ValClass.size)
        
        #k, success, i_TruePositives, i_FakePositives, i_FakeNegatives, i_TrueNegatives = executeQuery( naTrain, naTest, bClassification = True, lkRange=l_K )
    
        if success > maxSuccess:
            maxSuccess = success
            maxClf = clf
            l_maxFeatSet = list()
            for feat in lfc_combination:
                l_maxFeatSet.append(feat.func_name)
            l_maxFeatSet.sort()
            print "CV: " + str(success) + " Test:" + str(testSuccess) + " combination: " + str(l_maxFeatSet)
            if b_Plot == True:
                plt.clf()
                for i in range(0, na_TrainClass.shape[0]):
                    if na_TrainClass[i] == 1:
                        plt.plot( na_trainData[i][0], na_trainData[i][1], 'g+' )
                    elif na_TrainClass[i] == -1:
                        plt.plot( na_trainData[i][0], na_trainData[i][1], 'ro' )
                    elif na_TrainClass[i] == 0:
                        plt.plot( na_trainData[i][0], na_trainData[i][1], 'bo' )
                    else:
                        plt.plot( na_trainData[i][0], na_trainData[i][1], 'kx' )
                #plt.legend( ('Trend') )
                plt.ylabel(lfc_combination[0].func_name)
                plt.xlabel(lfc_combination[1].func_name)
                plt.show()            
        elif success == maxSuccess:
            l_feat = list()
            for feat in lfc_combination:
                l_feat.append(feat.func_name)
            l_feat.sort()
            print "CV: " + str(success) + " Test:" + str(testSuccess) + " combination: " + str(l_feat)
             

        combinations += 1
        
    print str(combinations) + " combinations tested"
    return l_maxFeatSet, maxSuccess





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
    ld_FeatureParameters = {}
    for feat in lfc_TestFeatures:
        ld_FeatureParameters[feat] = {}
    ld_FeatureParameters[featTrend] = {'lForwardlook':1}
#    ldArgs = [ {'lLookback':30, 'bRel':True},\
#               {},\
#               {}]             
         

    t1 = datetime.now()
    findBestFeaturesSetAmongCombinationsSet(dData, bsetools.getAllFeaturesCombinationsList(lfc_TestFeatures), lfc_TestFeatures, featTrend, ld_FeatureParameters)
    #findBestFeaturesSetAmongCombinationsSet(dData, itertools.combinations(lfc_TestFeatures, 4), lfc_TestFeatures, featTrend, ld_FeatureParameters, b_Plot = False)
    t2 = datetime.now()
    tdelta = t2 - t1
    print "findBestFeaturesSetAmongCombinationsSet " + str(tdelta) + " seconds"
    #todo test data to be chosen randomly
    #feature normalization to be optimized






