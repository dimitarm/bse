'''
Created on Apr 9, 2014

@author: I028663
'''

import bse.utils.dateutil as bsedateutl
import bse.utils.reader.data as bsereader
import bse.utils.classes as bseclass 
import bse.utils.equities as bseeq
import datetime as dt
import QSTK.qstkutil.tsutil as tsutil

_prediction_period = 5 #days
_train_period = 60

def get_symbols_for_prediction(date_end = dt.date.today(), days_period = 90):
    # calculate limit dates
    date_start = date_end - dt.timedelta(days=days_period) #fixed number of days which cover the biggest lookback period in all features + some coefficient for non working days
    #get data
    full_data = bsereader.get_data(date_start, date_end, symbols = bseeq.get_all_equities())
    # get symbols to be predicted
    return tsutil.stockFilter(full_data['close'], full_data['volumes'], fNonNan=0.95, fPriceVolume=1)

def get_next_prediction_PERIOD(current_start, cur_end):
    count = _prediction_period 
    new_end = cur_end
    while count > 0:
        if bsedateutl.isBSEDay(new_end) == bsedateutl.WORK:
            count -= 1
        new_end = new_end + dt.timedelta(days = 1)
    return (cur_end, new_end)
    
def get_trend(symbols, start_date, trend_days):
    data = bsereader.get_data(start_date, start_date + dt.timedelta(days = trend_days * 2), symbols)
    feat = bseclass.featTrend(data, trend_days)
    trends = {}
    for symbol in symbols:
        trends[symbol] = feat[symbol][start_date]
    return trends


    

if __name__ == '__main__':
#    bsereader.get_data(dt.date(year = 2014, month = 1, day = 1), dt.date(year = 2014, month = 4, day = 1), ['SOFIX'])
#    print get_trend(['SOFIX', '3JR'], dt.date(year = 2014, month = 4, day = 1), 5)
    dtEnd = dt.datetime(2014,9,23). replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    print get_symbols_for_prediction(date_end = dtEnd, days_period = 365*4)
    pass

'''
Things to be saved in persistent file:
prediction_period_start
prediction_period_end
forecast_symbols
'''


#update data

#get list of latest predicted symbols
#get their closing data
#calculate forecast success rate for each one of them
#store list of latest prediction symbols with forecast success in DB
#update index.html 

#get current prediction date

#calculate next due prediction date
    #next_due_prediction_date

#get predictions 

#set index.html link in current prediction page

#move current prediction page to archive folder

#generate new prediction page (set link to previous prediction page)

#copy new prediction page     
    