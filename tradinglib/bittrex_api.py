# -*- coding: utf-8 -*-

from decimal import Decimal

from bittrex.bittrex import API_V1_1, PROTECTION_PRV, Bittrex as Client

from .base_api import BaseAPI


class BittrexAPI(BaseAPI):
    def __init__(self, api_key=None, api_secret=None):
        self._client = self._get_client(api_key, api_secret)

    def _get_client(self, api_key, api_secret):
        try:
            return Client(api_key=api_key, api_secret=api_secret, api_version=API_V1_1)
        except:
            return self._get_client(api_key, api_secret)

    def get_balance(self, currency=None):
        if currency:
            balance = self._client.get_balance(currency).get('result')
            return self.build_balance(
                currency=balance.get('Currency'),
                available=balance.get('Available'),
                pending=balance.get('Pending'),
                total=balance.get('Balance')
            )
        balances = [
            self.build_balance(
                currency=balance.get('Currency'),
                available=balance.get('Available'),
                pending=balance.get('Pending'),
                total=balance.get('Balance')
            )
            for balance in self._client.get_balances().get('result')
        ]
        return balances

    def list_orderbook(self, currency_price: str = 'USDT', currency_quantity: str = 'BTC', limit: int = 10):
        market = currency_price + '-' + currency_quantity
        book = self._client.get_orderbook(market=market).get('result')

        buy_orders = book.get('buy')[:limit]
        buy_orders = [self.build_orderbook(order.get('Rate'), order.get('Quantity')) for order in buy_orders]

        sell_orders = book.get('sell')[:limit]
        sell_orders = [self.build_orderbook(order.get('Rate'), order.get('Quantity')) for order in sell_orders]

        return buy_orders, sell_orders

    def create_order(self, order_type: str, currency_price: str, currency_quantity: str,
                     unit_price: Decimal = None, quantity: Decimal = None,
                     execution_type: str = BaseAPI.ORDER_LIMIT) -> dict:
        order = {}
        market = currency_price + '-' + currency_quantity
        if execution_type == self.ORDER_LIMIT:
            if order_type == self.ORDER_BUY:
                order = self._client.buy_limit(market, quantity, unit_price)
            elif order_type == self.ORDER_SELL:
                order = self._client.sell_limit(market, quantity, unit_price)
        return order

    def create_withdraw(self, currency: str, quantity: Decimal, address: str, tag: str = None) -> dict:
        options = {
            'currency': currency,
            'quantity': quantity,
            'address': address,
        }
        if tag:
            options['paymentid'] = tag

        withdraw = self._client._api_query(PROTECTION_PRV, {API_V1_1: '/account/withdraw'}, options)
        return withdraw
