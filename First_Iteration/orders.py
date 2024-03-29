from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time

from logger import log
from v1.const import LOG_PATH


class Orders(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)


def websocket_con():
    app.run()


app = Orders()
app.connect("127.0.0.1", 7497, clientId=1)

# starting a separate daemon thread to execute the websocket connection
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()
time.sleep(1)  # some latency added to ensure that the connection is established


# creating object of the Contract class - will be used as a parameter for other function calls
def contract(symbol="ES", secType="FUT", exchange="GLOBEX", lastTradeDateOrContractMonth="202103"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.currency = "USD"
    contract.exchange = exchange
    contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    print('Contract details are retrieved', contract)
    return contract


def market_order(action, size):
    order = Order()
    order.action = action
    order.orderType = "MKT"
    order.totalQuantity = size
    app.placeOrder(app.nextValidOrderId, contract(), order)
    log(f'market order placed, {action, size}', LOG_PATH)


def stop_order(order_id, action, size, stopPrice):
    app.reqIds(-1)
    order = Order()
    order.action = action
    order.orderType = "STP"
    order.auxPrice = stopPrice
    order.totalQuantity = size
    app.placeOrder(order_id, contract(), order)
    log(f'stop order placed {order_id, action, size, stopPrice}')



def stop_limit_order(action, size, limitPrice, stopPrice):
    app.reqIds(-1)
    order = Order()
    order.action = action
    order.orderType = "STP LMT"
    order.totalQuantity = size
    order.lmtPrice = limitPrice
    order.auxPrice = stopPrice
    app.placeOrder(app.nextValidOrderId, contract(), order)
    log(f'stop limit order placed {action, size, limitPrice, stopPrice}')


def limit_order(action, size, limitPrice):
    order = Order()
    order.action = action
    order.orderType = "LMT"
    order.totalQuantity = size
    order.lmtPrice = limitPrice
    app.placeOrder(app.nextValidOrderId, contract(), order)
    log(f'limit order placed: {action}, {size}, {limitPrice}')


def cancel_order(order_id):
    app.cancelOrder(order_id)
    log(f'order cancelled {order_id}')


def cancel_all_orders():
    app.reqGlobalCancel()
    log('All orders cancelled')

# cancel_all_orders()
# limit_order('BUY', 1, 3700)
# time.sleep(6)
# app.reqIds(-1)
cancel_order(2)
# stop_order(app.nextValidOrderId, 'SELL', 1, 3783)


