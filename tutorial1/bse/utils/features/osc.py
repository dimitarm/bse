'''
Created on Nov 7, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import QSTK.qstkfeat.features as qstkfeat
import math 

def featFASTK(dFullData, serie='close', lLookback=12):
    dfPrice = dFullData[serie]
    dfLowestLow = pand.rolling_min(dFullData['low'], lLookback)
    dfHighestHigh = pand.rolling_max(dFullData['high'], lLookback)
    return 100 * (dfPrice - dfLowestLow) / (dfHighestHigh - dfLowestLow)

def featFASTD(dFullData, serie='close', lLookback=12):
    dfFAST = featFASTK(dFullData, serie=serie, lLookback=lLookback)
    dTmp = {}
    dTmp['close'] = dfFAST
    return qstkfeat.featEMA(dTmp, lLookback=3, bRel=False)

def featSLOWK(dFullData, serie='close', lLookback=12):
    return featFASTD(dFullData, serie, lLookback)

def featSLOWD(dFullData, serie='close', lLookback=12):
    dfSLOW = featSLOWK(dFullData, serie=serie, lLookback=lLookback)
    dTmp = {}
    dTmp['close'] = dfSLOW
    return qstkfeat.featEMA(dTmp, lLookback=3, bRel=False)

def featSLOWTradingRule(dFullData, serie='close', lLookback=12):
    dfSlowkt = featSLOWK(dFullData=dFullData, serie=serie, lLookback=lLookback)
    dfSlowkt1 = dfSlowkt.shift(1)
    dfSlowd = featSLOWD(dFullData=dFullData, serie=serie, lLookback=lLookback)
    rule_func = np.vectorize(tradeRuleSLOW)
    return pand.DataFrame(data=rule_func(dfSlowkt1, dfSlowkt, dfSlowd), index=dfSlowkt.index, columns=dfSlowkt.columns)

def tradeRuleSLOW(slowkt1, slowkt, slowd):
    if math.isnan(slowkt1) or math.isnan(slowkt) or math.isnan(slowd):
        return np.nan
    if slowkt1 <= slowd and slowkt > slowd:
        return 1  # buy
    if slowkt1 >= slowd and slowkt < slowd:
        return -1  # sell
    return 0  # hold

def tradeRuleFAST(fastkt1, fastkt, fastd):
    if math.isnan(fastkt1) or math.isnan(fastkt) or math.isnan(fastd):
        return np.nan
    if fastkt1 <= fastd and fastkt > fastd:
        return 1  # buy
    if fastkt1 >= fastd and fastkt < fastd:
        return -1  # sell
    return 0  # hold

def featFASTTradingRule(dFullData, serie='close', lLookback=12):
    dfFastkt = featFASTK(dFullData=dFullData, serie=serie, lLookback=lLookback)
    dfFastkt1 = dfFastkt.shift(1)
    dfFastd = featFASTD(dFullData=dFullData, serie=serie, lLookback=lLookback)
    rule_func = np.vectorize(tradeRuleFAST)
    return pand.DataFrame(data=rule_func(dfFastkt1, dfFastkt, dfFastd), index=dfFastkt.index, columns=dfFastkt.columns)
    
def featFastKFastD(dFullData, serie='close', lLookback=12):
    return featFASTK(dFullData, serie, lLookback) / featFASTD(dFullData, serie, lLookback)

def featSlowKSlowD(dFullData, serie='close', lLookback=12):
    return featSLOWK(dFullData, serie, lLookback) / featSLOWD(dFullData, serie, lLookback)

def featWILL(dFullData, serie='close', lLookback=14):
    dfPrice = dFullData[serie]
    dfLowestLow = pand.rolling_min(dFullData['low'], lLookback)
    dfHighestHigh = pand.rolling_max(dFullData['high'], lLookback)
    return (dfHighestHigh - dfPrice) * -100 / (dfHighestHigh - dfLowestLow)

def tradeRuleWILL(willt1, will):
    if math.isnan(will) or math.isnan(willt1):
        return np.nan
    if willt1 >= -20 and will < -80:
        return 1  # buy
    if willt1 <= -20 and will > -80:
        return -1  # sell
    return 0  # hold

def featWILLTradingRule(dFullData, serie='close', lLookback=14):
    dfWill = featWILL(dFullData, serie, lLookback)
    dfWillt1 = dfWill.shift(1)
    rule_func = np.vectorize(tradeRuleWILL)
    return pand.DataFrame(data=rule_func(dfWillt1, dfWill), index=dfWill.index, columns=dfWill.columns)

def featTypicalPrice(dFullData):
    return (dFullData['high'] + dFullData['low'] + dFullData['close']) / 3

def featMFI(dFullData, lLookback=14):
    dfPriceTyp = featTypicalPrice(dFullData)
    dfMF = dfPriceTyp * dFullData['volume']
    dfPriceTypt1 = dfPriceTyp.shift(1)
    dfUptrend = dfPriceTyp > dfPriceTypt1
    dfPosMF = pand.DataFrame(data=np.zeros(dfPriceTyp.values.shape), index=dfPriceTyp.index, columns=dfPriceTyp.columns)
    dfNegMF = pand.DataFrame(data=np.zeros(dfPriceTyp.values.shape), index=dfPriceTyp.index, columns=dfPriceTyp.columns)
    
    for col in dfUptrend:
        first = True
        for index, value in dfUptrend[col].iteritems():
            if first:
                dfPosMF.set_value(index, col, np.nan)
                dfNegMF.set_value(index, col, np.nan)
                first = False
            else: 
                if value == True:
                    dfPosMF.set_value(index, col, dfMF.get_value(index, col))
                else:
                    dfNegMF.set_value(index, col, dfMF.get_value(index, col))
    dfPosMF = pand.rolling_sum(dfPosMF, lLookback)
    dfNegMF = pand.rolling_sum(dfNegMF, lLookback)
    dfMFRatio = dfPosMF / dfNegMF
    dfMFI = 100 - 100 / (1 + dfMFRatio)
    #check for dfNegNF values which are 0
    #for those values dfMFI should be 100
    for col in dfNegMF:
        for index, value in dfNegMF[col].iteritems():
            if value == 0:
                dfMFI.set_value(index, col, 100)
    
    return dfMFI

def tradeRuleMFI(mfit1, mfi):
    if math.isnan(mfit1) or math.isnan(mfi):
        return np.nan
    if mfit1 >= 30 and mfi < 70:
        return 1 #buy
    if mfit1 <= 30 and mfi > 70:
        return -1 #sell
    return 0 #hold

def featMFITradingRule(dFullData, lLookback = 14):
    dfMFI = featMFI(dFullData, lLookback)
    dfMFIt1 = dfMFI.shift(1)
    rule_func = np.vectorize(tradeRuleMFI)
    return pand.DataFrame(data=rule_func(dfMFIt1, dfMFI), index=dfMFI.index, columns=dfMFI.columns)    
    
    
    


