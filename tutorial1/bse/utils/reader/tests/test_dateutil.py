'''
Created on Mar 30, 2014

@author: dimitar
'''
import unittest
import datetime as dt
import bse.utils.dateutil as bsedateutil
import bse.utils.reader.data as bsereader
import bse.utils.equities as bseeq
from QSTK.qstkutil import DataAccess as da
import pandas.util.testing as pandtest


class Test(unittest.TestCase):


    def testSameDataWithDataAccess(self):
        dtEnd = dt.datetime.today().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        dtStart = dtEnd - dt.timedelta(days = 365)
        dataobj = da.DataAccess(da.DataSource.CUSTOM)      
        lsKeys = ['open', 'high', 'low', 'close', 'volumes']
        
        #get train data
        ldtTimestamps = bsedateutil.getBSEdays( dtStart, dtEnd, dt.timedelta(hours=16))
        ldfData = dataobj.get_data( ldtTimestamps, bseeq.get_few_equities(), lsKeys, verbose=False )
        dFullData = dict(zip(lsKeys, ldfData))
        
        bse_data = bsereader.get_data(dtStart, dtEnd, bseeq.get_few_equities())
        self.assertEquals(dFullData.keys(), bse_data.keys(), "keys not equal: " + str(dFullData.keys()) + " " + str(bse_data.keys()))
        for serie in bse_data.keys():
            pandtest.assert_almost_equal(bse_data[serie], dFullData[serie])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSameDataWithDataAccess']
    unittest.main()