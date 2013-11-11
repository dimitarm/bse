'''
Created on Nov 7, 2013

@author: dimitar
'''
import pandas as pand
import numpy as np
import QSTK.qstkfeat.features as qstkfeat
import math 

def featFAST(dData, serie = 'close', lLookback = 12):
    dfPrice = dData[serie]
    dfLowestLow = pand.rolling_min(dData['low'], lLookback)
    dfHighestHigh = pand.rolling_max(dData['high'], lLookback)
    return (dfPrice - dfLowestLow)/(dfHighestHigh - dfLowestLow)

def featFASTD(dData, serie = 'close', lLookback = 12):
    dfFAST = featFAST(dData, serie = serie, lLookback = lLookback)
    dTmp = {}
    dTmp['close'] = dfFAST
    return qstkfeat.featEMA(dData, lLookback=3, bRel=False)        