'''
Created on Jan 6, 2013

@author: dimitar
'''

import pandas 
import numpy as np
import math
import copy

import matplotlib.pyplot as plt

import QSTK.qstkutil.tsutil as tsu


import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.tsutil as tsu
import utils.data as bsedata
import utils.dateutil as bsedateutil
import utils.equities as bseequutil

import bse.utils.reader.data as bsereader
"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

def eventprofiler(df_events_arg, d_data, i_lookback=20, i_lookforward=20,
                b_market_neutral=True, b_errorbars=True,
                s_market_sym='SOFIX'):
    ''' Event Profiler for an event matix'''
    df_close = d_data['close'].copy()
    df_rets = df_close.copy()

    # Do not modify the original event dataframe.
    df_events = df_events_arg.copy()
    tsu.returnize0(df_rets.values)

    if b_market_neutral == True:
        df_rets = df_rets - df_rets[s_market_sym]
        del df_rets[s_market_sym]
        del df_events[s_market_sym]

    df_close = df_close.reindex(columns=df_events.columns)

    # Removing the starting and the end events
    df_events.values[0:i_lookback, :] = np.NaN
    df_events.values[-i_lookforward:, :] = np.NaN

    # Number of events
    i_no_events = int(np.logical_not(np.isnan(df_events.values)).sum())
    assert i_no_events > 0, "Zero events in the event matrix"
    na_event_rets = "False"

    # Looking for the events and pushing them to a matrix
    for i, s_sym in enumerate(df_events.columns):
        for j, dt_date in enumerate(df_events.index):
            if df_events[s_sym][dt_date] == 1:
                na_ret = df_rets[s_sym][j - i_lookback:j + 1 + i_lookforward]
                if type(na_event_rets) == type(""):
                    na_event_rets = na_ret
                else:
                    na_event_rets = np.vstack((na_event_rets, na_ret))

    if len(na_event_rets.shape) == 1:
        na_event_rets = np.expand_dims(na_event_rets, axis=0)

    # Computing daily rets and retuns
    na_event_rets = np.cumprod(na_event_rets + 1, axis=1)
    na_event_rets = (na_event_rets.T / na_event_rets[:, i_lookback]).T

    # Study Params
    na_mean = np.mean(na_event_rets, axis=0)
    na_std = np.std(na_event_rets, axis=0)
    li_time = range(-i_lookback, i_lookforward + 1)

    # Plotting the chart
    plt.clf()
    plt.axhline(y=1.0, xmin=-i_lookback, xmax=i_lookforward, color='k')
    if b_errorbars == True:
        plt.errorbar(li_time[i_lookback:], na_mean[i_lookback:],
                    yerr=na_std[i_lookback:], ecolor='#333333',
                    alpha=0.1, elinewidth=2)
    plt.plot(li_time, na_mean, linewidth=3, label='mean', color='b')
    plt.xlim(-i_lookback - 1, i_lookforward + 1)
    if b_market_neutral == True:
        plt.title('Market Relative mean return of ' +\
                str(i_no_events) + ' events')
    else:
        plt.title('Mean return of ' + str(i_no_events) + ' events')
    plt.xlabel('Days')
    plt.ylabel('Cumulative Returns')
    plt.show()

def findEvents(dData, symbols, startday,endday, marketSymbol,verbose=False):

    timestamps = bsedateutil.getBSEdays(startday,endday)
    # Reading the Data
    ret0 = dData['close'].copy()

    # Calculating Daily Returns for the Market
    tsu.returnize0(ret0.values)
    SPYValues=ret0[marketSymbol]

    # Calculating the Returns of the Stock Relative to the Market 
    # So if a Stock went up 5% and the Market rised 3%. The the return relative to market is 2% 
    mktneutDM = ret0 - ret0[marketSymbol]
    np_eventmat = copy.deepcopy(mktneutDM)
    for sym in symbols:
        for time in timestamps:
            np_eventmat[sym][time]=np.NAN

    # Generating the Event Matrix
    # Event described is : Market falls more than 3% plus the stock falls 5% more than the Market
    # Suppose : The market fell 3%, then the stock should fall more than 8% to mark the event.
    # And if the market falls 5%, then the stock should fall more than 10% to mark the event.

    for symbol in symbols:
        for i in range(1,len(mktneutDM[symbol])):
            if SPYValues[i]<-0.01 and mktneutDM[symbol][i] < SPYValues[i] : # When market fall is more than 3% and also the stock compared to market is also fell by more than 5%.
#            if SPYValues[i]<-0.01 and mktneutDM[symbol][i] < -0.02 : # When market fall is more than 3% and also the stock compared to market is also fell by more than 5%.
                     np_eventmat[symbol][i] = 1.0  #overwriting by the bit, marking the event
            
    return np_eventmat


#################################################
################ MAIN CODE ######################
#################################################


#symbols = ['3JR', '4CF', '4EH', '5F4', '5MB', '6C4', '6K1', 'E4A', 'SOFIX', 'T57']
symbols = ['3JR', '4CF', '4EH', '5F4', '5MB', '6C4', 'SOFIX']

# You might get a message about some files being missing, don't worry about it.

#symbols =['BFRE','ATCS','RSERF','GDNEF','LAST','ATTUF','JBFCF','CYVA','SPF','XPO','EHECF','TEMO','AOLS','CSNT','REMI','GLRP','AIFLY','BEE','DJRT','CHSTF','AICAF']
startday = dt.datetime(2009,2,1)
endday = dt.datetime(2012,12,31)

dData = bsereader.get_data( startday, endday, symbols)
bsedata.prepare_data_for_prediction(dData)
eventMatrix = findEvents(dData,symbols,startday,endday,marketSymbol='SOFIX',verbose=False)
timestamps = bsedateutil.getBSEdays(startday,endday)

#for symbol in symbols:
#    for timestamp in timestamps:
#        if eventMatrix[symbol][timestamp] == 1:
#            print symbol
#            print timestamp 
#            print eventMatrix[symbol][timestamp]
        
            
#    df_events_arg, d_data, i_lookback=20, i_lookforward=20,
#                s_filename='study', b_market_neutral=True, b_errorbars=True,
#                s_market_sym='SPY'

eventprofiler(eventMatrix, dData, i_lookback=20, i_lookforward=20, b_market_neutral=True, b_errorbars=True, s_market_sym='SOFIX')                
#eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,timestamps,lookback_days=20,lookforward_days=20,verbose=False)
#eventProfiler.study(filename="BSE-EventStudy.pdf",plotErrorBars=True,plotMarketNeutral=True,plotEvents=True,marketSymbol='SOFIX')


