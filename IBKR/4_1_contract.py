#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 18:21:06 2020

@author: boo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:54:36 2020

@author: boo
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class TradingApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self,self) 
        EWrapper.__init__(self)
        
    def error(self, reqId, errorCode, errorString):
        print("Error{}{}{}".format(reqId, errorCode, errorString))
        
    def contractDetails(self, reqId, contractDetails):
        print("reqId:{}, contract:{}".format(reqId, contractDetails))

        
app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=35)

contract=Contract()
contract.symbol="TATAMOTOR"
contract.secType = "STK"
contract.exchange = "NSE"
contract.currency = "INR"

app.reqContractDetails(35, contract)

app.run( )     