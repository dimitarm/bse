'''
Created on Jan 23, 2013

@author: I028663
'''

import random



def init():
    nums = list()
    for a in range(0, 10):
        for b in range(0, 10):
            for c in range(0, 10):
                for d in range(0, 10):
                    if a != b and a != c and a != d and b != c and b != d and c != d:
                        nums.append((a, b, c, d))
    return nums       
    
    
def getEstimate(guess, target):
    if len(guess) != len(target):
        print "Error", guess, " - ", target
        return
    bulls = 0
    cows = 0
    for i in range(0, len(guess)):
        if guess[i] == target[i]:
            bulls += 1
        if guess[i] in target:
            cows += 1
    cows -= bulls
    return (bulls, cows)
        

def removeUnrelatedCombinations(nums, guess, answer):
    to_be_removed = list()
    for num in nums:
        estimate = getEstimate(num, guess)
        if estimate != answer:
            to_be_removed.append(num)
        else:
            pass
        
    for num in to_be_removed:
        nums.remove(num)

def getAnswer(guess, number):
    return getEstimate(guess, number)

def getUserAnswer():
    bulls = raw_input('bulls --> ')
    cows = raw_input('cows --> ')
    return (int(bulls), int(cows))




if __name__ == '__main__':

    random.seed()
    guesses = init()
    number = guesses[random.randint(0, len(guesses) - 1)]
    print number
    print "initial array of guesses ", len(guesses)
    while len(guesses) > 1:
        
        guess = guesses[random.randint(0, len(guesses) - 1)]
        print ""
        print "Guess: ", guess
        answer = getUserAnswer()
        #answer = getAnswer(guess, number)
        removeUnrelatedCombinations(guesses, guess, answer)
        print "array of guesses ", len(guesses)


    print "Your number is ", guesses[0]

