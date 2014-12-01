'''
Created on Sep 26, 2013

@author: I028663
'''
import numpy as np
import pandas as pand
import math
import sys
import QSTK.qstkutil.tsutil as tsutil

def get_random_data(l_keys, l_index, l_symbols, method = 'normal'):
    '''
    @summary returns random data
    @param l_keys: keys with series
    @param l_index: index to be used when creating series
    @param l_symbols: symbols to be create data for
    @param method: could be normal or anything else
    when normal data is generated as normal distribution if other data is generated using sinus function  
    
    
    @return dict with dataframes for each l_keys
    '''
    dFullData = {}
    for key in l_keys:
        if method == 'normal':
            na_data = np.random.rand(len(l_index), len(l_symbols)) * 100 + 5
        else:
            na_data = np.empty((len(l_index), len(l_symbols)))
            for index in range(0, len(l_index)):
                y = math.sin( float(index) * 62.83/len(l_index) )
                for col in range(0, len(l_symbols)):
                    na_data[index][col] = y
        dFullData[key] = pand.DataFrame( index=l_index, columns=l_symbols, data=na_data )
    return dFullData
    
def get_highest_lookback(data):
    if isinstance(data, pand.DataFrame):
        na_data = data.values
    else:
        na_data = data
    l_lookbacks = []
    if len(na_data.shape) == 1:
        i_firstNan = 0
        for row in range(0, na_data.shape[0]):
            if math.isnan(na_data[row]):
                i_firstNan = row + 1    
            else:
                break
        l_lookbacks.append(i_firstNan)
    else:
        for col in range(na_data.shape[1]):
            i_firstNan = 0
            for row in range(0, na_data.shape[0]):
                if math.isnan(na_data[row, col]):
                    i_firstNan = row + 1    
                else:
                    break
            l_lookbacks.append(i_firstNan)
    return np.array(l_lookbacks, copy = False)

def is_data_correct(data):
    for col in range(data.shape[1]):
        for row in range(0, data.shape[0]):
            if math.isnan(data[row, col]) or math.isinf(data[row, col]):
                sys.stderr.write("col: " + str(col) + " row: " + str(row) + " : " + str(data[row, col]) + "\n")  
                return False
    return True   

if __name__ == '__main__':
    pass