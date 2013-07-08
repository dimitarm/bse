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
    for arr in d_Data.itervalues():
        for y in range(0, arr.shape[0]):
            if np.any(np.isnan(arr[y])):
                i_linesWithNan.append(y)
    np_linesWithNan = np.array(i_linesWithNan)
    np_sortIndexes = np.argsort(np_linesWithNan) 
    i_removedLines = 0
    for idx in np_sortIndexes:
        for arr in d_Data.itervalues():
            np_arrWithoutNan = np.delete(arr, np_linesWithNan[idx] + i_removedLines, 0)
            arr = np_arrWithoutNan
        i_removedLines += 1
        