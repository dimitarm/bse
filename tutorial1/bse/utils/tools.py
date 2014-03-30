'''
Created on Jun 28, 2013

@author: I028663
'''
import math
import numpy as np
import QSTK.qstkutil.tsutil as tsutil
from sklearn import cross_validation
from sklearn import metrics
import pandas as pand 

def getAllFeaturesCombinationsList(l_items):
    ll_retItems = list()
    for i in range(1, 2 ** len(l_items)):
        l_curListItems = list()
        num = bin(i)
        num = list(num)
        num = num[2:]
        num.reverse()
        for n in range(0, len(num)):
            if num[n] <> '0':
                l_curListItems.append(l_items[n])
        ll_retItems.append(l_curListItems)
    return ll_retItems

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

def removeNansInDict(d_Data, sDelNan='ALL', bShowRemoved=False):
    i_linesWithNan = list()
    d_resultData = dict()
    for arr in d_Data.itervalues():
        for y in range(arr.shape[0]):
            if np.any(np.isnan(arr[y])):
                i_linesWithNan.append(y)
    i_linesWithNan = list(set(i_linesWithNan)) #remove duplicate values
    i_linesWithNan.sort() 
    for key,arr in d_Data.iteritems():
        i_removedLines = 0
        for idx in i_linesWithNan:
            arr = np.delete(arr, idx - i_removedLines, 0)
            i_removedLines += 1
        d_resultData[key] = arr
    return d_resultData

def calculateFeatures(d_dfData, s_symbol, lfc_Features, ld_FeatureParameters):
    """
    @summary: calculates features and removes all NANs
    """
    ldfRet = dict()
    for i, fcFeature in enumerate(lfc_Features):
        ldFeatureData = fcFeature( d_dfData, **ld_FeatureParameters[fcFeature] )
    
        ldfRet[fcFeature] = ldFeatureData[s_symbol].values
    dna_dataWithoutNans = removeNansInDict(ldfRet)
    return dna_dataWithoutNans

def calculateSymbolFeatures(d_dfData, symbol, lfc_Features, ld_FeatureParameters):
    """
    @summary: Calculate features only for a given symbol preserving NANs
    """
    dFullData= {}
    for serie in d_dfData.iterkeys():
        dFullData[serie] = pand.DataFrame({symbol:d_dfData[serie][symbol]}) 
    
    na_features = np.empty((0, 0))
    for feat_ind in range(0, len(lfc_Features)):
        ldFeatureData = lfc_Features[feat_ind]( dFullData, **ld_FeatureParameters[lfc_Features[feat_ind]] )
        naShapedData = ldFeatureData[symbol].values.reshape(ldFeatureData[symbol].values.size, 1)
        if na_features.shape == (0,0):
            na_features = naShapedData
        else:
            na_features =  np.hstack((na_features, naShapedData))
    #na_dataWithoutNans = removeNans(na_features)
    #return na_dataWithoutNans
    return na_features

def calculateFeaturesNA(d_dfData, s_symbol, lfc_Features, ld_FeatureParameters):
    """
    @summary: Calculate features preserving NANs
    """
    
    na_features = np.empty((0, 0))
    for feat_ind in range(0, len(lfc_Features)):
        ldFeatureData = lfc_Features[feat_ind]( d_dfData, **ld_FeatureParameters[lfc_Features[feat_ind]] )
        naShapedData = ldFeatureData[s_symbol].values.reshape(ldFeatureData[s_symbol].values.size, 1)
        if na_features.shape == (0,0):
            na_features = naShapedData
        else:
            na_features =  np.hstack((na_features, naShapedData))
    #na_dataWithoutNans = removeNans(na_features)
    #return na_dataWithoutNans
    return na_features

def getFeaturesCombination(na_featData, l_featCombination):
    na_data = np.empty((na_featData.shape[0], 0))
    #stack feat data from combination
    for i_featIndex in l_featCombination:
        na_data = np.hstack((na_data, na_featData[:, i_featIndex].reshape(na_featData.shape[0], 1)))
    return na_data
    
def getBestFeaturesCombinationBruteSearch(na_featData, na_class, l_featCombinations, fc_learnerFactory):
    i_bestResult = -1
    for l_featCombination in l_featCombinations:
        na_TrainSet = getFeaturesCombination(na_featData, l_featCombination)
        #stack feat data and class
        na_TrainSet = np.hstack((na_TrainSet, na_class))
        na_TrainSet, na_TestSet = cross_validation.train_test_split(na_TrainSet, test_size=0.3, random_state=1)

        na_TrainClass = na_TrainSet[:,-1]
        na_TrainSet = na_TrainSet[:,:-1]
    
        na_TestClass = na_TestSet[:,-1]
        na_TestSet = na_TestSet[:,:-1]

        clf = fc_learnerFactory()
        clf.fit(na_TrainSet, na_TrainClass)
        #make prediction
        na_Prediction = clf.predict(na_TestSet)
        #calculate result
        success = metrics.metrics.accuracy_score(na_TestClass, na_Prediction)
        #check result with best so far
        if success > i_bestResult:
            i_bestResult = success
            clf_bestCLF = clf
            l_bestFeatCombination = l_featCombination
    #print "best success: " + str(i_bestResult)
    return clf_bestCLF, l_bestFeatCombination

def getBestFeaturesCombinationForwardSearch(na_featData, na_class, fc_learnerFactory):
    i_BestResult = -1
    l_featBestSet = list()
    l_untestedFeats = range(0, na_featData.shape[1])
    for ll in range(0, na_featData.shape[1]):
        i_bestIntResult = -1
        #iterate over all untested features
        for i_curFeat in l_untestedFeats:
            #initialize with best feat combination so far
            l_curFeatSet = list(l_featBestSet)
            #append current feature index
            l_curFeatSet.append(i_curFeat)
            #get features
            na_TrainSet = getFeaturesCombination(na_featData, l_curFeatSet)
            #test again feature set
            na_TrainSet = np.hstack((na_TrainSet, na_class.reshape(na_class.shape[0], 1)))
            na_TrainClass = na_TrainSet[:,-1]
            na_TrainSet = na_TrainSet[:,:-1]
            #fit learner
            clf = fc_learnerFactory()
            #calculate success ratio
            scores = cross_validation.cross_val_score(clf, na_TrainSet, na_TrainClass, cv=3)
            success = scores.mean()
            #check if we've got better temp result 
            if success > i_bestIntResult:
                i_bestIntResult = success
                i_bestFeatIndex = i_curFeat
                clf_bestIntCLF = clf
        if i_bestIntResult > i_BestResult:
            i_BestResult = i_bestIntResult
            l_featBestSet.append(i_bestFeatIndex)
            l_untestedFeats.remove(i_bestFeatIndex)
            clf_bestCLF = clf_bestIntCLF
        else:
            break    
    #print "success: " + str(i_bestIntResult) + " " + str(l_featBestSet)
    return clf_bestCLF, l_featBestSet
        
        
        