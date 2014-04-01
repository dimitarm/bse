'''
Created on Nov 14, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import datetime
import math
import mom
import sys

def featOBV(dFullData):
    dfPt = dFullData['close']
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
                last_obv = last_obv + dFullData['volumes'].get_value(row, column)
            elif dfPt.get_value(row, column) < dfPt1.get_value(row, column):
                last_obv = last_obv - dFullData['volumes'].get_value(row, column)
            else:
                last_obv = 0
            dfOBV.set_value(row, column, last_obv)
    dfOBV.values[0, :] = np.nan
    return dfOBV    

def featADL(dFullData):
    dfCLV = (2 * dFullData['close'] - dFullData['low'] - dFullData['high']) / (dFullData['high'] - dFullData['low'])
    dfADL = dfCLV * dFullData['volumes']
    dfADL.values[np.isnan(dfADL.values)]=0
    return dfADL

def featCHO(dFullData, lLookback1=3, lLookback2=10):
    dfADL = featADL(dFullData)
    return pand.ewma(dfADL, lLookback1) - pand.ewma(dfADL, lLookback2)

def featChaikinTradeRule(dFullData, lLookback1=3, lLookback2=10):
    rule_func = np.vectorize(lambda y: math.copysign(1, y))
    dfCHO = featCHO(dFullData, lLookback1, lLookback2)
    return pand.DataFrame(data=rule_func(dfCHO.values), index=dfCHO.index, columns=dfCHO.columns)

def featNVI(dFullData, iInitValue=100):
    dfROC = mom.featROC(dFullData, lLookback=1)
    dfNVI = pand.DataFrame(data=np.empty(dfROC.values.shape), index=dfROC.index, columns=dfROC.columns)
    dfNVI.values[:, :] = iInitValue
    dfVOL = dFullData['volumes']
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
    
def featPVI(dFullData, iInitValue=100):
    dfROC = mom.featROC(dFullData, lLookback=1)
    dfPVI = pand.DataFrame(data=np.empty(dfROC.values.shape), index=dfROC.index, columns=dfROC.columns)
    dfPVI.values[:, :] = iInitValue
    dfVOL = dFullData['volumes']
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

def featNVITradeRule(dFullData, lLookback=10):
    dfNVI = featNVI(dFullData)
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

def featPVITradeRule(dFullData, lLookback=10):
    dfPVI = featPVI(dFullData)
    dfPVIt1 = dfPVI.shift(1)
    dfSMA = pand.rolling_mean(dfPVI, lLookback)
    rule_func = np.vectorize(tradeRulePVI)
    return pand.DataFrame(data=rule_func(dfPVIt1, dfPVI, dfSMA), index=dfPVI.index, columns=dfPVI.columns)

def featNVI2SMA(dFullData, lLookback=10):
    dfNVI = featNVI(dFullData)
    dfSMA = pand.rolling_mean(dfNVI, lLookback)
    dfResult = dfNVI / dfSMA
    dfResult = dfResult.replace([np.inf, -np.inf], [sys.float_info.max, -sys.float_info.max])    
    return dfResult    

def featPVI2SMA(dFullData, lLookback=10):
    dfPVI = featNVI(dFullData)
    dfSMA = pand.rolling_mean(dfPVI, lLookback)
    dfResult = dfPVI / dfSMA
    return dfResult.replace([np.inf, -np.inf], [sys.float_info.max, -sys.float_info.max])

def featPriceVolumeTrend(dFullData):
    dfROC = mom.featROC(dFullData, serie='close', lLookback = 1)
    dfPV = dFullData['volumes'] * dfROC
    return pand.rolling_sum(dfPV, 1)
    
