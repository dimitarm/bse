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




import utils.bsedateutil as bsedateutil
import utils.equities as bseeq
import utils.data as datautil



if __name__ == '__main__':
    
    lsSym = np.array(bseeq.get_all_equities())
    
    #get data
    dtStart = dt.datetime(2010,2,18)
    dtEnd = dt.datetime(2014,2,17)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      

    #get train data
    ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16) )
    
    dmPrice = dataobj.get_data( ldtTimestamps, lsSym, 'close')
    dmVolume = dataobj.get_data( ldtTimestamps, lsSym, 'volume' )
    
    
    print tsutil.stockFilter(dmPrice, dmVolume, fNonNan = 0.9, fPriceVolume = 1)
    
    