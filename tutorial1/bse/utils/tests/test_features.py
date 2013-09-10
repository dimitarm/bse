'''
Created on Jul 19, 2013

@author: I028663
'''
import unittest
import pandas as pand
import bse.utils.features as bsefeatures
import numpy as np

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass
    
    # featTrend(dData, lForwardlook=2, b_human=False)
    def testFeatTrend(self):
        d_data = {'one' : pand.Series([0., 2.1, 0., 2.2, np.nan], index=['a', 'b', 'c', 'd', 'e']),
             'two' : pand.Series([1., 2., 0.9, -2., 5.], index=['a', 'b', 'c', 'd', 'e'])}
        df_data = pand.DataFrame(d_data)
        df_orgDatacopy = df_data.copy()
        d_featdata = {'close': df_data, 'dfg' : df_data}
        
        d_featResData = bsefeatures.featTrend(d_featdata, lForwardlook=2)
        
        self.assertEqual(len(d_featResData.index) , len(d_featdata['close'].index), 'lengths not equal')
        
        df_expectedResult = pand.DataFrame({'one' : pand.Series([np.nan, 1., np.nan, np.nan, np.nan], index=['a', 'b', 'c', 'd', 'e']),
             'two' : pand.Series([-1., -1., 1., np.nan, np.nan], index=['a', 'b', 'c', 'd', 'e'])})
        self.assertTrue((pand.DataFrame.fillna(df_orgDatacopy, -5) == pand.DataFrame.fillna(df_data, -5)).values.all().all(), 'data passed to featTrend has changed')
        self.assertTrue((pand.DataFrame.fillna(d_featResData, -5) == pand.DataFrame.fillna(df_expectedResult, -5)).values.all().all(), 'result of featTrend not as expected')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
