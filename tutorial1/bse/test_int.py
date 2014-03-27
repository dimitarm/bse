'''
Created on Mar 27, 2014

@author: I028663
'''
import sys
import numpy as np
import pandas as pand

if __name__ == '__main__':
    data = np.array([-1.65628897e-14,   1.35419853e-15,   1.35419853e-15,   1.28549237e-15,   1.84014643e-15,   1.51462141e-15,   1.51462141e-15,   1.51462141e-15,   1.51462141e-15,   1.51462141e-15,   1.74527442e-15])
    print pand.rolling_mean(data, 10)


'''
result
[             nan              nan              nan              nan
              nan              nan              nan              nan
              nan  -3.15574679e-16   1.51524173e-15]




'''