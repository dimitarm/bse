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
import numpy as np



_processed_data = {}
_series = ('close', 'open', 'high', 'low', 'volumes')

def _date_parser(string):
    #2014-03-27
    date = dt.datetime.strptime(string, '%Y-%m-%d')
    date = dt.date(date.year, date.month, date.day)
    return date

def _read_data_init(symbol):
    if _processed_data.has_key(symbol) == False:
        local_file_name = os.environ['QSDATA'] + "/Processed/Custom/" + symbol + '.csv' 
        raw_data = pand.read_csv(local_file_name, index_col=0, parse_dates = True, date_parser = _date_parser).sort_index().astype(float)
        df_with_nans = _add_nans(raw_data)
        _processed_data[symbol] = df_with_nans 

def _add_nans(data):
    bsedays = bsedateutil.getBSEdays(bsedateutil.getFirstDateOfData(), dt.date.today())
    missing_days = []
    
    for day in bsedays:
        if not day in data[_series[0]].index:
            missing_days.append(day)
    df_missing = pand.DataFrame(data = np.NaN, columns = _series, index = missing_days)
    return pand.concat((data, df_missing), verify_integrity = True)

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
        for symbol in symbols:
            if serie_name in result:
                result[serie_name][symbol] = pand.Series(series[symbol].ix[bsedates])
            else:
                tmp_serie = series[symbol].loc[bsedates]
                df_new = pand.DataFrame(tmp_serie.values, columns = (symbol,), index = tmp_serie.index)
                result[serie_name] = df_new 
#    for serie in _series:
#        result[serie] = pand.DataFrame(result[serie], copy = True)
    return result 

if __name__ == '__main__':
    sofix = get_data(dt.date(year = 2014, month = 1, day = 1), dt.date.today(), 'SOFIX')
    print sofix
