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
    
    def testMOM(self):
        npData = np.random.random(100)
        dfData = pd.DataFrame(npData)
        dData = {}
        dData['close'] = dfData
        bseMom = mom.featMomentum(dData, serie = 'close', lLookback = 10)
        taMom = ta.MOM(real = npData, timeperiod = 10)
        np.testing.assert_equal(bseMom.values.ravel(), taMom.ravel(), "mom values not equal", verbose = True)
        pass

    def tearDown(self):
        pass


    def testName(self):
        pass