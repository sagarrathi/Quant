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
    
def MACD(DF,a=12,b=26,c=9):
    df=DF.copy()
    df["MaFast"]=df["Close"].ewm(span=a, min_periods=a).mean()
    df["MaSlow"]=df["Close"].ewm(span=b, min_periods=b).mean()
    df["MACD"]=df["MaFast"]-df["MaSlow"]
    df["Signal"]=df["MACD"].ewm(span=c, min_periods=c).mean()
    return df


def boll_band(DF, n=20):
    df=DF.copy()
    df["MA"]=df['Close'].ewm(span=n, min_periods=n).mean()
    df["BB_up"]=df['MA']+2*df["Close"].rolling(n).std(ddof=0)
    df["BB_dn"]=df['MA']-2*df["Close"].rolling(n).std(dd0f=0)
    df["BB_width"]=df["BB_up"]-df["BB_dn"]
    df.dropna(inplace=True)
    return df

def atr(DF, n=9):
    df=DF.copy()
    df['H-L']=abs(df["High"]-df["Low"])
    df['H-C']=abs(df["High"]-df["Close"].shift(1))
    df['L-C']=abs(df["Low"]-df["Close"].shift(1))
    df['TR']=df[['H-L','H-C','L-C']].max(axis=1, skipna=False)   
    df['ATR']=df['TR'].ewm(com=n, min_periods=n).mean()
    return df    
    
def websocket_conn():
    app.run()
    
app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)   

con_thread=threading.Thread(target=websocket_conn, daemon=True)
con_thread.start()
time.sleep(1)

tickers=['SAIL',	'SIEMENS','FORTIS']
df_dict={}

for ticker in tickers:
    contract=nse_contract(ticker)
    histData(tickers.index(ticker),contract)
    time.sleep(5)
    
    df_dict[ticker]=pd.DataFrame(app.data[tickers.index(ticker)])
    df_dict[ticker].set_index("Date", inplace=True)
    
time.sleep(2)
macd_df=MACD(df_dict[ticker])

time.sleep(2)
bb_df=boll_band(df_dict[ticker])
        

time.sleep(2)
atr_df=atr(df_dict[ticker],10)
    