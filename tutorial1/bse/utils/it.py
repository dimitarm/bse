'''
Created on Jun 28, 2013

@author: I028663
'''

def getAllFeaturesCombinationsList(lfcAllFeatures):
    lfcFeaturesList = list()
    featCombinationsList = range(1,2 ** len(lfcAllFeatures),1)
    for featCombination in featCombinationsList:
        lfcCurFeaturesList = list()
        featFlag =  (2 ** len(lfcAllFeatures)) >> 1
        #add features
        while True:
            if featCombination & featFlag:
               lfcCurFeaturesList.append(lfcAllFeatures[featFlag])
            if featFlag == 0:
                break 
            featFlag = featFlag >> 1
    lfcCurFeaturesList.append(lfcCurFeaturesList)
    return lfcCurFeaturesList
        
if __name__ == '__main__':
    num = bin(33)
    print num