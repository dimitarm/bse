'''
Created on Nov 13, 2013

@author: dimitar
'''

import unittest
import pandas as pd
import bse.utils.features.mom as mom
import numpy as np
import talib as ta

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
        np.testing.assert_equal(bseMom.values.ravel(), taMom.ravel(), "mom values not equal", verbose = True)
    
    def testROC(self):
        npData = np.random.random(100)
        dfData = pd.DataFrame(npData)
        dData = {}
        dData['close'] = dfData
        bseRoc = mom.featROC(dData, serie = 'close', lLookback = 10)
        taRoc = ta.ROC(real = npData, timeperiod = 10)
        np.testing.assert_array_almost_equal(bseRoc.values.ravel(), taRoc.ravel(), err_msg = "values not equal", verbose = True)

#    def testMACD(self):
#        npData = np.random.random(100)
#        dfData = pd.DataFrame(npData)
#        dData = {}
#        dData['close'] = dfData
#        bse = mom.featMACD(dData, slow = 26, fast = 12)
#        macd, macdsignal, macdhist = ta.MACD(real = npData, fastperiod = 12, slowperiod = 26, signalperiod = 9)
#        np.testing.assert_array_almost_equal(bse.values.ravel(), macdhist.ravel(), err_msg = "values not equal", verbose = True)
#        
    def testMACDS(self):
        npData = np.random.random(100)
        dfData = pd.DataFrame(npData)
        dData = {}
        dData['close'] = dfData
        bse = mom.featMACDS(dData, slow = 8, fast = 4, lLookback = 2)
        macd, macdsignal, macdhist = ta.MACD(real = npData, fastperiod = 4, slowperiod = 8, signalperiod = 2)
        np.testing.assert_array_almost_equal(bse.values.ravel(), macd.ravel(), err_msg = "values not equal", verbose = True)
        
    def tearDown(self):
        pass


    def testName(self):
        pass