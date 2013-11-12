'''
Created on Jan 2, 2013

@author: dimitar
'''

import csv
import urllib2
import datetime
import shlex
import os
import pandas as pand
import codecs
import binascii

equities = [line.strip() for line in open('../equities.txt')]

urllib2.install_opener(
    urllib2.build_opener(
        urllib2.ProxyHandler({'http': 'http://proxy:8080'})
    )
)     

#22/12/2012"
count = 0
decodefunc = codecs.getdecoder('utf_16_be') 
for equity in equities:
    equity = equity.strip()
    if (not equity or equity[0] == '#'):
        continue
    #http://www.bse-sofia.bg/?page=ExportData&target=security&code=3JR
    #;13.05.08;2.617;2.591;9768;8.42;8.02;7.01;3.97;1.52;.41;.97;.82

    url = "http://www.bse-sofia.bg/?page=ExportData&target=security&code=" + equity 
    print url
#    urllib2.install_opener(
#        urllib2.build_opener(
#            urllib2.ProxyHandler({'http': 'http://proxy:8080'})
#        )
#    )    
    fl_url = urllib2.urlopen(url)
    fl_url.read(3) #read BOM
    
    
    equity_file_name = os.environ['QSDATA'] + "/Processed/Custom/" + equity + '.csv' 
    df_data = pand.io.parsers.read_csv(equity_file_name, index_col = 0)
    
    trades = list()
    sym = fl_url.read(1)
    day_data = str()
    while sym:
        case sym:
        if sym == '\n':
            trades.append(day_data)
            day_data = str()
        if sym == 'E':
            of = fl_url.read(4)
            if of == '\x00O\x00F':
                trades.append(day_data)
                day_data = str()
                break;
        else:
            day_data += sym
        sym = fl_url.read(1)
    if day_data:
        trades.append(day_data)
    
        #if line.strip():
            #continue
    for trade in trades:
        print str(len(trade)) + " : " + trade.encode('string_escape')
        trade, b = decodefunc(trade)
        print trade

    #split main line
        main_splitter = shlex.shlex(trade.strip(), posix=True)
        main_splitter.whitespace += ';'
        main_splitter.whitespace_split = True
        trade = list(main_splitter)
            #split date
#            date_splitter = shlex.shlex(trade[0], posix=True)
#            date_splitter.whitespace += '/'
#            date_splitter.whitespace_split = True
#            date = list(date_splitter)
            #2012-12-21,10000,14046.26,1.423,1.4,1.4,1.423
        print trade
    fl_url.close()
    count = count + 1
    todo = len(equities) - count
    print str(todo) + " to do...\n" 
    

