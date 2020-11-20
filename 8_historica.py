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


contract=Contract()
contract.symbol="TATAMOTOR"
contract.secType = "STK"
contract.exchange = "NSE" 
contract.currency = "INR" 


app.reqHistoricalData (reqId=35,
                       contract=contract,
                       endDateTime='20201118 09:00:00',
                       durationStr='3 M',
                       barSizeSetting='5 mins',
                       whatToShow='MIDPOINT',
                       useRTH=0,
                       formatDate=1,
                       keepUpToDate=0,
                       chartOptions=[],)
time.sleep(5)

