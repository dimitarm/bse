'''
Created on Sep 24, 2014

@author: dimitar

portfolio_value = _sym1_br * sym1_price + _sym2_br * sym2_price + _sym3_br * sym3_price + _cash 

sym1_br = ( portfolio_value * sym1% ) / sym1_price

sell:
_costs += trans_cost3
operating_cash += ( _sym3_br - sym3 ) * sym3_price  

buy: 
_costs += trans_cost1
operating_cash ?= (sym1_br - _sym1_br) * sym1_price + ...
 
_sym1_br * sym1_price + ... = portfolio_value
'''

import bse.utils.reader.data as bsedata
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import math
"""
    Calculate current portfolio value
"""
def calculate_portfolio_value(dPortfolio, day, dPrices):
    portfolio_value = 0
    for stock, allocation in dPortfolio.iteritems():
        stock_price = (dPrices['open'][stock][day] + dPrices['close'][stock][day])/2
        portfolio_value += stock_price * allocation
    return portfolio_value 

def remove_zero_allocations(dAllocs):
    zeros = []
    for stock, alloc in dAllocs.iteritems():
        if alloc ==  0:
            zeros.append(stock)
    for stock in zeros:
        del dAllocs[stock]

"""
    @summary simulates trading of allocations (backtest)
    @param dAlloc: {'10-10-2014': {'E4B':0.5, 'E6T':0.25}, ...}
    @param dPrices: historic prices against the back test is done
    @param iCash: initial cash  
"""
def simulate_trades(dAlloc, dPrices, iCash, bPrint = False):
    
    portfolio = {}  #symbol:number_of_shares
    cash = iCash
    transaction_costs = 0.0
    cash_available = iCash
    #TODO: check if dAlloc has NaNs
    #TODO: check if dPrices has Nans

    #check if all allocation dates are present in the supplied historical prices
    for allocday in dAlloc.iterkeys():
        dPrices['close'].loc[allocday]
     
    sorted_days = sorted(dAlloc.keys())
    
    backtest_prices = dPrices['close'].loc[sorted_days[0]: sorted_days[-1]]
    dfResult = pd.DataFrame(index = backtest_prices.index, columns=['_PORT', '_CASH', '_COSTS'])
    #loop over all transactions
    for row in backtest_prices.iterrows():
        day = row[0]
        if day in dAlloc:
            allocs = dAlloc[day]
            #TODO check if all allocs equal to 1
            new_allocs = {}
            portfolio_value = calculate_portfolio_value(portfolio, day,dPrices)
    
            #calculate new allocs
            for stock, allocation in allocs.iteritems():
                stock_price = (dPrices['open'][stock][day] + dPrices['close'][stock][day])/2
                new_allocs[stock] = int((cash_available + portfolio_value) * allocation / stock_price)
            remove_zero_allocations(new_allocs)
            #handle the ones which we have to sell completely
            for stock, shares_to_transfer in portfolio.iteritems():
                if stock not in new_allocs:
                    sell_price = (dPrices['open'][stock][day] + dPrices['close'][stock][day])/2
                    cash_available += shares_to_transfer*sell_price #shares_to_transfer is negative!!!!
                    transaction_costs += 0.00375 * shares_to_transfer*sell_price #TODO
                    print "{0}: Selling {1} shares of {2} for {3}".format(day, abs(shares_to_transfer), stock, sell_price)
                    portfolio[stock] = 0
            remove_zero_allocations(portfolio)    
            
            #process the one in which we have change in quantity
            for stock, allocation in new_allocs.iteritems():
                if stock in portfolio:
                    shares_to_transfer = allocation - portfolio[stock]  
                else:
                    shares_to_transfer = allocation   #the brand new ones that we have to buy 
                
                if shares_to_transfer > 0:  #buy
                    buy_price = (dPrices['open'][stock][day] + dPrices['close'][stock][day])/2
                    cash_available -= shares_to_transfer*buy_price
                    transaction_costs += 0.00375 * shares_to_transfer*buy_price #TODO
                    print "{0}: Buying {1} shares of {2} for {3}".format(day, abs(shares_to_transfer), stock, buy_price)
                    portfolio[stock] = allocation
                elif shares_to_transfer < 0:                       #sell
                    sell_price = (dPrices['open'][stock][day] + dPrices['close'][stock][day])/2
                    cash_available += (-1)*shares_to_transfer*sell_price #shares_to_transfer is negative!!!!
                    transaction_costs += 0.00375 * shares_to_transfer*sell_price #TODO
                    print "{0}: Selling {1} shares of {2} for {3}".format(day, abs(shares_to_transfer), stock, sell_price)
                    portfolio[stock] = allocation
        #output current value of portfolio
        portfolio_value = calculate_portfolio_value(portfolio, day,dPrices)
        dfResult.at[day,'_PORT'] = portfolio_value
        dfResult.at[day,'_CASH'] = cash_available
        dfResult.at[day,'_COSTS'] = transaction_costs
        if bPrint:
            print day, ": [",
            for stock, allocation in portfolio.items():
                stock_price = (dPrices['open'][stock][day] + dPrices['close'][stock][day])/2
                print stock, ":", allocation, " = ", stock_price*allocation , ", ",
            print "] value: ", portfolio_value, " cash: ", cash_available
    if bPrint:
        print "transaction costs: ", transaction_costs      
    return dfResult   

if __name__ == '__main__':
    alloc = {dt.datetime(2013,8,2): {'SOFIX':0.9, '3JR':0.1}, 
             dt.datetime(2013,8,5): {'SOFIX':0.5, '3JR':0.5}, 
             dt.datetime(2013,8,15): {'SOFIX':0.1, '3JR':0.9},
             dt.datetime(2013,8,30): {'SOFIX':0.3, '3JR':0.7}
             }
    dPrices = bsedata.get_data(dt.datetime(2013,8,1), dt.datetime(2013,12,31), ['SOFIX', '3JR'])
    dfRes = simulate_trades(alloc, dPrices, 1000, bPrint = True)
    #plt.clf()
    dfRes.plot()
    dPrices['close']['SOFIX'].plot()
    plt.show()
    
