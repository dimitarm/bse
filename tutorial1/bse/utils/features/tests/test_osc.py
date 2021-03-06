'''
Created on Mar 21, 2014

@author: dimitar
'''
import unittest
import pandas as pand
import bse.utils.features.osc as osc
import pandas.util.testing as pandtest
import numpy as np
import talib as ta

class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def testFASTK(self):
        dData = {}
        dData['close'] = pand.DataFrame(data= {'aaaaaa': (np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,127.2876,127.1781,128.0138,127.1085,127.7253,127.0587,127.3273,128.7103,127.8745,128.5809,128.6008,127.9342,128.1133,127.596,127.596,
                                                          128.6904,128.2725)})
        dData['high'] = pand.DataFrame(data={'aaaaaa': (127.009,127.6159,126.5911,127.3472,128.173,128.4317,127.3671,126.422,126.8995,126.8498,125.646,125.7156,127.1582,127.7154,127.6855,128.2228,
                                                        128.2725,128.0934,128.2725,127.7353,128.77,129.2873,130.0633,129.1182,129.2873,128.4715,128.0934,128.6506,129.1381,128.6406)})
        dData['low'] = pand.DataFrame(data={'aaaaaa': (125.3574,126.1633,124.9296,126.0937,126.8199,126.4817,126.034,124.8301,126.3921,125.7156,124.5615,124.5715,125.0689,126.8597,126.6309,
                                                       126.8001,126.7105,126.8001,126.1335,125.9245,126.9891,127.8148,128.4715,128.0641,127.6059,127.596,126.999,126.8995,127.4865,127.397)})
        dfResult = osc.featFASTK(dData, lLookback=14)
        dfExpectedResult = pand.DataFrame(data={'aaaaaa': (np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan, 
                                                           70.438220247,67.6089091003,89.2021084182,65.8105524262,81.7477132965,64.5237972198,74.5297763406,98.5814423191,70.1045325659,
                                                           73.0560907339,73.4177905413,61.2312902873,60.9562710235,40.3861022519,40.3861022519,66.828549338,56.7314197352)}) 
        pandtest.assert_frame_equal(dfResult, dfExpectedResult)
        
    def testMFI(self):
        dData = {}
        dData['close'] = pand.DataFrame(data= {'aaaaaa': (24.7486,24.7088,25.0373,25.545,25.0672,25.107,24.888,24.9975,25.0473,25.336,25.0572,25.4455,25.5649,25.555,25.4057,25.3658,25.0373,
                                                          24.9178,24.878,24.9676,25.0473,24.45,24.5694,24.0219,23.8825,24.2011,24.2807,24.3305,24.44,25)})
        dData['volumes'] = pand.DataFrame(data={'aaaaaa': (18730.144,12271.74,24691.414,18357.606,22964.08,15918.948,16067.044,16568.487,16018.729,9773.569,22572.712,12986.669,10906.659,5799.259,
                                                          7395.274,5818.162,7164.726,5672.914,5624.742,5023.469,7457.091,11798.009,12366.132,13294.865,9256.87,9690.604,8870.318,7168.965,11356.18,
                                                          13379.374)})
        dData['high'] = pand.DataFrame(data={'aaaaaa': (24.8283,24.7586,25.1568,25.5848,25.6844,25.336,25.2862,25.1269,25.2762,25.3857,25.5351,25.6048,25.7441,25.7242,25.6744,25.4455,25.3161,
                                                        25.2563,25.0373,25.0074,25.3061,25.117,24.6889,24.5495,24.2708,24.2708,24.5993,24.4798,24.5595,25.16)})
        dData['low'] = pand.DataFrame(data={'aaaaaa': (24.3205,24.5993,24.7785,24.9477,24.8083,25.0572,24.8482,24.7496,24.9278,25.0274,25.0473,25.0622,25.5351,25.4554,25.2862,25.1667,24.9178,
                                                       24.9079,24.8283,24.7088,25.0274,24.3404,24.2708,23.8925,23.778,23.7232,24.2011,24.2409,23.4345,24.27)})
        dfResult = osc.featMFI(dData, lLookback=14)
        dfExpectedResult = pand.DataFrame(data={'aaaaaa': (np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan, 
                                                           49.4663108282,45.109744933,36.272153727,28.4066474923,31.5280573421,33.8681514976,41.3001006079,42.8033707555,31.8304833642,23.7601201016,
                                                           26.5061813287,24.0726611636,22.3832923429,22.1787457859,21.5340496579,30.8361838885)}) 
        pandtest.assert_frame_equal(dfResult, dfExpectedResult)


    def testMFI2(self):
        npClose = np.random.random(100) + 1.5
        npHigh = npClose + np.random.random(100)
        npLow = npClose - np.random.random(100)
        npVol = np.array(np.random.randint(1, 100, 100), dtype = float)
        
        dData = {}
        dData['close'] = pand.DataFrame(npClose)
        dData['volumes'] = pand.DataFrame(npVol)
        dData['high'] = pand.DataFrame(npHigh)
        dData['low'] = pand.DataFrame(npLow)
        
        bseMfi = osc.featMFI(dData, lLookback = 10)
        taMfi = ta.MFI(high = npHigh, low = npLow, close = npClose, volume = npVol, timeperiod = 10)
        np.testing.assert_almost_equal(bseMfi.values.ravel(), taMfi.ravel(), verbose = True)

        
    def testWILL(self):
        dData = {}
        dData['close'] = pand.DataFrame(data= {'aaaaaa': (np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,
                                                          127.2876,127.1781,128.0138,127.1085,127.7253,127.0587,127.3273,128.7103,127.8745,128.5809,128.6008,127.9342,128.1133,127.596,127.596,
                                                          128.6904,128.2725)})
        dData['high'] = pand.DataFrame(data={'aaaaaa': (127.009,127.6159,126.5911,127.3472,128.173,128.4317,127.3671,126.422,126.8995,126.8498,125.646,125.7156,127.1582,127.7154,127.6855,128.2228,
                                                        128.2725,128.0934,128.2725,127.7353,128.77,129.2873,130.0633,129.1182,129.2873,128.4715,128.0934,128.6506,129.1381,128.6406)})
        dData['low'] = pand.DataFrame(data={'aaaaaa': (125.3574,126.1633,124.9296,126.0937,126.8199,126.4817,126.034,124.8301,126.3921,125.7156,124.5615,124.5715,125.0689,126.8597,126.6309,
                                                       126.8001,126.7105,126.8001,126.1335,125.9245,126.9891,127.8148,128.4715,128.0641,127.6059,127.596,126.999,126.8995,127.4865,127.397)})
        dfResult = osc.featWILL(dData, lLookback=14)
        dfExpectedResult = pand.DataFrame(data={'aaaaaa': (np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan, 
                                                           -29.561779753,-32.3910908997,-10.7978915818,-34.1894475738,-18.2522867035,-35.4762027802,-25.4702236594,-1.4185576809,-29.8954674341,
                                                           -26.9439092661,-26.5822094587,-38.7687097127,-39.0437289765,-59.6138977481,-59.6138977481,-33.171450662,-43.2685802648)}) 
        pandtest.assert_frame_equal(dfResult, dfExpectedResult)
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMFI']
    unittest.main()