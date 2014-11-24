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
        size = 1000
        dfData = pd.DataFrame(np.NAN, index = range(0, size), columns = ['a', 'b'])
        npData_a = np.random.random(1000) 
        dfData['a'] = npData_a
        npData_b = np.random.random(1000)
        dfData['b'] = npData_b
        
        dData = {}
        dData['close'] = dfData
        bse = mom.featRSI(dData, lLookback = 14)
        rsi = ta.RSI(real = npData_a, timeperiod = 14)
        np.testing.assert_array_almost_equal(bse['a'].values.ravel(), rsi)
        rsi = ta.RSI(real = npData_b, timeperiod = 14)
        np.testing.assert_array_almost_equal(bse['b'].values.ravel(), rsi)
        
    def tearDown(self):
        pass


    def testName(self):
        pass