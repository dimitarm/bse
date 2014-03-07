'''
Created on Jan 4, 2013

@author: dimitar
'''
import datetime as dt
import pandas as pd
import os
import numpy


def _cache_dates():
    

    ''' Caches dates '''
    try:
        filepath = os.environ['QSDATA'] + "/Processed/Custom/SOFIX.csv"
        sofix = pd.read_csv(filepath, index_col = 0, parse_dates = True, date_parser = bgDateParser)
        dates = numpy.sort(sofix.index.values)
    except KeyError:
        print "SOFIX.csv\n"

    return dates

#2013/05/29

def bgDateParser(date):
    zerohms = dt.timedelta(0,0,0)
    dat = dt.datetime.strptime(date,"%Y-%m-%d")
    dat = dat + zerohms
    return dat
    
def getBSEdays(startday, endday):
    start = startday
    end = endday
    timeofday = dt.timedelta(hours = 16)
    bsedates = _cache_dates()

    ret = list()
    for dat in bsedates:
        if dat >= start and dat <= end:
            ret.append(dat + timeofday)

    return(ret)

if __name__ == '__main__':
    print _cache_dates()