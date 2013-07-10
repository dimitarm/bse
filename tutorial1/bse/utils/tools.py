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
    i_linesWithNan = list(set(i_linesWithNan))
    i_linesWithNan.sort() 
    for key,arr in d_Data.iteritems():
        i_removedLines = 0
        for idx in i_linesWithNan:
            arr = np.delete(arr, idx - i_removedLines, 0)
            i_removedLines += 1
        d_resultData[key] = arr
    for key, arr in d_resultData.iteritems():
        d_Data[key] = arr
    
