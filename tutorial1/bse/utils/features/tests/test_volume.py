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
import pandas.util.testing as pandtest
import matplotlib.pyplot as plt

class Test(unittest.TestCase):

    def setUp(self):
        dFullData = {}
        base = datetime.datetime.today()
        dateList = [ base - datetime.timedelta(days=x) for x in range(0, 10) ]    
        
        dFullData['close'] = pand.DataFrame(data=np.random.randn(10, 2) + 10, columns=('aaaaaa', 'bbb'), index=dateList)
        dFullData['high'] = pand.DataFrame(data=np.random.randn(10, 2) + 10, columns=('aaaaaa', 'bbb'), index=dateList)
        dFullData['low'] = pand.DataFrame(data=np.random.randn(10, 2) + 10, columns=('aaaaaa', 'bbb'), index=dateList)
        dFullData['volumes'] = pand.DataFrame(data=np.random.randn(10, 2) * 5 + 100, columns=('aaaaaa', 'bbb'), index=dateList)
        pass


    def tearDown(self):
        pass

    def testfeatNVITradeRule(self):
        dFullData = {}
        dFullData['close'] = pand.DataFrame(data=np.random.randn(100) + 10, columns=['aaaaaa'])
        dFullData['volumes'] = pand.DataFrame(data=np.random.randn(100)*5 + 100, columns=['aaaaaa'])
        dfRule = vol.featNVITradeRule(dFullData)
        
    def testfeatPVITradeRule(self):
        dFullData = {}
        dFullData['close'] = pand.DataFrame(data=np.random.randn(100) + 10, columns=['aaaaaa'])
        dFullData['volumes'] = pand.DataFrame(data=np.random.randn(100)*5 + 100, columns=['aaaaaa'])
        dfRule = vol.featPVITradeRule(dFullData)
        
    def testfeatPVI2SMA(self):
        dFullData = {}
        dFullData['close'] = pand.DataFrame(data=np.random.randn(100) + 10, columns=['aaaaaa'])
        dFullData['volumes'] = pand.DataFrame(data=np.random.randn(100)*5 + 100, columns=['aaaaaa'])
        vol.featPVI2SMA(dFullData)
        
    def testfeatPriceVolumeTrend(self):
        dFullData = {}
        dFullData['close'] = pand.DataFrame(data=np.random.randn(100) + 10, columns=['aaaaaa'])
        dFullData['volumes'] = pand.DataFrame(data=np.random.randn(100)*5 + 100, columns=['aaaaaa'])
        #print vol.featPriceVolumeTrend(dFullData)

    def testNVI(self):
        dFullData = {}
        dFullData['close'] = pand.DataFrame(data=[1355.69, 1325.51, 1335.02, 1313.72, 1319.99, 1331.85, 1329.04, 1362.16, 1365.51, 1374.02, 1367.58, 1354.68, 1352.46, 1341.47, 1341.45, 1334.76, 1356.78, 1353.64, 1363.67, 1372.78, 1376.51, 1362.66, 1350.52, 1338.31, 1337.89, 1360.02, 1385.97, 1385.3, 1379.32, 1375.32], columns=['aaaaaa'])
        dFullData['volumes'] = pand.DataFrame(data=[2739.554304, 3119.458048, 3466.876416, 2577.124096, 2480.44672, 2329.789184, 2793.069568, 3378.778368, 2417.586944, 1442.810752, 2122.5632, 2083.558016, 2103.846784, 2526.193152, 2491.886848, 2730.317312, 2311.589632, 2135.4208, 2642.721536, 2701.346816, 3122.259968, 3125.065984, 2728.037888, 2844.188672, 2810.242048, 3256.421888, 3261.50272, 2296.256, 2701.690368, 2935.853312], columns=['aaaaaa'])
        dfNVI = pand.DataFrame(data=[1000.00,1000.00,1000.00,998.40,998.88,999.78,999.78,999.78,1000.03,1000.65,1000.65,999.71,999.71,999.71,999.70,999.70,1001.35,1001.12,1001.12,1001.12,1001.12,1001.12,1000.23,1000.23,1000.20,1000.20,1000.20,1000.15,1000.15,1000.15], columns=['aaaaaa'])       
        dfResult = vol.featNVI(dFullData, iInitValue=1000)
        pandtest.assert_frame_equal(dfNVI, dfResult)        
        


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
