'''
Created on Jan 4, 2013

@author: dimitar
'''
import datetime as dt

HOLIDAY = 0
WORK = 1

_special_days = {

   #2009-2013
    dt.date(2009,1,1):HOLIDAY,dt.date(2009,1,2):HOLIDAY,dt.date(2009,3,2):HOLIDAY,dt.date(2009,3,3):HOLIDAY,dt.date(2009,4,10):HOLIDAY,dt.date(2009,4,13):HOLIDAY,dt.date(2009,4,20):HOLIDAY,
    dt.date(2009,5,1):HOLIDAY,dt.date(2009,5,4):HOLIDAY,dt.date(2009,5,5):HOLIDAY,dt.date(2009,5,6):HOLIDAY,dt.date(2009,8,4):HOLIDAY,dt.date(2009,9,21):HOLIDAY,dt.date(2009,9,22):HOLIDAY,
    dt.date(2009,12,24):HOLIDAY,dt.date(2009,12,25):HOLIDAY,dt.date(2009,12,29):HOLIDAY,dt.date(2009,12,30):HOLIDAY,dt.date(2009,12,31):HOLIDAY,dt.date(2010,1,1):HOLIDAY,dt.date(2010,3,3):HOLIDAY,
    dt.date(2010,4,2):HOLIDAY,dt.date(2010,4,5):HOLIDAY,dt.date(2010,5,6):HOLIDAY,dt.date(2010,5,7):HOLIDAY,dt.date(2010,5,24):HOLIDAY,dt.date(2010,9,6):HOLIDAY,dt.date(2010,9,22):HOLIDAY,
    dt.date(2010,12,24):HOLIDAY,dt.date(2010,12,31):HOLIDAY,dt.date(2011,3,3):HOLIDAY,dt.date(2011,3,4):HOLIDAY,dt.date(2011,4,22):HOLIDAY,dt.date(2011,4,25):HOLIDAY,dt.date(2011,5,6):HOLIDAY,
    dt.date(2011,5,23):HOLIDAY,dt.date(2011,5,24):HOLIDAY,dt.date(2011,9,5):HOLIDAY,dt.date(2011,9,6):HOLIDAY,dt.date(2011,9,22):HOLIDAY,dt.date(2011,9,23):HOLIDAY,dt.date(2011,12,26):HOLIDAY,
    dt.date(2012,1,2):HOLIDAY,dt.date(2012,4,6):HOLIDAY,dt.date(2012,4,9):HOLIDAY,dt.date(2012,4,13):HOLIDAY,dt.date(2012,4,16):HOLIDAY,dt.date(2012,4,30):HOLIDAY,dt.date(2012,5,1):HOLIDAY,
    dt.date(2012,5,24):HOLIDAY,dt.date(2012,5,25):HOLIDAY,dt.date(2012,9,6):HOLIDAY,dt.date(2012,9,7):HOLIDAY,dt.date(2012,12,24):HOLIDAY,dt.date(2012,12,25):HOLIDAY,dt.date(2012,12,26):HOLIDAY,
    dt.date(2012,12,31):HOLIDAY,dt.date(2013,1,1):HOLIDAY,dt.date(2013,3,29):HOLIDAY,dt.date(2013,4,1):HOLIDAY,dt.date(2013,5,1):HOLIDAY,dt.date(2013,5,2):HOLIDAY,dt.date(2013,5,3):HOLIDAY,
    dt.date(2013,5,6):HOLIDAY,dt.date(2013,5,24):HOLIDAY,dt.date(2013,9,6):HOLIDAY,dt.date(2013,12,23):HOLIDAY,dt.date(2013,12,24):HOLIDAY,dt.date(2013,12,25):HOLIDAY,dt.date(2013,12,26):HOLIDAY,
    dt.date(2013,12,31):HOLIDAY,
    #2014
    dt.date(2014, 1, 1): HOLIDAY, dt.date(2014, 3, 3): HOLIDAY, dt.date(2014, 4, 18): HOLIDAY, dt.date(2014, 4, 21): HOLIDAY, dt.date(2014, 5, 1): HOLIDAY,dt.date(2014, 5, 2): HOLIDAY,
    dt.date(2014, 5, 5): HOLIDAY, dt.date(2014, 5, 6): HOLIDAY, dt.date(2014, 9, 22): HOLIDAY, dt.date(2014, 12, 24): HOLIDAY,dt.date(2014, 12, 25): HOLIDAY,dt.date(2014, 12, 26): HOLIDAY,
    dt.date(2014, 12, 31): HOLIDAY
   }

def getBSEdays(startday, endday, timeofday = dt.timedelta(0)):
    start = startday
    end = endday
    dates = list()
    while start <= end:
        if isBSEDay(start):
            dates.append(start)
        start += dt.timedelta(days = 1)
    ret = [x + timeofday for x in dates]
    return(ret)

def isBSEDay(date):
    date = dt.date(year = date.year, month = date.month, day = date.day)
    if date in _special_days:
        return _special_days[date]
    if date.weekday() == 5 or date.weekday() == 6:
        return HOLIDAY
    else:
        return WORK

if __name__ == "__main__":
    #get special_days for 2009-2013
    import pandas as pd
    import os
    import sys
    import numpy as np
    
    def bgDateParser(date):
        dat = dt.datetime.strptime(date,"%Y-%m-%d")
        return dt.date(dat.year, dat.month, dat.day)
    
    filepath = os.environ['QSDATA'] + "/Processed/Custom/SOFIX.csv"
    sofix = pd.read_csv(filepath, index_col = 0, parse_dates = True, date_parser = bgDateParser)
    sf_dates = np.sort(sofix.index.values)
    dat_in_row = 7
    in_row = 0
    start = dt.date(2009, 1, 1)
    incr = dt.timedelta(days = 1)
    end = dt.date(2013, 12, 31)
    while(start <= end):
        if start.weekday() == 5 or start.weekday() == 6:
            if start in sf_dates:
                sys.stdout.write("dt.date(" + str(start.year) + "," + str(start.month) + "," + str(start.day) + "):WORK,")
                in_row += 1
        else:
            if start not in sf_dates:
                sys.stdout.write("dt.date(" + str(start.year) + "," + str(start.month) + "," + str(start.day) + "):HOLIDAY,")
                in_row += 1
        if in_row == dat_in_row:
            in_row = 0
            print "" 
        start = start + incr