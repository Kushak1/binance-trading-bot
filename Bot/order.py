from config import Connect
import math
import time

class Order:
    def __init__(self):
        self.client = Connect().make_connection()

        max_amount = self.client.get_max_margin_loan(asset="BTC",isolatedSymbol='BTCUSDT')['amount']
        #Change for how much money you allow for trade. Current one 35% from maximum allowed borrow limit
        self.max_amount_sell = format(float(max_amount)*35/100,".6f")

        max_amount = self.client.get_max_margin_loan(asset="USDT",isolatedSymbol='BTCUSDT')['amount']
        #Change for how much money you allow for trade. Current one 35% from maximum allowed borrow limit
        self.max_amount_buy = format(float(max_amount)*35/100,".6f")
    

    def sell(self, last_price):

        order = self.client.create_margin_order(
        sideEffectType='MARGIN_BUY',
        symbol='BTCUSDT',
        side=self.client.SIDE_SELL,
        type=self.client.ORDER_TYPE_MARKET,
        quantity=self.max_amount_sell,
        isIsolated='TRUE'
        )
        
        return(order)


    def buy(self, last_price):

        order = self.client.create_margin_order(
        sideEffectType='MARGIN_BUY',
        symbol='BTCUSDT',
        side=self.client.SIDE_BUY,
        type=self.client.ORDER_TYPE_MARKET,
        #Converting USDT to BTC based on last price and trading 70% of that amount for the precision
        quantity=format((float(self.max_amount_buy)/last_price)/100 * 70, ".5f"),
        isIsolated='TRUE'
        )
        
        return(order)
        
    def close_order(self, qty, side):

        if side == "BUY":
            order = self.client.create_margin_order(
            symbol='BTCUSDT',
            side=self.client.SIDE_SELL,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=qty,
            isIsolated='TRUE',
            sideEffectType='AUTO_REPAY'
            )
        elif side == "SELL":
            order = self.client.create_margin_order(
            symbol='BTCUSDT',
            side=self.client.SIDE_BUY,
            type=self.client.ORDER_TYPE_MARKET,
            quantity=qty,
            isIsolated='TRUE',
            sideEffectType='AUTO_REPAY'
            )