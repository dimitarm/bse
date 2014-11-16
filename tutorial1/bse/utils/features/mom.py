'''
Created on Nov 6, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import bse.utils.features.price as pricefeat
import math
import price as price


def featMomentum(dFullData, serie='close', lLookback=12):
    '''
    @summary: price change in the last n periods
    '''
    dfPtn = dFullData[serie].shift(lLookback)
    return dFullData[serie] - dfPtn

def featMomentum2Ema(dFullData, serie='close', slow=6, lLookback=12):
    dfMomentum = featMomentum(dFullData, serie, lLookback)
    dDataMOM = {}
    dDataMOM[serie] = dfMomentum
    dfEmaMom = pricefeat.featEMA(dDataMOM, serie=serie, lLookback=slow)
    return dfMomentum / dfEmaMom

def featMomentumTradeRule(dFullData, serie='close', slow=10, lLookback=20):
    dfMomentum = featMomentum(dFullData, serie, lLookback)
    dfMomentum1 = dfMomentum.shift(1)
    
    dDataMOM = {}
    dDataMOM[serie] = dfMomentum
    dfEmaMom = pricefeat.featEMA(dDataMOM, serie=serie, lLookback=slow)

    ruleFunc = np.vectorize(tradeRuleMomentum)
    return pand.DataFrame(data=ruleFunc(dfMomentum, dfMomentum1, dfEmaMom), index=dfMomentum.index, columns=dfMomentum.columns)

def tradeRuleMomentum(mom, momt1, ema):
    if math.isnan(mom) or math.isnan(momt1) or math.isnan(ema):
        return np.nan
    if momt1 <= ema and mom > ema:
        return 1  # buy
    if momt1 >= ema and mom < ema:
        return -1  # sell
    return 0  # hold

def featAcceleration(dFullData, serie='close', lLookback=12):
    dfMomentum = featMomentum(dFullData, serie, lLookback)
    dfMomentum1 = dfMomentum.shift(1)
    return dfMomentum - dfMomentum1

def featAccelerationTradingRule(dFullData, serie='close', lLookback=20):
    dfAcceleration = featAcceleration(dFullData, serie, lLookback)
    dfAcceleration1 = dfAcceleration.shift(1)
    ruleFunc = np.vectorize(tradeRuleAcceleration)
    return pand.DataFrame(data=ruleFunc(dfAcceleration, dfAcceleration1), index=dfAcceleration.index, columns=dfAcceleration.columns)
 
def tradeRuleAcceleration(accel, accel1):
    if math.isnan(accel) or math.isnan(accel):
        return np.nan
    if accel1 + 1 <= 0 and accel + 1 > 0:
        return 1  # buy
    if accel1 + 1 >= 0 and accel + 1 < 0:
        return -1  # sell
    return 0  # hold

def featROC(dFullData, serie='close', lLookback=10):
    dfPrice = dFullData[serie]
    dfPriceTn = dfPrice.shift(lLookback)
    return ((dfPrice - dfPriceTn) * 100) / dfPriceTn

def featROCTradingRule(dFullData, serie='close', lLookback=10):
    dfRoc = featROC(dFullData, serie, lLookback)
    dfRoc1 = dfRoc.shift(1)
    ruleFunc = np.vectorize(tradeRuleRoc)
    return pand.DataFrame(data=ruleFunc(dfRoc, dfRoc1), index=dfRoc.index, columns=dfRoc.columns) 

def tradeRuleRoc(roc, roc1):
    if math.isnan(roc) or math.isnan(roc1):
        return np.nan
    if roc1 <= 0 and roc > 0:
        return 1  # buy
    if roc1 >= 0 and roc < 0:
        return -1  # sell
    return 0  # hold

def featMACD(dFullData, slow=26, fast=12):
    dfSlow = price.featEMA(dFullData, lLookback=slow, bRel=False)
    dfFast = price.featEMA(dFullData, lLookback=fast, bRel=False) 
    return dfFast - dfSlow
    
def featMACDS(dFullData, slow=26, fast=12, lLookback=9):
    if slow <= fast:
        raise Exception("slow must be bigger that fast")
    dPrice = dFullData['close']
    for serie in dPrice:
        if dPrice[serie].size <= (slow + lLookback) * price.EMA_MIN_DATA_COUNT:
            raise Exception('data is not sufficient for MACDS')
    dfMacd = featMACD(dFullData, slow=slow, fast=fast)
    dTmp = {}
    dTmp['close'] = dfMacd
    dfMacds = price.featEMA(dTmp, lLookback=lLookback, bRel=False)
    for serie in dfMacds:
        for i in range(0, (slow + lLookback) * price.EMA_MIN_DATA_COUNT):
            dfMacds[serie].iat[i] = np.nan    
    return dfMacds
    
def featMACDTradingRule(dFullData, slow=26, fast=12, lLookback=9):
    dfMacd = featMACD(dFullData, slow=slow, fast=fast)
    dfMacdt1 = dfMacd.shift(1)
    dfMacds = featMACDS(dFullData, slow=slow, fast=fast, lLookback=lLookback)
    ruleFunc = np.vectorize(tradeRuleMACD)
    return pand.DataFrame(data=ruleFunc(dfMacdt1, dfMacd, dfMacds), index=dfMacd.index, columns=dfMacd.columns)
    
def tradeRuleMACD(macdt1, macd, macds):
    if math.isnan(macdt1) or math.isnan(macd) or math.isnan(macds):
        return np.nan
    if macdt1 <= macds and macd > macds:
        return 1  # buy
    if macdt1 >= macds and macd < macds:
        return -1  # sell
    return 0  # hold

def featMACDR(dFullData, slow=26, fast=12, lLookback=9):
    dfMACD = featMACD(dFullData, slow = slow, fast = fast)
    dfMACDS = featMACDS(dFullData, slow = slow, fast = fast, lLookback = lLookback)
    return dfMACD/dfMACDS   

def featRSI( dFullData, lLookback=14):
    '''
    @summary: Calculate RSI
    @param dFullData: Dictionary of data to use
    @param lLookback: Number of days to look in the past, 14 is standard
    @param b_human: if true return dataframe to plot
    @return: DataFrame array containing values
    '''

    # create deltas per day
    dfDelta = dFullData['close'].copy()
    dfDelta.iloc[1:,:] -= dfDelta.iloc[:-1,:].values
    dfDelta.iloc[0,:] = np.NAN

    dfDeltaUp = dfDelta
    dfDeltaDown = dfDelta.copy()
    
    # seperate data into positive and negative for easy calculations
    for sColumn in dfDeltaUp.columns:
        tsColDown = dfDeltaDown[sColumn]
        tsColDown[tsColDown >= 0] = 0 
        
        tsColUp = dfDeltaUp[sColumn]
        tsColUp[tsColUp <= 0] = 0
    
    # Note we take abs() of negative values, all should be positive now
    dfRolUp = pand.rolling_mean(dfDeltaUp, lLookback, min_periods=1)
    dfRolDown = pand.rolling_mean(dfDeltaDown, lLookback, min_periods=1).abs()
    
    # relative strength
    dfRS = dfRolUp / dfRolDown
    dfRSI = 100.0 - (100.0 / (1.0 + dfRS))
    return dfRSI


def featRSITradingRule(dFullData, lLookback=9):
    dfRSI = featRSI(dFullData, lLookback=lLookback)
    dfRSIt1 = dfRSI.shift(1)
    ruleFunc = np.vectorize(tradeRuleRSI)
    return pand.DataFrame(data=ruleFunc(dfRSIt1, dfRSI), index=dfRSI.index, columns=dfRSI.columns)

def tradeRuleRSI(rsit1, rsi):
    if math.isnan(rsit1) or math.isnan(rsi):
        return np.nan
    if rsit1 >= 30 and rsi < 70:
        return 1  # buy
    if rsit1 <= 30 and rsi > 70:
        return -1  # sell
    return 0  # hold

