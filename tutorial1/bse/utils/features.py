'''
Created on Jun 25, 2013

@author: I028663
'''

# ''' 3rd Party Imports '''
import pandas as pand
import numpy as np
import datetime as dt
import math

# ''' QSTK Imports '''
import QSTK.qstkutil.tsutil as tsu


def featReturn0(dData, b_human=False):
    dfPrice = dData['close'].copy()
    
    # Calculate Returns
    tsu.returnize0(dfPrice.values)
    
    return dfPrice

def featTrend(dData, lForwardlook=2, b_human=False):
    dfPrice = dData['close']
    
    trds = np.array(map(trends, (dfPrice.values[lForwardlook:, :] - dfPrice.values[0:-lForwardlook, :])))
    nans = np.empty((lForwardlook, dfPrice.values.shape[1]))
    nans[0:lForwardlook,:] = np.nan
    
    trds2 = np.vstack((trds, nans))
    
    dfRet = pand.DataFrame(index=dfPrice.index, columns=dfPrice.columns, data=trds2)
    
    return dfRet

def trends(ret):
    na_res = np.array(ret)
    for pos, value in enumerate(na_res):
        if value > 0:
            na_res[pos] = 1
        elif value == 0:
            na_res[pos] = np.nan
        elif math.isnan(value):
            na_res[pos] = np.nan
        else:
            na_res[pos] = -1
    return na_res
