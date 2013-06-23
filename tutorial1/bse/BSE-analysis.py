
import qstkutil.tsutil as tsu
import qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
from pylab import *
import pandas
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches
import utils.dateutil as bsedateutil
import utils.equities as bseequutil
import math as mth
from pandas.core.frame import DataFrame

print pandas.__version__

marketsymbol = 'SOFIX'

startday = dt.datetime(2013,1,1)
endday = dt.datetime(2013,5,29)
timeofday=dt.timedelta(hours=16)
timestamps = bsedateutil.getBSEdays(startday,endday,timeofday)
dataobj = da.DataAccess('Investor')
symbols = np.array(['SOFIX', '0ALA', '0S8'])
marketsymbolpos = 0
close = dataobj.get_data(timestamps, dataobj.get_all_symbols(), "close",verbose=True)

#calculate NaNs
sharperatios = DataFrame(index = ['sr', 'NaNs'], columns = close.columns, dtype = float)
for sym in close.columns:
    nans = 0
    for price in close[sym]:
        if math.isnan(price):
            nans += 1
    if nans > len(timestamps) / 5:
        close.pop(sym)
        sharperatios.pop(sym)
    else:
        sharperatios[sym]['NaNs'] = nans
        sharperatios[sym]['sr'] = 0
        
sharperatios = sharperatios.T
#
# Plot the adjusted close data
#
plt.clf()
newtimestamps = close.index
pricedat = close.values # pull the 2D ndarray out of the pandas object

#normalize nans
for sym in close.columns:
    sharperatios['NaNs'][sym] = sharperatios['NaNs'][sym] / len(timestamps)

tsu.fillforward(pricedat)
tsu.fillbackward(pricedat)
dailyrets = (pricedat[1:,:]/pricedat[0:-1,:]) - 1

#print dailyrets
dailyrets = np.insert(dailyrets, 0, np.zeros(dailyrets.shape[1]), 0)

pp = PdfPages('bse-summary2013.pdf')

plt.plot(newtimestamps, dailyrets)
plt.legend(close.columns)
plt.ylabel('dailyrets')
plt.xlabel('Date')
pp.savefig()

for sym in range (0, len(close.columns)):
    averageret = np.average(dailyrets[:,sym])
    stdret = np.std(dailyrets[:,sym])
    sr = mth.sqrt(253) * averageret / stdret
    if math.isnan(sr):
        sr = 0
    
    sharperatios['sr'][close.columns[sym]] = sr

#    plt.clf()
#    plt.cla()
#    plt.plot(newtimestamps, pricedat[:,sym])
#    plt.ylabel(symbols[sym])
#    plt.xlabel('Date')
#    summary = "sr: " + str(sr) 
#    plt.figtext(0, 0, summary)
#    pp.savefig()
#
#    plt.clf()
#    plt.cla()
#    plt.scatter(dailyrets[:,marketsymbolpos],dailyrets[:,sym],c='blue') # $SPX v XOM
#    plt.ylabel(symbols[sym])
#    plt.xlabel(symbols[marketsymbolpos])
#    pp.savefig()
    sym_todo = len(close.columns) - sym - 1
    print str(sym_todo) + " to do!"


plt.clf()
plt.cla()

#take out stocks with nana > 10%
#for sym in symbols:
#    if sharperatios['NaNs'][sym] > 0.1:
#        sharperatios.

sharperatios = sharperatios.sort_index(by = 'sr', ascending = False)
sharperatios = sharperatios[0:10]

plt.figure()
sharperatios.plot()


pp.savefig()

pp.close()
