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
    
    #featTrend(dData, lForwardlook=2, b_human=False)
    def testFeatTrend(self):
        d_data = {'one' : pand.Series([0., 2.1, 0., 2.2], index=['a', 'b', 'c', 'd']), 
             'two' : pand.Series([1., 2., 0.9, -2., 5.], index=['a', 'b', 'c', 'd', 'e'])}
        df_data = pand.DataFrame(d_data)
        df_orgDatacopy = df_data.copy()
        d_featdata = {'abc': df_data, 'dfg' : df_data}
        
        #d_featResData = bsefeatures.featTrend(d_featdata, lForwardlook=2)
        d_featResData = d_featdata.copy()
        
        self.assertEqual(len(d_featResData) , len(d_featdata), '1')
        
        d_resultData = {'one' : pand.Series([0., 1., np.nan], index=['a', 'b', 'c']), 
             'two' : pand.Series([-1., 1., 1.], index=['c', 'd', 'e'])}
        df_resultData = pand.DataFrame(d_resultData)
        self.assertFalse(df_orgDatacopy == df_data, 'data passed to featTrend has changed')
        self.assertTrue(d_featResData['abc'] == df_resultData, 'result of featTrend not as expected')
        self.assertTrue(d_featResData['dfg'] == df_resultData, 'result of featTrend not as expected')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()