'''
Created on Feb 28, 2014

@author: dimitar
'''
from QSTK.qstkutil import DataAccess as da
from datetime import datetime, timedelta
from utils import tools as bsetools
from utils.classes import *
import datetime as dt
import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pand
import utils.data as datautil
import utils.dateutil as bsedateutil
import utils.features.feats as bsefeats
import utils.tools as bsetools
import matplotlib.ticker as ticker


''' 3rd party imports '''
''' QSTK imports '''


def adjust_Serie(serie, n=5):
    for i in range(0, n):
        max_vol = serie.max()
        for date, volume in serie.iteritems():
            if volume == max_vol:
                serie[date] = max_vol / 5


if __name__ == '__main__':

    lsSym = np.array(['SOFIX'])
    
    ''' Get data for 2009-2010 '''
    dtStart = dt.datetime(2009, 1, 1)
    dtEnd = dt.datetime(2014, 1, 1)
    dataobj = da.DataAccess(da.DataSource.CUSTOM)      
    lsKeys = ['close', 'volume']
    lLookback = 20
    # get train data
    ldtTimestamps = bsedateutil.getBSEdays(dtStart, dtEnd)
    ldfData = dataobj.get_data(ldtTimestamps, lsSym, lsKeys, verbose=False)
    d_data = dict(zip(lsKeys, ldfData))
    
    np_bollUp = bsefeats.price.featBollingerUp(d_data, lLookback=lLookback)
    s_bollUp = pand.Series(data=np_bollUp.values[lLookback - 1:-1].reshape(np_bollUp.shape[0] - lLookback), index=np_bollUp.index[lLookback - 1:-1])
    np_bollDn = bsefeats.price.featBollingerDown(d_data, lLookback=lLookback)
    s_bollDn = pand.Series(data=np_bollDn.values[lLookback - 1:-1].reshape(np_bollDn.shape[0] - lLookback), index=np_bollDn.index[lLookback - 1:-1])
    np_trend = featTrend(d_data, lForwardlook=1)    
    s_trend = pand.Series(data=np_trend.values[lLookback - 1:-1].reshape(np_trend.shape[0] - lLookback), index=np_trend.index[lLookback - 1:-1])
    # np_MA = bsefeats.price.featEMAlambda(d_data, lambd=0.0952)
    
    s_close = pand.Series(data=d_data['close'].values[lLookback - 1:-1].reshape(d_data['close'].shape[0] - lLookback), index=d_data['close'].index[lLookback - 1:-1])    
    s_volume = pand.Series(data=d_data['volume'].values[lLookback - 1:-1].reshape(d_data['volume'].shape[0] - lLookback), index=d_data['volume'].index[lLookback - 1:-1])    
    s_volume = s_volume / 50000
    adjust_Serie(s_volume, 9)
                          

    
    fig = plt.figure(figsize=(16.30, 1.4), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], axisbg='#e9e8ed')

#    locator = ticker.MultipleLocator(base = 25)    
#    ax.yaxis.set_minor_locator(locator)
    grid_color = '#000000'
    #ax.xaxis.grid(which='major', color=grid_color, linestyle='-', linewidth=0.1, drawstyle = 'steps-mid')
    #ax.yaxis.grid(which='major', color=grid_color, linestyle='-', linewidth=0.05)
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])


    
    linewidth = 0.6
    ax.plot(s_close.index, s_close.values, linewidth=linewidth)
    ax.plot(s_bollUp.index, s_bollUp.values, linewidth=linewidth)
    ax.plot(s_bollDn.index, s_bollDn.values, linewidth=linewidth)
    color = '#9b9b9b'
    for date, volume in s_volume.iteritems():
        bottom = s_close[date]
        if s_trend[date] == 1:
            ax.bar(left=date, height=volume, width=0.3, bottom=bottom, color=color, edgecolor=color)
        elif s_trend[date] == -1:
            ax.bar(left=date, height=volume, width=0.3, bottom=bottom - volume, color=color, edgecolor=color)
    plt.show()
