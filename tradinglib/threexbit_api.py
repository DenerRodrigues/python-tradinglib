# -*- coding: utf-8 -*-

from txb_api.client import Client
from txb_api.public import Public


class ThreeXBitAPI:
    def __init__(self, currency_price='CREDIT', currency_quantity='BTC', api_key=None, api_secret=None):
        self.market = currency_price + '_' + currency_quantity
        self.currency_price = currency_price
        self.currency_quantity = currency_quantity
        self._public = Public()
        self._client = self._get_client(api_key, api_secret)

    def _get_client(self, client_id, client_secret):
        try:
            return Client(client_id=client_id, client_secret=client_secret)
        except:
            return self._get_client(client_id, client_secret)

    def list_orderbook(self, limit=10):
        book = self._public.orderbook(self.currency_price, self.currency_quantity)
        book_buy_orders = book.get('buy_orders')[:limit]
        book_sell_orders = book.get('sell_orders')[:limit]
        return book_buy_orders, book_sell_orders
