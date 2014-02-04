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
    return pand.DataFrame(data=ruleFunc(dfMomentum, dfMomentum1, dfEmaMom), index=dfMomentum.index, columns=dfMomentum.columns)

def tradeRuleMomentum(mom, momt1, ema):
    if math.isnan(mom) or math.isnan(momt1) or math.isnan(ema):
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
    if math.isnan(accel) or math.isnan(accel):
        return np.nan
    if accel1 + 1 <= 0 and accel + 1 > 0:
        return 1  # buy
    if accel1 + 1 >= 0 and accel + 1 < 0:
        return -1  # sell
    return 0  # hold

def featROC(dData, serie='close', lLookback=10):
    dfPrice = dData[serie]
    dfPriceTn = dfPrice.shift(lLookback)
    return ((dfPrice - dfPriceTn) * 100) / dfPriceTn

def featRateOfChangeTradingRule(dData, serie='close', lLookback=10):
    dfRoc = featROC(dData, serie, lLookback)
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

def featMACDR(dData, slow=26, fast=12, lLookback=9):
    dfMACD = featMACD(dData, slow = slow, fast = fast)
    dfMACDS = featMACDS(dData, slow = slow, fast = fast, lLookback = lLookback)
    return dfMACD/dfMACDS   

def featRSITradingRule(dData, lLookback=9):
    dfRSI = qstkfeat.featRSI(dData, lLookback=lLookback)
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

if __name__ == '__main__':
        
    dData = {}
    dData['close'] = pand.DataFrame(data=[86.1557,89.0867,88.7829,90.3228,89.0671,91.1453,89.4397,89.175,86.9302,87.6752,86.9596,89.4299,89.3221,88.7241,87.4497,87.2634,89.4985,87.9006,89.126,90.7043,92.9001,92.9784,91.8021,92.6647,92.6843,92.3021,92.7725,92.5373,92.949,93.2039,91.0669,89.8318,89.7435,90.3994,90.7387,88.0177,88.0867,88.8439,90.7781,90.5416,91.3894,90.65], columns=['aaaaaa'])
    print featRSITradingRule(dData, lLookback=5)
