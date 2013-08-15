'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on Nov 7, 2011

@author: John Cornwell
@contact: JohnWCornwellV@gmail.com
@summary: File containing a simple test of the feature engine.
'''

''' Python imports '''
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


def executeQuery( naTrain, naTest, bClassification, lkRange=range(1,101,10), bPlot=False ):
    ''' 
    @summary: Takes testing and training data and computes average error over the test set
              This is compared to a baseline guess which is just the average of the training set
    '''
    
    lfRes = []
    for lK in lkRange:
        if lK > len(naTrain[:,0]):
            #print "no enough data " + str(len(naTrain[:,0])) + " " + str(lK) 
            continue            
            
        if bClassification:
            cLearn = myknn.myknn( k=lK, method='majority', leafsize=100)
        else:
            cLearn = myknn.myknn( k=lK, method='mean', leafsize=100)
    
        cLearn.addEvidence( naTrain )

        fError = 0.0
        naResult = cLearn.query( naTest[:,:-1] )
        if bClassification:
            i_precision = 0
            i_recall = 0
            i_TruePositives = 0
            i_FakePositives = 0
            i_FakeNegatives = 0
            i_TrueNegatives = 0
            for i,res in enumerate(naResult):
                if naResult[i] == 1 and naTest[i,-1] == naResult[i]:
                    i_TruePositives += 1
                elif naResult[i] == 1 and naTest[i,-1] != naResult[i]:
                    i_FakePositives += 1
                elif naResult[i] == -1 and naTest[i,-1] != naResult[i]:
                    i_FakeNegatives += 1
                elif naResult[i] == -1 and naTest[i,-1] == naResult[i]:
                    i_TrueNegatives += 1
            delta = naResult - naTest[:,-1]
            zeros_count = 0
            for dd in delta:
                if dd == 0: zeros_count += 1
            lError = float(zeros_count / float(naTest.shape[0]))
            lfRes.append((lK, lError, i_TruePositives, i_FakePositives, i_FakeNegatives, i_TrueNegatives))
        else:
            naError = abs( naResult - naTest[:,-1] )
            lfRes.append( (lK, np.average(naError)) )
        
    res_arr = np.array(lfRes)
    result = res_arr[np.argmax(res_arr[:,1])]
    
#    if naTrain.shape[1] > 2:
#        bPlot = True
    if bPlot:
        plt.clf()
        plt.plot( lkRange, res_arr[:,1] )
        if bClassification:
            plt.legend( ('Average Prediction success ')) 
            plt.ylabel('Success')
        else:
            plt.legend( ('Average Error Predict') )
            plt.ylabel('Error')
        plt.xlabel('K value')
        plt.show()
    return result[0], result[1], result[2], result[3], result[4], result[5]
    
def calculateFeatures(d_dfData, s_symbol, lfcFeatures, d_FeatureParameters):
    ldfRet = dict()
    for i, fcFeature in enumerate(lfcFeatures):
        ldFeatureData = fcFeature( d_dfData, **d_FeatureParameters[fcFeature] )
    
        ldfRet[fcFeature] = ldFeatureData[s_symbol].values
    d_dataWithoutNans = bsetools.removeNansInDict(ldfRet)
    return d_dataWithoutNans

def testFeaturesSet(ldFeaturesDict, dLeadDataColumn, lfcFeatures, l_K):
    ''' Pick Test and Training Points '''
    lDataLength = ldFeaturesDict[lfcFeatures[0]].shape[0] 
    lSplit = int(lDataLength * 0.7)
     
    ''' Stack all information into one Numpy array '''
    naFeatTrain = np.empty((lSplit, 0))
    naFeatTest =  np.empty((lDataLength - lSplit, 0))
    for i, fcFunc in enumerate(lfcFeatures):
        dFeatData = ldFeaturesDict[fcFunc];
        dTrainData = dFeatData[0: lSplit]
        dTrainData = dTrainData.reshape((lSplit, 1))
        dTestData = dFeatData[lSplit:]
        dTestData = dTestData.reshape((lDataLength - lSplit, 1))
        naFeatTrain = np.hstack((naFeatTrain, dTrainData))
        naFeatTest = np.hstack((naFeatTest, dTestData))

    bPlot = False
    
    if bPlot:
        ''' Plot feature for XOM '''
        for i, fcFunc in enumerate(lfcFeatures[:]):
            plt.clf()
            plt.subplot(211)
            plt.title( fcFunc.__name__ )
            timestamps = ldFeaturesDict[dLeadDataColumn].index
            datavalues = ldFeaturesDict[dLeadDataColumn].values
            plt.plot( timestamps, datavalues, 'r-' )
            plt.subplot(212)
            plt.plot( timestamps, ldFeaturesDict[fcFunc], 'g-' )
            plt.show()
    
    ''' Normalize features, use same normalization factors for testing data as training data '''
    ltWeights = ftu.normFeatures( naFeatTrain, -1.0, 1.0, False )
    ''' Normalize query points with same weights that come from test data '''
    ftu.normQuery( naFeatTest[:,:-1], ltWeights )

    return executeQuery( naFeatTrain, naFeatTest, bClassification = True, lkRange = l_K )



def findBestFeaturesSetAmongCombinationsSet (d_dfData, lfc_featCombinationSet, l_fcTestFeatures, fc_ClassificationFeature, d_FeatureParameters, l_K, b_Plot = False):
    maxSuccess = -1
    maxK = 0
    combinations = 0

    l_fcTestFeatures = list(l_fcTestFeatures)
    l_fcTestFeatures.append(fc_ClassificationFeature)
    d_featuresData = calculateFeatures(d_dfData, 'SOFIX', l_fcTestFeatures, d_FeatureParameters)
    np_dataHistogram = np.histogram(d_featuresData[fc_ClassificationFeature], 3)
    print "All Data Histogram: " + str(np_dataHistogram) 

    lSplit = d_featuresData[fc_ClassificationFeature].shape[0] 
    lSplit = int(lSplit * 0.7)
    
    print "Test Data Histogram: " + str(np.histogram(d_featuresData[fc_ClassificationFeature][lSplit:], 3)) 

    for featCombination in lfc_featCombinationSet:
        featCombination = list(featCombination)
        featCombination.append(fc_ClassificationFeature)
        k, success, i_TruePositives, i_FakePositives, i_FakeNegatives, i_TrueNegatives = testFeaturesSet(d_featuresData, 'close', featCombination, l_K = l_K)
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
                
            if b_Plot == True:
                plt.clf()
                for i in range(d_featuresData[fc_ClassificationFeature].shape[0]):
                    if d_featuresData[fc_ClassificationFeature][i] == 1:
                        plt.plot( d_featuresData[featCombination[0]][i], d_featuresData[featCombination[1]][i], 'go' )
                    elif d_featuresData[fc_ClassificationFeature][i] == -1:
                        plt.plot( d_featuresData[featCombination[0]][i], d_featuresData[featCombination[1]][i], 'ro' )
                    elif d_featuresData[fc_ClassificationFeature][i] == 0:
                        plt.plot( d_featuresData[featCombination[0]][i], d_featuresData[featCombination[1]][i], 'bo' )
                    else:
                        plt.plot( d_featuresData[featCombination[0]][i], d_featuresData[featCombination[1]][i], 'bo' )
                plt.legend( ('Trend') )
                plt.ylabel(featCombination[0].func_name)
                plt.xlabel(featCombination[1].func_name)
                plt.show()            
            
            
        combinations += 1
    print str(combinations) + " tested"
    return maxFeat, maxK, maxSuccess
    
    
def findBestFeaturesSetByIteration (dData, lfc_TestFeatures, lfcClassFeature, ldArgs, lkRange):
    lfcMaxFeaturesList = list()
    maxKK = 0
    maxSSuccess = -1
    lfcMaxFeaturesList.append(lfcClassFeature)
    ldFeaturesDict = calculateFeatures(dData, 'close', lfc_TestFeatures, ldArgs)
    ''' Imported functions from qstkfeat.features, NOTE: last function is classification '''
    while len(lfc_TestFeatures) > 1:
        maxSuccess = -1
        maxK = 0
        for lfcCurrentFeat in lfc_TestFeatures:
            if lfcCurrentFeat == lfcClassFeature: continue
            lfcFeatures2Test = list(lfcMaxFeaturesList)
            lfcFeatures2Test.insert(0, lfcCurrentFeat)
            ''' Default Arguments '''
            ldArgs = [{}] * len(lfcFeatures2Test) 
            
            k, success = testFeaturesSet(ldFeaturesDict, 'close', lfcFeatures2Test, lkRange = lkRange)
            if success > maxSuccess:
                maxSuccess = success
                maxK = k
                maxFeat = lfcCurrentFeat
        
        lfcMaxFeaturesList.insert(0, maxFeat)
        lfc_TestFeatures.remove(maxFeat)
        k, success = testFeaturesSet(ldFeaturesDict, 'close', lfcMaxFeaturesList, lkRange = lkRange)
        if success < maxSSuccess or success == maxSSuccess:
            lfcMaxFeaturesList.remove(maxFeat)
        elif success > maxSSuccess:
            maxSSuccess = success
            maxK = k
            print "best combination so far: " + str(lfcMaxFeaturesList) + " k: " + str(k) + " success: " + str(success)
    
    return lfcMaxFeaturesList, maxK, maxSSuccess
    
if __name__ == '__main__':
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
    #, featBeta, featCorrelation
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
         
#    t1 = datetime.now()
#    featList, k, successRate = findBestFeaturesSetByIteration(dData, list(lfc_TestFeatures), featTrend, d_FeatureParameters, lkRange = range(31, 32, 1))
#    t2 = datetime.now()
#    tdelta = t2 - t1
#    print "findBestFeaturesSetByIteration " + str(tdelta) + " seconds"
    
    t1 = datetime.now()
    #featList, k, successRate = findBestFeaturesSetAmongCombinationsSet(dData, bsetools.getAllFeaturesCombinationsList(lfc_TestFeatures), lfc_TestFeatures, featTrend, d_FeatureParameters, lkRange = range(30, 31, 1))
    featList, k, successRate = findBestFeaturesSetAmongCombinationsSet(dData, itertools.combinations(lfc_TestFeatures, 4), lfc_TestFeatures, featTrend, d_FeatureParameters, l_K = range(2, 52, 1))
    t2 = datetime.now()
    tdelta = t2 - t1
    print "findBestFeaturesSetAmongCombinationsSet " + str(tdelta) + " seconds"
    #todo test data to be chosen randomly
    #feature normalization to be optimized
