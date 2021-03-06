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
import sys


lines = bseeq.get_all_equities()

#22/12/2012"
count = 0
for equity in lines:
    url = "http://www.bse-sofia.bg/graphics/phpfiles/MYgethistoDeA.php?MonCode=" + equity + "&MonPays=BE&Periode=1&De=01/01/2009&A=" + datetime.date.today().strftime("%d/%m/%Y")
    #print url
    file_trades = urllib2.urlopen(url)
    tradedays = file_trades.readline()

    local_file_name = os.environ['QSDATA'] + "/Processed/Custom/" + equity + '.csv'

    with open(local_file_name, 'w+b') as csvfile:
        eqwriter = csv.writer(csvfile, delimiter=',')
        eqwriter.writerow(["date" , "open", "high", "low", "close", "volumes"])
        trades = list()
        trades_dict = {}
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
                date = datetime.datetime.strptime(trade[0], '%d/%m/%Y')
                #2012-12-21,10000,14046.26,1.423,1.4,1.4,1.423
                trade = (date.strftime('%Y-%m-%d'), float(trade[1])/100, float(trade[2])/100, float(trade[3])/100, float(trade[4])/100, trade[5])
                if date in trades_dict:
                    if trades_dict[date] != trade:
                        print equity + " has repeating values: " + str(trade) + " " + str(trades_dict[date])
                        sys.exit(1) 
                else:
                    trades_dict[date] = trade
                    trades.append(trade)
        trades.reverse()
        eqwriter.writerows(trades)
                
    file_trades.close()
    count = count + 1
    todo = len(lines) - count
    print str(todo) + " to do..." 