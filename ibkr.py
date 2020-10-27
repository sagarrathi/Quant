from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt

import datetime

import csv

class St(bt.Strategy):
    
    def __init__(self):
        self.dataclose=self.datas[0].close
        csvfile = open('bt_data', 'w')
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.writer = writer
        print("Running: init")
    

    def logdata(self):
        txt = []

        txt.append('{}'.format(
            self.data.datetime.datetime(0).isoformat())
        )
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(txt)
        self.writer.writerow(txt)

        print("Running: Log")
    
    
    def next(self):
        self.logdata()
        print("Running: next")
    

    print("Made: Stratedgy")
    
def run(from_date, to_date):
    brain=bt.Cerebro(stdstats=False, live=False, preload=False)
    ibstore = bt.stores.IBStore(host='127.0.0.1', port=7496, clientId=35)
    data = ibstore.getdata(
        dataname='CADILAHC-STK-NSE-INR',
        timeframe=bt.TimeFrame.Days,
        fromdate=from_date,
        todate=to_date,
        historical=True
        )
    print("Created: Data")
    brain.adddata(data)
    print("Added: Data")

    brain.addstrategy(St)
    print("Added: Stratedgy")


    brain.run()
    print("Completed: Run")
    


if __name__=='__main__':
    from_date=datetime.datetime(2020,8,1)
    to_date=datetime.datetime(2020,8,20)
    run(from_date, to_date)
    
    
    


    