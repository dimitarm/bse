'''
Created on Nov 19, 2013

@author: dimitar
'''
import unittest
import pandas as pand
import numpy as np
import datetime
import math
import bse.utils.features.volume as vol
import bse.utils.features.price as price
import pandas.util.testing as pandtest
import matplotlib.pyplot as plt
import talib as ta

class Test(unittest.TestCase):
    
    
    def setUp(self):
        self.dFullData = {}
        self.npClose = np.random.random(1000) + 2
        self.npHigh = self.npClose + 0.5
        self.npLow = self.npClose - 0.5
        self.npVol = np.random.random_sample(1000) * 100 + 1
        
        self.dFullData['close'] = pand.DataFrame(self.npClose)
        self.dFullData['high'] = pand.DataFrame(self.npHigh)
        self.dFullData['low'] = pand.DataFrame(self.npLow)
        self.dFullData['volumes'] = pand.DataFrame(self.npVol)

    def tearDown(self):
        pass

    def testNVI(self):
        dFullData = {}
        dFullData['close'] = pand.DataFrame(data=[1355.69, 1325.51, 1335.02, 1313.72, 1319.99, 1331.85, 1329.04, 1362.16, 1365.51, 1374.02, 1367.58, 1354.68, 1352.46, 1341.47, 1341.45, 1334.76, 1356.78, 1353.64, 1363.67, 1372.78, 1376.51, 1362.66, 1350.52, 1338.31, 1337.89, 1360.02, 1385.97, 1385.3, 1379.32, 1375.32], columns=['aaaaaa'])
        dFullData['volumes'] = pand.DataFrame(data=[2739.554304, 3119.458048, 3466.876416, 2577.124096, 2480.44672, 2329.789184, 2793.069568, 3378.778368, 2417.586944, 1442.810752, 2122.5632, 2083.558016, 2103.846784, 2526.193152, 2491.886848, 2730.317312, 2311.589632, 2135.4208, 2642.721536, 2701.346816, 3122.259968, 3125.065984, 2728.037888, 2844.188672, 2810.242048, 3256.421888, 3261.50272, 2296.256, 2701.690368, 2935.853312], columns=['aaaaaa'])
        dfNVI = pand.DataFrame(data=[1000.00,1000.00,1000.00,998.40,998.88,999.78,999.78,999.78,1000.03,1000.65,1000.65,999.71,999.71,999.71,999.70,999.70,1001.35,1001.12,1001.12,1001.12,1001.12,1001.12,1000.23,1000.23,1000.20,1000.20,1000.20,1000.15,1000.15,1000.15], columns=['aaaaaa'])       
        dfResult = vol.featNVI(dFullData, iInitValue=1000)
        pandtest.assert_frame_equal(dfNVI, dfResult)        
        
    def testOBV(self):
        dfOBV = vol.featOBV(self.dFullData)
        taOBV = ta.OBV(self.npClose, self.npVol)
        taOBV -= self.npVol[0]
        taOBV[0] = np.NAN
        np.testing.assert_array_almost_equal(dfOBV.values.ravel(), taOBV, verbose = True)

    def testADL(self):
        dFullData = {}
        npClose = np.array([62.15,60.81,60.45,59.18,59.24,60.2,58.48,58.24,58.69,58.65,58.47,58.02,58.17,58.07,58.13,58.94,59.1,61.92,61.37,61.68,62.09,62.89,63.53,64.01,64.77,65.22,63.28,62.4,61.55,62.69])
        npHigh = np.array([62.34,62.05,62.27,60.79,59.93,61.75,60,59,59.07,59.22,58.75,58.65,58.47,58.25,58.35,59.86,59.5299,62.1,62.16,62.67,62.38,63.73,63.85,66.15,65.34,66.48,65.23,63.4,63.18,62.7])
        npLow = np.array([61.37,60.69,60.1,58.61,58.712,59.86,57.97,58.02,57.48,58.3,57.8276,57.86,57.91,57.8333,57.53,58.58,58.3,58.53,59.8,60.93,60.15,62.2618,63,63.58,64.07,65.2,63.21,61.88,61.11,61.25])
        npVol = np.array([7849.025,11692.075,10575.307,13059.128,20733.508,29630.096,17705.294,7259.203,10474.629,5203.714,3422.865,3962.15,4095.905,3766.006,4239.335,8039.979,6956.717,18171.552,22225.894,14613.509,12319.763,15007.69,8879.667,22693.812,10191.814,10074.152,9411.62,10391.69,8926.512,7459.575])
        npADL = np.array([4774.1492268041,-4854.6184202547,-12018.536065416,-18248.5787810123,-21006.2374805197,-39975.7698403079,-48784.8077417858,-52784.7767417858,-47316.8886474462,-48561.2550387506,-47216.4520508928,-49573.6805319054,-49866.2451747625,-49353.8080732506,-47389.2381952018,-50906.7290077018,-48813.3222578034,-32474.1956695681,-25128.3493475342,-27144.0057613273,-18028.4860528071,-20193.4695305349,-17999.669448182,-33099.4431913726,-32056.1866401915,-41815.5213901916,-50574.8508951421,-53856.4372109316,-58988.1035297722,-51631.4192194274])
        dFullData['close'] = pand.DataFrame(npClose)
        dFullData['high'] = pand.DataFrame(npHigh)
        dFullData['low'] = pand.DataFrame(npLow)
        dFullData['volumes'] = pand.DataFrame(npVol)
        dfADL = vol.featADL(dFullData)
        np.testing.assert_array_almost_equal(dfADL.values.ravel(), npADL, verbose = True)
        #two series
        npClose = np.random.rand(100,2) + 1
        npHigh = npClose + 1
        npLow = npClose - 0.5
        npVol = np.random.rand(100,2) * 1000
        dFullData['close'] = pand.DataFrame(npClose)
        dFullData['high'] = pand.DataFrame(npHigh)
        dFullData['low'] = pand.DataFrame(npLow)
        dFullData['volumes'] = pand.DataFrame(npVol)
        dfADL = vol.featADL(dFullData)
        for serie in dFullData['close']:
            taADL = ta.AD(dFullData['high'][serie].values, dFullData['low'][serie].values, dFullData['close'][serie].values, dFullData['volumes'][serie].values)
            np.testing.assert_array_almost_equal(dfADL[serie].values.ravel(), taADL, verbose = True)        
        
    def testCHO(self):
        dFullData = {}
        npClose = np.random.rand(100,2) + 1
        npHigh = npClose + 1
        npLow = npClose - 0.5
        npVol = np.random.rand(100,2) * 1000 + 1
        dFullData['close'] = pand.DataFrame(npClose)
        dFullData['high'] = pand.DataFrame(npHigh)
        dFullData['low'] = pand.DataFrame(npLow)
        dFullData['volumes'] = pand.DataFrame(npVol)
        dfCHO = vol.featCHO(dFullData, fast = 3, slow = 10)  
        np.set_printoptions(threshold=1000)      
        for serie in dFullData['close']:
            taADOSC = ta.ADOSC(dFullData['high'][serie].values, dFullData['low'][serie].values, dFullData['close'][serie].values, dFullData['volumes'][serie].values, fastperiod = 3, slowperiod = 10)
            np.testing.assert_array_almost_equal(dfCHO[serie].values.ravel()[price.EMA_MIN_DATA_COUNT_MULTIPLIER * 10:], taADOSC[price.EMA_MIN_DATA_COUNT_MULTIPLIER * 10:], verbose = True)        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
