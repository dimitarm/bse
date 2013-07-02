'''
Created on Jun 28, 2013

@author: I028663
'''
import unittest

def getAllFeaturesCombinationsList(l_items):
    ll_retItems = list()
    for i in range(1, 2 ** len(l_items)):
        l_curListItems = list()
        num = bin(i)
        num = list(num)
        num = num[2:]
        num.reverse()
        for n in range(0, len(num)):
            if num[n] <> '0':
                l_curListItems.append(l_items[n])
        ll_retItems.append(l_curListItems)
    return ll_retItems



class TestIt(unittest.TestCase):

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
        
        l_combinations = getAllFeaturesCombinationsList(l_values)
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
                
        
