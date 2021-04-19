#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 00:33:19 2020

@author: boo
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

import threading
import time

import pandas as pd

class TradingApp(EWrapper, EClient): 
    def __init__(self):
        EClient.__init__(self,self) 
        self.data={}    
        self.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                              'Account', 'Symbol', 'SecType',
                                              'Exchange', 'Action', 'OrderType',
                                              'TotalQty', 'CashQty', 'LmtPrice',
                                              'AuxPrice', 'Status'])
    
    def openOrder(self, orderId, contract, order,orderState):
        super().openOrder(orderId, contract, order, orderState)
        order_dict = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": orderId,
                      "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty, 
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": orderState.status}
    
            
        self.order_df=self.order_df.append(order_dict, ignore_index=True)

        
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)

    
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

def histData(req_num,contract, durationStr='1 M',barSizeSetting='20 mins'):
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


def order_limit(symbol,action,qty, lim_price, dis_lim_price):
    order = Order()
    order.action = action
    order.orderType = "LMT"
    order.totalQuantity = qty
    order.lmtPrice = lim_price
    order.discretionaryAmt = dis_lim_price
    return order


def order_market(symbol,action,qty):
    order = Order()
    order.action = action
    order.orderType = "MKT"
    order.totalQuantity = qty
    return order

def order_stop(symbol,action,qty, stp_price):
    order = Order()
    order.action = action
    order.orderType = "STP"
    order.totalQuantity = qty
    
    return order

def order_trail_stop(symbol,action,qty,stp_price,
                     pr_pc_swtich,trail_price=2,trail_pct=2):
    order = Order()
    order.action = action
    order.orderType = "TRAIL"
    order.totalQuantity = qty
    order.trailStopPrice = stp_price
    
    if pr_pc_swtich=='PR':
        order.auxPrice = trail_price
    elif pr_pc_swtich=='PC':
        order.trailingPercent = trail_pct
    
    return order
        
    
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




tickers=['SAIL',	'SIEMENS','FORTIS', 	'NIFTYBEES']
df_dict={}


for ticker in tickers:
    contract=nse_contract(ticker)
    histData(tickers.index(ticker),contract)
    time.sleep(5)
    
    df_dict[ticker]=pd.DataFrame(app.data[tickers.index(ticker)])
    df_dict[ticker].set_index("Date", inplace=True)

 

contract=nse_contract(ticker)

order_id=app.nextValidOrderId
order=order_market(ticker, "BUY", 1)
app.placeOrder(order_id, 
               contract,
               order)
app.cancelOrder(order_id)



app.reqIds(-1)
time.sleep(1)
order_id=app.nextValidOrderId
order=order_market(ticker, "BUY", 20)
app.placeOrder(order_id, 
               contract,
               order)

app.cancelOrder(order_id)

app.reqIds(-1)
time.sleep(1)
order_id=app.nextValidOrderId
order=order_stop(ticker, "BUY", 20, 48)
app.placeOrder(order_id, 
               contract,
               order)


app.reqIds(-1)
time.sleep(1)
order_id=app.nextValidOrderId
order=order_trail_stop(ticker, "BUY", 20, 45, 'PC',1,1)
app.placeOrder(order_id, 
               contract,
               order)




