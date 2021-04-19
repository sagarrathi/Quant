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
    
        
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)


def nse_contract(symbol):
    contract=Contract()
    contract.symbol=symbol
    contract.secType = "STK"
    contract.exchange = "NSE" 
    contract.currency = "INR" 
    return contract

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

 
ticker='SAIL'

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




