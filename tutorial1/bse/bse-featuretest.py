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

''' 3rd party imports '''
import numpy as np
import pandas as pand
import matplotlib.pyplot as plt

''' QSTK imports '''
from qstkutil import DataAccess as da

from qstkfeat.features import *
from qstkfeat.classes import class_fut_ret
import qstkfeat.featutil as ftu

import utils.dateutil as bsedateutil

import myknn as myknn
from utils.features import *
from datetime import datetime
from datetime import timedelta

def testLearner( naTrain, naTest, bClassification, lkRange=range(1,101,10), bPlot=False ):
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
            delta = naResult - naTest[:,-1]
            zeros_count = 0
            for dd in delta:
                if dd == 0: zeros_count += 1
            lError = float(zeros_count / float(naTest.shape[0]))
            lfRes.append((lK, lError))
        else:
            naError = abs( naResult - naTest[:,-1] )
            lfRes.append( (lK, np.average(naError)) )
        
    res_arr = np.array(lfRes)
    result = res_arr[np.argmax(res_arr[:,1])]
    #print str(result[0]) + " " + str(result[1])
    
    if bPlot:
        plt.clf()
        plt.plot( llRange, res_arr[:,1] )
        if bClassification:
            plt.legend( ('Average Prediction success ')) 
            plt.ylabel('Success')
        else:
            plt.legend( ('Average Error Predict') )
            plt.ylabel('Error')
        plt.xlabel('K value')
        plt.show()
    return result[0], result[1]
    
def calculateFeatures(dData, dLeadDataColumn, lfcFeatures, ldArgs):
    ldfRet = dict()
    for i, fcFeature in enumerate(lfcFeatures):
        ldFeatureData = fcFeature( dData, **ldArgs[i] )
        diff = dData[dLeadDataColumn].values.shape[0] - ldFeatureData.values.shape[0]
        
        trds = np.empty((diff, 1))
        trds[0:diff,:] = np.nan
    
        trds2 = np.vstack((ldFeatureData.values, trds))
    
        ldfRet[fcFeature] = trds2 
    return ldfRet

def testFeatures(dData, dLeadDataColumn, lfcFeatures, ldArgs, lkRange):
    ldFeaturesDict = calculateFeatures(dData, dLeadDataColumn, lfcFeatures, ldArgs)
    
    bPlot = False
    if bPlot:
        ''' Plot feature for XOM '''
        for i, fcFunc in enumerate(lfcFeatures[:]):
            plt.clf()
            plt.subplot(211)
            plt.title( fcFunc.__name__ )
            timestamps = dData[dLeadDataColumn].index
            datavalues = dData[dLeadDataColumn].values
            plt.plot( timestamps, datavalues, 'r-' )
            plt.subplot(212)
            plt.plot( timestamps, ldFeaturesDict[fcFunc], 'g-' )
            plt.show()
     
    ''' Pick Test and Training Points '''
    lSplit = int(dData[dLeadDataColumn].shape[0] * 0.7)
     
    ''' Stack all information into one Numpy array '''
    naFeatTrain = np.empty((lSplit, 0))
    naFeatTest =  np.empty((dData[dLeadDataColumn].shape[0] - lSplit, 0))
    for i, fcFunc in enumerate(lfcFeatures[:]):
        dFeatData = ldFeaturesDict[fcFunc];
        dTrainData = dFeatData[0: lSplit,:]
        dTestData = dFeatData[lSplit:,:]
        naFeatTrain = np.hstack((naFeatTrain, dTrainData))
        naFeatTest = np.hstack((naFeatTest, dTestData))
        
    naFeatTrain = removeNans(naFeatTrain)     
    naFeatTest = removeNans(naFeatTest)
    ''' Normalize features, use same normalization factors for testing data as training data '''
    ltWeights = ftu.normFeatures( naFeatTrain, -1.0, 1.0, False )
    ''' Normalize query points with same weights that come from test data '''
    ftu.normQuery( naFeatTest[:,:-1], ltWeights )

    return testLearner( naFeatTrain, naFeatTest, bClassification = True, lkRange = lkRange )

def removeNans(naData, sDelNan='ALL', bShowRemoved=False):
    llValidRows = list()
    for i in range(naData.shape[0]):
        if 'ALL' == sDelNan and not math.isnan( np.sum(naData[i,:]) ) or\
              'FEAT' == sDelNan and not math.isnan( np.sum(naData[i,:-1]) ):
            llValidRows.append(i)
        elif  bShowRemoved:
            print 'Removed ', naData[i,:]
    naData = naData[llValidRows,:]
    return naData

def testFeatures_(dData, dummy, lfcFeatures, ldArgs, lkRange):
    ''' Generate a list of DataFrames, one for each feature, with the same index/column structure as price data '''
    ldfFeatures = ftu.applyFeatures( dData, lfcFeatures, ldArgs )
    
    bPlot = False
    if bPlot:
        ''' Plot feature for XOM '''
        for i, fcFunc in enumerate(lfcFeatures[:]):
            plt.clf()
            plt.subplot(211)
            plt.title( fcFunc.__name__ )
            timestamps = ldfData.index
            datavalues = ldfData['SOFIX'].values
            plt.plot( timestamps, datavalues, 'r-' )
            plt.subplot(212)
            plt.plot( ldfData.index, ldfFeatures[i]['SOFIX'].values, 'g-' )
            plt.show()
     
    ''' Pick Test and Training Points '''
    lSplit = int(len(ldtTimestamps) * 0.7)
    dtStartTrain = ldtTimestamps[0]
    dtEndTrain = ldtTimestamps[lSplit]
    dtStartTest = ldtTimestamps[lSplit+1]
    dtEndTest = ldtTimestamps[-1]
     
    ''' Stack all information into one Numpy array ''' 
    naFeatTrain = ftu.stackSyms( ldfFeatures, dtStartTrain, dtEndTrain )
    naFeatTest = ftu.stackSyms( ldfFeatures, dtStartTest, dtEndTest )
    
    ''' Normalize features, use same normalization factors for testing data as training data '''
    ltWeights = ftu.normFeatures( naFeatTrain, -1.0, 1.0, False )
    ''' Normalize query points with same weights that come from test data '''
    ftu.normQuery( naFeatTest[:,:-1], ltWeights )

    return testLearner( naFeatTrain, naFeatTest, bClassification = True, lkRange = lkRange )

def findBestFeaturesSetAmongAllCombinations (dData, lfcAllFeatures, lfcClassFeature, lkRange):
    featCombinationsList = range(1,2 ** len(lfcAllFeatures),1)
    maxSuccess = -1
    maxK = 0
    maxFeat = 0

    for featCombination in featCombinationsList:
        lfcFeaturesList = list()
        featFlag =  2 ** len(lfcAllFeatures) >> 1
        featPos = len(lfcAllFeatures)
        #add features
        while featFlag > 0:
            if featCombination & featFlag:
               lfcFeaturesList.append(lfcAllFeatures[featPos-1]) 
            featPos-=1
            featFlag = featFlag >> 1
            
        lfcFeaturesList.append(lfcClassFeature)
        ldArgs = [{}] * len(lfcFeaturesList)
        k, success = testFeatures(dData, 'close', lfcFeaturesList, ldArgs, lkRange = lkRange)
        if success > maxSuccess:
            maxSuccess = success
            maxK = k
            maxFeat = lfcFeaturesList
            print "best combination so far: " + str(maxFeat) + " k: " + str(k) + " success: " + str(success)
    return maxFeat, maxK, maxSuccess
    
    
def findBestFeaturesSet (dData, lfcAllFeatures, lfcClassFeature, lkRange):
    lfcMaxFeaturesList = list()
    maxKK = 0
    maxSSuccess = -1
    lfcMaxFeaturesList.append(lfcClassFeature)
    ''' Imported functions from qstkfeat.features, NOTE: last function is classification '''
    while len(lfcAllFeatures) > 0:
        maxSuccess = -1
        maxK = 0
        for lfcCurrentFeat in lfcAllFeatures:
            lfcFeatures2Test = list(lfcMaxFeaturesList)
            lfcFeatures2Test.insert(0, lfcCurrentFeat)
            ''' Default Arguments '''
            ldArgs = [{}] * len(lfcFeatures2Test) 
            
            k, success = testFeatures_(dData, 'close', lfcFeatures2Test, ldArgs, lkRange = lkRange)
            if success > maxSuccess:
                maxSuccess = success
                maxK = k
                maxFeat = lfcCurrentFeat
        
        lfcMaxFeaturesList.insert(0, maxFeat)
        lfcAllFeatures.remove(maxFeat)
        k, success = testFeatures_(dData, 'close', lfcMaxFeaturesList, ldArgs, lkRange = lkRange)
        if success < maxSSuccess or success == maxSSuccess:
            lfcMaxFeaturesList.remove(maxFeat)
        elif success > maxSSuccess:
            maxSSuccess = success
            maxK = k
            print "best combination so far: " + str(lfcMaxFeaturesList) + " k: " + str(k) + " success: " + str(success)
    
    return lfcMaxFeaturesList, maxK, maxSSuccess
    
if __name__ == '__main__':
    
    lsSym = np.array(['SOFIX'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2012,5,31)
    dtEnd = dt.datetime(2013,5,30)
    
    dataobj = da.DataAccess('Investor')      
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16) )
    
    lsKeys = ['open', 'high', 'low', 'close', 'volume']
    ldfData = dataobj.get_data( ldtTimestamps, lsSym, lsKeys, verbose=True )
    
    dData = dict(zip(lsKeys, ldfData))

    #, featBeta, featCorrelation
    #lfcAllFeatures = [featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featBollinger]
    lfcAllFeatures = [featMomentum, featHiLow, featMA, featEMA, featSTD, featRSI, featDrawDown, featRunUp, featAroon, featVolumeDelta, featStochastic, featVolume, featBollinger]
    t1 = datetime.now()
    featList, k, successRate = findBestFeaturesSet(dData, list(lfcAllFeatures), featTrend, lkRange = range(31, 32, 1))
    t2 = datetime.now()
    tdelta = t2 - t1
    print "findBestFeaturesSet(dData, lfcAllFeatures, featTrend, lkRange = range(31, 32, 1)) " + str(tdelta) + " seconds"
    
#    t1 = datetime.now()
#    featList, k, successRate = findBestFeaturesSetAmongAllCombinations(dData, lfcAllFeatures, featTrend, lkRange = range(31, 32, 1))
#    t2 = datetime.now()
#    tdelta = t2 - t1
#    print "findBestFeaturesSetAmongAllCombinations(dData, lfcAllFeatures, featTrend, lkRange = range(31, 32, 1)) " + str(tdelta) + " seconds"
