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
import numpy as np



def get_adj_close_data(equity):
    url2 = "http://www.bse-sofia.bg/?page=ExportData&target=security&code=" + equity 
    print url2
    fl_url = urllib2.urlopen(url2)
    fl_url.read(3)  # read BOM
    trades = list()
    sym = fl_url.read(1)
    day_data = str()
    while sym:
        if sym == '\n':
            trades.append(day_data)
            day_data = str()
        elif sym == 'E':
            of = fl_url.read(4)
            if of == '\x00O\x00F':
                trades.append(day_data)
                day_data = str()
                break;
            day_data += sym
            day_data == of
        else:
            day_data += sym
        sym = fl_url.read(1)
    if day_data:
        trades.append(day_data)
    
    np_data = np.empty((0, 7))
    for trade in trades:
        trade = trade[:-3]  # remove \x00\r\x00 at the end
        trade, b = decodefunc(trade)
        trade = trade.strip()
        if not trade:
            continue
    # split main line
        main_splitter = shlex.shlex(trade, posix=True)
        main_splitter.whitespace += ';'
        main_splitter.whitespace_split = True
        trade = list(main_splitter)
        # ['13.11.11', '3.348', '3.379', '9129', '11.51', '10.86', '8.17', '5.23', '1.85', '.59', '1.15', '1.1']
        # split date
        # trade[0] date
        # trade[1] adjusted close
        # trade[2] close
        # trade[3] volume
        if trade:
            date_splitter = shlex.shlex(trade[0], posix=True)
            date_splitter.whitespace += '.'
            date_splitter.whitespace_split = True
            date = list(date_splitter)
            date = str('20' + str(date[0] + '-' + date[1]) + '-' + str(date[2])) 
            np_data = np.append(np_data, values=[[date, float(0), float(0), float(0), float(trade[2]), float(trade[1]), float(trade[3])]], axis=0)
    fl_url.close()
    return pand.DataFrame(data=np_data[:, 1:], index=np_data[:, 0], columns=("Open", "High", "Low", "Close", "AdjClose", "Volumes"), dtype=float) 

    
def get_new_data(equity, last_date):
    date_splitter = shlex.shlex(last_date, posix=True)
    date_splitter.whitespace += '-'
    date_splitter.whitespace_split = True
    date = list(date_splitter)
    last_date = str(date[2]) + '/' + str(date[1]) + '/' + str(date[0]) 

    url = "http://www.bse-sofia.bg/graphics/phpfiles/MYgethistoDeA.php?MonCode=" + equity + "&MonPays=BE&Periode=1&De=" + last_date + "&A=" + datetime.date.today().strftime("%d/%m/%Y")     
    file_trades = urllib2.urlopen(url)
    tradedays = file_trades.readline()
    np_data = np.empty((0, 7))
    for line in file_trades: 
        if not line.strip():
            continue
        # split main line
        main_splitter = shlex.shlex(line.strip(), posix=True)
        main_splitter.whitespace += ';'
        main_splitter.whitespace_split = True
        trade = list(main_splitter)
        # if any trading for this day
        if trade[1] != 'N':
            # split date
            date_splitter = shlex.shlex(trade[0], posix=True)
            date_splitter.whitespace += '/'
            date_splitter.whitespace_split = True
            date = list(date_splitter)
            # "Date" , "Open", "High", "Low", "Close", Volumes"
            # 2012-12-21,10000,14046.26,1.423,1.4,1.4,1.423
            np_data = np.append(np_data, [[date[2] + "-" + date[1] + "-" + date[0], float(trade[1]) / 100, float(trade[2]) / 100, float(trade[3]) / 100, float(trade[4]) / 100, -1, trade[5]]], axis=0)
    return pand.DataFrame(data=np_data[:, 1:], index=np_data[:, 0], columns=("Open", "High", "Low", "Close", "AdjClose", "Volumes"), dtype=float)


if __name__ == '__main__':


    equities = [line.strip() for line in open('../equities.txt')]
    
    urllib2.install_opener(
        urllib2.build_opener(
            urllib2.ProxyHandler({'http': 'http://proxy:8080'})
        )
    )     
    
    # 22/12/2012"
    count = 0
    decodefunc = codecs.getdecoder('utf_16_be') 
    for equity in equities:
        equity = equity.strip()
        if (not equity or equity[0] == '#'):
            continue
        local_file_name = os.environ['QSDATA'] + "/Processed/Custom/" + equity + '.csv' 
        df_data = pand.read_csv(local_file_name, index_col=0)
        df_data.sort_index(inplace=True)
        last_index = df_data.index[-1]
        
        df_new_data = get_new_data(equity, last_index)
        df_new_data = df_new_data.drop(last_index)
        df_data = pand.concat((df_data, df_new_data), verify_integrity=True)  # concatenate old data with existing data 
        df_adj_close_data = get_adj_close_data(equity)
        for index in df_adj_close_data.index:
            try:
                if round(df_adj_close_data.at[index, 'Close'], 3) <> round(df_data.at[index, 'Close'], 3) or round(df_adj_close_data.at[index, 'Volumes'], 3) <> round(df_data.at[index, 'Volumes'], 3):
                    print index + df_adj_close_data.at[index, 'Close'] + df_data.at[index, 'Close']
            except KeyError:
                print "missing key: " + index   
        count = count + 1
        todo = len(equities) - count
        print str(todo) + " to do...\n"
        
         
