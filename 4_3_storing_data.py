from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time



class TradingApp(EWrapper, EClient): 
    def __init__(self):
        EClient.__init__(self,self) 
        self.data={}    
    
    
    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId]=[{
                    "Date":bar.date,
                    "Close":bar.close
                    }]
        if reqId in self.data:
            self.data[reqId].append([{
                    "Date":bar.date,
                    "Close":bar.close
                    }])
        print(self.data)


def nse_contract(symbol):
    contract=Contract()
    contract.symbol=symbol
    contract.secType = "STK"
    contract.exchange = "NSE" 
    contract.currency = "INR" 
    return contract


def histData(reqId,contract, durationStr='1 M',barSizeSetting='20 mins'):
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
    
def websocket_conn():
    app.run()
    
app=TradingApp()
app.connect("127.0.0.1", 7497, clientId=1)   

con_thread=threading.Thread(target=websocket_conn, daemon=True)
con_thread.start()
time.sleep(1)

   

contract=nse_contract('SAIL')
histData(1,contract)
time.sleep(5)

app.data
