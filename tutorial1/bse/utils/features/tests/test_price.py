'''
Created on Nov 19, 2013

@author: dimitar
'''
import unittest
import bse.utils.features.price as price
import pandas as pand
import numpy as np
import talib as ta

class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSTD(self):
        npData = np.random.random(10000)
        dData = {}
        dData['close'] = pand.DataFrame(npData)
        feat = price.featSTDReturn(dData, lLookback = 10, bRel = False).values.ravel() * np.sqrt( 0.9 ) #correction for Degrees of Freedom
        import QSTK.qstkutil.tsutil as tsu
        npData2 = np.copy(npData)
        npData2 = tsu.returnize1(npData2).ravel()
        tastd = ta.STDDEV(real = npData2, timeperiod = 10) 
        np.testing.assert_array_almost_equal(feat, tastd, err_msg = "values not equal", verbose = True)

    def testEMA(self):
        npData = np.random.random(10000) * 10
        #npData = np.asarray([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], dtype=float)
        dData = {}
        dData['close'] = pand.DataFrame(npData)
        feat = price.featEMA(dData, lLookback = 3).values.ravel()
        ema = ta.EMA(real = npData, timeperiod = 3)
        np.testing.assert_array_almost_equal(feat[3*price.EMA_MIN_DATA_COUNT_MULTIPLIER:], ema[3*price.EMA_MIN_DATA_COUNT_MULTIPLIER:], err_msg = "values not equal", verbose = True)

    def testBollinger(self):
        dFullData = {}
        npData = np.random.random(1000) * 10
        dFullData['close'] = pand.DataFrame(data=npData)
        
        dfResultUp = price.featBollingerUp(dFullData, 'close', lLookback = 20)
        dfResultDown = price.featBollingerDown(dFullData, 'close', lLookback = 20)

        taBollUp, taBollMd, taBollDn = ta.BBANDS(real = dFullData['close'].values.ravel(), timeperiod = 20)
        taStd = ta.STDDEV(real  = dFullData['close'].values.ravel(), timeperiod = 20)
        
        taBollUp = taBollUp - 2 * taStd  + 2 * taStd * np.sqrt(float(20)/19) #correction for Degrees of Freedom
        taBollDn = taBollDn + 2 * taStd  - 2 * taStd * np.sqrt(float(20)/19) #correction for Degrees of Freedom
        
        np.testing.assert_array_almost_equal(taBollUp, dfResultUp.values.ravel())
        np.testing.assert_array_almost_equal(taBollDn, dfResultDown.values.ravel())
        
#    def testBollingerTradeRule(self):
#        dFullData = {}
#        dFullData['close'] = pand.DataFrame(data=[86.1557,89.0867,88.7829,90.3228,89.0671,91.1453,89.4397,89.175,86.9302,87.6752,86.9596,89.4299,89.3221,88.7241,87.4497,87.2634,89.4985,87.9006,89.126,90.7043,92.9001,92.9784,91.8021,92.6647,92.6843,92.3021,92.7725,92.5373,92.949,93.2039,91.0669,89.8318,89.7435,90.3994,90.7387,88.0177,88.0867,88.8439,90.7781,90.5416,91.3894,90.65], columns=['aaaaaa'])
#        dfBollingerRule = price.featBollingerTradeRule(dFullData, lLookback = 20)
#        #print dfBollingerRule 
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBollingerUp']
    unittest.main()