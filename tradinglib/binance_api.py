# -*- coding: utf-8 -*-

from decimal import Decimal

from binance.client import Client

from .base_api import BaseAPI


class BinanceAPI(BaseAPI):
    def __init__(self, api_key=None, api_secret=None):
        self._client = self._get_client(api_key, api_secret)
        self.recv_window = 1000

    def _get_client(self, api_key, api_secret):
        try:
            return Client(api_key=api_key, api_secret=api_secret)
        except:
            return self._get_client(api_key, api_secret)

    def get_balance(self, currency=None):
        if currency:
            balance = self._client.get_asset_balance(currency, **{'recvWindow': self.recv_window})
            return self.build_balance(
                currency=balance.get('asset'),
                available=balance.get('free'),
                pending=balance.get('locked')
            )
        balances = [
            self.build_balance(
                currency=balance.get('asset'),
                available=balance.get('free'),
                pending=balance.get('locked'),
            )
            for balance in self._client.get_account(**{'recvWindow': self.recv_window}).get('balances')
        ]
        return balances

    def list_orderbook(self, currency_price='USDT', currency_quantity='BTC', limit=10):
        symbol = currency_quantity + currency_price
        book = self._client.get_order_book(symbol=symbol)

        book_buy_orders = book.get('bids')[:limit]
        book_buy_orders = [{
            'unit_price': Decimal(str(order[0])),
            'quantity': Decimal(str(order[1])),
        } for order in book_buy_orders]

        book_sell_orders = book.get('asks')[:limit]
        book_sell_orders = [{
            'unit_price': Decimal(str(order[0])),
            'quantity': Decimal(str(order[1])),
        } for order in book_sell_orders]

        return book_buy_orders, book_sell_orders

    def create_order(self, order_type: str, currency_price: str, currency_quantity: str,
                     unit_price: Decimal = None, quantity: Decimal = None,
                     execution_type: str = BaseAPI.ORDER_LIMIT) -> dict:
        order = {}
        symbol = currency_quantity + currency_price
        params = {
            'symbol': symbol,
            'price': unit_price,
            'recvWindow': self.recv_window,
        }
        if execution_type == self.ORDER_LIMIT:
            if order_type == self.ORDER_BUY:
                params['quantity'] = quantity
                order = self._client.order_limit_buy(**params)
            elif order_type == self.ORDER_SELL:
                params['quantity'] = quantity
                order = self._client.order_limit_sell(**params)
        return order

    def create_withdraw(self, currency: str, quantity: Decimal, address: str, tag: str = None) -> dict:
        params = {
            'asset': currency,
            'amount': quantity,
            'address': address,
            'recvWindow': self.recv_window,
        }
        if tag:
            params['addressTag'] = tag

        withdraw = self._client.withdraw(**params)
        return withdraw
