# -*- coding: utf-8 -*-

from decimal import Decimal

from binance.client import Client


class BinanceAPI:
    def __init__(self, currency_price='USDT', currency_quantity='BTC', api_key=None, api_secret=None):
        self.market = currency_quantity + currency_price
        self.currency_price = currency_price
        self.currency_quantity = currency_quantity
        self._client = self._get_client(api_key, api_secret)

    def _get_client(self, api_key, api_secret):
        try:
            return Client(api_key=api_key, api_secret=api_secret)
        except:
            return self._get_client(api_key, api_secret)

    def list_orderbook(self, limit=10):
        book = self._client.get_order_book(symbol=self.market)

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
