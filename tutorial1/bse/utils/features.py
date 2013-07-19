'''
Created on Jun 25, 2013

@author: I028663
'''

# ''' 3rd Party Imports '''
import pandas as pand
import numpy as np
import datetime as dt

# ''' QSTK Imports '''
import qstkutil.tsutil as tsu


def featReturn0(dData, b_human=False):
    dfPrice = dData['close'].copy()
    
    # Calculate Returns
    tsu.returnize0(dfPrice.values)
    
    return dfPrice

def featTrend(dData, lForwardlook=2, b_human=False):
    dfPrice = dData['close']
    
    trds = np.array(map(trends, (dfPrice.values[lForwardlook:, :] - dfPrice.values[0:-lForwardlook, :])))
    trds = np.reshape(trds, (trds.shape[0], dfPrice.values.shape[1]))
    trds1 = np.empty((lForwardlook, dfPrice.values.shape[1]))
    trds1[0:lForwardlook,:] = np.nan
    
    trds2 = np.vstack((trds1, trds))
    
    dfRet = pand.DataFrame(index=dfPrice.index, columns=dfPrice.columns, data=trds2)
    
    return dfRet

def trends(ret):
    if ret > 0:
        return 1
    elif ret == 0:
        return 0
    else:
        return -1
