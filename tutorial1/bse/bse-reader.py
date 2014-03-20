'''
Created on Jan 2, 2013

@author: dimitar
'''

import csv
import urllib2
import datetime
import shlex
import os
import utils.equities as bseeq


lines = bseeq.get_all_equities()

 

#22/12/2012"
count = 0
for equity in lines:
    equity = equity.strip()
    if (not equity or equity[0] == '#'):
        continue

    url = "http://www.bse-sofia.bg/graphics/phpfiles/MYgethistoDeA.php?MonCode=" + equity + "&MonPays=BE&Periode=1&De=01/01/2009&A=" + datetime.date.today().strftime("%d/%m/%Y")
    print url
    if 'HTTP_PROXY_HOST' in os.environ:  
        urllib2.install_opener(
            urllib2.build_opener(
                urllib2.ProxyHandler({'http': 'http://proxy:8080'})
            )
        ) 
    file_trades = urllib2.urlopen(url)
    tradedays = file_trades.readline()

    local_file_name = os.environ['QSDATA'] + "/Processed/Custom/" + equity + '.csv'

    with open(local_file_name, 'w+b') as csvfile:
        eqwriter = csv.writer(csvfile, delimiter=',')
        eqwriter.writerow(["Date" , "Open", "High", "Low", "Close", "Volumes"])
        trades = list()
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
                #split date
                date_splitter = shlex.shlex(trade[0], posix=True)
                date_splitter.whitespace += '/'
                date_splitter.whitespace_split = True
                date = list(date_splitter)
                #2012-12-21,10000,14046.26,1.423,1.4,1.4,1.423
                trades.append([date[2] + "-" + date[1] + "-" + date[0],
                                  float(trade[1])/100, float(trade[2])/100, float(trade[3])/100, float(trade[4])/100, trade[5]])
        trades.reverse()
        for trade in trades:
            eqwriter.writerow(trade)
                
    file_trades.close()
    count = count + 1
    todo = len(lines) - count
    print str(todo) + " to do...\n" 