'''
Created on Mar 20, 2014

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

import utils.bsedateutil as bsedateutil
import utils.equities as bseeq
import utils.data as datautil



if __name__ == '__main__':
    
    lsSym = np.array(bseeq.get_all_equities())
    
    #get data
    dtEnd = dt.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    dtStart = dtEnd - dt.timedelta(days = 365)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      

    #get train data
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16) )
    
    dmPrice = dataobj.get_data( ldtTimestamps, lsSym, 'close' )
    dmVolume = dataobj.get_data( ldtTimestamps, lsSym, 'volume' )
    
    
    print tsutil.stockFilter(dmPrice, dmVolume, fNonNan = 0.9, fPriceVolume = 1)
    
    