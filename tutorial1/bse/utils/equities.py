'''
Created on Jan 5, 2013

@author: dimitar
'''


def get_all_equities():
    equities = list()
    f = open('equities.txt', 'rb')
    for line in f:
        line = line.strip('\n')
        equities.append(line)
    f.close()
    return equities


def get_few_equities():
    
    return ['SOFIX', '3JU', '6L1']