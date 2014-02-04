'''
Created on Nov 5, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import math

def featEMAlambda( dData, serie='close', lambd = 0.9, bRel = False ):
    '''
    @summary: Calculate exponential moving average
    @param dData: Dictionary of data to use
    @param lLookback: Number of days to look in the past
    @param b_human: if true return dataframe to plot
    @return: DataFrame array containing values
    '''
    
    dfPrice = dData[serie]
    
    dfRet = pand.ewma(dfPrice, span=(2/lambd) - 1)
    
    if bRel:
        dfRet = dfRet / dfPrice;
         
    return dfRet


def featBollinger( dData, serie = 'close', lLookback = 20):
    dfPrice = dData[serie]
    #''' Loop through stocks '''
    dfAvg = pand.rolling_mean(dfPrice, lLookback)
    return dfAvg
    
def featBollingerUp( dData, serie = 'close', lLookback = 20):
    dfPrice = dData[serie]
    #''' Loop through stocks '''
    dfAvg = pand.rolling_mean(dfPrice, lLookback)
    dfStd = pand.rolling_std(dfPrice, lLookback)
    
    dfRet = dfAvg + 2.0 * dfStd * dfStd
    return dfRet
   
def featBollingerDown( dData, serie = 'close', lLookback = 20):
    dfPrice = dData[serie]
    #''' Loop through stocks '''
    dfAvg = pand.rolling_mean(dfPrice, lLookback)
    dfStd = pand.rolling_std(dfPrice, lLookback)
    
    dfRet = dfAvg - 2.0 * dfStd * dfStd
    return dfRet
                   
def featPrice2BollingerUp( dData, serie='close', lLookback = 20):
    return dData[serie]/featBollingerUp(dData, serie, lLookback)

def featPrice2BollingerDown( dData, serie='close', lLookback = 20):
    return dData[serie]/featBollingerDown(dData, serie, lLookback)

def featBollingerTradeRule( dData, serie = 'close', lLookback = 20):
    dfBollUp = featBollingerUp(dData, serie, lLookback)
    dfBollDown = featBollingerDown(dData, serie, lLookback)
    
    dfPt1 = dData[serie].shift(1)
    ruleFunc = np.vectorize(tradeRuleBollinger)
    
    naRet = ruleFunc(dfPt1.values, dData[serie].values, dfBollUp.values, dfBollDown.values)
    dfRet = pand.DataFrame(data=naRet, index=dData[serie].index, columns=dData[serie].columns)
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
    dData={}
    dData['close'] = pand.DataFrame({'Aaa': [1.0, 2.0, 3.0, 4.0], 'bbbbb': [5.0, 6.0, 7.0, 8.0]})
    featBollingerTradeRule(dData, 'close', 2)