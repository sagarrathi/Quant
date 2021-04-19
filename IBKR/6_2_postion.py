#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 16:03:07 2020

@author: boo
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading
import time
import pandas as pd

class TradingApp(EWrapper, EClient): 
    def __init__(self):
        EClient.__init__(self,self) 
        self.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                              'Account', 'Symbol', 'SecType',
                                              'Exchange', 'Action', 'OrderType',
                                              'TotalQty', 'CashQty', 'LmtPrice',
                                              'AuxPrice', 'Status'])
    
        self.pos_df=pd.DataFrame(columns=["Account", "Symbol", "SecType",
                                          "Currency", "Position",  "Avg cost"])
        
    def openOrder(self, orderId, contract, order,orderState):
        super().openOrder(orderId, contract, order, orderState)
        order_dict = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": orderId,
                      "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty, 
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": orderState.status}
    
        self.order_df=self.order_df.append(order_dict, ignore_index=True)



    
    def position(self, account, contract, position,avgCost: float):
         super().position(account, contract, position, avgCost)
         pos_dict={"Account": account, "Symbol": contract.symbol, 
                   "SecType":contract.secType, "Currency": contract.currency,
                   "Position": position, "Avg cost": avgCost
               }
         
         self.pos_df=self.pos_df.append(pos_dict, ignore_index=True)


                
    def positionEnd(self):
             super().positionEnd()
             print("PositionEnd")
    

def websocket_conn():
    app.run()

app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)   

con_thread=threading.Thread(target=websocket_conn, daemon=True)
con_thread.start()
time.sleep(1)

 
app.reqOpenOrders()
time.sleep(5)
order_df = app.order_df
time.sleep(5)

app.reqPositions()
pos_df=app.pos_df
time.sleep(5)

