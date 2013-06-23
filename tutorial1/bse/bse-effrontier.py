
import qstkutil.tsutil as tsu
import qstkutil.DataAccess as da
import datetime as dt

import matplotlib.pyplot as plt
import utils.dateutil as bsedateutil
import utils.equities as bseequutil
from pylab import *
from math import isnan
from copy import copy

''' Function gets a 100 sample point frontier for given returns '''
def getFrontier(naData):
    ''' Special case for fTarget = None, just get average returns '''
    (naAvgRets,naStd, b_error) = tsu.OptPort( naData, None )

    naLower = np.zeros(naData.shape[1])
    naUpper = np.ones(naData.shape[1])
    
    (fMin, fMax) = tsu.getRetRange( naData, naLower, naUpper, naAvgRets, s_type="long")
    
    fStep = (fMax - fMin) / 100.0
    
    lfReturn =  [fMin + x * fStep for x in range(101)]
    lfStd = []
    lnaPortfolios = []
    
    ''' Call the function 100 times for the given range '''
    for fTarget in lfReturn: 
        (naWeights, fStd, b_error) = tsu.OptPort( naData, fTarget, naLower, naUpper, s_type = "long")
        #if b_error == False:
        lfStd.append(fStd)
        lnaPortfolios.append( naWeights )
        #lfReturn.pop(lfReturn.index(fTarget))
    return (lfReturn, lfStd, lnaPortfolios, naAvgRets, naStd)
    


''' ******************************************************* '''
''' ******************** MAIN SCRIPT ********************** '''
''' ******************************************************* '''

''' portfolio '''
lsSymbols = [ '4BJ','5OTZ','3JR','6K1','T57','5MB','5BN','6C4','E4A' ] #2009

#lsSymbols = [ '4BJ', '5OTZ','3JR','6K1','T57', '5ALB', '5MB', '6AB', '5BN' ]   #2012


''' Create norgate object and query it for stock data '''
norgateObj = da.DataAccess('Investor')

lsAll = norgateObj.get_all_symbols()
intersect = set(lsAll) & set(lsSymbols)

if len(intersect) < len(lsSymbols):
    print "Warning: portfolio contains symbols that do not exist: ", 
    print set(lsSymbols) - intersect 
    
    lsSymbols = sort(list( intersect )) 

''''Read in historical data'''
lYear = 2009
dtEnd = dt.datetime(lYear+1,1,1) 
dtStart = dtEnd - dt.timedelta(days=365) 
dtTest = dtEnd + dt.timedelta(days=365) 
timeofday=dt.timedelta(hours=16)

ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, timeofday )
ldtTimestampTest = bsedateutil.getBSEdays( dtEnd, dtTest, timeofday )

dmClose = norgateObj.get_data(ldtTimestamps, lsSymbols, "close", True)
dmTest = norgateObj.get_data(ldtTimestampTest, lsSymbols, "close", True)

naData = dmClose.values.copy()
naDataTest = dmTest.values.copy()

tsu.fillforward(naData)
tsu.fillbackward(naData)
tsu.returnize0(naData)

tsu.fillforward(naDataTest)
tsu.fillbackward(naDataTest)
tsu.returnize0(naDataTest)

''' Get efficient frontiers '''
(lfReturn, lfStd, lnaPortfolios, naAvgRets, naStd) = getFrontier( naData)
(lfReturnTest, lfStdTest, unused, unused, unused) = getFrontier( naDataTest)

plt.clf()
fig = plt.figure()

''' Plot efficient frontiers '''
plt.plot(lfStd,lfReturn, 'b')
plt.plot(lfStdTest,lfReturnTest, 'r')

''' Plot where efficient frontier WOULD be the following year '''
lfRetTest = []
lfStdTest = []
naRetsTest = naDataTest
for naPortWeights in lnaPortfolios:
    naPortRets =  np.dot( naRetsTest, naPortWeights)
    lfStdTest.append( np.std(naPortRets) )
    lfRetTest.append( np.average(naPortRets) )

plt.plot(lfStdTest,lfRetTest,'k')

#''' plot some arrows showing transition of efficient frontier '''
#for i in range(0,101,10):
#    arrow( lfStd[i],lfReturn[i], lfStdTest[i]-lfStd[i], lfRetTest[i]-lfReturn[i], color='k' )

''' Plot indifidual stock risk/return as green + ''' 
for i, fReturn in enumerate(naAvgRets):
    plt.plot( naStd[i], fReturn, 'g+' ) 

plt.legend( ['this year Frontier', 'next year Frontier', 'Performance of this Frontier in next year'], loc='lower right' )

plt.title('Efficient Frontier ' + str(lYear))
plt.ylabel('Expected Return')
plt.xlabel('StDev')

savefig('bse-effrontier' + str(lYear) + '.pdf',format='pdf')

    
    


