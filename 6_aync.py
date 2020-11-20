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
        
    def error(self, reqId, errorCode, errorString):
        print("Error{}{}{}".format(reqId, errorCode, errorString))
        
    def contractDetails(self, reqId, contractDetails):
        print("reqId:{}, contract:{}".format(reqId, contractDetails))

        
def websocket_conn():
    app.run()
    event.wait(3)
    if event.is_set():
        app.close()
    
event=threading.Event()
app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=35)


contract=Contract()
contract.symbol="TATAMOTOR"
contract.secType = "STK"
contract.exchange = "NSE"
contract.currency = "INR" 


app.reqContractDetails(35, contract)

thr23=threading.Thread(target=websocket_conn)
thr23.start()
event.set()


