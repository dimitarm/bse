'''
Created on Nov 14, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import datetime
import math
import mom

def featOBV(dData):
    dfPt = dData['close']
    dfPt1 = dfPt.shift(1)
    dfOBV = pand.DataFrame(data=np.zeros(dfPt.values.shape), index=dfPt.index, columns=dfPt.columns)
    for column in dfOBV:
        first = True
        last_obv = 0
        for row, index in dfOBV[column].iteritems():
            if first == True:
                first = False
                continue
            if dfPt.get_value(row, column) > dfPt1.get_value(row, column):
                last_obv = last_obv + dData['volume'].get_value(row, column)
            elif dfPt.get_value(row, column) < dfPt1.get_value(row, column):
                last_obv = last_obv - dData['volume'].get_value(row, column)
            else:
                last_obv = 0
            dfOBV.set_value(row, column, last_obv)
    dfOBV.values[0, :] = np.nan
    return dfOBV    

def featADL(dData):
    dfCLV = (2 * dData['close'] - dData['low'] - dData['high']) / (dData['high'] - dData['low'])
    return dfCLV * dData['volume']

def featCHO(dData, lLookback1=3, lLookback2=10):
    dfADL = featADL(dData)
    return pand.ewma(dfADL, lLookback1) - pand.ewma(dfADL, lLookback2)

def featChaikinTradeRule(dData, lLookback1=3, lLookback2=10):
    rule_func = np.vectorize(lambda y: math.copysign(1, y))
    dfCHO = featCHO(dData, lLookback1, lLookback2)
    return pand.DataFrame(data=rule_func(dfCHO.values), index=dfCHO.index, columns=dfCHO.columns)

def featNVI(dData, iInitValue=100):
    dfROC = mom.featROC(dData, lLookback=1)
    dfNVI = pand.DataFrame(data=np.empty(dfROC.values.shape), index=dfROC.index, columns=dfROC.columns)
    dfNVI.values[:, :] = iInitValue
    dfVOL = dData['volume']
    dfVOLt1 = dfVOL.shift(1)
    
    for column in dfNVI:
        first = True
        last_obv = iInitValue
        for row, index in dfNVI[column].iteritems():
            if first == True:
                first = False
                continue
            if dfVOL.get_value(row, column) < dfVOLt1.get_value(row, column):
                last_obv = last_obv + last_obv * dfROC.get_value(row, column)
            dfNVI.set_value(row, column, last_obv)
    return dfNVI
    
def featPVI(dData, iInitValue=100):
    dfROC = mom.featROC(dData, lLookback=1)
    dfPVI = pand.DataFrame(data=np.empty(dfROC.values.shape), index=dfROC.index, columns=dfROC.columns)
    dfPVI.values[:, :] = iInitValue
    dfVOL = dData['volume']
    dfVOLt1 = dfVOL.shift(1)
    
    for column in dfPVI:
        first = True
        last_obv = iInitValue
        for row, index in dfPVI[column].iteritems():
            if first == True:
                first = False
                continue
            if dfVOL.get_value(row, column) >= dfVOLt1.get_value(row, column):
                last_obv = last_obv + last_obv * dfROC.get_value(row, column)
            dfPVI.set_value(row, column, last_obv)
    return dfPVI

def tradeRuleNVI(nvit1, nvi, sma):
    if math.isnan(nvit1) or math.isnan(nvi) or math.isnan(sma):
        return np.nan
    if nvit1 <= sma and nvi > sma:
        return 1  # buy
    else:
        return 0  # hold 

def featNVITradeRule(dData, lLookback=10):
    dfNVI = featNVI(dData)
    dfNVIt1 = dfNVI.shift(1)
    dfSMA = pand.rolling_mean(dfNVI, lLookback)
    rule_func = np.vectorize(tradeRuleNVI)
    return pand.DataFrame(data=rule_func(dfNVIt1, dfNVI, dfSMA), index=dfNVI.index, columns=dfNVI.columns)

def tradeRulePVI(pvit1, pvi, sma):
    if math.isnan(pvit1) or math.isnan(pvi) or math.isnan(sma):
        return np.nan
    if pvit1 <= sma and pvi > sma:
        return 1  # buy
    if pvit1 >= sma and pvi < sma:
        return -1  # sell 
    else:
        return 0  # hold 

def featPVITradeRule(dData, lLookback=10):
    dfPVI = featPVI(dData)
    dfPVIt1 = dfPVI.shift(1)
    dfSMA = pand.rolling_mean(dfPVI, lLookback)
    rule_func = np.vectorize(tradeRulePVI)
    return pand.DataFrame(data=rule_func(dfPVIt1, dfPVI, dfSMA), index=dfPVI.index, columns=dfPVI.columns)

def featNVI2SMA(dData, lLookback=10):
    dfNVI = featNVI(dData)
    dfSMA = pand.rolling_mean(dfNVI, lLookback)
    return dfNVI / dfSMA

def featPVI2SMA(dData, lLookback=10):
    dfPVI = featNVI(dData)
    dfSMA = pand.rolling_mean(dfPVI, lLookback)
    return dfPVI / dfSMA

def featPriceVolumeTrend(dData):
    dfROC = mom.featROC(dData, serie='close', lLookback = 1)
    dfPV = dData['volume'] * dfROC
    return pand.rolling_sum(dfPV, 1)
    
