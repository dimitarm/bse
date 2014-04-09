'''
Created on Apr 9, 2014

@author: I028663
'''

import bse.utils.dateutil as bsedateutl
import datetime as dt

_prediction_period = 5 #days

def get_next_prediction_date(current_prediction_date):
    count = _prediction_period 
    curr = current_prediction_date
    while count > 0:
        if bsedateutl.isBSEDay(curr) == bsedateutl.WORK:
            count -= 1
        curr = curr + dt.timedelta(days = 1)
    

if __name__ == '__main__':
    pass

'''
Things to be saved in persistent file:
current_prediction_date
forecast_symbols
'''


#update data

#get list of latest predicted symbols
#get their closing data
#calculate forecast success rate for each one of them
#update index.html 

#get current prediction date

#calculate next due prediction date
    #next_due_prediction_date

#get predictions 

#set index.html link in current prediction page

#move current prediction page to archive folder

#generate new prediction page (set link to previous prediction page)

#copy new prediction page     
    