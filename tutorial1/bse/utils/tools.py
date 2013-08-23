'''
Created on Jun 28, 2013

@author: I028663
'''
import math
import numpy as np

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
    ldfRet = dict()
    for i, fcFeature in enumerate(lfc_Features):
        ldFeatureData = fcFeature( d_dfData, **ld_FeatureParameters[fcFeature] )
    
        ldfRet[fcFeature] = ldFeatureData[s_symbol].values
    dna_dataWithoutNans = removeNansInDict(ldfRet)
    return dna_dataWithoutNans

def calculateFeaturesNA(d_dfData, s_symbol, lfc_Features, ld_FeatureParameters):
    na_features = np.empty((0, 0))
    for i, fcFeature in enumerate(lfc_Features):
        ldFeatureData = fcFeature( d_dfData, **ld_FeatureParameters[fcFeature] )
    
        na_features.hstack(ldFeatureData[s_symbol].values)
    na_dataWithoutNans = removeNans(na_features)
    return na_dataWithoutNans

def getTrainTestValidationSets(na_data, fc_func):
    na_TrainSet = np.empty((0, na_data.shape[1]))
    na_ValidationSet = np.empty((0, na_data.shape[1]))
    na_TestSet = np.empty((0, na_data.shape[1]))
    
    for i in range(0, na_data.shape[0]):
        vote = fc_func(i, na_data)
        if vote == 0:
            na_TrainSet = np.vstack((na_TrainSet, na_data[i,:]))
        elif vote == 1:
            na_ValidationSet = np.vstack((na_ValidationSet, na_data[i,:]))
        else:
            na_TestSet = np.vstack((na_TestSet, na_data[i,:]))
        
    return na_TrainSet, na_ValidationSet, na_TestSet


def defaultTrainTestValidationFunc(i_Index, na_Data):
    if i_Index < na_Data.shape[0]*0.6:
        return 0
    elif i_Index < na_Data.shape[0]*0.8:
        return 1
    else:
        return 2
    