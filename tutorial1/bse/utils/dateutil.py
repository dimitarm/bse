'''
Created on Jan 4, 2013

@author: dimitar
'''

import datetime as dt
import numpy as np
import pandas as pd


def _cache_dates():
    ''' Caches dates '''
    try:
        filename = "BSE_dates.txt"
    except KeyError:
        print "BSE_dates.txt cannot be found\n"

    datestxt = np.loadtxt(filename,dtype=str)
    dates = []
    for i in datestxt:
        dates.append(dt.datetime.strptime(i,"%Y/%m/%d"))
    return pd.TimeSeries(index=dates, data=dates)

BSE_DATES = _cache_dates()

def getBSEdays(startday = dt.datetime(1964,7,5), endday = dt.datetime(2020,12,31),
    timeofday = dt.timedelta(0)):
    """
    @summary: Create a list of timestamps between startday and endday (inclusive)
    that correspond to the days there was trading at the NYSE. This function
    depends on a separately created a file that lists all days since July 4,
    1962 that the NYSE has been open, going forward to 2020 (based
    on the holidays that NYSE recognizes).

    @param startday: First timestamp to consider (inclusive)
    @param endday: Last day to consider (inclusive)
    @return list: of timestamps between startday and endday on which NYSE traded
    @rtype datetime
    """
    start = startday - timeofday
    end = endday - timeofday

    dates = BSE_DATES[start:end]

    ret = [x + timeofday for x in dates]

    return(ret)
