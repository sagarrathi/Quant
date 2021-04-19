n
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

def nse_order(symbol,action, order_type, qty, lim_price, dis_lim_price):
    order = Order()
    order.action = action
    order.orderType = order_type
    order.totalQuantity = qty
    order.lmtPrice = lim_price
    order.discretionaryAmt = dis_lim_price
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

order=nse_order(ticker, "BUY", "LMT",1, 47, 50)
order_id=app.nextValidOrderId
app.placeOrder(order_id, 
               contract,
               order)


time.sleep(5)

        
    