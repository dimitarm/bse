'''
Created on Jul 5, 2013

@author: I028663
'''

import sys
print sys.path

import unittest
import numpy as np
import bse.utils.tools

class TestTools(unittest.TestCase):

    def setUp(self):
        pass
        #self.seq = range(10)

    def testAllFeaturesCombinationsList(self):
        i_valueSeed = 1345
        i_rang = 10
        l_values = list()
        li_valuesPositions = list()
        for i in range(1, i_rang + 1):
            l_values.append(i_valueSeed)
            i_valueSeed += 1
        
        l_combinations = tools.getAllFeaturesCombinationsList(l_values)
        self.assertGreater(len(l_combinations), 0)
        for combination in l_combinations:
            i_valuePos = 0
            for value in combination:
                self.assertEqual(combination.count(value), 1, 'value: ' + str(value) + " appears: " + str(combination.count(value)) + ' times' + ' combination: ' + str(combination))
                i_valuePos += 2 ** l_values.index(value)
            li_valuesPositions.append(i_valuePos)
        li_valuesPositions.sort()
        i_prevPos = -1
        for i in li_valuesPositions:
            if i_prevPos == -1:
                self.assertEqual(i, 1, 'Start index is not one')
            else:
                self.assertEqual(i, i_prevPos + 1, 'Not sequential indexes: ' + str(i) + ' ' + str(i_prevPos))
            i_prevPos = i
                
    def testRemoveNansInDict(self):
        #np.random.seed(0)
        d_data = dict()
        d_changedData = dict()
        l_positionsNaN = list()
        for d in range(0, 2):
            na_arr = np.random.random_sample((1000, 50))
            for ii in range(0, na_arr.shape[0]/5):
                x = np.random.randint(0, na_arr.shape[1])
                y = np.random.randint(0, na_arr.shape[0])
                na_arr[y][x] = np.nan
                l_positionsNaN.append(y)
            d_data[d] = na_arr
            d_changedData[d] = np.copy(na_arr)
        tools.removeNansInDict(d_changedData)
        #check if there are no nans
        for arr in d_changedData.itervalues():
            for y in range(arr.shape[0]):
                self.assertFalse(np.any(np.isnan(arr[y])))
        #insert nan rows for removed rows
        l_positionsNaN = list(set(l_positionsNaN))
        l_positionsNaN.sort() 
        for key, arr in d_changedData.iteritems():
            for i in l_positionsNaN:
                arr = np.insert(arr, i, np.nan, axis=0)
            d_changedData[key] = arr
        #check if shapes are equal
        for key, arr in d_changedData.iteritems():
            self.assertEqual(arr.shape, d_data[key].shape, 'Not equal shapes')
            sh_shape = d_data[key].shape
            
        for y in range(0, sh_shape[0]):
            if l_positionsNaN.count(y) > 0:
                continue
            for key in d_data.iterkeys():
                if np.array_equal(d_changedData[key][y],d_data[key][y]) is True:
                    continue
                else:
                    print d_changedData[key][y]
                    print d_data[key][y]
                    self.fail('Not equal arrays ' + str(key) + ' ' + str(y))
                    return
                #
                
                
                
if __name__ == '__main__':
    pass                
                
                
                
        
            