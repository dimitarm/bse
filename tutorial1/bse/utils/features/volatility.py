'''
Created on Nov 13, 2013

@author: dimitar
'''
import pandas as pand

def featCHV(dFullData, lLookback=10):
    dfDiff = dFullData['high'] - dFullData['low']
    dfDiffEMA = pand.ewma(dfDiff, span=10)
    dfDiffEMAn = dfDiffEMA.shift(lLookback)
    return dfDiffEMA / dfDiffEMAn - 1

def featGK(dFullData):
    u = dFullData['high'] - dFullData['open']
    d = dFullData['low'] - dFullData['open']
    firstTerm = 0.511 * ((u - d) ** 2)
    secondterm = 0.019 * (dFullData['AdjClose'] ** 2) * (u + d)
    thirdTerm = 2 * u * d
    fourthTerm = 0.383 * (dFullData['close'] ** 2)
    sigma = firstTerm - secondterm - thirdTerm - fourthTerm
    return 0.631578947 * (dFullData['open'] - dFullData['close']) + 1.086419753 * sigma 

def featSharpeRatio(dFullData, lLookback = 26): 
    dfRet = dFullData['close'] - dFullData['close'].shift(lLookback)
    return dfRet / pand.rolling_std(dFullData['close'], lLookback)
    
if __name__ == '__main__':
    pass
