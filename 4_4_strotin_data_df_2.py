#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 13:36:46 2020

@author: boo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 03:20:55 2020

@author: boo
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

import pandas as pd

class TradingApp(EWrapper, EClient): 
    def __init__(self):
        EClient.__init__(self,self) 
        self.data={}    
    
    
    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId]=[{
                    "Date": bar.date,
                    "Open": bar.open,
                    "High": bar.high,
                    "Low":  bar.low,
                    "Close":bar.close,
                    "Volume":bar.volume,
                    }]
        else:
            self.data[reqId].append({
                    "Date": bar.date,
                    "Open": bar.open,
                    "High": bar.high,
                    "Low":  bar.low,
                    "Close":bar.close,
                    "Volume":bar.volume,
                    })
        print(self.data)


def nse_contract(symbol):
    contract=Contract()
    contract.symbol=symbol
    contract.secType = "STK"
    contract.exchange = "NSE" 
    contract.currency = "INR" 
    return contract


def histData(req_num,contract, durationStr='2 D',barSizeSetting='5 mins'):
    app.reqHistoricalData (reqId=req_num,
                           contract=contract,
                           endDateTime='',
                           durationStr=durationStr, 
                           barSizeSetting=barSizeSetting,
                           whatToShow='ADJUSTED_LAST',
                           useRTH=0,
                           formatDate=1,
                           keepUpToDate=0,
                           chartOptions=[],)
    

    
    
def websocket_conn():
    app.run()
    
app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)   

con_thread=threading.Thread(target=websocket_conn, daemon=True)
con_thread.start()
time.sleep(1)

tickers=['TATACONSUM',  'ADANIGAS',  'DLF',  'INFRATEL',  'TATASTEEL',  'TECHM']
df_dict={}

for ticker in tickers:
    contract=nse_contract(ticker)
    histData(tickers.index(ticker),contract)
    time.sleep(5)
    
    df_dict[ticker]=pd.DataFrame(app.data[tickers.index(ticker)])
    df_dict[ticker].set_index("Date", inplace=True)
