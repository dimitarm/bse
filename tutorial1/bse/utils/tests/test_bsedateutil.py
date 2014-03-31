'''
Created on Mar 13, 2014

@author: dimitar
'''
import unittest
import pandas as pd
import os
import numpy as np
import datetime as dt
import bse.utils.dateutil as bsedate

class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSOFIXValueIsPresent(self):
        filepath = os.environ['QSDATA'] + "/Processed/Custom/SOFIX.csv"
        sofix = pd.read_csv(filepath, index_col = 0, parse_dates = True, date_parser = bgDateParser)
        sf_dates = np.sort(sofix.index.values)
        bse_dates = bsedate.getBSEdays(sf_dates[0], sf_dates[-1])
        bse_dates = np.sort(bse_dates)
        for dat in range(0, sf_dates.shape[0]):
            self.assertTrue(bse_dates[dat] == sf_dates[dat], str(bse_dates[dat]) + " " + str(sf_dates[dat]))
        np.testing.assert_array_equal(sf_dates, bse_dates, verbose = True)
            
    
#2013/05/29
def bgDateParser(date):
    dat = dt.datetime.strptime(date,"%Y-%m-%d")
    return dt.date(dat.year, dat.month, dat.day)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()