'''
Created on Mar 30, 2014

@author: dimitar
'''

import bse.utils.dateutil as bsedateutil
import bse.utils.equities as bseeq
import os
import datetime as dt   
import pandas as pand
import types



_processed_data = {}
_series = ('close', 'open', 'high', 'low', 'volumes')

def _date_parser(string):
    #2014-03-27
    date = dt.datetime.strptime(string, '%Y-%m-%d')
    date = date.replace(hour = 16)
    return date

def _read_data_init(symbol):
    if _processed_data.has_key(symbol) == False:
        local_file_name = os.environ['QSDATA'] + "/Processed/Custom/" + symbol + '.csv' 
        _processed_data[symbol] = pand.read_csv(local_file_name, index_col=0, parse_dates = True, date_parser = _date_parser).sort_index()

def _get_series(serie, symbols):
    series = {}
    for symbol in symbols:
        series[symbol] = _processed_data[symbol][serie]
    return series

def get_data(start, end, symbols):
    bsedates = bsedateutil.getBSEdays(startday = start, endday = end)
    if isinstance(symbols, types.StringTypes) == True:
        symbols = (symbols,)
    for symbol in symbols:
        _read_data_init(symbol)
    
    result = {}
    for serie_name in _series:
        series = _get_series(serie_name, symbols)
        dfres = pand.DataFrame(series)
        result[serie_name] = dfres.ix[bsedates]
    return result 

if __name__ == '__main__':
    sofix = get_data(dt.date(year = 2014, month = 1, day = 1), dt.date.today(), 'SOFIX')
    print sofix
