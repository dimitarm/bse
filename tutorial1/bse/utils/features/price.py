'''
Created on Nov 5, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import math
import QSTK.qstkutil.tsutil as tsu
import warnings

def featSTDReturn( dFullData, lLookback=20, bRel=True ):
    '''
    @summary: Calculate standard deviation
    @param dFullData: Dictionary of data to use
    @param lLookback: Number of days to look in the past
    @param b_human: if true return dataframe to plot
    @return: DataFrame array containing values
    '''
    
    dfPrice = dFullData['close'].copy()
    
    tsu.returnize1(dfPrice.values)
    dfRet = pand.rolling_std(dfPrice, lLookback)
    
    if bRel:
        dfRet = dfRet / dfPrice
    return dfRet

EMA_MIN_DATA_COUNT = 8

def featEMA( dFullData, serie='close', lLookback = 20, bRel = False ):
    '''
    @summary: Calculate exponential moving average
    @param dFullData: Dictionary of data to use
    @param lLookback: Number of days to look in the past
    @param b_human: if true return dataframe to plot
    @return: DataFrame array containing values
    '''
    dfPrice = dFullData[serie]
    for serie in dfPrice:
        if dfPrice[serie].size <= lLookback * EMA_MIN_DATA_COUNT:
            raise Exception('data is not sufficient for EMA')
        
    dfRet = pand.ewma(dfPrice, span=lLookback)
    
    if bRel:
        dfRet = dfRet / dfPrice;
         
    for serie in dfRet:
        for i in range(0, lLookback * EMA_MIN_DATA_COUNT):
            dfRet[serie].iat[i] = np.nan
    return dfRet


#def featBollinger( dFullData, serie = 'close', lLookback = 20):
#    dfPrice = dFullData[serie]
#    #''' Loop through stocks '''
#    dfAvg = pand.rolling_mean(dfPrice, lLookback)
#    return dfAvg
    
def featBollingerUp( dFullData, serie = 'close', lLookback = 20):
    dfPrice = dFullData[serie]
    #''' Loop through stocks '''
    dfAvg = pand.rolling_mean(dfPrice, lLookback)
    dfStd = pand.rolling_std(dfPrice, lLookback)
    
    dfRet = dfAvg + 2.0 * dfStd
    return dfRet
   
def featBollingerDown( dFullData, serie = 'close', lLookback = 20):
    dfPrice = dFullData[serie]
    #''' Loop through stocks '''
    dfAvg = pand.rolling_mean(dfPrice, lLookback)
    dfStd = pand.rolling_std(dfPrice, lLookback)
    
    dfRet = dfAvg - 2.0 * dfStd
    return dfRet
                   
def featPrice2BollingerUp( dFullData, serie='close', lLookback = 20):
    return dFullData[serie]/featBollingerUp(dFullData, serie, lLookback)

def featPrice2BollingerDown( dFullData, serie='close', lLookback = 20):
    return dFullData[serie]/featBollingerDown(dFullData, serie, lLookback)

def featBollingerTradeRule( dFullData, serie = 'close', lLookback = 20):
    dfBollUp = featBollingerUp(dFullData, serie, lLookback)
    dfBollDown = featBollingerDown(dFullData, serie, lLookback)
    
    dfPt1 = dFullData[serie].shift(1)
    ruleFunc = np.vectorize(tradeRuleBollinger)
    
    naRet = ruleFunc(dfPt1.values, dFullData[serie].values, dfBollUp.values, dfBollDown.values)
    dfRet = pand.DataFrame(data=naRet, index=dFullData[serie].index, columns=dFullData[serie].columns)
    return dfRet

def tradeRuleBollinger(pt1, pt, bu, bd):
    if math.isnan(pt1) or math.isnan(pt) or math.isnan(bu) or math.isnan(bd):
        return np.nan
    if pt1 >= bd and pt < bu:
        return 1 #buy
    if pt1<=bd and pt > bu:
        return -1 #sell
    return 0 #hold 
    
     
    
    
if __name__ == '__main__':
    dFullData={}
    dFullData['close'] = pand.DataFrame({'Aaa': [1.0, 2.0, 3.0, 4.0], 'bbbbb': [5.0, 6.0, 7.0, 8.0]})
    featBollingerTradeRule(dFullData, 'close', 2)