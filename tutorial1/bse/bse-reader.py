'''
Created on Jan 2, 2013

@author: dimitar
'''

import csv
import urllib2
import datetime
import shlex
import os
import pandas as pd
import numpy as np
import utils.equities as bseequities
import datetime as dt

def bgDateParser(date):
    dat = dt.datetime.strptime(date,"%Y-%m-%d")
    return dt.date(dat.year, dat.month, dat.day)    


lines = bseequities.get_few_equities() 

#22/12/2012"
count = 0
for equity in lines:
    local_file_name = os.environ['QSDATA'] + "/Processed/Custom/" + equity + '.csv' 
    df_data = pd.read_csv(local_file_name, index_col = 0, parse_dates = True, date_parser = bgDateParser)
    l_dates = np.sort(df_data.index.values)
    last_avail_date = l_dates[-1] + dt.timedelta(days = 1)
        
    url = "http://www.bse-sofia.bg/graphics/phpfiles/MYgethistoDeA.php?MonCode=" + equity + "&MonPays=BE&Periode=1&De=" + last_avail_date.strftime("%d/%m/%Y") + "&A=" + datetime.date.today().strftime("%d/%m/%Y")
    print url 
#    urllib2.install_opener(
#        urllib2.build_opener(
#            urllib2.ProxyHandler({'http': 'http://proxy:8080'})
#        )
#    )    
    file_trades = urllib2.urlopen(url)
    tradedays = file_trades.readline()
    l_close = list()
    l_open = list()
    l_high = list()
    l_low = list()
    l_volumes = list()
    l_date = list()
    for line in file_trades: 
        #if line.strip():
            #continue
        #split main line
        main_splitter = shlex.shlex(line.strip(), posix=True)
        main_splitter.whitespace += ';'
        main_splitter.whitespace_split = True
        trade = list(main_splitter)
        #if any trading for this day
        if trade[1] != 'N':
            #21/02/2014;58060;58752;58039;58592;296839
            l_date.append(dt.datetime.strptime(trade[0],"%d/%m/%Y"))
            l_open.append(float(trade[1])/100)
            l_high.append(float(trade[2])/100)
            l_low.append(float(trade[3])/100)
            l_close.append(float(trade[4])/100)
            l_volumes.append(trade[5])
    file_trades.close()
    d_newData = {'Open':l_open, 'High':l_high, 'Low':l_low, 'Close':l_close, 'Volumes':l_volumes}
    df_newData = pd.DataFrame(d_newData, index = l_date)
    df_data = df_data.append(df_newData)
    df_data.sort_index()
    #with open(local_file_name, 'w+b') as csvfile:
    #    pass
    count = count + 1
    todo = len(lines) - count
    print str(todo) + " to do...\n" 


