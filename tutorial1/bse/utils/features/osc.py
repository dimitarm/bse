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
    return (dfPrice - dfLowestLow) / (dfHighestHigh - dfLowestLow)

def featFASTD(dData, serie='close', lLookback=3):
    dfFAST = featFASTK(dData, serie=serie, lLookback=lLookback)
    dTmp = {}
    dTmp['close'] = dfFAST
    return qstkfeat.featEMA(dData, lLookback=3, bRel=False)

def tradeRuleFAST(fastkt1, fastkt, fastd):
    if math.isnan(fastkt1) or math.isnan(fastkt) or math.isnan(fastd):
        return np.nan
    if fastkt1 <= fastd and fastkt > fastd:
        return 1  # buy
    if fastkt1 >= fastd and fastkt < fastd:
        return -1  # sell
    return 0  # hold

def featFASTTradingRule(dData, serie='close', lLookback=12):
    dfFastkt = featFASTK(dData=dData, serie=serie, lLookBack=lLookback)
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
        for index, value in dfUptrend[col].iteritems():
            if value == True:
                dfPosMF.set_value(index, col, dfMF.get_value(index, col))
            else:
                dfNegMF.set_value(index, col, dfMF.get_value(index, col))
    dfPosMF = pand.rolling_sum(dfPosMF, lLookback)
    dfNegMF = pand.rolling_sum(dfNegMF, lLookback)
    dfMFRatio = dfPosMF / dfNegMF
    return 100 - 100 * (1 + dfMFRatio)

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
    
    
    
if __name__ == '__main__':
        
    dData = {}
    dData['close'] = pand.DataFrame(data= {'aaaaaa': (24.6324666667,24.6889,24.9908666667,25.3591666667,25.1866333333,25.1667333333,25.0074666667,24.958,25.0837666667,25.2497,25.2132,25.3708333333,25.6147,25.5782,25.4554333333,25.326,25.0904,25.0273333333,24.9145333333,24.8946,25.1269333333,24.6358,24.5097,24.1546333333,23.9771,24.0650333333,24.3603666667,24.3504,24.1446666667,24.81)})
    dData['volume'] = pand.DataFrame(data={'aaaaaa': (18730.14,12271.74,24691.41,18357.61,22964.08,15918.95,16067.04,16568.49,16018.73,9773.57,22572.71,12986.67,10906.66,5799.26,7395.27,5818.16,7164.73,5672.91,5624.74,5023.47,7457.09,11798.01,12366.13,13294.87,9256.87,9690.60,8870.32,7168.97,11356.18,13379.37)})
    

    print featMFI(dData, lLookback=14)


