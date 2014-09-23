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
    if method == 'normal':
        na_data = (np.random.randint(low = 5, high = 500000, size = (len(l_index), len(l_symbols))) * 0.99 ) / 10000
    else:
        na_data = np.empty((len(l_index), len(l_symbols)))
        for index in range(0, len(l_index)):
            y = math.sin( float(index) * 62.83/len(l_index) )
            for col in range(0, len(l_symbols)):
                na_data[index][col] = y
    for key in l_keys:
        dFullData[key] = pand.DataFrame( index=l_index, columns=l_symbols, data=na_data )
    return dFullData
    
def get_highest_lookback(na_data):
    l_lookbacks = []
    for col in range(na_data.shape[1]):
        i_firstNan = -1
        for row in range(0, na_data.shape[0]):
            if math.isnan(na_data[row, col]):
                i_firstNan = row + 1    
            else:
                break
        l_lookbacks.append(i_firstNan)
    return np.array(l_lookbacks, copy = False)

def fillforward(df):
    """
    @summary Removes NaNs from a 2D array by scanning forward in the 
    1st dimension.  If a cell is NaN, the value above it is carried forward.
    @param df: dataframe to fill forward
    @return the dataframe is revised in place
    """
    for col in df:
        first = True
        for row in df[col].index:
            if first == True:
                last_value = df.at[row, col]
            else:
                if math.isnan(df.at[row, col]):
                    df.at[row, col] = last_value
                last_value = df.at[row, col]
            first = False

def fillbackward(df):
    """
    @summary Removes NaNs from a 2D array by scanning backward in the 
    1st dimension.  If a cell is NaN, the value above it is carried backward.
    @param nds: the array to fill backward
    @return the array is revised in place
    """
    for col in df:
        first = True
        rows = []
        for row in df[col].index:
            rows.append(row)
        rows.reverse()
        for row in rows:
            if first == True:
                last_value = df.at[row, col]
            else:
                if math.isnan(df.at[row, col]):
                    df.at[row, col] = last_value
                last_value = df.at[row, col]
            first = False


def prepare_data_for_prediction(dFullData):
    '''
    @summary prepares data for prediction. Replaces nans by filling forward and then filling backward values.
    '''
    for key in dFullData.iterkeys():
        # fill forward
        fillforward(dFullData[key])
        # fill backward
        fillbackward(dFullData[key])

def is_data_correct(data):
    for col in range(data.shape[1]):
        for row in range(0, data.shape[0]):
            if math.isnan(data[row, col]) or math.isinf(data[row, col]):
                sys.stderr.write("col: " + str(col) + " row: " + str(row) + " : " + str(data[row, col]) + "\n")  
                return False
    return True   

if __name__ == '__main__':
    pass