'''
Created on Nov 19, 2013

@author: dimitar
'''
import unittest
import bse.utils.features.price as price
import pandas as pand
import pandas.util.testing as pandtest
import numpy as np
import matplotlib.pyplot as plt

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testBollingerTradeRule(self):
        dData = {}
        dData['close'] = pand.DataFrame(data=[86.1557,89.0867,88.7829,90.3228,89.0671,91.1453,89.4397,89.175,86.9302,87.6752,86.9596,89.4299,89.3221,88.7241,87.4497,87.2634,89.4985,87.9006,89.126,90.7043,92.9001,92.9784,91.8021,92.6647,92.6843,92.3021,92.7725,92.5373,92.949,93.2039,91.0669,89.8318,89.7435,90.3994,90.7387,88.0177,88.0867,88.8439,90.7781,90.5416,91.3894,90.65], columns=['aaaaaa'])
        dfBollingerRule = price.featBollingerTradeRule(dData, lLookback = 20)
        #print dfBollingerRule 
        
    
    def testBollinger(self):
        dData = {}
        dData['close'] = pand.DataFrame(data=[86.1557,89.0867,88.7829,90.3228,89.0671,91.1453,89.4397,89.175,86.9302,87.6752,86.9596,89.4299,89.3221,88.7241,87.4497,87.2634,89.4985,87.9006,89.126,90.7043,92.9001,92.9784,91.8021,92.6647,92.6843,92.3021,92.7725,92.5373,92.949,93.2039,91.0669,89.8318,89.7435,90.3994,90.7387,88.0177,88.0867,88.8439,90.7781,90.5416,91.3894,90.65], columns=['aaaaaa'])

        dfBollUp = pand.DataFrame(data=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,91.2918624279,91.9492676236,92.6125951399,92.9341995376,93.3119499729,93.7284499462,93.8995921801,94.2662548675,94.5650961486,94.7869123196,95.0430009771,94.9076050235,94.9029115183,94.8953200436,94.8610129333,94.6736291873,94.5565929787,94.678751506,94.5757855878,94.5342713064,94.5323060978,94.3692507015,94.1485034683], columns=['aaaaaa'])       
        dfResultUp = price.featBollingerUp(dData, 'close', lLookback = 20)

        dfBollDown = pand.DataFrame(data=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,86.1240175721,86.1410523764,85.8668948601,85.8472104624,85.7036500271,85.6488700538,85.5934078199,85.5600251325,85.5974138514,85.9774776804,86.2742590229,86.8203849765,86.8652684817,86.9149999564,87.1168370667,87.6331208127,87.8255870213,87.562248494,87.7595444122,87.9662686936,87.9519639022,87.9639492985,87.9518565317], columns=['aaaaaa'])       
        dfResultDown = price.featBollingerDown(dData, 'close', lLookback = 20)
        
        pandtest.assert_frame_equal(dfBollUp, dfResultUp)        
        pandtest.assert_frame_equal(dfBollDown, dfResultDown)        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBollingerUp']
    unittest.main()