#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 18:42:56 2020

@author: boo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:08:36 2020

@author: boo
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time


class TradingApp(EWrapper, EClient): 
    def __init__(self):
        EClient.__init__(self,self) 
        EWrapper.__init__(self)
        
    
    
    def historicalData(self, reqId, bar):
        print("HistoricalData. ReqId:", reqId, "BarData.", bar)
    
    
def websocket_conn():
    app.run()
    
   

app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=35)   


con_thread=threading.Thread(target=websocket_conn, daemon=True)
con_thread.start()
time.sleep(1)

def nse_contract(symbol):
    contract=Contract()
    contract.symbol=symbol
    contract.secType = "STK"
    contract.exchange = "NSE" 
    contract.currency = "INR" 
    return contract


def histData(reqId,contract, durationStr='3 M',barSizeSetting='5 mins'):
    app.reqHistoricalData (reqId=reqId,
                           contract=contract,
                           endDateTime='',
                           durationStr=durationStr,
                           barSizeSetting=barSizeSetting,
                           whatToShow='ADJUSTED_LAST',
                           useRTH=0,
                           formatDate=1,
                           keepUpToDate=0,
                           chartOptions=[],)
    
tickers=['SAIL']
for tick in tickers:
    print("\n",tick,"::::::\n")
    contract=nse_contract(tick)
    histData(35,contract)

time.sleep(5)

