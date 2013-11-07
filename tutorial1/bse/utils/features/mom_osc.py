'''
Created on Nov 6, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import bse.utils.features.price as pricefeat
import QSTK.qstkfeat.features as qstkfeat
import math


def featMomentum(dData, serie='close', lLookback=20):
    '''
    @summary: price change in the last n periods
    '''
    dfPtn = dData[serie].shift(lLookback)
    return dData[serie] - dfPtn

def featMomentum2Ema(dData, serie='close', lambd=0.75, lLookback=20):
    dfMomentum = featMomentum(dData, serie, lLookback)
    dDataMOM = {}
    dDataMOM[serie] = dfMomentum
    dfEmaMom = pricefeat.featEMAlambda(dDataMOM, serie=serie, lambd=lambd)
    return dfMomentum / dfEmaMom

def featMomentumTradeRule(dData, serie='close', lambd=0.75, lLookback=20):
    dfMomentum = featMomentum(dData, serie, lLookback)
    dfMomentum1 = dfMomentum.shift(1)
    
    dDataMOM = {}
    dDataMOM[serie] = dfMomentum
    dfEmaMom = pricefeat.featEMAlambda(dDataMOM, serie=serie, lambd=lambd)

    ruleFunc = np.vectorize(tradeRuleMomentum)
    return pand.DataFrame(data=ruleFunc(dfMomentum.values, dfMomentum1.values, dfEmaMom.values), index=dfMomentum.index, columns=dfMomentum.columns)

def tradeRuleMomentum(mom, momt1, ema):
    if mom == np.nan or momt1 == np.nan or ema == np.nan:
        return np.nan
    if momt1 <= ema and mom > ema:
        return 1  # buy
    if momt1 >= ema and mom < ema:
        return -1  # sell
    return 0  # hold

def featAcceleration(dData, serie='close', lLookback=20):
    dfMomentum = featMomentum(dData, serie, lLookback)
    dfMomentum1 = dfMomentum.shift(1)
    return dfMomentum - dfMomentum1

def featAccelerationTradingRule(dData, serie='close', lLookback=20):
    dfAcceleration = featAcceleration(dData, serie, lLookback)
    dfAcceleration1 = dfAcceleration.shift(1)
    ruleFunc = np.vectorize(tradeRuleAcceleration)
    return pand.DataFrame(data=ruleFunc(dfAcceleration, dfAcceleration1), index=dfAcceleration.index, columns=dfAcceleration.columns)
 
def tradeRuleAcceleration(accel, accel1):
    if accel == np.nan or accel1 == np.nan:
        return np.nan
    if accel1 + 1 <= 0 and accel + 1 > 0:
        return 1  # buy
    if accel1 + 1 >= 0 and accel + 1 < 0:
        return -1  # sell
    return 0  # hold

def featRateOfChange(dData, serie='close', lLookback=10):
    dfPrice = dData[serie]
    dfPriceTn = dfPrice.shift(lLookback)
    return ((dfPrice - dfPriceTn) * 100) / dfPriceTn

def featRateOfChangeTradingRule(dData, serie='close', lLookback=10):
    dfRoc = featRateOfChange(dData, serie, lLookback)
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

def featMACD(dData, slow=26, fast=12):
    dfSlow = qstkfeat.featEMA(dData, lLookback=slow, bRel=False)
    dfFast = qstkfeat.featEMA(dData, lLookback=fast, bRel=False) 
    return dfSlow - dfFast
    
def featMACDS(dData, slow=26, fast=12, lLookback=9):    
    dfMacd = featMACD(dData, slow=slow, fast=fast)
    dTmp = {}
    dTmp['close'] = dfMacd
    return qstkfeat.featEMA(dData, lLookback=lLookback, bRel=False)
    
def featMACDTradingRule(dData, slow=26, fast=12, lLookback=9):
    dfMacd = featMACD(dData, slow=slow, fast=fast)
    dfMacdt1 = dfMacd.shift(1)
    dfMacds = featMACDS(dData, slow=slow, fast=fast, lLookback=lLookback)
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

def featRSITradingRule(dData, lLookback = 9):
    dfRSI = qstkfeat.featRSI(dData, lLookback = lLookback)
    dfRSIt1 = dfRSI.shift(1)
    ruleFunc = np.vectorize(tradeRuleRSI)
    return pand.DataFrame(data=ruleFunc(dfRSIt1, dfRSI), index = dfRSI.index, columns=dfRSI.columns)

def tradeRuleRSI(rsit1, rsi):
    if math.isnan(rsit1) or math.isnan(rsi):
        return np.nan
    if rsit1 >= 30 and rsi < 70:
        return 1 #buy
    if rsit1 <= 30 and rsi > 70:
        return -1 #sell
    return 0 #hold

if __name__ == '__main__':
        
    dData = {}
    dData['close'] = pand.DataFrame(data=np.random.rand(100, 2) * 10, columns=('aaaaaa', 'bb'), index = range(100))
    print featRSITradingRule(dData, lLookback=2)
