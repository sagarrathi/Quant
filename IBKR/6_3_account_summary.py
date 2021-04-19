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
    
        self.ac_df=pd.DataFrame(columns=["ReqId","Account",
                                         "Tag", "Value", 
                                         "Currency"])
    
        self.pl_df=pd.DataFrame(columns=["ReqId","DailyPnL",
                                         "UnrealizedPnL","RealizedPnL"])
    
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
    

    def accountSummary(self, reqId, account, tag, value,currency):
        super().accountSummary(reqId, account, tag, value, currency)
        ac_dict={"ReqId": reqId, "Account": account,
               "Tag":tag, "Value": value, 
               "Currency": currency}
        
        self.ac_df=self.ac_df.append(ac_dict, ignore_index=True)
        
    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        print("AccountSummaryEnd. ReqId:", reqId)


    def pnl(self, reqId, dailyPnL,unrealizedPnL, realizedPnL):
        super().pnl(reqId, dailyPnL, unrealizedPnL, realizedPnL)
        pl_dict={"ReqId": reqId, "DailyPnL": dailyPnL,
                 "UnrealizedPnL": unrealizedPnL, "RealizedPnL": realizedPnL
                   }
        
        
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


app.reqPositions()
time.sleep(5)
pos_df=app.pos_df

app.reqAccountSummary(1, "All", "$LEDGER:ALL")
time.sleep(5)
ac_df=app.ac_df


app.reqPnL(2, "DU1801304", "")
time.sleep(5)
pl_df=app.pl_df
