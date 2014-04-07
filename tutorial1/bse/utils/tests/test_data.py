'''
Created on Apr 7, 2014

@author: dimitar
'''
import unittest
import pandas as pand
import pandas.util.testing as pandtest
import numpy as np

import bse.utils.data as bsedataut

class Test(unittest.TestCase):


    def testFillForward(self):
        d_data = {'one' : pand.Series([np.nan, 2.1, np.nan, np.nan, 2.2, np.nan], index=['a', 'b', 'c', 'd', 'e', 'f']),
             'two' : pand.Series([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], index=['a', 'b', 'c', 'd', 'e', 'f'])}
        data = pand.DataFrame(d_data)
        bsedataut.fillforward(data)
        expected_res = pand.DataFrame( {'one' : pand.Series([np.nan, 2.1, 2.1, 2.1, 2.2, 2.2], index=['a', 'b', 'c', 'd', 'e', 'f']),
             'two' : pand.Series([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], index=['a', 'b', 'c', 'd', 'e', 'f'])})
        pandtest.assert_frame_equal(data, expected_res)

    def testFillBackward(self):
        d_data = {'one' : pand.Series([np.nan, 2.1, np.nan, np.nan, 2.2, np.nan], index=['a', 'b', 'c', 'd', 'e', 'f']),
             'two' : pand.Series([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], index=['a', 'b', 'c', 'd', 'e', 'f'])}
        data = pand.DataFrame(d_data)
        bsedataut.fillbackward(data)
        expected_res = pand.DataFrame( {'one' : pand.Series([2.1, 2.1, 2.2, 2.2, 2.2, np.nan], index=['a', 'b', 'c', 'd', 'e', 'f']),
             'two' : pand.Series([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], index=['a', 'b', 'c', 'd', 'e', 'f'])})
        pandtest.assert_frame_equal(data, expected_res)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testFillForward']
    unittest.main()
