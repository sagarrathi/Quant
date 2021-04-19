#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 20:47:15 2020

@author: boo
"""

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
    
def atr(df, n=1):
    df['H-L']=abs(df["High"]-df["Low"])
    df['H-C']=abs(df["High"]-df["Close"].shift(1))
    df['L-C']=abs(df["Low"]-df["Close"].shift(1))
    df['TR']=df[['H-L','H-C','L-C']].max(axis=1, skipna=False)   
    df['ATR']=df['TR']
    return df    

def gapper_cols(df, ema_vol_n=3,atr_n=14):
    df["Gap"]= df['Open']/df['Close'].shift(1)
    df["AverageVolume"]=df["Volume"].ewm(span=ema_vol_n,adjust=False).mean()
    df=atr(df,atr_n)
    return df
    

def signal(df,min_gap=1.02 ,min_vol=4000,min_atr=5):
    df["min_gap"]=(df["Gap"]> min_gap)
    df["min_vol"]=(df["Volume"]> min_vol)
    df["min_ema_vol"]=(df["AverageVolume"]> min_vol)
    df["min_atr"]=(df["ATR"]> min_atr)
    df[["min_gap", "min_vol","min_ema_vol","min_atr"]] *= 1
    
    print("\n\nDF:\n",df[["min_gap", "min_vol","min_ema_vol","min_atr"]].sum())
    return df
    
    
def websocket_conn():
    app.run()
    
app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)   

con_thread=threading.Thread(target=websocket_conn, daemon=True)
con_thread.start()
time.sleep(1)

tickers=['TATACONSU', 'ADANIGAS',  'DLF',  'INFRATEL',  'TATASTEEL',  'TECHM']
df_dict={}

writer = pd.ExcelWriter(
        "/home/boo/notebook/IBKR/data/0112.xlsx", 
        engine='xlsxwriter')

for ticker in tickers:
    contract=nse_contract(ticker)
    histData(tickers.index(ticker),contract)
    time.sleep(5)
    
    df_dict[ticker]=pd.DataFrame(app.data[tickers.index(ticker)])
    
    df_dict[ticker].set_index("Date", inplace=True)
    
    df_dict[ticker]=gapper_cols(df_dict[ticker])
    df_dict[ticker]=signal(df_dict[ticker])
    df_dict[ticker].to_excel(writer, sheet_name=ticker)
writer.save()

