'''
Created on Feb 11, 2014

@author: dimitar
'''
import math
import datetime as dt
import itertools

''' 3rd party imports '''
import numpy as np
import pandas as pand
import matplotlib.pyplot as plt
import bse.utils as bseutils
from datetime import datetime
from datetime import timedelta

''' QSTK imports '''
from QSTK.qstkutil import DataAccess as da
import QSTK.qstkutil.tsutil as tsutil

import utils.dateutil as bsedateutil
import utils.equities as bseeq
import utils.data as datautil
import bse.utils.reader.data as bsereader1

if __name__ == '__main__':
    
    lsSym = np.array(bseeq.get_all_equities())
    
    #get data
    dtStart = dt.datetime(2013,9,24)
    dtEnd = dt.datetime(2014,9,23)

    #dataobj = da.DataAccess(da.DataSource.CUSTOM)      

    #get train data
    dData = bsereader1.get_data( dtStart, dtEnd, bseeq.get_all_equities())
    #dmVolume = bsereader1.get_data( ldtTimestamps, bseeq.get_all_equities(), 'volume' )
    
    
    print tsutil.stockFilter(dData['close'], dData['volumes'], fNonNan = 0.9, fPriceVolume = 1)
    
    