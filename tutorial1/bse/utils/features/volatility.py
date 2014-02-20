'''
Created on Nov 13, 2013

@author: dimitar
'''
import pandas as pand

def featCHV(dData, lLookback=10):
    dfDiff = dData['high'] - dData['low']
    dfDiffEMA = pand.ewma(dfDiff, span=10)
    dfDiffEMAn = dfDiffEMA.shift(lLookback)
    return dfDiffEMA / dfDiffEMAn - 1

def featGK(dData):
    u = dData['high'] - dData['open']
    d = dData['low'] - dData['open']
    firstTerm = 0.511 * ((u - d) ** 2)
    secondterm = 0.019 * (dData['AdjClose'] ** 2) * (u + d)
    thirdTerm = 2 * u * d
    fourthTerm = 0.383 * (dData['close'] ** 2)
    sigma = firstTerm - secondterm - thirdTerm - fourthTerm
    return 0.631578947 * (dData['open'] - dData['close']) + 1.086419753 * sigma 

def featSharpeRatio(dData, risk_free_rate): 
    return (dData['close'] - risk_free_rate) / dData['close'].std()
    
    
    
if __name__ == '__main__':
    pass
