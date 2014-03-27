'''
Created on Sep 26, 2013

@author: I028663
'''
import numpy as np
import pandas as pand
import math

def get_random_data(l_keys, l_index, l_symbols, method = 'normal'):
    dData = {}
    if method == 'normal':
        na_data = (np.random.randint(low = 5, high = 500000, size = (len(l_index), len(l_symbols))) * 0.99 ) / 10000
    else:
        na_data = np.empty((len(l_index), len(l_symbols)))
        for index in range(0, len(l_index)):
            y = math.sin( float(index) * 62.83/len(l_index) )
            for col in range(0, len(l_symbols)):
                na_data[index][col] = y
    for key in l_keys:
        dData[key] = pand.DataFrame( index=l_index, columns=l_symbols, data=na_data )
    return dData
    
def get_highest_lookback(na_data):
    l_lookbacks = []
    for col in range(na_data.shape[1]):
        i_firstNan = -1
        for row in range(0, na_data.shape[0]):
            if math.isnan(na_data[row, col]) or math.isinf(na_data[row, col]):
                i_firstNan = row + 1    
            else:
                break
        l_lookbacks.append(i_firstNan)
    return np.array(l_lookbacks, copy = False)
    
if __name__ == '__main__':
    pass