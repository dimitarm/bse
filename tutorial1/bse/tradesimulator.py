'''
Created on Sep 24, 2014

@author: dimitar
'''

def simulate_trades(dAlloc, dPrices, iCash):
    
    portfolio = {}  #symbol:number_of_shares
    cash = iCash
    #loop over all transactions
    for day, allocs in enumerate(dAlloc):  
        for symbol2trade, trans_type in enumerate(allocs):
            if symbol2trade in portfolio:
                if trans_type == True: #buy
                    #buy stock if free cash available
                    shares2buy = cash / dPrices['close'][symbol2trade][day]
                    if shares2buy == 0:
                        continue
                else:
                    #sell stock 
                    pass
            else:
                if trans_type == True:
                    #buy stock if free cash available
                    pass
                else:
                    #sell something that is not in a portfolio?
                    print("Cannot sell " + symbol2trade + " no such stock in my portfolio!")
    pass



if __name__ == '__main__':
    pass