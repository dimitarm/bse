'''
Created on Nov 22, 2014

@author: dimitar
'''
import unittest
import numpy as np
import pandas as pd
import talib as ta
import bse.utils.features.volatility as volatility

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


#    def testCHV(self):
#        npLow = np.random.random(1000) + 1
#        npHigh = npLow + 1
#        dData = {}
#        dData['high'] = pd.DataFrame(npHigh)
#        dData['low'] = pd.DataFrame(npLow)
#        dfCHV = volatility.featCHV(dData, lLookback = 10)


if __name__ == "__main__":
    unittest.main()