import random
import uuid

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time
import pandas as pd


class Account(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                              'Account', 'Symbol', 'SecType',
                                              'Exchange', 'Action', 'OrderType',
                                              'TotalQty', 'CashQty', 'LmtPrice',
                                              'AuxPrice', 'Status'])

        self.pos_df = pd.DataFrame(columns=['Account', 'Symbol', 'SecType',
                                            'Currency', 'Position', 'Avg cost'])
        self.pnldef = pd.DataFrame(columns=["Daily PnL Single. ReqId:", "Position:", "DailyPnL:", "UnrealizedPnL:",
                                            "RealizedPnL:", "Value"])

        self.acc_summary = pd.DataFrame(columns=['ReqId', 'Account', 'Tag', 'Value', 'Currency'])

    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)
        dictionary = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": orderId,
                      "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty,
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": orderState.status}
        self.order_df = self.order_df.append(dictionary, ignore_index=True)

    def position(self, account, contract, position, avgCost):
        super().position(account, contract, position, avgCost)
        dictionary = {"Account": account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Currency": contract.currency, "Position": position, "Avg cost": avgCost}
        self.pos_df = self.pos_df.append(dictionary, ignore_index=True)

    def pnlSingle(self, reqId, pos, dailyPnL, unrealizedPnL, realizedPnL, value):
        super().pnlSingle(reqId, pos, dailyPnL, unrealizedPnL, realizedPnL, value)
        dictionary = {"Daily PnL Single. ReqId:", reqId, "Position:", pos,
                      "DailyPnL:", dailyPnL, "UnrealizedPnL:", unrealizedPnL,
                      "RealizedPnL:", realizedPnL, "Value:", value}
        self.pnldef = self.pnldef.append(dictionary, ignore_index=True)

    def accountSummary(self, reqId, account, tag, value, currency):
        super().accountSummary(reqId, account, tag, value, currency)
        dictionary = {"ReqId": reqId, "Account": account, "Tag": tag, "Value": value, "Currency": currency}
        self.acc_summary = self.acc_summary.append(dictionary, ignore_index=True)


def websocket_con():
    app.run()


app = Account()
app.connect("127.0.0.1", 7497, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)  # some latency added to ensure that the connection is established


def get_open_orders():
    app.reqOpenOrders()
    time.sleep(2)
    open_orders = app.order_df
    return open_orders


def get_open_positions():
    app.reqPositions()
    time.sleep(2)
    pos_df = app.pos_df
    return pos_df


def get_pnl():
    app.reqPnL(1, "DU3148837", "")
    time.sleep(1)
    pnl_summ_df = app.pnldef
    return pnl_summ_df


def get_account_summary():
    app.reqAccountSummary(1, "All", "$LEDGER:ALL")
    time.sleep(1)
    acc_summ_df = app.acc_summary
    return acc_summ_df
