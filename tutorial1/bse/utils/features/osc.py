'''
Created on Nov 7, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import QSTK.qstkfeat.features as qstkfeat
import math 

def featFASTK(dData, serie='close', lLookback=12):
    dfPrice = dData[serie]
    dfLowestLow = pand.rolling_min(dData['low'], lLookback)
    dfHighestHigh = pand.rolling_max(dData['high'], lLookback)
    return 100 * (dfPrice - dfLowestLow) / (dfHighestHigh - dfLowestLow)

def featFASTD(dData, serie='close', lLookback=3):
    dfFAST = featFASTK(dData, serie=serie, lLookback=lLookback)
    dTmp = {}
    dTmp['close'] = dfFAST
    return qstkfeat.featEMA(dTmp, lLookback=3, bRel=False)

def tradeRuleFAST(fastkt1, fastkt, fastd):
    if math.isnan(fastkt1) or math.isnan(fastkt) or math.isnan(fastd):
        return np.nan
    if fastkt1 <= fastd and fastkt > fastd:
        return 1  # buy
    if fastkt1 >= fastd and fastkt < fastd:
        return -1  # sell
    return 0  # hold

def featFASTTradingRule(dData, serie='close', lLookback=12):
    dfFastkt = featFASTK(dData=dData, serie=serie, lLookback=lLookback)
    dfFastkt1 = dfFastkt.shift(1)
    dfFastd = featFASTD(dData=dData, serie=serie, lLookback=lLookback)
    rule_func = np.vectorize(tradeRuleFAST)
    return pand.DataFrame(data=rule_func(dfFastkt1, dfFastkt, dfFastd), index=dfFastkt.index, columns=dfFastkt.columns)
    
def featFastKFastD(dData, serie='close', lLookback=12):
    return featFASTK(dData, serie, lLookback) / featFASTD(dData, serie, lLookback)

def featWILL(dData, serie='close', lLookback=14):
    dfPrice = dData[serie]
    dfLowestLow = pand.rolling_min(dData['low'], lLookback)
    dfHighestHigh = pand.rolling_max(dData['high'], lLookback)
    return (dfHighestHigh - dfPrice) * -100 / (dfHighestHigh - dfLowestLow)

def tradeRuleWILL(willt1, will):
    if math.isnan(will) or math.isnan(willt1):
        return np.nan
    if willt1 >= -20 and will < -80:
        return 1  # buy
    if willt1 <= -20 and will > -80:
        return -1  # sell
    return 0  # hold

def featWILLTradingRule(dData, serie='close', lLookback=14):
    dfWill = featWILL(dData, serie, lLookback)
    dfWillt1 = dfWill.shift(1)
    rule_func = np.vectorize(tradeRuleWILL)
    return pand.DataFrame(data=rule_func(dfWillt1, dfWill), index=dfWill.index, columns=dfWill.columns)

def featTypicalPrice(dData):
    return (dData['high'] + dData['low'] + dData['close']) / 3

def featMFI(dData, lLookback=14):
    dfPriceTyp = featTypicalPrice(dData)
    dfMF = dfPriceTyp * dData['volume']
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

def featMFITradingRule(dData, lLookback = 14):
    dfMFI = featMFI(dData, lLookback)
    dfMFIt1 = dfMFI.shift(1)
    rule_func = np.vectorize(tradeRuleMFI)
    return pand.DataFrame(data=rule_func(dfMFIt1, dfMFI), index=dfMFI.index, columns=dfMFI.columns)    
    
    
    


