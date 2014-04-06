'''
Created on Apr 5, 2014

@author: dimitar
'''
import math
import datetime as dt
import itertools
import sys
from bse.utils.classes import featTrend
''' 3rd party imports '''
import numpy as np
import pandas as pand
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.axes as ax

import sys

def prepare_data(dFullData):

    nds = dFullData.values
    # fill forward
    for col in range(nds.shape[1]):
        for row in range(1, nds.shape[0]):
            if math.isnan(nds[row, col]):
                nds[row, col] = nds[row-1, col]        
    # fill backward
    for col in range(nds.shape[1]):
        for row in range(nds.shape[0] - 2, -1, -1):
            if math.isnan(nds[row, col]):
                nds[row, col] = nds[row+1, col]

if __name__ == '__main__':
    
    array = np.random.random_sample((30))
    array[10] = np.NAN
    array[11] = np.NAN
    array[12] = np.NAN
    array[13] = np.NAN
    array[20] = np.NAN
    array[21] = np.NAN
    array[22] = np.NAN
    array[23] = np.NAN
    array[24] = np.NAN
    
    
    d = {'one' : pand.Series(array), 'two': pand.Series(np.random.random_sample((30)))}

    data = pand.DataFrame(d)
    data1 = pand.DataFrame(data, copy = True)
    for symbol in data:
        data[symbol].plot()
    plt.show()
    
    data.set_value(5, 'one', 666)
    prepare_data(data)
    
    
    print data['one']