'''
Created on Nov 13, 2013

@author: dimitar
'''

import unittest
import pandas as pd
import bse.utils.features.mom as mom
import numpy as np
import talib as ta
import bse.utils.features.price as price

class Test(unittest.TestCase):

    def setUp(self):
        pass
    
    def testMomentum(self):
        npData = np.random.random(100)
        dfData = pd.DataFrame(npData)
        dData = {}
        dData['close'] = dfData
        bseMom = mom.featMomentum(dData, serie = 'close', lLookback = 10)
        taMom = ta.MOM(real = npData, timeperiod = 10)
        np.testing.assert_equal(bseMom.values.ravel(), taMom.ravel(), verbose = True)
    
    def testROC(self):
        npData = np.random.random(100)
        dfData = pd.DataFrame(npData)
        dData = {}
        dData['close'] = dfData
        bseRoc = mom.featROC(dData, serie = 'close', lLookback = 10)
        taRoc = ta.ROC(real = npData, timeperiod = 10)
        np.testing.assert_array_almost_equal(bseRoc.values.ravel(), taRoc.ravel(), verbose = True)

    def testMACD(self):
        npData = np.random.random(1000)
        dfData = pd.DataFrame(npData)
        dData = {}
        dData['close'] = dfData
        bse = mom.featMACD(dData, slow = 26, fast = 12)
        macd, macdsignal, macdhist = ta.MACD(real = npData, fastperiod = 12, slowperiod = 26, signalperiod = 9)
        np.testing.assert_array_almost_equal(bse.values.ravel()[price.EMA_MIN_DATA_COUNT_MULTIPLIER * 26:], macd.ravel()[price.EMA_MIN_DATA_COUNT_MULTIPLIER * 26:], verbose = True)
        
        
    def testMACDS(self):
        npData = np.random.random(1000)
        dfData = pd.DataFrame(npData)
        dData = {}
        dData['close'] = dfData
        bse = mom.featMACDS(dData, slow = 26, fast = 12, lLookback = 6)
        macd, macdsignal, macdhist = ta.MACD(real = npData, fastperiod = 12, slowperiod = 26, signalperiod = 6)
        np.testing.assert_array_almost_equal(bse.values.ravel()[price.EMA_MIN_DATA_COUNT_MULTIPLIER * (26 + 6):], macdsignal[price.EMA_MIN_DATA_COUNT_MULTIPLIER * (26 + 6):])
        
    def testRSI(self):
        dFullData = {}
        npClose = np.array([44.3389,44.0902,44.1497,43.6124,44.3278,44.8264,45.0955,45.4245,45.8433,46.0826,45.8931,46.0328,45.614,46.282,46.282,46.0028,46.0328,46.4116,46.2222,45.6439,46.2122,46.2521,45.7137,46.4515,45.7835,45.3548,44.0288,44.1783,44.2181,44.5672,43.4205,42.6628,43.1314])
        npRSI = np.array([np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,np.NAN,70.5327894837,66.3185618052,66.5498299355,69.4063053388,66.3551690563,57.9748557143,62.9296067546,63.2571475625,56.0592987153,62.3770714432,54.7075730813,50.4227744115,39.9898231454,41.4604819757,41.8689160925,45.4632124453,37.3040420899,33.0795229944,37.7729521144])
        dFullData['close'] = pd.DataFrame(npClose)
        dfRSI = mom.featRSI(dFullData, lLookback=14)
        np.testing.assert_array_almost_equal(dfRSI.values.ravel(), npRSI)
    
    def testRSI2(self):
        dFullData = {}
        npClose = np.random.random(100)
        npClose[7] = np.NAN
        dFullData['close'] = pd.DataFrame(npClose)
        dfZeroNAN = dFullData['close'].fillna(method='ffill')
        dfRSI = mom.featRSI(dFullData, lLookback=5)
        taRSI = ta.RSI(real = dfZeroNAN.values.ravel(), timeperiod = 5)
        np.testing.assert_array_almost_equal(dfRSI.values.ravel(), taRSI)        
        
    def tearDown(self):
        pass


    def testName(self):
        pass