'''
Created on Sep 26, 2013

@author: I028663
'''
import numpy as np
import pandas as pand
import math

def get_random_data(l_keys, l_index, l_symbols, method = 'normal'):
    dData = {}
    if method = 'normal':
        for key in l_keys:
            na_data = np.random.randint(low = 5, high = 50, size = (len(l_index), len(l_symbols))) * 0.99
            dData[key] = pand.DataFrame( index=l_index, columns=l_symbols, data=na_data )
    else:
        for index in range(0, len(l_index)):
            y = math.sin( index * 10/len(l_index) )
            
        for key in l_keys:
            dData[key] = pand.DataFrame( index=l_index, columns=l_symbols, data=na_data )
            
        print(y)
        
    return dData
    
if __name__ == '__main__':
    pass