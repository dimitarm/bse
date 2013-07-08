'''
Created on Jul 5, 2013

@author: I028663
'''
import utils.tools
import unittest
import numpy as np

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
        
        l_combinations = utils.tools.getAllFeaturesCombinationsList(l_values)
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
        np.random.seed(0)
        d_data = dict()
        d_changedData = dict()
        l_positionsNaN = list()
        for d in range(0, 5):
            na_arr = np.random.random_sample((100, 100))
            for i in range(0, 5):
                x = np.random.randint(0, 100)
                y = np.random.randint(0, 100)
                na_arr[x][y] = np.nan
                l_positionsNaN.append(y)
            d_data[d] = na_arr
            d_changedData[d] = np.copy(na_arr)
        l_positionsNaN.sort()
        utils.tools.removeNansInDict(d_changedData)
#        for arr in d_changedData:
#            for i in l_positionsNaN:
#                np.insert(arr, i, np.nan, axis=2)
        sh_arrShape = None
        for arr in d_changedData.itervalues():
            if sh_arrShape is None:
                sh_arrShape = arr.shape
            self.assertEqual(sh_arrShape, arr.shape, 'Not equal shapes')
        for y in range(0, sh_arrShape[0]):
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
                
                
                
                
                
                
                
        
            