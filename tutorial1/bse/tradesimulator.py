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
                    shares2buy = cash / dPrices['open'][symbol2trade][day]
                    if shares2buy == 0:
                        continue
                    portfolio[symbol2trade] += shares2buy
                    cash -= shares2buy * cash / dPrices['open'][symbol2trade][day]
                    print "{0}: Buying {1} shares of {2} for {3}".format(day, shares2buy, symbol2trade, dPrices['open'][symbol2trade][day])
                else:
                    #sell stock 
                    shares2sell = portfolio.pop(symbol2trade)
                    cash += shares2sell * dPrices['close'][symbol2trade][day] 
                    print "{0}: Selling {1} shares of {2} for {3}".format(day, shares2sell, symbol2trade, dPrices['close'][symbol2trade][day])
            else:
                if trans_type == True:
                    #buy stock if free cash available
                    shares2buy = cash / dPrices['open'][symbol2trade][day]
                    if shares2buy == 0:
                        continue
                    portfolio[symbol2trade] = shares2buy
                    cash -= shares2buy * cash / dPrices['open'][symbol2trade][day]
                    print "{0}: Buying {1} shares of {2} for {3}".format(day, shares2buy, symbol2trade, dPrices['open'][symbol2trade][day])
                else:
                    #sell something that is not in a portfolio?
                    print "Cannot sell {0} no such stock in my portfolio!".format(symbol2trade)
    pass



if __name__ == '__main__':
    pass