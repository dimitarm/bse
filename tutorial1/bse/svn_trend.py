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
from qstkfeat.classes import class_fut_ret
import qstkfeat.featutil as ftu

import utils.dateutil as bsedateutil

from utils.features import *
import utils.tools as bsetools
import bse.myknn as myknn

from sklearn import svm



def findBestFeaturesSetAmongCombinationsSet (d_dfData, lfc_featCombinationSet, t_fcTestFeatures, fc_ClassificationFeature, ld_FeatureParameters, l_K, b_Plot = False):
    maxSuccess = -1
    maxK = 0
    combinations = 0

    l_fcTestFeatures = list(t_fcTestFeatures).append(fc_ClassificationFeature)
    na_featuresData = bsetools.calculateFeaturesNA(d_dfData, 'SOFIX', l_fcTestFeatures, ld_FeatureParameters)
    
    (na_TrainSet, na_ValSet, na_TestSet) = bsetools.getTrainTestValidationSets(na_featuresData, bsetools.defaultTrainTestValidationFunc)
    na_TrainClass = na_TrainSet[:,-1]
    na_TrainSet = na_TrainSet[:,:-1]

    na_ValClass = na_ValSet[:,-1]
    na_ValSet = na_ValSet[:,:-1]
    
    na_TestClass = na_TestSet[:,-1]
    na_TestSet = na_TestSet[:,:-1]

    
#    print "All Data Histogram: " + str(np.histogram(d_featuresData[fc_ClassificationFeature], 3)) 
#    print "Test Data Histogram: " + str(np.histogram(d_TestSet[fc_ClassificationFeature], 3)) 

    #test each combination
    for lfc_combination in lfc_featCombinationSet:
        na_trainData = np.empty((na_TrainSet.shape[0], 0))
        for fcFeat in lfc_combination:
            na_trainData = np.hstack((na_trainData, na_TrainSet[:, l_fcTestFeatures.index(fcFeat)]))
        
        clf = svm.SVC()
        clf.fit(na_trainData, na_TrainClass) 
        
        #k, success, i_TruePositives, i_FakePositives, i_FakeNegatives, i_TrueNegatives = executeQuery( naTrain, naTest, bClassification = True, lkRange=l_K )
        
        if success > maxSuccess:
            maxSuccess = success
            maxK = k
            maxFeat = list()
            for feat in featCombination:
                maxFeat.append(feat.func_name)
            maxFeat.remove(fc_ClassificationFeature.func_name)
            maxFeat.sort()
            i_precision = i_TruePositives/(i_TruePositives+i_FakePositives)
            i_recall = i_TruePositives/(i_TruePositives+i_FakeNegatives)
            i_f1score = 2*i_precision*i_recall/(i_precision + i_recall)
            print "best combination so far: " + str(maxFeat) + " k: " + str(k) + " success: " + str(success) + " precision: " + str(i_precision) + " recall: " + str(i_recall) + " f1score: " + str(i_f1score)
                
#            if b_Plot == True:
#                plt.clf()
#                for i in range(d_featuresData[fc_ClassificationFeature].shape[0]):
#                    if d_featuresData[fc_ClassificationFeature][i] == 1:
#                        plt.plot( d_featuresData[featCombination[0]][i], d_featuresData[featCombination[1]][i], 'go' )
#                    elif d_featuresData[fc_ClassificationFeature][i] == -1:
#                        plt.plot( d_featuresData[featCombination[0]][i], d_featuresData[featCombination[1]][i], 'ro' )
#                    elif d_featuresData[fc_ClassificationFeature][i] == 0:
#                        plt.plot( d_featuresData[featCombination[0]][i], d_featuresData[featCombination[1]][i], 'bo' )
#                    else:
#                        plt.plot( d_featuresData[featCombination[0]][i], d_featuresData[featCombination[1]][i], 'bo' )
#                plt.legend( ('Trend') )
#                plt.ylabel(featCombination[0].func_name)
#                plt.xlabel(featCombination[1].func_name)
#                plt.show()            
            
            
        combinations += 1
    print str(combinations) + " tested"
    return maxFeat, maxK, maxSuccess





if __name__ == '__main__':
    
    X = np.array([[0, 0], [1, 1]])
    y = [0, 1]
    clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
    gamma=0.0, kernel='rbf', probability=False, shrinking=True, tol=0.001,
    verbose=False)
    clf.fit(X, y)  
    print clf.predict([[2., 2.]])
    
    lsSym = np.array(['SOFIX', '3JR'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2010,1,1)
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
    #featList, k, successRate = findBestFeaturesSetAmongCombinationsSet(dData, bsetools.getAllFeaturesCombinationsList(lfc_TestFeatures), lfc_TestFeatures, featTrend, ld_FeatureParameters, l_K = range(2, 52, 1))
    featList, k, successRate = findBestFeaturesSetAmongCombinationsSet(dData, itertools.combinations(lfc_TestFeatures, 2), lfc_TestFeatures, featTrend, ld_FeatureParameters, l_K = range(2, 52, 1))
    t2 = datetime.now()
    tdelta = t2 - t1
    print "findBestFeaturesSetAmongCombinationsSet " + str(tdelta) + " seconds"
    #todo test data to be chosen randomly
    #feature normalization to be optimized






