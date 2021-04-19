#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 13:54:36 2020

@author: boo
"""

from ibapi.client import EClient

from ibapi.wrapper import EWrapper

def TradingApp(EWrapper, EClient):
    def __init__(self):
         EWrapper.__init__(self,self)
         EClient.__init__(self,self)
         we are passing the object of TradingApp class as an argument to EClient. The second self pertains to that. Think of it as the argument in lieu of wrapper.


    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print("Error{}{}{}", reqId, errorCode, errorString)