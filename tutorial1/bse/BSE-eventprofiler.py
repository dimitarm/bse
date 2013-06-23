'''
Created on Jan 6, 2013

@author: dimitar
'''

import pandas 
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep
import utils.dateutil as bsedateutil
import utils.equities as bseequutil

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

# Available field names: open, close, high, low, close, actual_close, volume
closefield = "close"
volumefield = "volume"
window = 10

def findEvents(symbols, startday,endday, marketSymbol,verbose=False):

    # Reading the Data for the list of Symbols.    
    timeofday=dt.timedelta(hours=16)
    timestamps = bsedateutil.getBSEdays(startday,endday,timeofday)
    dataobj = da.DataAccess('Investor')
    if verbose:
            print __name__ + " reading data"
    # Reading the Data
    close = dataobj.get_data(timestamps, symbols, closefield)

    # Completing the Data - Removing the NaN values from the Matrix
    close = (close.fillna(method='ffill')).fillna(method='backfill')

    
    # Calculating Daily Returns for the Market
    tsu.returnize0(close.values)
    SPYValues=close[marketSymbol]

    # Calculating the Returns of the Stock Relative to the Market 
    # So if a Stock went up 5% and the Market rised 3%. The the return relative to market is 2% 
    mktneutDM = close - close[marketSymbol]
    np_eventmat = copy.deepcopy(mktneutDM)
    for sym in symbols:
        for time in timestamps:
            np_eventmat[sym][time]=np.NAN

    if verbose:
            print __name__ + " finding events"

    # Generating the Event Matrix
    # Event described is : Market falls more than 3% plus the stock falls 5% more than the Market
    # Suppose : The market fell 3%, then the stock should fall more than 8% to mark the event.
    # And if the market falls 5%, then the stock should fall more than 10% to mark the event.

    for symbol in symbols:
        
        for i in range(1,len(mktneutDM[symbol])):
            if SPYValues[i]<-0.03 and mktneutDM[symbol][i] < -0.05 : # When market fall is more than 3% and also the stock compared to market is also fell by more than 5%.
                     np_eventmat[symbol][i] = 1.0  #overwriting by the bit, marking the event
            
    return np_eventmat


#################################################
################ MAIN CODE ######################
#################################################


symbols = da.DataAccess('Investor').get_all_symbols()
# You might get a message about some files being missing, don't worry about it.

#symbols =['BFRE','ATCS','RSERF','GDNEF','LAST','ATTUF','JBFCF','CYVA','SPF','XPO','EHECF','TEMO','AOLS','CSNT','REMI','GLRP','AIFLY','BEE','DJRT','CHSTF','AICAF']
startday = dt.datetime(2009,2,1)
endday = dt.datetime(2012,12,31)
eventMatrix = findEvents(symbols,startday,endday,marketSymbol='SOFIX',verbose=False)

timestamps = bsedateutil.getBSEdays(startday,endday,dt.timedelta(hours=16))


for symbol in symbols:
    for timestamp in timestamps:
        if eventMatrix[symbol][timestamp] == 1:
            print symbol
            print timestamp 
            print eventMatrix[symbol][timestamp]
        
            
    
eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,timestamps,lookback_days=20,lookforward_days=20,verbose=False)

eventProfiler.study(filename="BSE-EventStudy.pdf",plotErrorBars=True,plotMarketNeutral=True,plotEvents=True,marketSymbol='SOFIX')


